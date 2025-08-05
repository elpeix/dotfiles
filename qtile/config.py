# -*- coding: utf-8 -*-
import os
import random
import socket
import subprocess

from libqtile import bar, hook, layout, qtile
from libqtile.config import Click, Drag, Group, Key, Screen, KeyChord
from libqtile.lazy import lazy
from libqtile.widget import (
    Clock,
    CPU,
    CurrentLayout,
    GroupBox,
    Image,
    Memory,
    Prompt,
    Sep,
    Systray,
    TaskList,
    TextBox,
    Volume,
)

DEBUG = os.environ.get("DEBUG")

GREY = "#242424"
DARK_GREY = "#111111"
LIGHT_GREY = "#303030"
SILVER = "#aaaaaa"

COLOR_SCREEN_ACTIVE = "#005f4f"
COLOR_SCREEN_FOCUS = "#00a466"
COLOR_URGENT = "#004a2a"
COLOR_WINDOW_FOCUS = "#004a2a"
COLOR_WINDOW_FLOAT = "#00bd66"
COLOR_TASK_FLOATING = "#00bd66"
COLOR_TASK_MINIMIZED = "#777777"
DATE_COLOR = "#667"

WALLPAPERS = [
    os.path.expanduser("~/.config/qtile/wallpapers/wallpaper.png"),
]

SCREEN_LOCK_IMAGE = os.path.expanduser("~/.config/qtile/wallpapers/wallpaper.png")
ICON_THEME_PATH = "/usr/share/icons/Paper"

BROWSER = "firefox"
TERMINAL = "alacritty"
FILE_MANAGER = "thunar"
CALENDAR = "alacritty -e calcurse"
TERMINAL_FILE_MANAGER = "alacritty -e yazi"
SCREEN_LOCKER = f"i3lock -t -i {SCREEN_LOCK_IMAGE}"
SYSTEM_MONITOR = "alacritty -e btop"
LAUNCHER = os.path.expanduser("~/.config/rofi/launchers/type-3/launcher.sh")
POWER_MENU = os.path.expanduser("~/.config/rofi/powermenu/type-2/powermenu.sh")
VOLUME_APP = "pavucontrol"
FLOATING_WINDOWS = ("nm-connection-editor", "galculator")

if qtile.core.name == "wayland":
    from libqtile.backend.wayland import InputConfig

    wl_input_rules = {
        "type:keyboard": InputConfig(kb_layout="es"),
        "type:mouse": InputConfig(natural_scroll=True),
        "type:pointer": InputConfig(natural_scroll=True),
    }


def focus_previous_group(qtile):
    group = qtile.current_screen.group
    group_index = qtile.groups.index(group)
    previous_group = group.get_previous_group(skip_empty=True)
    previous_group_index = qtile.groups.index(previous_group)
    if previous_group_index < group_index:
        qtile.current_screen.set_group(previous_group)


def focus_next_group(qtile):
    group = qtile.current_screen.group
    group_index = qtile.groups.index(group)
    next_group = group.get_next_group(skip_empty=True)
    next_group_index = qtile.groups.index(next_group)
    if next_group_index > group_index:
        qtile.current_screen.set_group(next_group)


def window_to_previous_column_or_group(qtile):
    layout = qtile.current_group.layout
    group_index = qtile.groups.index(qtile.current_group)
    previous_group_name = qtile.current_group.get_previous_group().name

    if layout.name != "columns":
        qtile.current_window.togroup(previous_group_name)
    elif layout.current == 0 and len(layout.cc) == 1:
        if group_index != 0:
            qtile.current_window.togroup(previous_group_name)
    else:
        layout.cmd_shuffle_left()


def window_to_next_column_or_group(qtile):
    layout = qtile.current_group.layout
    group_index = qtile.groups.index(qtile.current_group)
    next_group_name = qtile.current_group.get_next_group().name

    if layout.name != "columns":
        qtile.current_window.togroup(next_group_name)
    elif layout.current + 1 == len(layout.columns) and len(layout.cc) == 1:
        if group_index + 1 != len(qtile.groups):
            qtile.current_window.togroup(next_group_name)
    else:
        layout.cmd_shuffle_right()


def window_to_previous_screen(qtile):
    i = qtile.screens.index(qtile.current_screen)
    if i != 0:
        group = qtile.screens[i - 1].group.name
        qtile.current_window.togroup(group)


def window_to_next_screen(qtile):
    i = qtile.screens.index(qtile.current_screen)
    if i + 1 != len(qtile.screens):
        group = qtile.screens[i + 1].group.name
        qtile.current_window.togroup(group)


