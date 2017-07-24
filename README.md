# nagaozen OS customizations and notes

# Initialization

I'm currently using a Manjaro/XFCE + gedit 2.30.4 (a bit modified) setup for my daily work.

## `/home/nagaozen/`

This package provides a `/home/nagaozen/` which probably doesn't exists in your system, so just copy the contents from inside this folder to your own user folder. Don't forget the dot folders (the invisible ones).

## et cetera

Just merge all folders, except `/home/` as mentioned before, to the file system `/`.

# Compile modified tools

`/home/nagaozen/` comes with a modified version of ctags, gedit e gedit plugins. You must install dependencies before trying to compile:

```sh
$ yaourt -S gconf gcolor2 pygtksourceview2 enchant desktop-file-utils iso-codes libsm python2
$ yaourt -S gnome-doc-utils intltool
```

then, compile ctags:

```sh
$ ./configure
$ make
$ sudo make install
```

compile gedit:

```sh
$ export PYTHON=/usr/bin/python2
$ ./configure --disable-scrollkeeper --enable-python
$ make LDFLAGS="$LDFLAGS -lgmodule-2.0 -lICE"
$ sudo make install
```

copy gedit-plugins:

```sh
$ sudo cp -r usr /
```

# Themes and Icons

```sh
$ sudo pacman -S adapta-maia-theme
$ yaourt papirus-icon-theme-git
$ yaourt papirus-libreoffice-theme
```

# Fonts

```sh
$ yaourt ttf-iosevka ttf-roboto
```

# Fixes

## Desktop Icons Positions

If somehow your desktop icons are losing their positions between reboots, you can set their properties as `immutable`:

```sh
$ sudo chattr +i ~/.config/xfce4/desktop/icons*
```

Then, if you want to change their position again you need to turn `immutable` off:

```sh
$ sudo chattr -i ~/.config/xfce4/desktop/icons*
```
