from environment import AppEnvironment
import fitz

doc = fitz.open(AppEnvironment.PDF_FILES_PATH + '1.pdf')
for page in doc:
    blocks = page.get_text("dict", flags=11)["blocks"]
    for block in blocks:
        text = ""
        for line in block["lines"]:
            for span in line["spans"]:
                if span["size"] == 8.5:
                    text += span["text"]
        print(text)

