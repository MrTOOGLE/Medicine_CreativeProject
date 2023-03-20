import functools
import logging
import os
import re

from collections import namedtuple
from typing import Optional, Any, Callable, Generator
from PIL import Image, ImageOps, ImageFile


class FileUtils:
    STANDARD_IMAGE_EXTENSIONS = ["jpeg", "jpg", "png"]
    IMAGE_FOOTER_FONTS = {
        "1": (8.5, 0),
        "2": (8.0, 10.5),
        "3": (9.0, 0),
        "4": (8.5, 0)
    }

    @staticmethod
    def convert_image(image_path: str, to_extension=".png") -> None:
        image = Image.open(image_path)
        image.save(FileUtils.cut_extension(image_path) + to_extension)
        os.remove(image_path)

    @staticmethod
    def to_rgb_image(image: ImageFile) -> ImageFile:
        if image.mode == "CMYK":
            image = Image.merge(image.mode, [ImageOps.invert(b.convert('L')) for b in image.split()]).convert("RGB")
        elif image.mode == "RGBA":
            image = ImageOps.invert(image.convert("RGB"))

        return image

    @staticmethod
    def get_file_name(file_path: str, with_extension: bool = True) -> str:
        if with_extension:
            return file_path.split("/")[-1]

        return FileUtils.cut_extension(file_path).split("/")[-1]

    @staticmethod
    def cut_extension(file_path: str) -> str:
        *path, name = file_path.split("/")
        return '/'.join(path) + '/' + name[:name.index(".")]

    @staticmethod
    def is_collage(text: str) -> int:
        side_values = len(re.findall(r"\(.*[a-zA-Z]\)", text))
        return len(re.findall(r"[( ][a-zA-Z]\s?[)–]", text)) - side_values

    @staticmethod
    def is_footer(text: str) -> bool:
        if text.lower().strip().startswith("fig"):
            return True
        return False


def triable(func: Callable):
    @functools.wraps(func)
    def _wrapper(*args, **kwargs) -> Optional[Any]:
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logging.error(f"An error occurred while trying to execute the <{func.__name__}> function")
            logging.error(e)
            return None

    return _wrapper


ImageInfo = namedtuple("ImageInfo", ["image", "extension"])


class GeneratorHandler:
    def __init__(self, generator: Generator):
        self.values = list(generator)
        self.generator = (i for i in self.values)

    def next(self):
        try:
            return next(self.generator)
        except StopIteration:
            return self.values[-1]


if __name__ == '__main__':
    print(FileUtils.is_collage("Fig. 89 Graphical form of an analysis result – two parameters A – dot plots and B – single parameter histo-grams 2"))
