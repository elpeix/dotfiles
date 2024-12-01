# OpenSUSE Tumbleweed

## Codecs

```console
sudo zypper addrepo -cfp 99 'https://ftp.gwdg.de/pub/linux/misc/packman/suse/openSUSE_Tumbleweed/' packman
sudo zypper dist-upgrade --from packman --allow-vendor-change
sudo zypper install --from packman ffmpeg gstreamer-plugins-{good,bad,ugly,libav} libavcodec vlc-codecs
```

## Force dark mode

```console
gtk-query-settings | grep dark
gsettings set org.gnome.desktop.interface color-scheme prefer-dark
```

Create file to /etc/environment

```text
GTK_THEME=Adwaita-dark
```

Or other theme.

## Dev packages

```console
sudo zypper install --type pattern devel_basis
```

## Network manager applet

```console
sudo zypper install NetworkManager-applet
```
