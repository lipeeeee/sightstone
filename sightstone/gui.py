# Module that handles gui

import dearpygui.dearpygui as dpg

WIDTH = 200
HEIGHT = 300

def init_gui(sightstone_hook):
    """Inits dearpygui window"""
    dpg.create_context()
    
    with dpg.window(label="sightstone", width=WIDTH, height=HEIGHT, no_resize=True, no_title_bar=True, tag="p1"):
        with dpg.tab_bar():
            with dpg.tab(label="Client"):
                dpg.add_checkbox(label="Test", callback=lambda: True)
    dpg.set_primary_window("p1", True)

    dpg.create_viewport(
        title="sightstone", # TODO: Make title safe
        width=WIDTH, height=HEIGHT,
        resizable=True
    )
    dpg.show_viewport()

    dpg.setup_dearpygui()
    while dpg.is_dearpygui_running():
        dpg.render_dearpygui_frame()
    dpg.destroy_context()
