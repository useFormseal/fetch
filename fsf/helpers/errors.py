# helpers/errors — Error handler functions

from fsf.ui import neutral, C, WHITE, R


def unknown_command():
    neutral(f"{WHITE}This command doesn't exist. Run {C}fsf --help{R}{WHITE} for available commands.{R}")


def handle_interrupt():
    from fsf.ui import br, info
    br()
    info("Interrupted.")
    br()


def handle_exception(e):
    from fsf.ui import fail
    fail(str(e))
