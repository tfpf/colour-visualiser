#! /usr/local/bin/python3.8

import tkinter as tk

#######################################################################################################################

class colour_visualiser(tk.Tk):
    '''\
Display a GUI with entries in which a user may enter how they want to generate
a colour. Multiple colour spaces are supported. When the user updates the
numbers for one colour space, the numbers for the others are automatically
updated.

Attributes:
    horz_padding: int (horizontal padding around a widget)
    vert_padding: int (vertical padding around a widget)
    main_lbl: tk.Label (to display header text)
    *_*_lbl: tk.Label (prompt user for proportion of an item in a colour space)
    *_*_ent: tk.Entry (where user must enter said proportion)
    *_*_str: tk.StringVar (said proportion in `str' form)

Methods:
    __init__
    __repr__
    __str__
    colour_update
'''

    ###########################################################################

    def __init__(self):
        '''\
    Create the front-end window.

    Args:
        no arguments

    Returns:
        None
'''

        super().__init__()
        self.title('Colour Visualiser')
        self.resizable(False, False)

        # space to be left around widgets
        self.horz_padding = 10
        self.vert_padding = 10

        self.main_lbl = tk.Label(self, text = 'Colour Visualiser', padx = self.horz_padding, pady = self.vert_padding)
        self.main_lbl.grid(row = 0, column = 0, columnspan = 3)

        # RGB colour space
        self.rgb_lbl = tk.Label(self, text = 'RGB Colour Space', padx = self.horz_padding, pady = self.vert_padding)
        self.rgb_lbl.grid(row = 1, column = 0, columnspan = 2)

        self.rgb_red_str = tk.StringVar()
        self.rgb_red_lbl = tk.Label(self, text = 'Red')
        self.rgb_red_ent = tk.Entry(self, textvariable = self.rgb_red_str)
        self.rgb_red_str.trace_add('write', self.colour_update_using_rgb)
        self.rgb_red_lbl.grid(row = 2, column = 0, padx = self.horz_padding, pady = self.vert_padding)
        self.rgb_red_ent.grid(row = 2, column = 1, padx = self.horz_padding, pady = self.vert_padding)

        self.rgb_grn_str = tk.StringVar()
        self.rgb_grn_lbl = tk.Label(self, text = 'Green')
        self.rgb_grn_ent = tk.Entry(self, textvariable = self.rgb_grn_str)
        self.rgb_grn_str.trace_add('write', self.colour_update_using_rgb)
        self.rgb_grn_lbl.grid(row = 3, column = 0, padx = self.horz_padding, pady = self.vert_padding)
        self.rgb_grn_ent.grid(row = 3, column = 1, padx = self.horz_padding, pady = self.vert_padding)

        self.rgb_blu_str = tk.StringVar()
        self.rgb_blu_lbl = tk.Label(self, text = 'Blue')
        self.rgb_blu_ent = tk.Entry(self, textvariable = self.rgb_blu_str)
        self.rgb_blu_str.trace_add('write', self.colour_update_using_rgb)
        self.rgb_blu_lbl.grid(row = 4, column = 0, padx = self.horz_padding, pady = self.vert_padding)
        self.rgb_blu_ent.grid(row = 4, column = 1, padx = self.horz_padding, pady = self.vert_padding)

        # HSV colour space
        self.hsv_lbl = tk.Label(self, text = 'HSV Colour Space', padx = self.horz_padding, pady = self.vert_padding)
        self.hsv_lbl.grid(row = 5, column = 0, columnspan = 2)

        self.hsv_hue_str = tk.StringVar()
        self.hsv_hue_lbl = tk.Label(self, text = 'Hue')
        self.hsv_hue_ent = tk.Entry(self, textvariable = self.hsv_hue_str)
        self.hsv_hue_str.trace_add('write', self.colour_update_using_hsv)
        self.hsv_hue_lbl.grid(row = 6, column = 0, padx = self.horz_padding, pady = self.vert_padding)
        self.hsv_hue_ent.grid(row = 6, column = 1, padx = self.horz_padding, pady = self.vert_padding)

        self.hsv_sat_str = tk.StringVar()
        self.hsv_sat_lbl = tk.Label(self, text = 'Saturation')
        self.hsv_sat_ent = tk.Entry(self, textvariable = self.hsv_sat_str)
        self.hsv_sat_str.trace_add('write', self.colour_update_using_hsv)
        self.hsv_sat_lbl.grid(row = 7, column = 0, padx = self.horz_padding, pady = self.vert_padding)
        self.hsv_sat_ent.grid(row = 7, column = 1, padx = self.horz_padding, pady = self.vert_padding)

        self.hsv_val_str = tk.StringVar()
        self.hsv_val_lbl = tk.Label(self, text = 'Value')
        self.hsv_val_ent = tk.Entry(self, textvariable = self.hsv_val_str)
        self.hsv_val_str.trace_add('write', self.colour_update_using_hsv)
        self.hsv_val_lbl.grid(row = 8, column = 0, padx = self.horz_padding, pady = self.vert_padding)
        self.hsv_val_ent.grid(row = 8, column = 1, padx = self.horz_padding, pady = self.vert_padding)

        # display the colour selected
        self.update()
        self.colour_lbl = tk.Label(self, bg = 'white', width = 15, height = 20)
        self.colour_lbl.grid(row = 2, column = 2, rowspan = 8, padx = self.horz_padding, pady = self.vert_padding)

    ###########################################################################

    def colour_update_using_rgb(self, *args, **kwargs):
        '''\
    Change the background colour of the designated label according to the RGB
    numbers provided by the user.

    Args:
        none of the arguments received are used

    Returns:
        None
'''

        # sanity: all entries must contain integers
        try:
            red = int(self.rgb_red_str.get())
            grn = int(self.rgb_grn_str.get())
            blu = int(self.rgb_blu_str.get())
            self.colour_lbl.config(bg = '#FFFFFF')
        except ValueError:
            return

        # sanity: all integers must be unsigned 8-bit integers
        if not all(0 <= colour <= 255 for colour in (red, grn, blu)):
            self.colour_lbl.config(bg = '#FFFFFF')
            return

        hex_code_of_colour = ''.join(f'{colour:02x}' for colour in (red, grn, blu))
        self.colour_lbl.config(bg = f'#{hex_code_of_colour}')

    ###########################################################################

    def colour_update_using_hsv(self, *args, **kwargs):
        '''\
    Change the background colour of the designated label according to the HSV
    numbers provided by the user.

    Args:
        none of the arguments received are used

    Returns:
        None
'''

        # sanity: all entries must contain integers
        try:
            red = int(self.rgb_red_str.get())
            grn = int(self.rgb_grn_str.get())
            blu = int(self.rgb_blu_str.get())
        except ValueError:
            return

        # sanity: all integers must be unsigned 8-bit integers
        if not all(0 <= colour <= 255 for colour in (red, grn, blu)):
            return

        hex_code_of_colour = ''.join(f'{colour:02x}' for colour in (red, grn, blu))
        self.colour_lbl.config(bg = f'#{hex_code_of_colour}')


