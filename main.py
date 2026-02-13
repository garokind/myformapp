import json
from datetime import datetime
from pathlib import Path

from kivy.app import App
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.properties import DictProperty
from kivy.uix.boxlayout import BoxLayout


KV_FILE = "tailor_form.kv"
SAVE_FILE = "last_form_data.json"


class TailorFormRoot(BoxLayout):
    inputs = DictProperty({})

    def register_input(self, key, widget):
        self.inputs[key] = widget

    def save_data(self):
        form_data = {key: widget.text for key, widget in self.inputs.items()}
        data = {
            "saved_at": datetime.now().isoformat(timespec="seconds"),
            "form": form_data,
        }
        save_path = Path(App.get_running_app().user_data_dir) / SAVE_FILE
        save_path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

    def load_data(self):
        save_path = Path(App.get_running_app().user_data_dir) / SAVE_FILE
        if not save_path.exists():
            return
        data = json.loads(save_path.read_text(encoding="utf-8"))
        form_data = data.get("form", data)
        for key, widget in self.inputs.items():
            widget.text = form_data.get(key, "")

    def clear_data(self):
        for widget in self.inputs.values():
            widget.text = ""

    @property
    def table_height(self):
        return dp(52) * 24


class TailorFormApp(App):
    def build(self):
        return Builder.load_file(KV_FILE)


if __name__ == "__main__":
    TailorFormApp().run()
