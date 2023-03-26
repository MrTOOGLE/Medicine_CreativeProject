from pdf import PDFHandler
from environment import AppEnvironment


def main():
    AppEnvironment.configure()
    for pdf_path in AppEnvironment.get_pdf_paths():
        handler = PDFHandler(pdf_path)
        #handler.extract_images()
        handler.extract_text()


if __name__ == '__main__':
    main()
