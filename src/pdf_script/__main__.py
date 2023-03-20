from pdf import PDFHandler
from environment import AppEnvironment


def main():
    AppEnvironment.configure()
    PDFHandler(AppEnvironment.PDF_FILES_PATH + "2.pdf").extract_all_text()
    #for pdf_path in AppEnvironment.get_pdf_paths()[1:]:
    #    handler = PDFHandler(pdf_path)
        # handler.extract_images()
    #    handler.extract_all_text()


if __name__ == '__main__':
    main()
