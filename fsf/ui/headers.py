# ui/headers.py
# Header and rule functions

from fsf.ui.styles import C, G, R, W, D, HEAD, BORDER


def header(title=""):
    if title:
        print(f"{C} \u250c\u2500 {HEAD} {R}{W}formseal-fetch{R}   {D}\\{R}   {W}{title}{R}")
    else:
        print(f"{C} \u250c\u2500 {HEAD} {R}{W}formseal-fetch{R}")
    print(G + " " + BORDER + R)


def rule():
    print(G + " " + BORDER + R)