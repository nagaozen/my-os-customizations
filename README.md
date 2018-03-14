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

# System Monitor

```sh
$ yaourt xfce4-multiload-ng-plugin-gtk3
```

# Themes and Icons

```sh
$ sudo pacman -S adapta-maia-theme
$ yaourt papirus-icon-theme-git
$ yaourt papirus-libreoffice-theme

$ gconftool-2 --set "/apps/gnome-terminal/profiles/Default/use_theme_background" --type bool false
$ gconftool-2 --set "/apps/gnome-terminal/profiles/Default/use_theme_colors" --type bool false
$ gconftool-2 --set "/apps/gnome-terminal/profiles/Default/palette" --type string "#000000:#E06C75:#98c379:#d19a66:#61aeee:#c678dd:#56b6c2:#abb2bf:#5c6370:#e06c75:#98c379:#d19a66:#62afee:#c678dd:#56b6c2:#ffffff"
$ gconftool-2 --set "/apps/gnome-terminal/profiles/Default/background_color" --type string "#282c34"
$ gconftool-2 --set "/apps/gnome-terminal/profiles/Default/foreground_color" --type string "#abb2bf"
$ gconftool-2 --set "/apps/gnome-terminal/profiles/Default/font" --type string "Anka/Coder Narrow 10"
```

# Fonts

```sh
$ yaourt ttf-iosevka ttf-roboto
```

# Fixes

## Desktop Icons Positions

If somehow your desktop icons are losing their positions between reboots, you can set their properties as `immutable`:

### quick method

```sh
$ ./freeze_desktop.sh	
```

### manual method

```sh
$ chattr +i ~/.config/xfce4/desktop/icons*
```

Then, if you want to change their position again you need to turn `immutable` off:

### quick method

```sh
$ ./unfreeze_desktop.sh	
```

### manual method

```sh
$ chattr -i ~/.config/xfce4/desktop/icons*
```