def switch_screens(qtile):
    if len(qtile.screens) == 1:
        previous_switch = getattr(qtile, "previous_switch", None)
        qtile.previous_switch = qtile.current_group
        return qtile.current_screen.toggle_group(previous_switch)

    i = qtile.screens.index(qtile.current_screen)
    group = qtile.screens[i - 1].group
    qtile.current_screen.set_group(group)


def init_keys():
    keys = [
        Key([mod, "mod1"], "Left", lazy.function(focus_previous_group)),
        Key([mod, "mod1"], "Right", lazy.function(focus_next_group)),
        Key([mod], "Left", lazy.prev_screen()),
        Key([mod], "h", lazy.prev_screen()),
        Key([mod], "Right", lazy.next_screen()),
        Key([mod], "l", lazy.next_screen()),
        Key([mod, "shift"], "Left", lazy.function(window_to_previous_column_or_group)),
        Key([mod, "shift"], "h", lazy.function(window_to_previous_column_or_group)),
        Key([mod, "shift"], "Right", lazy.function(window_to_next_column_or_group)),
        Key([mod, "shift"], "l", lazy.function(window_to_next_column_or_group)),
        Key([mod, "control"], "Up", lazy.layout.grow_up()),
        Key([mod, "control"], "Down", lazy.layout.grow_down()),
        Key([mod, "control"], "Left", lazy.layout.grow_left()),
        Key([mod, "control"], "Right", lazy.layout.grow_right()),
        Key([mod, "shift", "mod1"], "Left", lazy.function(window_to_previous_screen)),
        Key([mod, "shift", "mod1"], "Right", lazy.function(window_to_next_screen)),
        Key([mod], "Up", lazy.group.prev_window()),
        Key([mod], "k", lazy.group.prev_window()),
        Key([mod], "Prior", lazy.group.prev_window()),
        Key([mod], "Down", lazy.group.next_window()),
        Key([mod], "j", lazy.group.next_window()),
        Key([mod], "Next", lazy.group.next_window()),
        Key([mod, "shift"], "Up", lazy.layout.shuffle_up()),
        Key([mod, "shift"], "Down", lazy.layout.shuffle_down()),
        Key([mod], "tab", lazy.next_layout()),
        Key([mod], "p", lazy.next_layout()),
        Key([mod, "shift"], "tab", lazy.spawn("rofi -show windowcd")),
        Key([mod], "f", lazy.window.toggle_floating()),
        Key([mod, "shift"], "f", lazy.window.toggle_fullscreen()),
        Key([mod], "b", lazy.window.bring_to_front()),
        Key([mod], "s", lazy.layout.toggle_split()),
        Key([mod], "g", lazy.labelgroup()),
        Key([mod], "q", lazy.spawn(POWER_MENU)),
        Key([mod], "Space", lazy.spawn(LAUNCHER)),
        Key([mod], "u", lazy.spawn(browser)),
        Key([mod], "Return", lazy.spawn(terminal)),
        Key([mod], "BackSpace", lazy.window.kill()),
        Key([mod, "shift"], "r", lazy.reload_config()),
        Key([mod, "control"], "r", lazy.restart()),
        Key([mod, "shift"], "q", lazy.shutdown()),
        Key([mod], "v", lazy.validate_config()),
        Key([], "Print", lazy.spawn("gnome-screenshot -a")),
        Key([mod], "Print", lazy.spawn("gnome-screenshot -p")),
        Key([], "Scroll_Lock", lazy.spawn(screenlocker)),
        Key([mod], "t", lazy.spawn(screenlocker)),
        Key([mod], "r", lazy.spawncmd()),
        KeyChord(
            [mod],
            "x",
            [
                Key([], "b", lazy.spawn(SYSTEM_MONITOR)),
                Key([], "n", lazy.spawn(fileManager)),
                Key([], "f", lazy.spawn(browser)),
                Key([], "c", lazy.spawn(CALENDAR)),
                Key([], "y", lazy.spawn(TERMINAL_FILE_MANAGER)),
            ],
        ),
        # Volume
        Key(
            [],
            "XF86AudioLowerVolume",
            lazy.spawn("amixer set Master 2%-"),
        ),
        Key(
            [],
            "XF86AudioRaiseVolume",
            lazy.spawn("amixer set Master 2%+"),
        ),
        Key([], "XF86AudioMute", lazy.spawn("amixer set Master toggle")),
    ]

    return keys


