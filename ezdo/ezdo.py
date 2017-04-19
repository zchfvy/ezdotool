import subprocess
import signal
import sys

import ui


# -- Core --

class Section(object):
    def __init__(self):
        self.fulltext = ""
        self.commands = []
        self.markuptext = []
        self.name = None

    def add_text(self, style, text):
        if self.fulltext:
            self.fulltext += '\n'

        self.fulltext += text

        if self.markuptext:
            # HACK : curse those immutable tuples!
            last = self.markuptext[-1]
            self.markuptext[-1] = (last[0], last[1] + '\n')

        self.markuptext.append((style, text))


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
            new_sect = Section()
            new_sect.add_text('', '')
            sections.append(new_sect)
            continue

        if line[0] == '>':
            curr_sect.commands.append(line[1:].strip())
            curr_sect.add_text('command', line)
        elif line[0] == '#':
            curr_sect.add_text('descr', line)
        elif line[0] == ':':
            curr_sect.name = line[1:].strip()
            curr_sect.add_text('name', line)
        else:
            curr_sect.add_text('comment', line)

    return sections


# -- Proces Management --


proc = None


def signal_handler(signal, frame):
    if proc is None:
        sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)


def exec_cmd(command):
    global proc
    for cmd in command:
        # args = [os.environ["SHELL"], '-i', '-c', cmd]
        print('>>> \033[1m' + cmd + '\033[0m')
        proc = subprocess.Popen(cmd, shell=True)
        proc.wait()

# -- Main --


def main():
    global cmd
    with open('ezdofile') as f:
        lines = f.readlines()
        script = parse_script(lines)

    if len(sys.argv) > 1:
        cmd_name = sys.argv[1]
        section = next((s for s in script if s.name == cmd_name), None)
        if section:
            cmd = section.commands
        else:
            print("Unknown command '{}'".format(cmd))
    else:
        cmd = ui.run(script)
    exec_cmd(cmd)

if __name__ == '__main__':
    main()
