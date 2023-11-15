import dearpygui.dearpygui as dpg
import threading
import os

dpg.create_context()


def search_keyword(directory, file, keyword, output_file):
    file_path = os.path.join(directory, file)
    with open(file_path, 'r', encoding=dpg.get_value("encoding")) as f:
        for line_number, line in enumerate(f, start=1):
            if keyword in line:
                print(f"Keyword '{keyword}' found in '{file_path}' at line {line_number}")
                if line.endswith('\n'):
                    output_file.write(line)
                else:
                    output_file.write(line + '\n')


def scan():
    supported_extensions = ["all_extensions", "txt", "dat", "log", "sav", "csv", "key", "db", "dbf"]
    extensions = []

    if dpg.get_value("all_extensions") is True:
        extensions = ["txt", "dat", "log", "sav", "csv", "key", "db", "dbf"]
    else:
        for sup_ext in supported_extensions:
            cse = dpg.get_value(sup_ext)
            if cse is True:
                extensions.append(sup_ext)

    keyword = dpg.get_value("keyword")
    directory = dpg.get_value("directory")
    file_list = os.listdir(directory)
    files = [file for file in file_list if any(file.lower().endswith(ext) for ext in extensions)]
    if keyword is not None:
        output_file_name = keyword + ".txt"
    else:
        output_file_name = "output.txt"

    with open(output_file_name, 'w', encoding=dpg.get_value("encoding")) as output_file:
        threads = []

        for file in files:
            thread = threading.Thread(target=search_keyword, args=(directory, file, keyword, output_file))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

    if os.path.exists(output_file_name):
        with open(output_file_name, 'r', encoding=dpg.get_value("encoding")) as output_file:
            lines = '\n'.join(line.strip() for line in output_file)
        if lines:
            dpg.set_value("output", lines)
        else:
            dpg.set_value("output", None)
    else:
        dpg.set_value("output", "File not found")

    if os.path.exists(output_file_name) and os.path.getsize(output_file_name) == 0:
        os.remove(output_file_name)


def select_directory(sender, app_data):
    file_path = app_data.get("file_path_name")
    dpg.set_value("directory", file_path)


with dpg.window(tag="choose_extensions", pos=(570, 0), no_title_bar=True, no_resize=True, no_move=True, no_background=True):
    dpg.add_checkbox(label="all types", tag="all_extensions")
    dpg.add_checkbox(label="txt", tag="txt")
    dpg.add_checkbox(label="dat", tag="dat")
    dpg.add_checkbox(label="log", tag="log")
    dpg.add_checkbox(label="sav", tag="sav")
    dpg.add_checkbox(label="csv", tag="csv")
    dpg.add_checkbox(label="key", tag="key")
    dpg.add_checkbox(label="db", tag="db")
    dpg.add_checkbox(label="dbf", tag="dbf")

with dpg.window(tag="Primary Window"):
    dpg.add_file_dialog(
        directory_selector=True, show=False, tag="file_dialog_1", height=250, callback=select_directory)

    dpg.add_input_text(label="Keyword", tag="keyword")
    with dpg.tooltip(dpg.last_item()):
        dpg.add_text("Word to search in database")

    encoding_items = ["UTF-8", "UTF-16", "UTF-32", "ISO-8859-1", "Latin-1", "Windows-1252", "ASCII"]
    dpg.add_listbox(items=encoding_items, default_value="UTF-8", tag="encoding", label="Encoding")

    dpg.add_button(label="Set directory", callback=lambda: dpg.show_item("file_dialog_1"), width=100)
    dpg.add_button(label="Scan", width=100, callback=scan)
    dpg.add_spacer(parent=2)
    dpg.add_text(tag="directory")

    dpg.add_input_text(label="Output", tag="output", readonly=True, multiline=True, height=146)

with dpg.theme() as global_theme:
    with dpg.theme_component(dpg.mvAll):
        dpg.add_theme_style(dpg.mvStyleVar_WindowRounding, 3)
        dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 3)
        dpg.add_theme_style(dpg.mvStyleVar_GrabRounding, 3)
        dpg.add_theme_style(dpg.mvStyleVar_TabRounding, 3)
        dpg.add_theme_style(dpg.mvStyleVar_ChildRounding, 3)
        dpg.add_theme_style(dpg.mvStyleVar_PopupRounding, 3)
        dpg.add_theme_style(dpg.mvStyleVar_ScrollbarRounding, 3)
        dpg.add_theme_style(dpg.mvStyleVar_FramePadding, 4, 4)
        dpg.add_theme_style(dpg.mvStyleVar_ItemSpacing, 5, 5)

dpg.bind_theme(global_theme)
dpg.create_viewport(title='Keyword searcher', width=700, height=385)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window("Primary Window", True)
dpg.start_dearpygui()
dpg.destroy_context()
