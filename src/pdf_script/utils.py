import functools
import logging
import os
import re
import time

from collections import namedtuple
from string import ascii_lowercase
from typing import Optional, Any, Callable, Generator
from PIL import Image, ImageOps, ImageFile


class FileUtils:
    STANDARD_IMAGE_EXTENSIONS = ["jpeg", "jpg", "png"]

    CAPTION_PATTERNS = {
        "1": re.compile(r"(?<=~Fig\. )(\d+) (.*?)(?<=~[A-Z ])"),
        "2": re.compile(r"(?<=• )Fig.? (\d+\.\d+) (?<!A–B)(.*?)~[.• ]"),
        "3": re.compile(r"(?:Fig|Plate)\.\s*?((?:\d+|[A-Z])\.\d+)\s*?\.(.*?(?:\.~|~$|Used via license:.*/[~ ]))"),
        "4": re.compile(r"Figure (\d+\.\d+)\s+([A-Z(].*?)\.~")
    }

    __CAPTION_PRE_REPLACEMENTS = [
        ("\n", "~"),
        ("\t", " "),
        ("\xa0", " "),
        ("\xad", " "),
        ("–", "-"),
        ("—", "-"),
        ("×", "x"),
        ("’", "'")
    ]
    __CAPTION_REPLACEMENTS = {
        "1": [(re.compile(r"~\w$"), "")],
        "2": [(re.compile(r"(?<=\.)\s*[A-Z ]*:?$"), "")],
        "3": [],
        "4": []
    }
    __CAPTION_POST_REPLACEMENTS = [
        ("-~", ""),
        ("~", ""),
        ("- ", "-"),
        (re.compile(r"\s{2,}"), " ")
    ]

    __IMAGE_INDEX_PATTERN = re.compile(r"(?:\d+|[A-Z])\.(\d+)")
    __IMAGE_POINTER_PATTERN = re.compile(r"\(?([a-zA-Z])\)")
    __IMAGE_DOUBLE_POINTER_PATTERN = re.compile(r"\(([a-zA-Z]) and ([a-zA-Z])\)?")

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
    def count_images_in_caption(text: str) -> int:
        selected_values = sorted(list(set(map(str.lower, re.findall(FileUtils.__IMAGE_POINTER_PATTERN, text)))))
        special_values = re.findall(FileUtils.__IMAGE_DOUBLE_POINTER_PATTERN, text)
        result = set()
        for char in ascii_lowercase:
            if not selected_values:
                break
            if selected_values.pop(0).lower() == char:
                result.add(char)
            else:
                break

        for special_value in special_values:
            result.update(*special_value)

        return len(result) if len(result) > 0 else 1

    @staticmethod
    def correct_caption(caption: str, name_file_source: str) -> str:
        replacements = FileUtils.__CAPTION_REPLACEMENTS[name_file_source] + FileUtils.__CAPTION_POST_REPLACEMENTS
        for replace_pattern, replacement in replacements:
            if isinstance(replace_pattern, str):
                caption = caption.replace(replace_pattern, replacement)
            else:
                caption = re.sub(replace_pattern, replacement, caption)

        return caption

    @staticmethod
    def extract_captions(text: str, name_file_source: str) -> list[str]:
        for replace_pattern, replacement in FileUtils.__CAPTION_PRE_REPLACEMENTS:
            text = text.replace(replace_pattern, replacement)

        captions = re.findall(FileUtils.CAPTION_PATTERNS[name_file_source], text + " ")
        for i in range(len(captions)):
            image_index, caption = captions[i]
            caption = FileUtils.correct_caption(caption, name_file_source)
            captions[i] = (image_index, caption)

        captions.sort()
        return captions

    @staticmethod
    def sort_captions(captions: list[str]) -> None:
        captions.sort(key=lambda caption: tuple(map(int, *re.findall(FileUtils.__IMAGE_INDEX_PATTERN, caption[0]))))


ImageInfo = namedtuple("ImageInfo", ["image", "extension"])


def triable(func: Callable) -> Callable:
    @functools.wraps(func)
    def _wrapper(*args, **kwargs) -> Optional[Any]:
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logging.error(f"An error occurred while trying to execute the <{func.__name__}> function")
            logging.error(e)
            return None

    return _wrapper


def timer(func: Callable) -> Callable:
    @functools.wraps(func)
    def __wrapper(*args, **kwargs) -> Optional[Any]:
        start = time.time()
        result = func(*args, **kwargs)
        logging.info(f"Function <{func.__name__}> has executed in {round(time.time() - start, 4)}s")
        return result

    return __wrapper


class GeneratorHelper:
    def __init__(self, generator: Generator):
        self.generator = generator
        self.is_empty = False
        self.last_value = None

    def next(self) -> Optional[Any]:
        try:
            self.last_value = next(self.generator)
            return self.last_value
        except StopIteration:
            self.is_empty = True
            return None

    def back(self) -> None:
        self.generator = (i for i in [self.last_value] + list(self.generator))


if __name__ == '__main__':
    print(__name__)
