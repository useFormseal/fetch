# ui/bodies.py
# Body output functions

from fsf.ui.styles import D, G, O, R, W, Y, ERROR


def br():
    print()


def fail(msg):
    br()
    print(f"  {ERROR}Error:{R} {msg}")
    raise SystemExit(1)


def neutral(msg):
    br()
    print(f" \U0001f610 {msg}")
    raise SystemExit(1)


def info(msg):
    print(f"  {O}{msg}{R}")


def ok(msg):
    print(f"  {G}✨{R} {msg}")


def warn(msg):
    print(f"{Y}⚠️ {R}{msg}")