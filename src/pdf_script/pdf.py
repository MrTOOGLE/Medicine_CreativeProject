import io
import logging
import fitz
import json

from string import ascii_uppercase
from PIL import Image, ImageFile
from environment import AppEnvironment
from utils import FileUtils, triable, ImageInfo, GeneratorHandler


class PDFHandler:
    def __init__(self, pdf_path: str):
        self.pdf_file = fitz.open(pdf_path)
        self.pdf_name = FileUtils.get_file_name(pdf_path, with_extension=False)

    def extract_images(self) -> None:
        logging.info(f"Extracting images from {self.pdf_file.name}...")
        for page_index in range(len(self.pdf_file)):
            page = self.pdf_file[page_index]
            image_list = page.get_images()
            if image_list:
                logging.info(f"{self.pdf_file.name} Found a total of {len(image_list)} images in page {page_index}")

            for image_index, base_image in enumerate(image_list, start=1):
                image_info = self.__extract_image(base_image)
                if image_info.image:
                    self.__save_image(image_info, page_index, image_index)

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

    def extract_all_text(self):
        logging.info(f"Extracting text from {self.pdf_file.name}...")
        self.__extract_text()

    #@triable
    def __extract_text(self) -> None:
        save_directory = AppEnvironment.TEXT_PATH + self.pdf_name
        text = ""
        json_dict = {}
        page_image_getter = AppEnvironment.page_images(self.pdf_name)
        pages = [page for page in self.pdf_file][1:]
        for page in pages:
            blocks = page.get_text("dict", flags=11)["blocks"]
            image_footers = []
            for block in blocks:
                image_footer = ""
                for line in block["lines"]:
                    for span in line["spans"]:
                        font_size, text = span["size"], span["text"]
                        if font_size in FileUtils.IMAGE_FOOTER_FONTS[self.pdf_name]:
                            print(text)
                            image_footer += text

                if image_footer and FileUtils.is_footer(image_footer):
                    count_images = FileUtils.is_collage(image_footer)
                    image_footers.append((image_footer, count_images if count_images != 0 else 1))
            print(image_footers)
            if not image_footers:
                continue
            page_images = GeneratorHandler(next(page_image_getter))
            print(page_images.values)
            for footer, count_images in image_footers:
                if count_images > 1:
                    json_dict[", ".join([page_images.next() + "_" + ascii_uppercase[i] for i in range(count_images)])] = footer
                else:
                    a = page_images.next()
                    json_dict[a] = footer
        with open(AppEnvironment.TEXT_PATH + self.pdf_name + "/images_info.json", "w") as file:
            json.dump(json_dict, file)

    def __del__(self):
        self.pdf_file.close()