def init_mouse():
    mouse = [
        Drag(
            [mod],
            "Button1",
            lazy.window.set_position_floating(),
            start=lazy.window.get_position(),
        ),
        Drag(
            [mod],
            "Button3",
            lazy.window.set_size_floating(),
            start=lazy.window.get_size(),
        ),
        Click([mod], "Button2", lazy.window.kill()),
    ]
    return mouse


def init_groups():
    def _inner(key, name):
        keys.append(Key([mod], key, lazy.group[name].toscreen()))
        keys.append(Key([mod, "shift"], key, lazy.window.togroup(name)))
        return Group(name)

    groups = [(str(i), str(i)) for i in range(1, 5)]
    groups = [_inner(*i) for i in groups]
    return groups


def init_floating_layout():
    return layout.Floating(border_focus=LIGHT_GREY, border_normal=LIGHT_GREY)


def init_layouts():
    margin = 2
    if qtile.core.name == "X11" and len(qtile.core.conn.pseudoscreens) > 1:
        margin = 2
    kwargs = dict(
        margin=margin,
        border_width=0,
        border_normal=GREY,
        border_focus=COLOR_WINDOW_FOCUS,
        border_focus_stack=COLOR_WINDOW_FOCUS,
    )
    layouts = [
        layout.Max(margin=2),
        layout.Columns(border_on_single=True, num_columns=2, grow_amount=5, **kwargs),
    ]

    return layouts


def parse_notification(message):
    return message.replace("\n", "⏎")


def get_task_list():
    return TaskList(
        fontsize=11,
        borderwidth=0,
        padding_x=6,
        padding_y=3,
        margin=2,
        highlight_method="block",
        rounded=True,
        background=GREY,
        border=DARK_GREY,
        urgent_border=COLOR_URGENT,
        icon_size=14,
        theme_mode="preferred",
        theme_path=ICON_THEME_PATH,
        spacing=2,
        markup_floating=f'<span foreground="{COLOR_TASK_FLOATING}">{{}} </span>',
        markup_minimized=f'<span foreground="{COLOR_TASK_MINIMIZED}">{{}} </span>',
        markup_focused="{} ",
        markup_normal="{} ",
        max_title_width=140,
    )


def get_group_box():
    return GroupBox(
        fontsize=10,
        padding=3,
        padding_x=5,
        borderwidth=2,
        background=LIGHT_GREY,
        inactive=SILVER,
        urgent_border=COLOR_URGENT,
        disable_drag=True,
        highlight_method="block",
        this_screen_border=COLOR_SCREEN_ACTIVE,
        other_screen_border=COLOR_SCREEN_ACTIVE,
        this_current_screen_border=COLOR_SCREEN_FOCUS,
        other_current_screen_border=COLOR_SCREEN_FOCUS,
    )


def get_text_box(text: str, foreground: str, background: str):
    return TextBox(
        text="◤",
        # text=text,
        # font="Menlo for Powerline",
        fontsize=45,
        padding=-1,
        foreground=foreground,
        background=background,
    )


def get_separator(color: str = GREY):
    return Sep(padding=6, foreground=color, background=color)


def get_base_widgets():
    try:
        from libqtile.widget import CurrentLayoutIcon

        return [
            CurrentLayoutIcon(scale=0.6, padding=8, background=DARK_GREY),
            get_group_box(),
            get_task_list(),
        ]
    except ImportError:
        return [
            CurrentLayout(
                scale=0.6,
                padding=8,
                background=DARK_GREY,
                mode="icon",
            ),
            # get_text_box("", DARK_GREY, LIGHT_GREY),
            # get_separator(LIGHT_GREY),
            get_group_box(),
            # get_text_box("", LIGHT_GREY, GREY),
            # get_separator(),
            get_task_list(),
        ]


