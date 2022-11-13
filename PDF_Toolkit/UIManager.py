import json
from localization import localization


class UIManager:

    def __init__(self, default_language: str):
        self.settings = {}
        self.read_settings(default_language)
        self.translation = localization[self.settings["ui"]["language"]]

    def output(self, key: str, **kwargs):
        # print a line with optional text replacement and optional prefix
        if kwargs.get("text") is None:
            print_text = self.translation["info"][key]
        else:
            print_text = self.translation["info"][key].replace("[[TEXT]]", kwargs.get("text"))
        if kwargs.get("prefix") is not None:
            print_text = kwargs.get("prefix") + print_text
        print(print_text)

    def add_line(self):
        # add a single empty line
        print()

    def print_title(self, key: str):
        # print the title of a section with empty lines before and after
        print(f"\n{self.translation['title'][key]}\n")

    def change_language(self):
        # change output language
        languages = [lang for lang in localization]
        option = self.menu(options=languages, title="language")
        self.translation = localization[option]
        self.settings["ui"]["language"] = option
        self.write_settings()

    def menu(self, options: [], **kwargs) -> str:
        # print a menu with the given options and title
        if kwargs.get("title") is not None:
            self.print_title(key=kwargs.get("title"))
        numbers = ""
        for key in range(len(options)):
            print(f"{key + 1}: {self.translation['menu'][options[key]]['text']}")
            if key > 0:
                numbers += "/"
            numbers += str(key + 1)
        try:
            option = input(self.translation["info"]["choose_option"].replace("[[TEXT]]", numbers))
            if int(option) < 1:
                option = len(options) + 1
            return options[int(option) - 1]
        except IndexError:
            self.output(key="option_invalid")
            return self.menu(options, title=kwargs.get("title"))
        except ValueError:
            self.output(key="not_a_number")
            return self.menu(options, title=kwargs.get("title"))

    def show_help(self, options: []):
        # print out the help entries for the given options
        self.print_title(key="help")
        for i in range(len(options)):
            print(f"{i+1}. {self.translation['menu'][options[i]]['help']}\n")

    def read_settings(self, default: str):
        try:
            with open("../settings.json", mode="r") as file:
                self.settings = json.load(file)
        except FileNotFoundError:
            self.settings = {
                "ui": {
                    "language": default,
                },
            }
            self.write_settings()

    def write_settings(self):
        with open("../settings.json", mode="w") as json_file:
            json.dump(self.settings, json_file, indent=4)
