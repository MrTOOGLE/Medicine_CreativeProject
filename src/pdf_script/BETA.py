import re

from environment import AppEnvironment
import fitz

from src.pdf_script.utils import FileUtils

pdf = fitz.open(AppEnvironment.PDF_FILES_PATH + "4.pdf")
a = [("\n", "~"), ("\t", " "), ("\xa0", " "), ("\xad", " "), ("–", "-"), ("—", "-")]
l = 0
p = re.compile(r"(?:Fig|Figure|Plate).*?(?:\d+|[A-Z])\.(\d+)")
for page in pdf:
    l += 1
    text = page.get_text()
    if "Figure" not in text:
        continue
    for i, j in a:
        text = text.replace(i, j)
    res = re.findall(r"Figure (\d+\.\d+)\s+[A-Z(](.*?)\.~", text)
    if not res:
        continue
    FileUtils.sort_captions(res)
    for r in res:
        #print(re.findall(p, r))
        print(r)
    print("-" * 100)
    if l > 150:
        break

"""
txt = txt.replace("\n", "~").replace("\t", " ") + " "
    # for image_index, footer in re.findall(FOOTER_PATTERNS["2"], txt):
    #    print(image_index, correct_footer(footer))
    a: list[str] = re.findall(r"(?<=• )Fig.? (\d+\.\d+) (?<!A–B)(.*?)~[.• ]", txt)
    for n, b in a:
        print(n, b)
        b = b.replace("~", " ")
        b = re.sub(r"(?<=\.)\s*[A-Z ]*:?$", "", b)
        b = re.sub(re.compile(r"\s{2,}"), " ", b)
        print(n, b)
        print("-" * 100)
    l += 1
    if l == 500:
        break
"""
