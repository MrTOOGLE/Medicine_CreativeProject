from src.pdf_script.environment import AppEnvironment
import fitz

doc = fitz.open(AppEnvironment.PDF_FILES_PATH + '1.pdf')
for page in doc:
    blocks = page.get_text("dict", flags=11)["blocks"]
    for b in blocks:
        for l in b["lines"]:
            for s in l["spans"]:
                print(f'{s["text"]} - {s["size"]}')
    print()
