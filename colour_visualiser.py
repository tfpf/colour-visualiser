#! /usr/local/bin/python3.8

import colorsys
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
    *_*_str: tk.StringVar (the above-mentioned proportion)
    *_*_tid: str (ID of the trace added to the tk.StringVar)

Methods:
    __init__
    __repr__
    __str__
    colour_update_using_rgb: convert from RGB
    colour_update_using_hsv: convert from HSV
'''

    ###########################################################################

    def __init__(self):
        '''\
Create the front-end window. Update the entries with the colour space values in
real time when the user writes valid numbers for a single colour space. Also
fill a patch with that colour to show the colour generated.
'''

        super().__init__()
        self.title('Colour Visualiser')
        self.resizable(False, False)

        # space to be left around widgets
        self.horz_padding = 10
        self.vert_padding = 10

        main_lbl = tk.Label(self, text = 'Colour Visualiser', padx = self.horz_padding, pady = self.vert_padding)
        main_lbl.grid(row = 0, column = 0, columnspan = 7, padx = self.horz_padding, pady = self.vert_padding)

        # the background colour of this label will be the input colour
        self.colour_lbl = tk.Label(self, text = (' ' * 140 + '\n') * 2, bg = 'white')
        self.colour_lbl.grid(row = 1, column = 0, columnspan = 7)

        # RGB colour space
        rgb_lbl = tk.Label(self, text = 'RGB Colour Space', padx = self.horz_padding, pady = self.vert_padding)
        rgb_lbl.grid(row = 2, column = 0, columnspan = 3)

        self.rgb_red_str = tk.StringVar()
        self.rgb_red_lbl = tk.Label(self, text = 'Red')
        self.rgb_red_ent = tk.Entry(self, textvariable = self.rgb_red_str)
        self.rgb_red_max = tk.Label(self, text = ' / 255')
        self.rgb_red_tid = self.rgb_red_str.trace_add('write', self.colour_update_using_rgb)
        self.rgb_red_lbl.grid(row = 3, column = 0, padx = self.horz_padding, pady = self.vert_padding)
        self.rgb_red_ent.grid(row = 3, column = 1, padx = (self.horz_padding, 0), pady = self.vert_padding)
        self.rgb_red_max.grid(row = 3, column = 2, padx = (0, self.horz_padding), pady = self.vert_padding)

        self.rgb_grn_str = tk.StringVar()
        self.rgb_grn_lbl = tk.Label(self, text = 'Green')
        self.rgb_grn_ent = tk.Entry(self, textvariable = self.rgb_grn_str)
        self.rgb_grn_max = tk.Label(self, text = ' / 255')
        self.rgb_grn_tid = self.rgb_grn_str.trace_add('write', self.colour_update_using_rgb)
        self.rgb_grn_lbl.grid(row = 4, column = 0, padx = self.horz_padding, pady = self.vert_padding)
        self.rgb_grn_ent.grid(row = 4, column = 1, padx = (self.horz_padding, 0), pady = self.vert_padding)
        self.rgb_grn_max.grid(row = 4, column = 2, padx = (0, self.horz_padding), pady = self.vert_padding)

        self.rgb_blu_str = tk.StringVar()
        self.rgb_blu_lbl = tk.Label(self, text = 'Blue')
        self.rgb_blu_ent = tk.Entry(self, textvariable = self.rgb_blu_str)
        self.rgb_blu_max = tk.Label(self, text = ' / 255')
        self.rgb_blu_tid = self.rgb_blu_str.trace_add('write', self.colour_update_using_rgb)
        self.rgb_blu_lbl.grid(row = 5, column = 0, padx = self.horz_padding, pady = self.vert_padding)
        self.rgb_blu_ent.grid(row = 5, column = 1, padx = (self.horz_padding, 0), pady = self.vert_padding)
        self.rgb_blu_max.grid(row = 5, column = 2, padx = (0, self.horz_padding), pady = self.vert_padding)

        # HSV colour space
        hsv_lbl = tk.Label(self, text = 'HSV Colour Space', padx = self.horz_padding, pady = self.vert_padding)
        hsv_lbl.grid(row = 2, column = 4, columnspan = 3)

        self.hsv_hue_str = tk.StringVar()
        self.hsv_hue_lbl = tk.Label(self, text = 'Hue')
        self.hsv_hue_ent = tk.Entry(self, textvariable = self.hsv_hue_str)
        self.hsv_hue_max = tk.Label(self, text = ' / 359')
        self.hsv_hue_tid = self.hsv_hue_str.trace_add('write', self.colour_update_using_hsv)
        self.hsv_hue_lbl.grid(row = 3, column = 4, padx = self.horz_padding, pady = self.vert_padding)
        self.hsv_hue_ent.grid(row = 3, column = 5, padx = (self.horz_padding, 0), pady = self.vert_padding)
        self.hsv_hue_max.grid(row = 3, column = 6, padx = (0, self.horz_padding), pady = self.vert_padding)

        self.hsv_sat_str = tk.StringVar()
        self.hsv_sat_lbl = tk.Label(self, text = 'Saturation')
        self.hsv_sat_ent = tk.Entry(self, textvariable = self.hsv_sat_str)
        self.hsv_sat_max = tk.Label(self, text = ' / 255')
        self.hsv_sat_tid = self.hsv_sat_str.trace_add('write', self.colour_update_using_hsv)
        self.hsv_sat_lbl.grid(row = 4, column = 4, padx = self.horz_padding, pady = self.vert_padding)
        self.hsv_sat_ent.grid(row = 4, column = 5, padx = (self.horz_padding, 0), pady = self.vert_padding)
        self.hsv_sat_max.grid(row = 4, column = 6, padx = (0, self.horz_padding), pady = self.vert_padding)

        self.hsv_val_str = tk.StringVar()
        self.hsv_val_lbl = tk.Label(self, text = 'Value')
        self.hsv_val_ent = tk.Entry(self, textvariable = self.hsv_val_str)
        self.hsv_val_max = tk.Label(self, text = ' / 255')
        self.hsv_val_tid = self.hsv_val_str.trace_add('write', self.colour_update_using_hsv)
        self.hsv_val_lbl.grid(row = 5, column = 4, padx = self.horz_padding, pady = self.vert_padding)
        self.hsv_val_ent.grid(row = 5, column = 5, padx = (self.horz_padding, 0), pady = self.vert_padding)
        self.hsv_val_max.grid(row = 5, column = 6, padx = (0, self.horz_padding), pady = self.vert_padding)

        # YIQ colour space
        yiq_lbl = tk.Label(self, text = 'YIQ Colour Space', padx = self.horz_padding, pady = self.vert_padding)
        yiq_lbl.grid(row = 6, column = 0, columnspan = 3)

        self.yiq_lum_str = tk.StringVar()
        self.yiq_lum_lbl = tk.Label(self, text = 'Luminance')
        self.yiq_lum_ent = tk.Entry(self, textvariable = self.yiq_lum_str)
        self.yiq_lum_max = tk.Label(self, text = ' / 255')
        # self.yiq_lum_tid = self.yiq_lum_str.trace_add('write', self.colour_update_using_yiq)
        self.yiq_lum_lbl.grid(row = 7, column = 0, padx = self.horz_padding, pady = self.vert_padding)
        self.yiq_lum_ent.grid(row = 7, column = 1, padx = (self.horz_padding, 0), pady = self.vert_padding)
        self.yiq_lum_max.grid(row = 7, column = 2, padx = (0, self.horz_padding), pady = self.vert_padding)


    ###########################################################################

    def __repr__(self):
        '''\
