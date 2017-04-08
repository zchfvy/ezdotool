import urwid
# import os
import subprocess
import signal
import sys

pallete = [
    ('command', 'light red', 'black'),
    ('descr', 'light gray', 'black'),
    ('name', 'light green', 'black'),
    ('comment', 'dark gray', ''),
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
        if line[0] == ':':
            curr_sect.name = line[1:].strip()
            curr_sect.markuptext.append(('name', line + '\n'))
        else:
            curr_sect.markuptext.append(('comment', line + '\n'))

    return sections


def menu(sections):
    body = []
    for sect in sections:
        if sect.commands:
            button = urwid.Button(sect.markuptext)
            urwid.connect_signal(button, 'click', execute, sect)
            body.append(button)
        else:
            label = urwid.Text(sect.markuptext)
            body.append(label)

    return urwid.ListBox(urwid.SimpleFocusListWalker(body))


proc = None
cmd = None


def signal_handler(signal, frame):
    if proc is None:
        sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)


def execute(button, section):
    global cmd
    cmd = section.name
    raise urwid.ExitMainLoop()


def exec_cmd(command):
    global proc
    for cmd in command:
        # args = [os.environ["SHELL"], '-i', '-c', cmd]
        proc = subprocess.Popen(cmd, shell=True)
        proc.wait()

with open('ezdofile') as f:
    lines = f.readlines()
    script = parse_script(lines)

if len(sys.argv) > 1:
    cmd = sys.argv[1]
else:
    urwid.MainLoop(menu(script), pallete).run()
section = next((s for s in script if s.name == cmd), None)
if section:
    exec_cmd(section.commands)
else:
    print("Unknown command '{}'".format(cmd))