def get_main_widgets():
    widgets = get_base_widgets() + [
        Prompt(background=GREY),
        # get_text_box("", GREY, LIGHT_GREY),
        get_separator(LIGHT_GREY),
        Systray(background=LIGHT_GREY),
        # get_text_box("", LIGHT_GREY, DARK_GREY),
        get_separator(LIGHT_GREY),
        Volume(
            emoji=True,
            emoji_list=[" ", " ", " ", " "],
            background=LIGHT_GREY,
            mouse_callbacks={"Button3": lazy.spawn(VOLUME_APP)},
        ),
        Volume(
            emoji=False,
            background=LIGHT_GREY,
            fmt="VOL: {}",
            mouse_callbacks={"Button3": lazy.spawn(VOLUME_APP)},
        ),
        get_separator(LIGHT_GREY),
        # Notify(fmt=" 🔥 {} ", parse_text=parse_notification),
        # PulseVolume(fmt=" {}", emoji=True, volume_app="pavucontrol"),
        # PulseVolume(volume_app="pavucontrol"),        get_separator(LIGHT_GREY),
        # get_separator(LIGHT_GREY),
        Image(
            filename="~/.config/qtile/cpu.svg",
            background=LIGHT_GREY,
            margin=4,
            mouse_callbacks={"Button1": lazy.spawn(SYSTEM_MONITOR)},
        ),
        CPU(
            format="CPU: {load_percent:2.0f}% ",
            update_interval=2,
            background=LIGHT_GREY,
            mouse_callbacks={"Button1": lazy.spawn(SYSTEM_MONITOR)},
        ),
        Image(
            filename="~/.config/qtile/mem.svg",
            background=LIGHT_GREY,
            margin=4,
            mouse_callbacks={"Button1": lazy.spawn(SYSTEM_MONITOR)},
        ),
        Memory(
            format="MEM: {MemPercent:2.0f}% | {SwapPercent:2.0f}% ",
            # format="MEM: {MemPercent:2.0f}% ",
            update_interval=2,
            background=LIGHT_GREY,
            mouse_callbacks={"Button1": lazy.spawn(SYSTEM_MONITOR)},
        ),
        get_separator(LIGHT_GREY),
        get_separator(DARK_GREY),
        Clock(
            format=f"<span color='{DATE_COLOR}'>%d-%m-%Y</span>  %H:%M",
            mouse_callbacks={"Button1": lazy.spawn(CALENDAR)},
        ),
        get_separator(DARK_GREY),
    ]

    return widgets


def get_additional_widgets():
    return get_base_widgets() + [
        get_separator(),
    ]


@hook.subscribe.startup_once
def autostart():
    name = "wautostart" if qtile.core.name == "wayland" else "autostart"
    home = os.path.expanduser(f"~/.config/qtile/{name}.sh")
    subprocess.Popen([home])


@hook.subscribe.client_new
def set_floating(window):
    if qtile.core.name == "wayland":
        return
    try:
        if window.window.get_wm_class()[0] in FLOATING_WINDOWS:
            window.floating = True
    except IndexError:
        pass


def animate_opacity(window, start, end, steps=10, delay=0.01):
    diff = (end - start) / steps
    current = start

    def step():
        nonlocal current
        current += diff
        if (diff > 0 and current >= end) or (diff < 0 and current <= end):
            window.opacity = end
            return
        window.opacity = current
        qtile.call_later(delay, step)

    window.opacity = start
    qtile.call_later(delay, step)


@hook.subscribe.client_focus
def client_focus(client):
    if qtile.core.name != "wayland":
        return
    for group in qtile.groups:
        for window in group.windows:
            animate_opacity(window, 1, 0.97, 8)

    animate_opacity(client, 0.97, 1)


@hook.subscribe.startup_complete
def set_logging():
    if DEBUG:
        qtile.cmd_debug()


def get_wallpapers():
    image1 = random.choice(WALLPAPERS)
    image2 = random.choice(WALLPAPERS)

    count = 0
    while image1 == image2 and count < 10:
        image2 = random.choice(WALLPAPERS)
        count += 1

    return [image1, image2]


if __name__ in ["config", "__main__"]:
    local_bin = os.path.expanduser("~") + "/.local/bin"
    if local_bin not in os.environ["PATH"]:
        os.environ["PATH"] = "{}:{}".format(local_bin, os.environ["PATH"])

    mod = "mod4"
    browser = BROWSER
    terminal = TERMINAL
    fileManager = FILE_MANAGER
    screenlocker = SCREEN_LOCKER
    hostname = socket.gethostname()
    cursor_warp = True
    focus_on_window_activation = "never"

    auto_fullscreen = False
    keys = init_keys()
    mouse = init_mouse()
    groups = init_groups()
    floating_layout = init_floating_layout()
    layouts = init_layouts()

    wallpapers = get_wallpapers()
    screens = [
        Screen(
            top=bar.Bar(
                widgets=get_main_widgets(),
                size=24,
                opacity=0.9 if qtile.core.name == "wayland" else 0.7,
                margin=[3, 2, 1, 2],
            ),
            wallpaper=wallpapers[0],
        ),
        # Screen(
        #     top=bar.Bar(
        #         widgets=get_additional_widgets(),
        #         size=24,
        #         opacity=0.7,
        #         margin=[3, 2, 1, 2],
        #     ),
        #     wallpaper=wallpapers[1],
        # ),
    ]
    widget_defaults = {
        "font": "DejaVu",
        "fontsize": 11,
        "padding": 4,
        "background": DARK_GREY,
    }
    wmname = "LG3D"
