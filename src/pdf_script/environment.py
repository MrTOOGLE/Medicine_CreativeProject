import os
import logging
import re

from datetime import datetime
from PIL import ImageFile
from utils import FileUtils
from typing import Generator


class AppEnvironment:
    RESOURCE_PATH = "../../resources/"
    PDF_FILES_PATH = RESOURCE_PATH + "PDF_files/"
    IMAGES_PATH = RESOURCE_PATH + "images/"
    TEXT_PATH = RESOURCE_PATH + "text/"
    LOGS_PATH = RESOURCE_PATH + "logs/"
    SOURCE_FOLDERS = [IMAGES_PATH, TEXT_PATH, LOGS_PATH]

    @staticmethod
    def configure():
        AppEnvironment.__create_source_folders()
        logging.basicConfig(
            level=logging.DEBUG,
            filename=f"{AppEnvironment.LOGS_PATH}{datetime.date(datetime.now())}.log",
            filemode="a",
            format="%(asctime)s %(levelname)s %(message)s"
        )
        logging.info(f"The application was launched")

        ImageFile.LOAD_TRUNCATED_IMAGES = True

    @staticmethod
    def __create_source_folders():
        if not os.path.exists(AppEnvironment.PDF_FILES_PATH):
            os.makedirs(AppEnvironment.PDF_FILES_PATH)

        _, _, file_names = next(os.walk(AppEnvironment.PDF_FILES_PATH))
        for file_name in file_names:
            AppEnvironment.SOURCE_FOLDERS.append(AppEnvironment.IMAGES_PATH + FileUtils.cut_extension(file_name))
            AppEnvironment.SOURCE_FOLDERS.append(AppEnvironment.TEXT_PATH + FileUtils.cut_extension(file_name))

        for folder_path in AppEnvironment.SOURCE_FOLDERS:
            if not os.path.exists(folder_path):
                os.mkdir(folder_path)

    @staticmethod
    def get_pdf_paths():
        _, _, files = next(os.walk(AppEnvironment.PDF_FILES_PATH))
        return [AppEnvironment.PDF_FILES_PATH + path for path in files]

    @staticmethod
    def page_images(folder_name: str) -> Generator:
        _, _, images = next(os.walk(AppEnvironment.IMAGES_PATH + f"/{folder_name}"))
        images.sort(key=lambda image: len(re.findall(r"(\d.*)\.", image)[0]))
        images = list(filter(lambda image: re.findall(r"(\d*)_", image)[0] != "1", images))
        pattern = r"(\d*)_"
        _page_images = [images[0]]

        for i in range(1, len(images)):
            if re.findall(pattern, images[i]) == re.findall(pattern, images[i - 1]):
                _page_images.append(images[i])
            else:
                yield (image for image in _page_images)
                _page_images = [images[i]]
        yield (image for image in _page_images)


if __name__ == '__main__':
    page_image_getter = AppEnvironment.page_images("2")
    next(page_image_getter)
