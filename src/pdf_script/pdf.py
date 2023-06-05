from __future__ import annotations

import abc
import io
import json
import logging
import os
import fitz

from typing import Iterator, Any, Optional, NamedTuple
from PIL import Image
from PIL.ImageFile import ImageFile
from fitz.fitz import Document, Page

from src.pdf_script.environment import AppEnvironment
from utils import FileUtils, triable, IteratorHandler, timer


class PDFHandler:
    def __init__(self, path: str):
        self._path: str = path
        self._name: str = FileUtils.get_file_name(path, with_extension=False)
        self._file: Optional[Document] = None

    @property
    def path(self) -> str:
        return self._path

    @property
    def name(self) -> str:
        return self._name

    @property
    def file(self) -> Optional[Document]:
        return self._file

    def get_pages(self, start=0) -> tuple[Page]:
        return tuple(self._file.pages())[start:]

    def __iter__(self) -> Iterator[Page]:
        return iter(self.get_pages())

    def __enter__(self) -> PDFHandler:
        self._file = fitz.open(self.path)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._file.close()


class PDFDataExtractor(abc.ABC):
    def __init__(self, handler: PDFHandler, start_page=0):
        self.handler = handler
        self._current_page_index = start_page

    @abc.abstractmethod
    def extract(self) -> Optional[Any]:
        pass


class ImageData(NamedTuple):
    page_index: int
    image_index: int
    image: Optional[Any]
    extension: str


class PDFImageExtractor(PDFDataExtractor):
    def __init__(self, handler: PDFHandler):
        super().__init__(handler, start_page=1)

        self._images: list[ImageData] = []

    @property
    def images(self):
        return self._images

    @timer
    def extract(self) -> list[ImageData]:
        logging.info(f"Extracting images from {self.handler.name}.pdf...")
        for page in self.handler:
            page_images = page.get_images()
            self._extract_images_data_from_page(page_images)

            self._current_page_index += 1

        return self.images

    def _extract_images_data_from_page(self, page_images) -> None:
        for image_index, page_image in enumerate(page_images, start=1):
            image = self._extract_image_data(xref=page_image[0])
            if image is None:
                continue

            image_data = ImageData(self._current_page_index, image_index, image, image.extension)
            self.images.append(image_data)

    @triable
    def _extract_image_data(self, xref: int) -> Optional[ImageFile]:
        base_image = self._get_image_on_xref(xref)
        image_extension = base_image["ext"]
        image_bytes = base_image["image"]
        image = Image.open(io.BytesIO(image_bytes))
        if not image:
            return None

        if image.mode != "RGB":
            image = FileUtils.to_rgb_image(image)
        setattr(image, "extension", image_extension)
        return image

    def _get_image_on_xref(self, xref: int):
        return self.handler.file.extract_image(xref)


class PDFImageCaptionsExtractor(PDFDataExtractor):
    def __init__(self, handler: PDFHandler):
        super().__init__(handler, start_page=2)

        self._image_captions = {}
        self._page_image_getter = IteratorHandler(AppEnvironment.get_page_images(self.handler.name))

    @property
    def image_captions(self) -> dict:
        return self._image_captions

    @timer
    def extract(self) -> dict:
        logging.info(f"Extracting caption text from {self.handler.name}...")
        pages = self.handler.get_pages(start=1)
        for page in pages:
            text = page.get_text()
            self._extract_captions_text_from_page(text)

            self._current_page_index += 1

        logging.info(f"Extracting caption text from {self.handler.name} is finished.")
        return self.image_captions

    @triable
    def _extract_captions_text_from_page(self, text: str) -> None:
        page_captions = FileUtils.extract_captions(text, self.handler.name)
        if not page_captions:
            return

        if not self._try_sync_page_indexes():
            return

        _, page_images = self._page_image_getter.last_value
        page_images_info = self._get_page_image_captions(page_images, iter(page_captions))
        self._image_captions.update(page_images_info)

    def _try_sync_page_indexes(self) -> bool:
        self._page_image_getter.next()
        images_page_index, page_images = self._page_image_getter.last_value

        while self._current_page_index != images_page_index:
            if images_page_index > self._current_page_index or self._page_image_getter.is_empty:
                self._page_image_getter.back()
                return False
            else:
                self._page_image_getter.next()
                images_page_index, page_images = self._page_image_getter.last_value

        return True

    @staticmethod
    def _get_page_image_captions(page_images: Iterator, page_captions: Iterator) -> dict:
        page_image_captions = {}
        page_images = IteratorHandler(page_images)
        page_captions = IteratorHandler(page_captions)

        while True:
            page_captions.next()
            image_index, caption = page_captions.last_value
            count_images = FileUtils.count_images_in_caption(caption)
            for _ in range(count_images):
                page_images.next()
                if page_captions.is_empty and page_images.is_empty:
                    return page_image_captions

                image = page_images.last_value
                page_image_captions[image] = {
                    "index": image_index,
                    "required": None,
                    "caption": caption
                }


class PDFDataSaver:
    _STANDARD_IMAGE_EXTENSIONS = ["jpeg", "jpg", "png"]

    @classmethod
    def save(cls, save_data: Any, save_directory_name: str) -> None:
        if isinstance(save_data, list) and isinstance(save_data[0], ImageData):
            cls.save_images(save_data, save_directory_name)
        elif isinstance(save_data, dict):
            cls.save_image_captions(save_data, save_directory_name)
        else:
            raise NotImplementedError("There is no implemented method for saving this data")

    @classmethod
    def save_images(cls, images: list[ImageData], save_directory_name: str) -> None:
        for image in images:
            cls.save_image(image, save_directory_name)

    @classmethod
    def save_image(cls, image_data: ImageData, save_directory_name: str) -> None:
        image, extension = image_data.image, image_data.extension
        page_index, image_index = image_data.page_index, image_data.image_index
        save_directory = AppEnvironment.IMAGES_PATH + save_directory_name
        image_path = f"{save_directory}/image{page_index}_{image_index}."

        with open(image_path + (extension if extension in cls._STANDARD_IMAGE_EXTENSIONS else "png"), "wb") as file:
            image.save(file)

    @staticmethod
    def _convert_image(image_path: str, to_extension: str) -> None:
        image = Image.open(image_path)
        image.save(FileUtils.cut_extension(image_path) + to_extension)
        os.remove(image_path)

    @staticmethod
    def save_image_captions(image_captions: dict, save_directory_name: str) -> None:
        with open(AppEnvironment.TEXT_PATH + save_directory_name + "/image_captions.json", "w") as file:
            json.dump(image_captions, file)
