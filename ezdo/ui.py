import urwid

pallete = [
    ('command', 'light red', ''),
    ('command_s', 'light red', 'dark blue'),
    ('descr', 'light gray', ''),
    ('descr_s', 'light gray', 'dark blue'),
    ('name', 'light green', ''),
    ('name_s', 'light green', 'dark blue'),
    ('button', '', ''),
    ('button_s', '', 'dark blue'),
    ('comment', 'dark gray', ''),
    ('selected', '', 'dark blue')
    ]

select_map = {
    'command': 'command_s',
    'descr': 'descr_s',
    'name': 'name_s',
    'button': 'button_s',
    }

cmd = None  # Holder for return command value


class SectionButton(urwid.Button):
    def __init__(self, caption, callback, callback_arg):
        super(SectionButton, self).__init__("")
        urwid.connect_signal(self, 'click', callback, callback_arg)

        txt = urwid.SelectableIcon(caption, float('inf'))
        txt = urwid.AttrMap(txt, 'button', None)
        txt = urwid.AttrMap(txt, None, select_map)
        self._w = txt


def menu(sections):
    body = []
    for sect in sections:
        if sect.commands:

            def button_cb(button, command):
                global cmd
                cmd = command
                raise urwid.ExitMainLoop()

            button = SectionButton(sect.markuptext, button_cb, sect.commands)
            body.append(button)
        else:
            label = urwid.Text(sect.markuptext)
            body.append(label)

    return urwid.ListBox(urwid.SimpleFocusListWalker(body))


def run(script):
    urwid.MainLoop(menu(script), pallete).run()
    return cmd
