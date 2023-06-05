import sys
import json
from typing import Dict

from application import Ui_MainWindow
from PyQt5.Qt import *
from textwrap import fill

from src.pdf_script.environment import AppEnvironment


class Application(QMainWindow):
    def __init__(self):
        super(Application, self).__init__()
        self.app = Ui_MainWindow()
        self.app.setupUi(self)
        self.configure()

    def configure(self):
        self.app.btnSearch.clicked.connect(self.search)

    def search(self):
        searching_text = fill(self.app.textEdit.toPlainText(), 65)
        found_data = self.select_data_by_key_words(searching_text.split(" "))[:10]
        for index, note in enumerate(found_data):
            name, image_info = note
            item = QTableWidgetItem()
            self.app.tableWidget.setItem(index, 0, item)
            item.setIcon(QIcon(AppEnvironment.IMAGES_PATH + f"Bacterias/{name}/{image_info['image']}"))
            self.app.tableWidget.setIconSize(QSize(200, 200))

            self.app.tableWidget.setItem(index, 1, QTableWidgetItem(image_info["caption"]))

    @staticmethod
    def select_data_by_key_words(keys: list[str]):
        coincidences = {}
        paths = [(name[:len(name)-4], AppEnvironment.TEXT_PATH + name[:len(name)-4] + "/") for name in AppEnvironment.get_pdf_file_names()]
        for name, path in paths:
            with open(path + r"\image_captions.json") as file:
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





if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Application()
    window.show()
    sys.exit(app.exec_())
