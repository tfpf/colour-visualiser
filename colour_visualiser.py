#! /usr/local/bin/python3.8

import colorsys
import time
import tkinter as tk

pad_x = 10
pad_y = 10

#######################################################################################################################


#######################################################################################################################

class colour_visualiser(tk.Frame):
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


    def __init__(self, parent):
        '''\
Create the front-end window. Update the entries with the colour space values in
real time when the user writes valid numbers for a single colour space. Also
fill a patch with that colour to show the colour generated.
'''

        tk.Frame.__init__(self, parent)
        self.grid(padx = pad_x, pady = pad_y)
        parent.title('Colour Visualiser')
        parent.resizable(False, False)

        # this is a dictionary of all the contents of the editable entries
        # they are indexed by the name of the colour space
        self.contents_dict = dict()

        # the plan is to use a chain of traces to update the colour information
        # hence, use these to determine whether to continue or not
        # otherwise, there will be an infinite loop of traces
        self.trace_disabled = False   # disable all traces
        self.update_disabled = 'none' # disable updating a colour space

        # title
        main_lbl = tk.Label(self, text = 'Colour Visualiser')
        main_lbl.grid(row = 0, column = 0, columnspan = 2, padx = pad_x, pady = pad_y)

        # the background colour of this label will be the input colour
        self.colour_lbl = tk.Label(self, text = (' ' * 180 + '\n') * 2, bg = 'white')
        self.colour_lbl.grid(row = 1, column = 0, columnspan = 2, padx = pad_x, pady = (pad_y, 2 * pad_y))

        rgb_frame = self.create_frame_for_new_colour_space('RGB', [('Red', 255), ('Green', 255), ('Blue', 255)])
        rgb_frame.grid(row = 2, column = 0, padx = pad_x, pady = pad_y)

        cmy_frame = self.create_frame_for_new_colour_space('CMY', [('Cyan', 255), ('Magenta', 255), ('Yellow', 255)])
        cmy_frame.grid(row = 2, column = 1, padx = pad_x, pady = pad_y)

        hsv_frame = self.create_frame_for_new_colour_space('HSV', [('Hue', 359), ('Saturation', 255), ('Value', 255)])
        hsv_frame.grid(row = 3, column = 0, padx = pad_x, pady = pad_y)

        hsl_frame = self.create_frame_for_new_colour_space('HSL', [('Hue', 359), ('Saturation', 255), ('Luminance', 255)])
        hsl_frame.grid(row = 3, column = 1, padx = pad_x, pady = pad_y)


        # self.hsv_hue_str = tk.StringVar()
        # self.hsv_hue_lbl = tk.Label(self, text = 'Hue')
        # self.hsv_hue_ent = tk.Entry(self, textvariable = self.hsv_hue_str)
        # self.hsv_hue_max = tk.Label(self, text = ' / 359')
        # self.hsv_hue_tid = self.hsv_hue_str.trace_add('write', self.colour_update_using_hsv)
        # self.hsv_hue_lbl.grid(row = 7, column = 0, padx = self.horz_padding, pady = self.vert_padding)
        # self.hsv_hue_ent.grid(row = 7, column = 1, padx = (self.horz_padding, 0), pady = self.vert_padding)
        # self.hsv_hue_max.grid(row = 7, column = 2, padx = (0, self.horz_padding), pady = self.vert_padding)

        # # # YIQ colour space
        # # yiq_lbl = tk.Label(self, text = 'YIQ colour space')
        # # yiq_lbl.grid(row = 6, column = 4, columnspan = 3, padx = self.horz_padding, pady = self.vert_padding)

        # # self.yiq_lum_str = tk.StringVar()
        # # self.yiq_lum_lbl = tk.Label(self, text = 'Luminance')
        # # self.yiq_lum_ent = tk.Entry(self, textvariable = self.yiq_lum_str)
        # # self.yiq_lum_max = tk.Label(self, text = ' / 255')
        # # # self.yiq_lum_tid = self.yiq_lum_str.trace_add('write', self.colour_update_using_yiq)
        # # self.yiq_lum_lbl.grid(row = 7, column = 0, padx = self.horz_padding, pady = self.vert_padding)
        # # self.yiq_lum_ent.grid(row = 7, column = 1, padx = (self.horz_padding, 0), pady = self.vert_padding)
        # # self.yiq_lum_max.grid(row = 7, column = 2, padx = (0, self.horz_padding), pady = self.vert_padding)

        # # self.yiq_inp_str = tk.StringVar()
        # # self.yiq_inp_lbl = tk.Label(self, text = 'Magenta')
        # # self.yiq_inp_ent = tk.Entry(self, textvariable = self.yiq_inp_str)
        # # self.yiq_inp_max = tk.Label(self, text = ' / 255')
        # # # self.yiq_inp_tid = self.yiq_inp_str.trace_add('write', self.colour_update_using_yiq)
        # # self.yiq_inp_lbl.grid(row = 8, column = 0, padx = self.horz_padding, pady = self.vert_padding)
        # # self.yiq_inp_ent.grid(row = 8, column = 1, padx = (self.horz_padding, 0), pady = self.vert_padding)
        # # self.yiq_inp_max.grid(row = 8, column = 2, padx = (0, self.horz_padding), pady = self.vert_padding)

        # # self.yiq_qdr_str = tk.StringVar()
        # # self.yiq_qdr_lbl = tk.Label(self, text = 'Yellow')
        # # self.yiq_qdr_ent = tk.Entry(self, textvariable = self.yiq_qdr_str)
        # # self.yiq_qdr_max = tk.Label(self, text = ' / 255')
        # # # self.yiq_qdr_tid = self.yiq_qdr_str.trace_add('write', self.colour_update_using_yiq)
        # # self.yiq_qdr_lbl.grid(row = 9, column = 0, padx = self.horz_padding, pady = self.vert_padding)
        # # self.yiq_qdr_ent.grid(row = 9, column = 1, padx = (self.horz_padding, 0), pady = self.vert_padding)
        # # self.yiq_qdr_max.grid(row = 9, column = 2, padx = (0, self.horz_padding), pady = self.vert_padding)

    ###########################################################################

    def __repr__(self):
        '''\
Representation of class object.
'''

        return '<colour_visualiser object>'

    ###########################################################################

    def create_frame_for_new_colour_space(self, title, parameter_list):

        curr_frame = tk.Frame(self)

        main_lbl = tk.Label(curr_frame, text = f'{title} Colour Space')
        main_lbl.grid(row = 0, column = 0, columnspan = 3, padx = pad_x, pady = pad_y)

        # this will contain the contents of the entries
        contents = []

        for i, item in enumerate(parameter_list, 1):
            var = tk.StringVar(name = f'{title}_{i}')
            lbl = tk.Label(curr_frame, text = item[0], width = 10)
            ent = tk.Entry(curr_frame, textvariable = var)
            lim = tk.Label(curr_frame, text = f' / {item[1]}', width = 6)

            var.trace_add('write', self.colour_update_wrapper)
            lbl.grid(row = i, column = 0, padx = pad_x, pady = pad_y)
            ent.grid(row = i, column = 1, pady = pad_y)
            lim.grid(row = i, column = 2, pady = pad_y)

            contents.append(var)

        # put `contents_item' in the dictionary
        # it should be easily accessible, so index it with the name
        self.contents_dict[title] = contents

        return curr_frame

    ###########################################################################

    def colour_update_wrapper(self, name, *args, **kwargs):

        if self.trace_disabled:
            return

        colour_space = name[: -2]
        colour_components = [item.get() for item in self.contents_dict[colour_space]]

        if colour_space == 'RGB':
            print('RGB update detected.')
            self.trace_disabled = True
            for i in self.contents_dict:
                if i != self.update_disabled and i != 'RGB':
                    print(f'{i} will be updated.')
                    self.contents_dict[i][0].set(1)
            self.trace_disabled = False
            return

        print(f'{colour_space} update detected.')
        self.update_disabled = colour_space
        print('RGB will be updated.')
        self.contents_dict['RGB'][0].set(1)
        time.sleep(1)
        self.update_disabled = 'none'

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

        # idea:
        #     if RGB is written, disable all other traces, write all converted values, enable all traces
        #     if any other is written, disable trace for itself, write RGB converted value, enable trace for itself
        # trace should take in the seconf one


        # update CMY numbers
        cyn, mgt, ylw = (255 - colour for colour in (red, grn, blu))
        # self.cmy_cyn_str.trace_remove('write', self.cmy_cyn_tid)
        self.cmy_cyn_str.set(cyn)
        # self.cmy_cyn_tid = self.cmy_cyn_str.trace_add('write', self.colour_update_using_cmy)
        # self.cmy_mgt_str.trace_remove('write', self.cmy_mgt_tid)
        self.cmy_mgt_str.set(mgt)
        # self.cmy_mgt_tid = self.cmy_mgt_str.trace_add('write', self.colour_update_using_cmy)
        # self.cmy_ylw_str.trace_remove('write', self.cmy_ylw_tid)
        self.cmy_ylw_str.set(ylw)
        # self.cmy_ylw_tid = self.cmy_ylw_str.trace_add('write', self.colour_update_using_cmy)

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

        # update HSL numbers
        hue, lum, sat = colorsys.rgb_to_hls(red / 255, grn / 255, blu / 255)
        # self.hsl_hue_str.trace_remove('write', self.hsl_hue_tid)
        self.hsl_hue_str.set(round(hue * 359))
        # self.hsl_hue_tid = self.hsl_hue_str.trace_add('write', self.colour_update_using_hsl)
        # self.hsl_sat_str.trace_remove('write', self.hsl_sat_tid)
        self.hsl_sat_str.set(round(sat * 255))
        # self.hsl_sat_tid = self.hsl_sat_str.trace_add('write', self.colour_update_using_hsl)
        # self.hsl_lum_str.trace_remove('write', self.hsl_lum_tid)
        self.hsl_lum_str.set(round(lum * 255))
        # self.hsl_lum_tid = self.hsl_lum_str.trace_add('write', self.colour_update_using_hsl)

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

