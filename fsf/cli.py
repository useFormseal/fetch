# cli — Entry point and command registry

import sys

from fsf.helpers.aliases import resolve
from fsf.helpers.errors import unknown_command, handle_interrupt, handle_exception

from fsf.commands import about as cmd_about
from fsf.commands import version as cmd_version
from fsf.commands import help as cmd_help
from fsf.commands.config import run_status, run_disconnect
from fsf.commands.connect import run as run_connect
from fsf.commands.fetch import run as run_fetch
from fsf.commands.providers import run as run_providers


COMMANDS = {
    "connect": ("Connect to a provider", lambda a: run_connect(a)),
    "fetch": ("Fetch ciphertexts", lambda a: run_fetch(a)),
    "status": ("Show connection status", lambda a: run_status()),
    "disconnect": ("Clear all credentials", lambda a: run_disconnect(a)),
}


def main():
    if len(sys.argv) < 2:
        cmd_about.run()
        return

    args = resolve(sys.argv[1:])
    cmd = args[0].lower()
    cmd_args = args[1:]

    if cmd == "--help":
        cmd_help.run()
        return

    if cmd == "version" or cmd == "--version":
        cmd_version.run()
        return

    if cmd == "--aliases":
        cmd_help.run_aliases()
        return

    if cmd == "--providers":
        run_providers([])
        return

    if cmd not in COMMANDS:
        unknown_command()

    _, handler = COMMANDS[cmd]

    try:
        handler(cmd_args)
    except KeyboardInterrupt:
        handle_interrupt()
        sys.exit(130)
    except Exception as e:
        handle_exception(e)


if __name__ == "__main__":
    main()
