:author: beberlei <kontakt@beberlei.de>
:date: 2008-11-12

Updating from KDE3.5 to KDE4 with Mac-Style Menubars
====================================================

It seems KDE4 has no Mac-Style menubars and when you upgrade from 3.5 to
4.1 within the same config folder (say you use the kubuntu distribution
upgrade installer like I did) you end up with no menubars at all.
To solve this little issue find a variable "macStyle = true" in the
/home/username/.kde/share/config/kdeglobals file and switch it to
macStyle = false and you have your menubars back.
