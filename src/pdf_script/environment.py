import os
import logging
import re

from datetime import datetime
from PIL import ImageFile


from utils import FileUtils
from typing import Generator, Tuple, Iterator


class AppEnvironment:
    RESOURCE_PATH = "../../resources/"
    PDF_FILES_PATH = RESOURCE_PATH + "PDF_files/"
    IMAGES_PATH = RESOURCE_PATH + "images/"
    TEXT_PATH = RESOURCE_PATH + "text/"
    LOGS_PATH = RESOURCE_PATH + "logs/"
    SOURCE_FOLDERS = [IMAGES_PATH, TEXT_PATH, LOGS_PATH]

    __IMAGE_INDEX_PATTERN = re.compile(r"(\d+)_(\d+)")
    __IMAGE_PAGE_PATTERN = re.compile(r"(\d+)_")

    @classmethod
    def configure(cls) -> None:
        cls.__create_source_folders()
        logging.basicConfig(
            level=logging.DEBUG,
            filename=f"{cls.LOGS_PATH}{datetime.date(datetime.now())}.log",
            filemode="a",
            format="%(asctime)s %(levelname)s %(message)s"
        )
        logging.info(f"The application was launched")

        ImageFile.LOAD_TRUNCATED_IMAGES = True

    @classmethod
    def __create_source_folders(cls) -> None:
        if not os.path.exists(cls.PDF_FILES_PATH):
            os.makedirs(cls.PDF_FILES_PATH)

        _, _, file_names = next(os.walk(AppEnvironment.PDF_FILES_PATH))
        for file_name in file_names:
            cls.SOURCE_FOLDERS.append(cls.IMAGES_PATH + FileUtils.cut_extension(file_name))
            cls.SOURCE_FOLDERS.append(cls.TEXT_PATH + FileUtils.cut_extension(file_name))

        for folder_path in cls.SOURCE_FOLDERS:
            if not os.path.exists(folder_path):
                os.mkdir(folder_path)

    @classmethod
    def get_pdf_paths(cls) -> list[str]:
        _, _, files = next(os.walk(cls.PDF_FILES_PATH))
        return [cls.PDF_FILES_PATH + path for path in files]

    @classmethod
    def get_page_images(cls, folder_name: str) -> Iterator[Tuple[int, Generator]]:
        _, _, images = next(os.walk(cls.IMAGES_PATH + f"/{folder_name}"))
        images.sort(key=lambda image: tuple(map(int, *re.findall(cls.__IMAGE_INDEX_PATTERN, image))))
        images = list(filter(lambda image: re.findall(cls.__IMAGE_PAGE_PATTERN, image)[0] != "1", images))
        _page_images = [images[0]]

        last_page_index = re.findall(cls.__IMAGE_PAGE_PATTERN, images[0])[0]
        for i in range(1, len(images)):
            current_page_index = re.findall(cls.__IMAGE_PAGE_PATTERN, images[i])[0]
            if current_page_index == last_page_index:
                _page_images.append(images[i])
            else:
                yield int(last_page_index), (image for image in _page_images)
                last_page_index = current_page_index
                _page_images = [images[i]]
        yield int(last_page_index), (image for image in _page_images)


if __name__ == '__main__':
    pass
