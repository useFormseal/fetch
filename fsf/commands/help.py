# commands/help — Help command (show commands and aliases)

from fsf.ui import br, header, rule
from fsf.ui.styles import C, G, R, W, GRAY


def _get_help_groups():
    return {
        "Connect": [
            ("fsf connect <name>", "connect storage provider"),
            ("fsf disconnect", "clear configuration"),
            ("fsf disconnect --wipe", "clear everything"),
        ],
        "Fetch": [
            ("fsf fetch", "download ciphertexts"),
            ("fsf fetch --output <file>", "custom output path"),
        ],
        "Info": [
            ("fsf status", "show configuration"),
            ("fsf --providers", "list available providers"),
            ("fsf --version", "show version"),
            ("fsf --aliases", "list shorthand flags"),
        ],
        "Docs": [
            ("https://github.com/useFormseal/fetch/blob/main/docs", None),
        ],
    }


def _show_help():
    groups = _get_help_groups()
    br()
    header("help")
    br()

    for group, cmds in groups.items():
        print(f"  {GRAY}>> {group}{R}")
        rule()
        for cmd, desc in cmds:
            if desc:
                print(f"  {W}{cmd:<27}{R} {G}{desc}{R}")
            else:
                print(f"  {C}{cmd}{R}")
        br()


def run():
    _show_help()


def run_aliases():
    br()
    header("shorthand aliases")
    br()

    print(f" {W}Short{R}  {G}Canonical{R}")
    rule()
    print(f" {W}-s{R}     {G}status{R}")
    print(f" {W}-c{R}     {G}connect{R}")
    print(f" {W}-p{R}     {G}--providers{R}")
    br()
