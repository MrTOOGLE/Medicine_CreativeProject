import io
import logging
import fitz
import json

from typing import Generator
from PIL import Image, ImageFile
from environment import AppEnvironment
from utils import FileUtils, triable, ImageInfo, GeneratorHandler, timer


class PDFHandler:
    def __init__(self, pdf_path: str):
        self.pdf_file = fitz.open(pdf_path)
        self.pdf_name = FileUtils.get_file_name(pdf_path, with_extension=False)

        self.__images_info = {}
        self.__page_image_getter = GeneratorHandler(AppEnvironment.get_page_images(self.pdf_name))

    def extract_info(self) -> None:
        self.extract_images()
        self.extract_text()

    @timer
    def extract_images(self) -> None:
        logging.info(f"Extracting images from {self.pdf_file.name}...")
        for page_index in range(len(self.pdf_file)):
            page = self.pdf_file[page_index]
            image_list = page.get_images()

            for image_index, base_image in enumerate(image_list, start=1):
                image_info = self.__extract_image(base_image)
                if image_info.image:
                    self.__save_image(image_info, page_index, image_index)

        logging.info(f"Extracting images from {self.pdf_file.name} is finished.")

    @triable
    def __extract_image(self, image: ImageFile) -> ImageInfo:
        base_image = self.pdf_file.extract_image(image[0])
        image_extension = base_image["ext"]
        image_bytes = base_image["image"]
        image = Image.open(io.BytesIO(image_bytes))
        if image.mode != "RGB":
            image = FileUtils.to_rgb_image(image)

        return ImageInfo(image=image, extension=image_extension)

    @triable
    def __save_image(self, image_info: ImageInfo, page_index: int, image_index: int) -> None:
        image, extension = image_info.image, image_info.extension
        save_directory = AppEnvironment.IMAGES_PATH + self.pdf_name
        image_path = f"{save_directory}/image{page_index + 1}_{image_index}.{extension}"
        image.save(open(image_path, "wb"))

        if extension not in FileUtils.STANDARD_IMAGE_EXTENSIONS:
            FileUtils.convert_image(image_path)

    @timer
    def extract_text(self):
        logging.info(f"Extracting text from {self.pdf_file.name}...")
        pages = [page for page in self.pdf_file][1:]
        for page_index, page in enumerate(pages, start=2):
            text = page.get_text()
            self.__extract_page_text(page_index, text)

        with open(AppEnvironment.TEXT_PATH + self.pdf_name + "/images_info.json", "w") as file:
            json.dump(self.__images_info, file)
        logging.info(f"Extracting text from {self.pdf_file.name} is finished.")

    @triable
    def __extract_page_text(self, page_index: int, text: str) -> None:
        if "Fig." in text or "Figure" in text:
            page_captions = FileUtils.extract_captions(text, self.pdf_name)
        else:
            return
        if not page_captions:
            return

        self.__process_page_data(page_index, page_captions)

    def __process_page_data(self, page_index: int, page_captions: list[str]) -> None:
        self.__page_image_getter.next()
        images_page_index, page_images = self.__page_image_getter.last_value

        to_next_page = False
        while page_index != images_page_index:
            if images_page_index > page_index or self.__page_image_getter.is_empty:
                self.__page_image_getter.back()
                to_next_page = True
                break
            else:
                self.__page_image_getter.next()
                images_page_index, page_images = self.__page_image_getter.last_value
        if to_next_page:
            return

        page_images_info = self.__get_page_images_info(page_images, (caption for caption in page_captions))
        self.__images_info.update(page_images_info)

    @staticmethod
    def __get_page_images_info(page_images: Generator, page_captions: Generator) -> dict:
        page_images_info = {}
        page_images = GeneratorHandler(page_images)
        page_captions = GeneratorHandler(page_captions)

        while True:
            page_captions.next()
            image_index, caption = page_captions.last_value
            count_images = FileUtils.count_images_in_caption(caption)
            for _ in range(count_images):
                page_images.next()
                if page_captions.is_empty and page_images.is_empty:
                    return page_images_info

                image = page_images.last_value
                page_images_info[image] = {
                    "index": image_index,
                    "scale": None,
                    "required": None,
                    "caption": caption
                }

    def __del__(self):
        self.pdf_file.close()
