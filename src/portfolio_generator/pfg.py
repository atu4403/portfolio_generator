import os
from pathlib import Path
import yaml
import arrow
import adash as _
from .templates import default_template
from .validate import validate


class ConfigExistsError(Exception):
    pass


class ConfigDirectoryNotExistsError(Exception):
    pass


class ConfigFileNotExistsError(Exception):
    pass


class TemplateFileNotExistsError(Exception):
    pass


class InvalidYamlFormatError(Exception):
    pass


class Pfg:
    PFG = ".pfg"
    CACHE_DIRNAME = "__pfgcache__"

    def __init__(self) -> None:
        pass

    @property
    def local_dir(self):
        return Path(self.PFG)

    @property
    def global_dir(self):
        d = Path().home() / ".config" / self.PFG
        return Path(os.getenv("XDG_CONFIG_HOME", d))

    @property
    def search_dir(self):
        if self.local_dir.exists():
            return self.local_dir
        elif self.global_dir.exists():
            return self.global_dir
        else:
            return None

    @property
    def search_cache_dir(self):
        if d := self.search_dir:
            return d / self.CACHE_DIRNAME
        return None

    def mkdir(self, glo: bool = False):
        d = self.global_dir if glo else self.local_dir
        os.makedirs(d, exist_ok=True)
        os.makedirs(d / self.CACHE_DIRNAME, exist_ok=True)


class Conf:
    def __init__(self) -> None:
        self.dot = Pfg()

    def _basic_yaml(self, name: str):
        y = {
            "user": name,
            "created_at": arrow.get().to("local").format(),
            "names": {
                "github": name,
                "qiita": name,
                "zenn": name,
            },
            "template": "portfolio.j2",
        }
        return yaml.dump(y)

    def init(self, name: str, glo: bool = False, force: bool = False):
        dot = self.dot
        if not force and (
            (dot.local_dir.exists() and not glo) or (dot.global_dir.exists() and glo)
        ):
            raise ConfigDirectoryNotExistsError(
                "config directory already exists. If you want to overwrite 'Force'Option"
            )
        else:
            dot.mkdir(glo)
            d = dot.global_dir if glo else dot.local_dir
            (d / "portfolio.yml").write_text(self._basic_yaml(name))
            (d / "portfolio.j2").write_text(default_template)

    def load(self, yaml_name):
        if d := self.dot.search_dir:
            path = d / yaml_name
            if not path.is_file():
                raise ConfigFileNotExistsError()
            obj = yaml.load(path.read_text(), Loader=yaml.SafeLoader)
            if v := validate(obj):
                raise InvalidYamlFormatError(v)
            template_path = obj.get("template")
            if not (d / template_path).exists():
                raise TemplateFileNotExistsError()
            return obj
        raise ConfigDirectoryNotExistsError()
