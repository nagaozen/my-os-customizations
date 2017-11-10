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

$ gconftool-2 --set "/apps/gnome-terminal/profiles/Default/use_theme_background" --type bool false
$ gconftool-2 --set "/apps/gnome-terminal/profiles/Default/use_theme_colors" --type bool false
$ gconftool-2 --set "/apps/gnome-terminal/profiles/Default/palette" --type string "#070736364242:#D3D301010202:#858599990000:#B5B589890000:#26268B8BD2D2:#D3D336368282:#2A2AA1A19898:#EEEEE8E8D5D5:#00002B2B3636:#CBCB4B4B1616:#58586E6E7575:#65657B7B8383:#838394949696:#6C6C7171C4C4:#9393A1A1A1A1:#FDFDF6F6E3E3"
$ gconftool-2 --set "/apps/gnome-terminal/profiles/Default/background_color" --type string "#00002B2B3636"
$ gconftool-2 --set "/apps/gnome-terminal/profiles/Default/foreground_color" --type string "#65657B7B8383"
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
