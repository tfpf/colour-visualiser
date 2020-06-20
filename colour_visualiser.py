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
updated. Also, a dedicated path (actually a `tk.Label') is updated to have that
colour. This happens in real time (as the user types).

Attributes:
    supported_colour_spaces: dict (map which can be used to access the
        `tk.IntVar' instances associated with a colour space, the names of the
        colour components, their maximum values, and functions to convert to
        and from the RGB colour space; this is accomplished using `namedtuple')
    trace_disabled: bool (whether changes to any `tk.IntVar' are ignored)
    update_disabled: str (name of colour space whose `tk.IntVar' were written
        by the user, and should not be updated by the program)
    colour_lbl: tk.Label (its background colour will be set according to the
        components provided by the user)

Methods:
    __init__
    __repr__
    colour_update_wrapper: wrapper to call the following conversion functions
    RGB_to_CMY: conversion function
    CMY_to_RGB: conversion function
    RGB_to_HSV: conversion function
    HSV_to_RGB: conversion function
    RGB_to_HSL: conversion function
    HSL_to_RGB: conversion function
'''

    ###########################################################################


    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.grid(padx = pad_x, pady = pad_y)
        parent.title('Colour Visualiser')
        parent.resizable(False, False)

        # trick to easily access any property of any colour space
        # `components': list of 3 `tk.IntVar's which contain the components
        # `names': names of the 3 components
        # `maximum': the maximum values the 3 components may take
        # `from_RGB': function to convert some colour space to RGB colour space
        # `to_RGB': function to convert RGB colour space to some colour space
        # example usage is as follows
        #     self.supported_colour_spaces['HSL'].maximum[1]
        #     self.supported_colour_spaces['RGB'].components[0]
        #     self.supported_colour_spaces['CMY'].from_RGB
        colour_options = namedtuple('colour_options', 'components names maximum from_RGB to_RGB')
        self.supported_colour_spaces = {
            'RGB': colour_options([None,  None,    None],
                                  ['Red', 'Green', 'Blue'],
                                  [255,   255,     255],
                                  None, None),
            'CMY': colour_options([None,   None,      None],
                                  ['Cyan', 'Magenta', 'Yellow'],
                                  [255,    255,       255],
                                  self.RGB_to_CMY, self.CMY_to_RGB),
            'HSV': colour_options([None,  None,         None],
                                  ['Hue', 'Saturation', 'Value'],
                                  [359,   100,          100],
                                  self.RGB_to_HSV, self.HSV_to_RGB),
            'HSL': colour_options([None,  None,         None],
                                  ['Hue', 'Saturation', 'Luminance'],
                                  [359,   100,          100],
                                  self.RGB_to_HSL, self.HSL_to_RGB),
        }

        # the plan is to use a chain of traces to update the colour information
        # hence, use these to determine whether to continue or not
        # otherwise, there will be an infinite loop of traces
        self.trace_disabled = False # switch to disable all traces
        self.update_disabled = None # disable updating a colour space

        # title
        main_lbl = tk.Label(self, text = 'Colour Visualiser')
        main_lbl.grid(row = 0, column = 0, columnspan = 2, padx = pad_x, pady = pad_y)

        # the background colour of this label will be the input colour
        self.colour_lbl = tk.Label(self, text = (' ' * 140 + '\n') * 2, bg = 'black')
        self.colour_lbl.grid(row = 1, column = 0, columnspan = 2, padx = pad_x, pady = (pad_y, 2 * pad_y))

        # create one frame for each colour space
        # arrange these frames in a two-column grid
        for i, colour_space in enumerate(self.supported_colour_spaces):
            current_frame = tk.Frame(self)

            name_lbl = tk.Label(current_frame, text = f'{colour_space} Colour Space')
            name_lbl.grid(row = 0, column = 0, columnspan = 3, padx = pad_x, pady = pad_y)

            for k in range(3):
                var = tk.IntVar(name = f'{colour_space}_{k}')
                lbl = tk.Label(current_frame, text = self.supported_colour_spaces[colour_space].names[k], width = 10)
                ent = tk.Entry(current_frame, textvariable = var, justify = 'right', width = 6)
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

        # initially, all the entries will contain 0
        # this makes no sense
        # representation of a colour cannot be the same in all colour spaces
        # hence, at the beginning, force a colour conversion
        for item in self.supported_colour_spaces['RGB'].components:
            item.set(0)

    ###########################################################################

    def __repr__(self):
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
    name: str (name of the `tk.IntVar' which triggered this function call)

Returns:
    None
'''

        if self.trace_disabled:
            return

        current_colour_space = name[: -2]

        # when any entry is written, check validity of all 3 components
        # calling `get' on an empty `tk.IntVar' can raise an exception
        # hence, handle it as a case of invalid input by doing nothing
        try:
            for i in range(3):
                current_component = self.supported_colour_spaces[current_colour_space].components[i].get()
                current_maximum = self.supported_colour_spaces[current_colour_space].maximum[i]
                if not 0 <= current_component <= current_maximum:
                    return
        except tk.TclError:
            return

        # check whether the entry written belongs to the RGB colour space
        # if yes, calculate and write the components of all other colour spaces
        # but disable the trace first
        # so that the latter action does not trigger a trace
        if current_colour_space == 'RGB':
            self.trace_disabled = True
            current_components = [item.get() for item in self.supported_colour_spaces[current_colour_space].components]

            # use the above, calculate the components for other colour spaces
            for colour_space in self.supported_colour_spaces:
                if colour_space == 'RGB' or colour_space == self.update_disabled:
                    continue

                changed_components = self.supported_colour_spaces[colour_space].from_RGB(current_components)
                for item, x in zip(self.supported_colour_spaces[colour_space].components, changed_components):
                    item.set(x)

            # set the background colour of the designated label
            hex_colour_code = ''.join(f'{i:02x}' for i in current_components)
            self.colour_lbl.config(bg = f'#{hex_colour_code}')

            self.trace_disabled = False
            return

        # the entry which was written does not belong to the RGB colour space
        # calculate and write the components of the RGB colour space
        self.update_disabled = current_colour_space
        current_components = [item.get() for item in self.supported_colour_spaces[current_colour_space].components]
        changed_components = self.supported_colour_spaces[current_colour_space].to_RGB(current_components)
        for item, x in zip(self.supported_colour_spaces['RGB'].components, changed_components):
            item.set(x)
        self.update_disabled = None

        # hex_code_of_colour = ''.join(f'{colour:02x}' for colour in (red, grn, blu))

    ###########################################################################

    def RGB_to_CMY(self, components):
        return [x - y for x, y in zip(self.supported_colour_spaces['RGB'].maximum, components)]

    ###########################################################################

    def CMY_to_RGB(self, components):
        return [x - y for x, y in zip(self.supported_colour_spaces['CMY'].maximum, components)]

    ###########################################################################

    def RGB_to_HSV(self, components):
        normalised = (x / y for x, y in zip(components, self.supported_colour_spaces['RGB'].maximum))
        changed = colorsys.rgb_to_hsv(*normalised)
        denormalised = [x * y for x, y in zip(changed, self.supported_colour_spaces['HSV'].maximum)]
        return [round(item) for item in denormalised]

    ###########################################################################

    def HSV_to_RGB(self, components):
        normalised = (x / y for x, y in zip(components, self.supported_colour_spaces['HSV'].maximum))
        changed = colorsys.hsv_to_rgb(*normalised)
        denormalised = [x * y for x, y in zip(changed, self.supported_colour_spaces['RGB'].maximum)]
        return [round(item) for item in denormalised]

    ###########################################################################

    def RGB_to_HSL(self, components):

        # this is not as straightforward as the previous ones
        # the library function available is `colorsys.rgb_to_hls'
        # I am representing the components as HSL, not HLS
        # so, the last two components have to be manually interchanged
        normalised = (x / y for x, y in zip(components, self.supported_colour_spaces['RGB'].maximum))
        changed = colorsys.rgb_to_hls(*normalised)
        changed = (changed[0], changed[2], changed[1])
        denormalised = [x * y for x, y in zip(changed, self.supported_colour_spaces['HSL'].maximum)]
        return [round(item) for item in denormalised]

    ###########################################################################

    def HSL_to_RGB(self, components):

        # same comments as above apply
        normalised = tuple(x / y for x, y in zip(components, self.supported_colour_spaces['HSL'].maximum))
        normalised = (normalised[0], normalised[2], normalised[1])
        changed = colorsys.hls_to_rgb(*normalised)
        denormalised = [x * y for x, y in zip(changed, self.supported_colour_spaces['RGB'].maximum)]
        return [round(item) for item in denormalised]

