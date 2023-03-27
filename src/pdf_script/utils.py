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

    __CAPTION_PATTERNS = {
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

    __IMAGE_INDEX_PATTERN = {
        "1": re.compile(r"(\d+)"),
        "2": re.compile(r"(\d+)\.(\d+)"),
        "3": re.compile(r"(\d+|[A-Z])\.(\d+)"),
        "4": re.compile(r"(\d+)\.(\d+)")
    }
    __IMAGE_POINTER_PATTERN = re.compile(r"\(?([a-zA-Z])\)")
    __IMAGE_DOUBLE_POINTER_PATTERN = re.compile(r"\(([a-zA-Z]) and ([a-zA-Z])\)?")

    @classmethod
    def convert_image(cls, image_path: str, to_extension=".png") -> None:
        image = Image.open(image_path)
        image.save(cls.cut_extension(image_path) + to_extension)
        os.remove(image_path)

    @classmethod
    def get_file_name(cls, file_path: str, with_extension: bool = True) -> str:
        if with_extension:
            return file_path.split("/")[-1]

        return cls.cut_extension(file_path).split("/")[-1]

    @classmethod
    def count_images_in_caption(cls, text: str) -> int:
        selected_values = sorted(list(set(map(str.lower, re.findall(cls.__IMAGE_POINTER_PATTERN, text)))))
        special_values = re.findall(cls.__IMAGE_DOUBLE_POINTER_PATTERN, text)
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

    @classmethod
    def correct_caption(cls, caption: str, name_file_source: str) -> str:
        replacements = cls.__CAPTION_REPLACEMENTS[name_file_source] + cls.__CAPTION_POST_REPLACEMENTS
        for replace_pattern, replacement in replacements:
            if isinstance(replace_pattern, str):
                caption = caption.replace(replace_pattern, replacement)
            else:
                caption = re.sub(replace_pattern, replacement, caption)

        return caption

    @classmethod
    def extract_captions(cls, text: str, name_file_source: str) -> list[str]:
        for replace_pattern, replacement in cls.__CAPTION_PRE_REPLACEMENTS:
            text = text.replace(replace_pattern, replacement)

        captions = re.findall(cls.__CAPTION_PATTERNS[name_file_source], text + " ")
        for i in range(len(captions)):
            image_index, caption = captions[i]
            caption = cls.correct_caption(caption, name_file_source)
            captions[i] = (image_index, caption)

        cls.sort_captions(captions, name_file_source)
        return captions

    @classmethod
    def sort_captions(cls, captions: list[str], name_file_source: str) -> None:
        def __sort_function(caption):
            image_index = re.findall(cls.__IMAGE_INDEX_PATTERN[name_file_source], caption[0])[0]
            first_index, second_index = "0", "0"
            if isinstance(image_index, tuple):
                first_index, second_index = image_index
            else:
                first_index = image_index[0]
            first_index = int(first_index) if first_index.isdigit() else first_index
            second_index = int(second_index) if second_index.isdigit() else second_index

            return (first_index, second_index) if second_index else (first_index, 0)

        captions.sort(key=__sort_function)

    @staticmethod
    def to_rgb_image(image: ImageFile) -> ImageFile:
        if image.mode == "CMYK":
            image = Image.merge(image.mode, [ImageOps.invert(b.convert('L')) for b in image.split()]).convert("RGB")
        elif image.mode == "RGBA":
            image = ImageOps.invert(image.convert("RGB"))

        return image

    @staticmethod
    def cut_extension(file_path: str) -> str:
        *path, name = file_path.split("/")
        return '/'.join(path) + '/' + name[:name.index(".")]


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


class GeneratorHandler:
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
