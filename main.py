#! /usr/bin/python3

from colour_visualiser import *

###############################################################################

def main():
    root = tk.Tk()
    Visualiser = colour_visualiser(root)
    root.mainloop()

###############################################################################

if __name__ == '__main__':
	main()
