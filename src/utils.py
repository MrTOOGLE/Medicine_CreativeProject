import functools
import logging
import os

from collections import namedtuple
from typing import Optional, Any, Callable
from PIL import Image, ImageOps, ImageFile


class FileUtils:
    STANDARD_IMAGE_EXTENSIONS = ["jpeg", "jpg", "png"]

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
