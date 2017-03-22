# nagaozen fast OS initialization

I'm currently using a Manjaro/XFCE + pluma-gtk2 setup for my daily work.

## pluma-gtk2

```sh
$ yaourt -S pluma-gtk2
$ yaourt -S pluma-plugins
```

Installing `pluma-plugins` for pluma-gtk2 requires editing `PKGBUILD`:

```
--- pluma
+++ pluma-gtk2
```

## `/home/nagaozen/`

This package provides a `/home/nagaoze/` which probably doesn't exists in your system, so just copy the contents from inside this folder to your own user folder. Don't forget the dot folders (the invisible ones).

## et cetera

Just merge all folders, except `/home/` as mentioned before, to the file system `/`.

