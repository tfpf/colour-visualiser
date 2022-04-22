#! /usr/bin/python3

import colorsys
import time
import tkinter as tk

from collections import namedtuple

pad_x = 10
pad_y = 10

###############################################################################

class colour_visualiser(tk.Frame):
    '''\
Display a GUI with entries in which a user may enter how they want to generate
a colour. Multiple colour models are supported. When the user updates the
numbers for one colour model, the numbers for the others are automatically
updated. Also, a dedicated patch (actually a `tk.Label') is updated to have
that colour. This happens in real time (as the user types).

Attributes:
    supported_colour_models: dict (map which can be used to access the
        `tk.IntVar' instances associated with a colour model, the names of the
        colour components, their maximum values, and functions to convert to
        and from the RGB colour model; this is accomplished using `namedtuple')
    trace_disabled: bool (whether changes to any `tk.IntVar' are ignored)
    update_disabled: str (name of colour model whose `tk.IntVar' were written
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
    RGB_to_YUV: conversion function
    YUV_to_RGB: conversion function
    RGB_to_YIQ: conversion function
    YIQ_to_RGB: conversion function
'''

    ###########################################################################

    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.grid(padx = pad_x, pady = pad_y)
        parent.title('Colour Visualiser')
        parent.resizable(False, False)

        # trick to easily access any property of any colour model
        # `components': list of 3 `tk.IntVar's which contain the components
        # `names': names of the 3 components
        # `minimum': the minimum values the 3 components may take
        # `maximum': the maximum values the 3 components may take
        # `from_RGB': function to convert components from RGB to another model
        # `to_RGB': function to convert components to RGB from another model
        # example usage is as follows
        #     self.supported_colour_models['HSL'].maximum[1]
        #     self.supported_colour_models['RGB'].components[0]
        #     self.supported_colour_models['CMY'].from_RGB
        colour_options = namedtuple('colour_options', 'components names minimum maximum from_RGB to_RGB')
        self.supported_colour_models = {
            'RGB': colour_options([None,  None,    None],
                                  ['Red', 'Green', 'Blue'],
                                  [0,     0,       0],
                                  [255,   255,     255],
                                  None, None),
            'CMY': colour_options([None,   None,      None],
                                  ['Cyan', 'Magenta', 'Yellow'],
                                  [0,      0,         0],
                                  [255,    255,       255],
                                  self.RGB_to_CMY, self.CMY_to_RGB),
            'HSV': colour_options([None,  None,         None],
                                  ['Hue', 'Saturation', 'Value'],
                                  [0,     0,            0],
                                  [359,   100,          100],
                                  self.RGB_to_HSV, self.HSV_to_RGB),
            'HSL': colour_options([None,  None,         None],
                                  ['Hue', 'Saturation', 'Luminance'],
                                  [0,     0,            0],
                                  [359,   100,          100],
                                  self.RGB_to_HSL, self.HSL_to_RGB),
            'YUV': colour_options([None,        None,   None],
                                  ['Luminance', 'Blue', 'Red'],
                                  [0,           -127,   -127],
                                  [255,         127,    127],
                                  self.RGB_to_YUV, self.YUV_to_RGB),
            'YIQ': colour_options([None,        None,       None],
                                  ['Luminance', 'In-Phase', 'Quadrature'],
                                  [0,           -127,       -127],
                                  [255,         127,        127],
                                  self.RGB_to_YIQ, self.YIQ_to_RGB),
        }

        # the plan is to use a chain of traces to update the colour information
        # hence, use these to determine whether to continue or not
        # otherwise, there will be an infinite loop of traces
        self.trace_disabled = False # switch to disable all traces
        self.update_disabled = None # disable update for a colour model

        # title
        main_lbl = tk.Label(self, text = 'Colour Visualiser')
        main_lbl.grid(row = 0, column = 0, columnspan = 2, padx = pad_x, pady = pad_y)

        # the background colour of this label will be the input colour
        self.colour_lbl = tk.Label(self, text = (' ' * 140 + '\n') * 2, bg = 'black', highlightbackground = 'white', highlightcolor = 'white', highlightthickness = 2)
        self.colour_lbl.grid(row = 1, column = 0, columnspan = 2, padx = pad_x, pady = (pad_y, 2 * pad_y))

        # create one frame for each colour model
        # arrange these frames in a two-column grid
        for i, colour_model in enumerate(self.supported_colour_models):
            current_frame = tk.Frame(self)

            name_lbl = tk.Label(current_frame, text = f'{colour_model} Colour Model')
            name_lbl.grid(row = 0, column = 0, columnspan = 6, padx = pad_x, pady = pad_y)

            for k in range(3):
                var = tk.IntVar(name = f'{colour_model}_{k}')
                lbl = tk.Label(current_frame, text = self.supported_colour_models[colour_model].names[k], width = 10)
                l_l = tk.Label(current_frame, text = f'{self.supported_colour_models[colour_model].minimum[k]}', width = 4, anchor = 'e')
                le1 = tk.Label(current_frame, text = '≤')
                ent = tk.Entry(current_frame, textvariable = var, justify = 'right', width = 6)
                le2 = tk.Label(current_frame, text = '≤')
                u_l = tk.Label(current_frame, text = f'{self.supported_colour_models[colour_model].maximum[k]}', width = 4, anchor = 'w')

                var.trace_add('write', self.colour_update_wrapper)
                lbl.grid(row = k + 1, column = 0, padx = pad_x, pady = pad_y)
                l_l.grid(row = k + 1, column = 1, pady = pad_y)
                le1.grid(row = k + 1, column = 2, pady = pad_y)
                ent.grid(row = k + 1, column = 3, pady = pad_y)
                le2.grid(row = k + 1, column = 4, pady = pad_y)
                u_l.grid(row = k + 1, column = 5, pady = pad_y)

                self.supported_colour_models[colour_model].components[k] = var

            # now, `current_frame' has to be placed in `self'
            # two rows of `self' are already occupied
            # this calculation is used to obtain the correct row and column
            current_frame.grid(row = i // 2 + 2, column = i % 2, padx = pad_x, pady = pad_y)

        # initially, all the entries will contain 0
        # this makes no sense
        # representation of a colour cannot be the same in all colour models
        # hence, at the beginning, force a colour conversion
        for item in self.supported_colour_models['RGB'].components:
            item.set(0)

    ###########################################################################

    def __repr__(self):
        return 'colour_visualiser(object)'

    ###########################################################################

    def colour_update_wrapper(self, name, *args, **kwargs):
        '''\
This function is called automatically whenever any entry in the GUI is written.
Depending on which entry is written, appropriate actions are taken.

If the user writes an entry associated with the RGB colour model, this function
will update the entries associated with all other colour models. A deadlock or
infinite loop is prevented by adding a `self.trace_disabled' guard at the
beginning.

If the user writes an entry associated with a colour model other than RGB, this
function will update the entries associated with the RGB colour model, which,
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

        current_colour_model = name[: -2]

        # when any entry is written, check validity of all 3 components
        # calling `get' on an empty `tk.IntVar' can raise an exception
        # hence, handle it as a case of invalid input by doing nothing
        try:
            for i in range(3):
                current_component = self.supported_colour_models[current_colour_model].components[i].get()
                current_minimum = self.supported_colour_models[current_colour_model].minimum[i]
                current_maximum = self.supported_colour_models[current_colour_model].maximum[i]
                if not current_minimum <= current_component <= current_maximum:
                    self.colour_lbl.config(highlightbackground = 'red', highlightcolor='red', highlightthickness = 2, bg = 'white')
                    return
        except tk.TclError:
            return

        # check whether the entry written belongs to the RGB colour model
        # if yes, calculate and write the components of all other colour models
        # but disable the trace first
        # so that the latter action does not trigger a trace
        if current_colour_model == 'RGB':
            self.trace_disabled = True
            current_components = [item.get() for item in self.supported_colour_models[current_colour_model].components]

            # using the above, calculate the components for other colour models
            for colour_model in self.supported_colour_models:
                if colour_model == 'RGB' or colour_model == self.update_disabled:
                    continue

                changed_components = self.supported_colour_models[colour_model].from_RGB(current_components)
                for item, x in zip(self.supported_colour_models[colour_model].components, changed_components):
                    item.set(x)

            # set the background colour of the designated label
            hex_colour_code = ''.join(f'{i:02x}' for i in current_components)
            self.colour_lbl.config(highlightbackground = 'white', highlightcolor = 'white', highlightthickness = 2, bg = f'#{hex_colour_code}')

            self.trace_disabled = False
            return

        # the entry which was written does not belong to the RGB colour model
        # calculate and write the components of the RGB colour model
        self.update_disabled = current_colour_model
        current_components = [item.get() for item in self.supported_colour_models[current_colour_model].components]
        changed_components = self.supported_colour_models[current_colour_model].to_RGB(current_components)
        for item, x in zip(self.supported_colour_models['RGB'].components, changed_components):
            item.set(x)
        self.update_disabled = None

    ###########################################################################

    def RGB_to_CMY(self, components):
        return [x - y for x, y in zip(self.supported_colour_models['RGB'].maximum, components)]

    ###########################################################################

    def CMY_to_RGB(self, components):
        return [x - y for x, y in zip(self.supported_colour_models['CMY'].maximum, components)]

    ###########################################################################

    def RGB_to_HSV(self, components):
        normalised = ((x - l) / (u - l) for x, l, u in zip(components, self.supported_colour_models['RGB'].minimum, self.supported_colour_models['RGB'].maximum))
        changed = colorsys.rgb_to_hsv(*normalised)
        denormalised = [l + x * (u - l) for x, l, u in zip(changed, self.supported_colour_models['HSV'].minimum, self.supported_colour_models['HSV'].maximum)]
        return [round(item) for item in denormalised]

    ###########################################################################

    def HSV_to_RGB(self, components):
        normalised = ((x - l) / (u - l) for x, l, u in zip(components, self.supported_colour_models['HSV'].minimum, self.supported_colour_models['HSV'].maximum))
        changed = colorsys.hsv_to_rgb(*normalised)
        denormalised = [l + x * (u - l) for x, l, u in zip(changed, self.supported_colour_models['RGB'].minimum, self.supported_colour_models['RGB'].maximum)]
        return [round(item) for item in denormalised]

    ###########################################################################

    def RGB_to_HSL(self, components):

        # this is not as straightforward as the previous ones
        # the library function available is `colorsys.rgb_to_hls'
        # I am representing the components as HSL, not HLS
        # so, the last two components have to be manually interchanged
        normalised = ((x - l) / (u - l) for x, l, u in zip(components, self.supported_colour_models['RGB'].minimum, self.supported_colour_models['RGB'].maximum))
        changed = colorsys.rgb_to_hls(*normalised)
        changed = (changed[0], changed[2], changed[1])
        denormalised = [l + x * (u - l) for x, l, u in zip(changed, self.supported_colour_models['HSL'].minimum, self.supported_colour_models['HSL'].maximum)]
        return [round(item) for item in denormalised]

    ###########################################################################

    def HSL_to_RGB(self, components):

        # same comments as above apply
        normalised = tuple((x - l) / (u - l) for x, l, u in zip(components, self.supported_colour_models['HSL'].minimum, self.supported_colour_models['HSL'].maximum))
        normalised = (normalised[0], normalised[2], normalised[1])
        changed = colorsys.hls_to_rgb(*normalised)
        denormalised = [l + x * (u - l) for x, l, u in zip(changed, self.supported_colour_models['RGB'].minimum, self.supported_colour_models['RGB'].maximum)]
        return [round(item) for item in denormalised]

    ###########################################################################

    def RGB_to_YUV(self, components):

        # like YIQ, YUV components can be negative
        #      0.000 ≤ Y ≤ 1.000
        #     -0.436 ≤ U ≤ 0.436
        #     -0.615 ≤ V ≤ 0.615
        # no library function available for this, so do calculation manually
        U_max = 0.436
        V_max = 0.615
        normalised = ((x - l) / (u - l) for x, l, u in zip(components, self.supported_colour_models['RGB'].minimum, self.supported_colour_models['RGB'].maximum))
        R, G, B = normalised
        Y = ( 0.29900 * R + 0.58700 * G + 0.11400 * B) * self.supported_colour_models['YUV'].maximum[0]
        U = (-0.14713 * R - 0.28886 * G + 0.43600 * B) / U_max * self.supported_colour_models['YUV'].maximum[1]
        V = ( 0.61500 * R - 0.51499 * G - 0.10001 * B) / V_max * self.supported_colour_models['YUV'].maximum[2]
        return [round(Y), round(U), round(V)]

    ###########################################################################

    def YUV_to_RGB(self, components):

        # reversing the above operation
        U_max = 0.436
        V_max = 0.615
        normalised = tuple(x / u for x, u in zip(components, self.supported_colour_models['YUV'].maximum))
        normalised = (normalised[0], normalised[1] * U_max, normalised[2] * V_max)
        Y, U, V = normalised
        R = (Y               + 1.13983 * V) * (self.supported_colour_models['RGB'].maximum[0] - self.supported_colour_models['RGB'].minimum[0]) + self.supported_colour_models['RGB'].minimum[0]
        G = (Y - 0.39465 * U - 0.58060 * V) * (self.supported_colour_models['RGB'].maximum[1] - self.supported_colour_models['RGB'].minimum[1]) + self.supported_colour_models['RGB'].minimum[1]
        B = (Y + 2.03211 * U              ) * (self.supported_colour_models['RGB'].maximum[2] - self.supported_colour_models['RGB'].minimum[2]) + self.supported_colour_models['RGB'].minimum[2]
        return [round(R), round(G), round(B)]

    ###########################################################################

    def RGB_to_YIQ(self, components):

        # this colour model is somewhat weird: the components can be negative
        #      0.0000 ≤ Y ≤ 1.0000
        #     -0.5990 ≤ I ≤ 0.5990
        #     -0.5251 ≤ Q ≤ 0.5251
        # after using library function, modify them to be in range: -1 to 1
        # magnitude of maximum and minimum values of `I' and `Q' must be same
        # otherwise, this conversion will not work
        I_max = colorsys.rgb_to_yiq(1, 0, 0)[1]
        Q_max = colorsys.rgb_to_yiq(1, 0, 1)[2]
        normalised = ((x - l) / (u - l) for x, l, u in zip(components, self.supported_colour_models['RGB'].minimum, self.supported_colour_models['RGB'].maximum))
        changed = colorsys.rgb_to_yiq(*normalised)
        changed = (changed[0], changed[1] / I_max, changed[2] / Q_max)
        denormalised = [x * u for x, u in zip(changed, self.supported_colour_models['YIQ'].maximum)]
        return [round(item) for item in denormalised]

    ###########################################################################

    def YIQ_to_RGB(self, components):

        # same comments as above apply
        I_max = colorsys.rgb_to_yiq(1, 0, 0)[1]
        Q_max = colorsys.rgb_to_yiq(1, 0, 1)[2]
        normalised = tuple(x / u for x, u in zip(components, self.supported_colour_models['YIQ'].maximum))
        normalised = (normalised[0], normalised[1] * I_max, normalised[2] * Q_max)
        changed = colorsys.yiq_to_rgb(*normalised)
        denormalised = [l + x * (u - l) for x, l, u in zip(changed, self.supported_colour_models['RGB'].minimum, self.supported_colour_models['RGB'].maximum)]
        return [round(item) for item in denormalised]
