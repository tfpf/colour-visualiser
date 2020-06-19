#! /usr/local/bin/python3.8

import colorsys
import time
import tkinter as tk

from collections import namedtuple

pad_x = 10
pad_y = 10

#######################################################################################################################

class colour_visualiser(tk.Frame):
    '''\
Display a GUI with entries in which a user may enter how they want to generate
a colour. Multiple colour spaces are supported. When the user updates the
numbers for one colour space, the numbers for the others are automatically
updated.

Attributes:
    supported_colour_spaces: dict (map which can be used to access the
        `tk.StringVar' instances associated with a colour space, the names of
        the colour components, their maximum values, and functions to convert
        to and from the RGB colour space; this is accomplished using
        `namedtuple')
    trace_disabled: bool (whether changes to any `tk.StringVar' are ignored)
    update_disabled: str (name of colour space whose `tk.StringVar' were
        written by the user, and should not be updated by the program)
    colour_lbl: tk.Label (its background colour will be set according to the
        components provided by the user)

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

        # trick to easily access any property of any colour space
        # `components': list of 3 `tk.StringVar's which contain the components
        # `names': names of the 3 components
        # `maximum': the maximum values the 3 components may take
        # `from_RGB': function to convert some colour space to RGB colour space
        # `to_RGB': function to convert RGB colour space to some colour space
        # example usage is as follows
        #     self.supported_colour_spaces['HSL'].maximum[1]
        #     self.supported_colour_spaces['RGB'].components[0]
        #     self.supported_colour_spaces['CMY'].from_RGB
        colour_options = namedtuple('colour_options', 'components names maximum from_RGB to_RGB ')
        self.supported_colour_spaces = {'RGB': colour_options([None,  None,    None],
                                                              ['Red', 'Green', 'Blue'],
                                                              [255,   255,     255],
                                                              None, None),
                                        'CMY': colour_options([None,   None,      None],
                                                              ['Cyan', 'Magenta', 'Yellow'],
                                                              [255,    255,       255],
                                                              self.RGB_to_CMY, self.CMY_to_RGB),
                                        'HSV': colour_options([None,  None,         None],
                                                              ['Hue', 'Saturation', 'Value'],
                                                              [359,   255,          255],
                                                              self.RGB_to_HSV, self.HSV_to_RGB),
                                        'HSL': colour_options([None,  None,         None],
                                                              ['Hue', 'Saturation', 'Luminance'],
                                                              [359,   255,          255],
                                                              self.RGB_to_HSL, self.HSL_to_RGB)}

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

        # create one frame for each colour space
        # arrange these frames in a two-column grid
        for i, colour_space in enumerate(self.supported_colour_spaces):
            current_frame = tk.Frame(self)

            name_lbl = tk.Label(current_frame, text = f'{colour_space} Colour Space')
            name_lbl.grid(row = 0, column = 0, columnspan = 3, padx = pad_x, pady = pad_y)

            for k in range(3):
                var = tk.StringVar(name = f'{colour_space}_{k}')
                lbl = tk.Label(current_frame, text = self.supported_colour_spaces[colour_space].names[k], width = 10)
                ent = tk.Entry(current_frame, textvariable = var)
                lim = tk.Label(current_frame, text = f' / {self.supported_colour_spaces[colour_space].maximum[k]}', width = 4)

                var.trace_add('write', self.colour_update_wrapper)
                lbl.grid(row = k + 1, column = 0, padx = pad_x, pady = pad_y)
                ent.grid(row = k + 1, column = 1, pady = pad_y)
                lim.grid(row = k + 1, column = 2, pady = pad_y)

                self.supported_colour_spaces[colour_space].components[k] = var

            # now, `current_frame' has to be placed in `self'
            # two rows of `self' are already occupied
            # this calculation is used to obtain the correct row and column
            current_frame.grid(row = i // 2 + 2, column = i % 2, padx = pad_x, pady = pad_y)

    ###########################################################################

    def __repr__(self):
        '''\
Representation of class object.
'''

        return 'colour_visualiser(object)'

    ###########################################################################

    def colour_update_wrapper(self, name, *args, **kwargs):
        '''\
This function is called automatically whenever any entry in the GUI is written.
Depending on which entry is written, appropriate actions are taken.

If the user writes an entry associated with the RGB colour space, this function
will update the entries associated with all other colour spaces. A deadlock or
infinite loop is prevented by adding a `self.trace_disabled' guard at the
beginning.

If the user writes an entry associated with a colour space other than RGB, this
function will update the entries associated with the RGB colour space, which,
in turn, will automatically cause the remaining entries to be updated. A
deadlock or infinite loop is prevented by checking `self.update_disabled'
before modifying any entry.

Args:
    name: str (name of the `tk.StringVar' which triggered this function call)

Returns:
    None
'''

        if self.trace_disabled:
            return

        # colour_space = name[: -2]
        # colour_components = [item.get() for item in self.contents_dict[colour_space]]

        # if colour_space == 'RGB':
        #     self.trace_disabled = True
        #     for i in self.contents_dict:
        #         if i == self.update_disabled or i == 'RGB': continue
        #         self.convert_from_RGB_to_other[i](colour_components)
        #     self.trace_disabled = False
        #     return
        # hex_code_of_colour = ''.join(f'{colour:02x}' for colour in (red, grn, blu))

        # self.update_disabled = colour_space
        # self.convert_from_other_to_RGB[colour_space](colour_components)
        # time.sleep(1)
        # self.update_disabled = 'none'

    ###########################################################################

    def RGB_to_CMY(self): pass
    def CMY_to_RGB(self): pass

    def RGB_to_HSV(self): pass
    def HSV_to_RGB(self): pass

    def RGB_to_HSL(self): pass
    def HSL_to_RGB(self): pass

