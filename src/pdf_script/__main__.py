from pdf import PDFHandler, PDFImageExtractor, PDFImageCaptionsExtractor, PDFDataSaver
from environment import AppEnvironment


def main():
    AppEnvironment.configure()
    for pdf_path in AppEnvironment.get_pdf_paths():
        with PDFHandler(pdf_path) as handler:
            extractor = PDFImageCaptionsExtractor(handler)
            PDFDataSaver.save(save_data=extractor.extract(), save_directory_name=handler.name)


if __name__ == '__main__':
    main()
