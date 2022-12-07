import os
from cudatext import *
from pathlib import Path
import tempfile
import json

class Command:
    def __init__(self):
        settings_dir = Path(app_path(APP_DIR_SETTINGS))
        self.history_filename = settings_dir / "cuda_pos_tmp.json"

    def check_tmp_dir(self, path):
        temp_dir = tempfile.TemporaryDirectory()
        if path.startswith(tempfile.gettempdir()):
            return True

        return False

    def get_path(self, path):
        tmp = str(path).split(os.sep)
        del tmp[slice(1, 3)]

        return os.sep.join(tmp)

    def get_caret(self, ed_self):
        return ed_self.get_carets()[0][1]

    def set_caret(self, ed_self, line):
        ed_self.set_caret(0, line)
        ed_self.set_prop(PROP_LINE_TOP, max(0, line-3))

    def on_close_pre(self, ed_self):
        path_full = ed_self.get_filename()
        if (self.check_tmp_dir(path_full)):
            path = self.get_path(path_full)
            self.save_pos(path, ed_self)

    def on_open(self, ed_self):
        path_full = ed_self.get_filename()
        data_load = self.load_pos()
        for path, line in data_load.items():
            if path_full.endswith(path):
                self.set_caret(ed_self, line)

    def load_pos(self):
        data_load = {}
        if self.history_filename.exists():
            with self.history_filename.open(encoding="utf-8") as fin:
                data_load = json.load(fin)

        return data_load

    def save_pos(self, path, ed_self):
        if self.get_caret(ed_self) > 0:
            data = {path: self.get_caret(ed_self)}
            data_load = self.load_pos()
            if data_load:
                data_load[path] = self.get_caret(ed_self)
            else:
                data_load.update(data)

            with self.history_filename.open(mode="w", encoding="utf-8") as fout:
                json.dump(data_load, fout, indent=2)
