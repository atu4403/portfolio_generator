import os
from pathlib import Path
import pathlib
import yaml
from jinja2 import Environment, FileSystemLoader
import adash as _
from .hub import hub_with_key, hub_with_type
from .j2filter import filters
from .pfg import Conf


class Build:
    def __init__(
        self, path: str = "portfolio.yml", offline: bool = False, output: str = ""
    ) -> None:
        c = Conf()
        self.offline = offline
        self.output = output
        self.conf = c.load(path)
        self.conf_dir = c.dot.search_dir
        self.cache_dir = c.dot.search_cache_dir
        self.values = {"user": self.conf.get("user")}
        for key in self.conf.get("names", []):
            self.values[key] = self._get_json(key)
        for key in self.conf.get("apis", []):
            self.values[key] = self._get_json("__" + key)

    def _get_json(self, key):
        conf = self.conf
        json_path = Path(self.cache_dir) / f"{key}.json"
        if (not json_path.exists()) or (not self.offline):
            if key.startswith("__"):
                d = conf["apis"][key[2:]]
                j = hub_with_type(d.get("type"), d.get("url"))
            else:
                j = hub_with_key(key, conf["names"][key])
            _.json_write(j, json_path, overwrite=True)
            return j
        return _.json_read(json_path)

    def execute(self):
        env = Environment(loader=FileSystemLoader("."))
        for key, filter in filters.items():
            env.filters[key] = filter
        template_path = str(self.conf_dir / self.conf["template"]).replace(os.path.sep, "/")
        template = env.get_template(template_path)
        res = template.render(self.values)
        if self.output:
            Path(self.output).write_text(res)
        else:
            print(res)
