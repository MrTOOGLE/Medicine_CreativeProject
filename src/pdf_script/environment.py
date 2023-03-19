import os
import logging

from datetime import datetime
from PIL import ImageFile
from utils import FileUtils


class AppEnvironment:
    RESOURCE_PATH = "../../resources/"
    PDF_FILES_PATH = RESOURCE_PATH + "PDF_files/"
    IMAGES_PATH = RESOURCE_PATH + "images/"
    TEXT_PATH = RESOURCE_PATH + "text/"
    LOGS_PATH = RESOURCE_PATH + "logs/"
    SOURCE_FOLDERS = [IMAGES_PATH, LOGS_PATH]

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