Representation of class object.
'''

        return '<colour_visualiser object>'

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

        try:
            red = round(float(self.rgb_red_str.get()))
            grn = round(float(self.rgb_grn_str.get()))
            blu = round(float(self.rgb_blu_str.get()))
        except ValueError:
            self.colour_lbl.config(bg = '#FFFFFF')
            return

        if not all(0 <= colour <= 255 for colour in (red, grn, blu)):
            self.colour_lbl.config(bg = '#FFFFFF')
            return

        # set the colour patch
        hex_code_of_colour = ''.join(f'{colour:02x}' for colour in (red, grn, blu))
        self.colour_lbl.config(bg = f'#{hex_code_of_colour}')

        # update HSV numbers
        hue, sat, val = colorsys.rgb_to_hsv(red / 255, grn / 255, blu / 255)
        self.hsv_hue_str.trace_remove('write', self.hsv_hue_tid)
        self.hsv_hue_str.set(round(hue * 359))
        self.hsv_hue_tid = self.hsv_hue_str.trace_add('write', self.colour_update_using_hsv)
        self.hsv_sat_str.trace_remove('write', self.hsv_sat_tid)
        self.hsv_sat_str.set(round(sat * 255))
        self.hsv_sat_tid = self.hsv_sat_str.trace_add('write', self.colour_update_using_hsv)
        self.hsv_val_str.trace_remove('write', self.hsv_val_tid)
        self.hsv_val_str.set(round(val * 255))
        self.hsv_val_tid = self.hsv_val_str.trace_add('write', self.colour_update_using_hsv)

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

        try:
            hue = round(float(self.hsv_hue_str.get()))
            sat = round(float(self.hsv_sat_str.get()))
            val = round(float(self.hsv_val_str.get()))
        except ValueError:
            self.colour_lbl.config(bg = '#FFFFFF')
            return

        if not 0 <= hue <= 359:
            self.colour_lbl.config(bg = '#FFFFFF')
            return

        if not all(0 <= ratio <= 255 for ratio in (sat, val)):
            self.colour_lbl.config(bg = '#FFFFFF')
            return

        # set the colour patch
        red, grn, blu = (round(colour * 255) for colour in colorsys.hsv_to_rgb(hue / 359, sat / 255, val / 255))
        hex_code_of_colour = ''.join(f'{colour:02x}' for colour in (red, grn, blu))
        self.colour_lbl.config(bg = f'#{hex_code_of_colour}')

        # update RGB numbers
        self.rgb_red_str.trace_remove('write', self.rgb_red_tid)
        self.rgb_red_str.set(red)
        self.rgb_red_tid = self.rgb_red_str.trace_add('write', self.colour_update_using_rgb)
        self.rgb_grn_str.trace_remove('write', self.rgb_grn_tid)
        self.rgb_grn_str.set(grn)
        self.rgb_grn_tid = self.rgb_grn_str.trace_add('write', self.colour_update_using_rgb)
        self.rgb_blu_str.trace_remove('write', self.rgb_blu_tid)
        self.rgb_blu_str.set(blu)
        self.rgb_blu_tid = self.rgb_blu_str.trace_add('write', self.colour_update_using_rgb)

