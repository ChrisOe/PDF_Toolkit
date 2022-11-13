import os
from PyPDF2 import PdfReader, PdfWriter, PdfMerger
from UIManager import UIManager


class PDFManager:

    def __init__(self, ui: UIManager, input_directory: str, output_directory: str):
        self.ui = ui
        self.check_for_dir(input_directory)
        self.check_for_dir(output_directory)
        self.input_directory = input_directory
        self.output_directory = output_directory

    def check_for_dir(self, directory: str):
        # check if directory exists and if not, create one
        if not os.path.isdir(f"./{directory}"):
            os.mkdir(f"./{directory}")
            self.ui.output(key="mk_folder", text=directory)

    def split_pdf(self, input_path: str, file_name: str):
        # create a new file for each page in a PDF file
        if file_name[-4:] == ".pdf":
            file_full_path = os.path.join(input_path, file_name)
            reader = PdfReader(file_full_path)
            number_of_pages = len(reader.pages)
            target_directory = os.path.join(self.output_directory, file_name[:-4])
            self.check_for_dir(target_directory)

            self.ui.output(key="file_name", text=file_name, prefix="┌─")
            self.ui.output(key="number_pages", text=str(number_of_pages), prefix="├─")
            self.ui.output(key="target_folder", text=target_directory, prefix="├─")

            for page_number in range(number_of_pages):
                writer = PdfWriter()
                page = reader.pages[page_number]
                writer.add_page(page)
                target_file_name = f"{file_name[:-4]}_{page_number}.pdf"
                target_full_path = os.path.join(target_directory, target_file_name)
                writer.write(target_full_path)
                self.ui.output(key="file_created", text=target_file_name, prefix="└─►")

    def split_all(self):
        # split up all files in the input folder
        self.ui.print_title("split_all")
        path = self.input_directory
        input_file_list = [file for file in os.listdir(path) if os.path.isfile(os.path.join(path, file))]
        for file_name in input_file_list:
            self.split_pdf(path, file_name)
            os.remove(os.path.join(path, file_name))

    def stitch_pdf(self):
        # merge all PDF files in a folder into one PDF file
        self.ui.print_title("stitch_pdf")
        path = self.input_directory
        input_dir_list = [file for file in os.listdir(path) if not os.path.isfile(os.path.join(path, file))]
        for dir_name in input_dir_list:
            sub_path = os.path.join(path, dir_name)
            target_file_name = f"{dir_name}.pdf"
            target_full_path = os.path.join(self.output_directory, target_file_name)
            input_file_list = [file for file in os.listdir(sub_path) if
                               os.path.isfile(os.path.join(sub_path, file))]
            merger = PdfMerger()
            for file_name in input_file_list:
                if file_name[-4:] == ".pdf":
                    input_file_full_path = os.path.join(sub_path, file_name)
                    merger.append(input_file_full_path)
                    self.ui.output(key="file_name", text=file_name, prefix="├─")
            if len(input_file_list) > 0:
                merger.write(target_full_path)
                self.ui.output(key="file_created", text=target_file_name, prefix="└─►")
                self.ui.add_line()
                merger.close()
