from pdf import PDFHandler
from environment import AppEnvironment


def main():
    AppEnvironment.configure()

    # for pdf_path in AppEnvironment.get_pdf_paths():
    #     PDFHandler(pdf_path).extract_images()

    for pdf_path in AppEnvironment.get_pdf_paths():
        PDFHandler(pdf_path).extract_images()



if __name__ == '__main__':
    main()
