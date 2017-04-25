Ez-Do Tool
==========

Easily manage esoteric console commands without having to rely on arcane
scripts!

Usage
-----

Put an ezdofile in the directory you want to work within

```
 This is plain comment text
 put it on lines that start with a space

: command-name
# The above is a command-name. It's line starts with a colon (:)
# This text is a command description. It's liens start with octothropes (#)
> echo "This is a command! It's line starts with a '>' character"
```

Then type `ezdo` from within that directory and you will be presented with a
menu for your commands! Type `ezdo command-name` as a shortcut to quickly
execute a specific command!

Installation
------------

Clone the repo, and use pip to install it!

```
git clone https://github.com/zchfvy/ezdotool.git
cd ezdotool
pip install .
```

To Do List
----------
- [ ] Add an appropriate license
- [ ] Add to pypi
- [ ] Add support for 'user' ezdofiles in user home dir
