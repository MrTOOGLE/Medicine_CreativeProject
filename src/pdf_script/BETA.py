from environment import AppEnvironment
import fitz
import re

from utils import FileUtils

FOOTER_PATTERNS = {
    "1": re.compile(r"(?<=~Fig\. )(\d+) (.*?)(?<=~[A-Z ])"),
    "2": re.compile(r"")
}

FOOTER_CORRECTIONS = {
    "1": [(re.compile(r"~\w$"), ""), ("-~", ""), ("~", ""), (re.compile(r"\s{2,}"), " ")],
    "2": []
}


def correct_footer(footer: str):
    for replace_pattern, replacement in FOOTER_CORRECTIONS["1"]:
        if type(replace_pattern) == re.Pattern:
            footer = re.sub(replace_pattern, replacement, footer)
        else:
            footer = footer.replace(replace_pattern, replacement)

    return footer


doc = fitz.open(AppEnvironment.PDF_FILES_PATH + '2.pdf')
_text = []
for page in doc:
    text = page.get_text()
    if "Fig." in text:
        _text.append(text)

l = 0
for txt in _text:
    txt = txt.replace("\n", "~").replace("\t", " ") + " "
    # for image_index, footer in re.findall(FOOTER_PATTERNS["2"], txt):
    #    print(image_index, correct_footer(footer))
    a = re.findall(r"(?<!\()Fig. (?<!A–B\))\d+\.\d+ .*?~[.• ]", txt)
    if a:
        for t in a:
            b = FileUtils.is_collage(t)
            l += b if b != 0 else 1
            if b < 0:
                print(t)
print(l)
# print(re.findall(r"(?<=~Fig\. )(\d+) (.*?)(?<=~[A-Z ])", "~Fig. 25 Basophil microphoto~Fig. 26 Basophil with dark coarse granules overlap-~ping the nucleus ~ "))
