import urwid
# import os
import subprocess
import signal
import sys

pallete = [
    ('command', 'light red', 'black'),
    ('descr', 'light gray', 'black'),
    ]


class Section(object):
    def __init__(self):
        self.fulltext = ""
        self.commands = []
        self.markuptext = []


def parse_script(lines):
    """

    Returns
    -------
    list of Section
    """
    sections = []
    curr_sect = None
    lines.append("")  # to load after EOF
    for line in lines:
        line = line.strip()
        if not line and curr_sect:
            sections.append(curr_sect)
            curr_sect = None
        elif not curr_sect:
            curr_sect = Section()

        if not line:
            continue

        if curr_sect.fulltext:
            curr_sect.fulltext += '\n'
        curr_sect.fulltext += line

        if line[0] == '>':
            curr_sect.commands.append(line[1:].strip())
            curr_sect.markuptext.append(('command', line + '\n'))
        if line[0] == '#':
            curr_sect.markuptext.append(('descr', line + '\n'))

    return sections


def menu(sections):
    body = []
    for sect in sections:
        button = urwid.Button(sect.markuptext)
        urwid.connect_signal(button, 'click', execute, sect.commands)
        body.append(button)
    return urwid.ListBox(urwid.SimpleFocusListWalker(body))


proc = None


def signal_handler(signal, frame):
    if proc is None:
        sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)


def execute(button, command):
    global proc
    for cmd in command:
        # args = [os.environ["SHELL"], '-i', '-c', cmd]
        proc = subprocess.Popen(cmd, shell=True)
        proc.wait()
    raise urwid.ExitMainLoop()


with open('ezdofile') as f:
    lines = f.readlines()
    script = parse_script(lines)

urwid.MainLoop(menu(script), pallete).run()
