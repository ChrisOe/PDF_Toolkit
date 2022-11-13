from UIManager import UIManager
from PDFManager import PDFManager


ui = UIManager(default_language="DE")
pdf = PDFManager(ui=ui, input_directory="input", output_directory="output")

keep_running = True
while keep_running:
    menu_items = ["split_all", "stitch_all", "show_help", "end_run", "change_language"]
    option = ui.menu(menu_items, title="main")
    if option == "split_all":
        pdf.split_all()
    elif option == "stitch_all":
        pdf.stitch_pdf()
    elif option == "show_help":
        ui.show_help(menu_items)
    elif option == "end_run":
        keep_running = False
    elif option == "change_language":
        ui.change_language()
