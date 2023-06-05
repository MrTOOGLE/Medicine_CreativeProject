import json
from pprint import pprint
from typing import Dict

from src.pdf_script.environment import AppEnvironment


def search():
    searching_text = input()
    found_data = select_data_by_key_words(searching_text.split(" "))[:10]
    pprint(found_data)
    for index, note in enumerate(found_data):
        name, image_info = note


def select_data_by_key_words(keys: list[str]):
    coincidences = {}
    paths = [(name[:len(name)-4], AppEnvironment.TEXT_PATH + name[:len(name)-4] + "/") for name in AppEnvironment.get_pdf_file_names()]
    for name, path in paths:
        with open(path + r"image_captions.json") as file:
            captions: Dict[str, Dict[str, str]] = json.load(file)
            for image, image_info in captions.items():
                count_coincidences = 0
                caption = image_info["caption"]
                for key in keys:
                    count_coincidences += caption.count(key)
                if count_coincidences != 0:
                    coincidences[name] = {
                        "image": image,
                        "coincidences": count_coincidences,
                        "caption": caption
                    }

    return sorted(coincidences.items(), key=lambda x: x[1]["coincidences"], reverse=True)


if __name__ == '__main__':
    search()
