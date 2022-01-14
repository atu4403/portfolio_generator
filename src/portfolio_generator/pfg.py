import os
from pathlib import Path
import yaml
import arrow
import adash as _
from .templates import default_template
from .validate import validate


class PfgError(Exception):
    def __init__(self, arg=""):
        super().__init__()
        self.arg = arg


class ConfigExistsError(PfgError):
    def __str__(self) -> str:
        return "config ディレクトリはすでに存在します"


class ConfigDirectoryNotExistsError(PfgError):
    def __str__(self):
        return "configディレクトリが存在しません。'pfg init'を実行してください"


class ConfigFileNotExistsError(PfgError):
    def __str__(self) -> str:
        return f"{self.arg}は存在しません"


class TemplateFileNotExistsError(PfgError):
    def __str__(self) -> str:
        return f"{self.arg}は存在しません"


class InvalidYamlFormatError(PfgError):
    def __str__(self) -> str:
        return self.arg


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
        if os.getenv("XDG_CONFIG_HOME"):
            return Path(os.getenv("XDG_CONFIG_HOME")) / self.PFG
        return Path().home() / ".config" / self.PFG

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
            raise ConfigExistsError()
        else:
            dot.mkdir(glo)
            d = dot.global_dir if glo else dot.local_dir
            (d / "portfolio.yml").write_text(self._basic_yaml(name))
            (d / "portfolio.j2").write_text(default_template)
            return str(d.resolve())

    def load(self, yaml_name):
        if d := self.dot.search_dir:
            path = d / yaml_name
            if not path.is_file():
                raise ConfigFileNotExistsError(yaml_name)
            obj = yaml.load(path.read_text(), Loader=yaml.SafeLoader)
            if v := validate(obj):
                raise InvalidYamlFormatError(f"{yaml_name} {v}")
            template_path = obj.get("template")
            if not (d / template_path).exists():
                raise TemplateFileNotExistsError(yaml_name)
            return obj
        raise ConfigDirectoryNotExistsError()
