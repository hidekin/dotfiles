#!/usr/bin/env python
# -*- coding: utf-8 -*-

import subprocess

from i3pystatus import Status
from i3pystatus.updates import pacman, cower
import os
import json
import collections
from i3pystatus.mail import imap


black       = "#2c2836"
darkblack   = "#73707e"
red         = "#bb7473"
darkred     = "#cf9fa4"
green       = "#68b782"
darkgreen   = "#9acbad"
yellow      = "#abb773"
darkyellow  = "#c5cba4"
blue        = "#7865c5"
darkblue    = "#a396d9"
magenta     = "#bb65b6"
darkmagenta = "#cf96cf"
cyan        = "#68a8c5"
darkcyan    = "#9ac1d9"
white       = "#f1edfb"
darkwhite   = "#f1edfb"
background  = "#133B47"

status = Status(standalone=True)

status.register("clock",
    format="%a %-d %b %X",)




# status.register("battery",
#     format="{status} {percentage:.0f}% {remaining:%E%hh:%Mm}",
#     alert=True,
#     alert_percentage=5,
#     color=white,
#     critical_color=red,
#     charging_color=yellow,
#     full_color=white,
#     status={
#         "DIS": "DIS",
#         "CHR": "CHR",
#         "FULL": "FUL",
#     },)

# status.register("network",
#     interface="enp0s2",
#     color_up=white,
#     color_down=red,
#     format_up="{v4cidr}",
#     format_down="")

# status.register("wireless",
#     interface="wlp3s0",
#     color_up=white,
#     color_down=red,
#     format_up="{essid} {quality:03.0f}%",)

# status.register("pulseaudio",
#     format="VOL {volume}%",
#     color_muted=red,
#     color_unmuted=white,)

# status.register('reddit',
#     username=hidekin,
#     password=83H63WYry43v,
#     mail_brackets=True,
#     format='{message_unread}',
#     interval=60,
#   )

status.register("updates",
                format = "Updates: {count}",
                format_no_updates = "No updates",
                backends = [pacman.Pacman(), cower.Cower()])




class MySettings(collections.MutableMapping):

    def __init__(self, settings_file=None, *args, **kwargs):
        """Settings object for retreiving personal user data for i3pystatus.
        Usage:
        .. code-block:: python
            >>> settings = MySettings()
            >>> settings.get("weather")
            { "weather": { "location_code": "USCA0001", "units": "imperial" }}
            >>> settings = MySettings(settings_file="/path/to/config.json")
            >>> settings.get("weather")
            { "weather": { "location_code": "USCA0001", "units": "imperial" }}
        :param settings_file: Location of JSON config file.
        :type settings_file: string
        """

        super(MySettings, self).__init__(*args, **kwargs)

        if not settings_file:
            settings_file = os.path.expanduser('~/.i3/local_settings.json')

        self.settings_file = settings_file

        if os.path.isfile(settings_file):
            self._data = json.loads(open(settings_file).read())
        else:
            self._data = {}

    def __getitem__(self, key):
        return self._data[key]

    def __setitem__(self, key, value):
        self._data[key] = value
        self.dirty = True

    def __delitem__(self, key):
        del self._data[key]
        self.dirty = True

    def keys(self):
        """Return list of keys."""
        return self._data.keys()

    def __iter__(self):
        return self._data.__iter__()

    def __len__(self):
        return len(self._data.keys())


# Load settings from ``$HOME/.i3/local_settings.json
my_settings = MySettings()



# Displays clock like this: # Tue 30 Jul 11:59:46 PM KW31
#                          ^-- calendar week
status.register("clock",
                format="%a %-d %b %l:%M%p",)

# Shows the average load of the last minute and the last 5 minutes
# (the default value for format is used)
status.register("load")

# Shows your CPU temperature, if you have a Intel CPU
status.register("temp",
                format="{temp:.0f}°C",)

# The battery monitor has many formatting options, see README for details

# This would look like this, when discharging (or charging)
# ↓14.22W 56.15% [77.81%] 2h:41m
# And like this if full:
# =14.22W 100.0% [91.21%]
#
# This would also display a desktop notification (via dbus) if the percentage
# goes below 5 percent while discharging. The block will also color RED.
# status.register("battery",
#                 format="{status}/{consumption:.2f}W {percentage:.2f}% [{percentage_design:.2f}%] {remaining:%E%hh:%Mm}",
#                 alert=True,
#                 alert_percentage=5,
#                 status={
#                     "DIS": "↓",
#                     "CHR": "↑",
#                     "FULL": "=",
#                 },)

# This would look like this:
# Discharging 6h:51m
# status.register("battery",
#                 format="{status} {remaining:%E%hh:%Mm}",
#                 alert=True,
#                 alert_percentage=5,
#                 status={
#                     "DIS":  "Discharging",
#                     "CHR":  "Charging",
#                     "FULL": "Bat full",
#                 },)

# Displays whether a DHCP client is running
status.register("runwatch",
                name="DHCP",
                path="/var/run/dhclient*.pid",)

# Shows the address and up/down state of eth0. If it is up the address is shown in
# green (the default value of color_up) and the CIDR-address is shown
# (i.e. 10.10.10.42/24).
# If it's down just the interface name (eth0) will be displayed in red
# (defaults of format_down and color_down)
#
# Note: the network module requires PyPI package netifaces-py3
# status.register("network",
#                 interface="enp0s2",
#                 format_up="{v4cidr}",)

# Has all the options of the normal network and adds some wireless specific things
# like quality and network names.
#
# Note: requires both netifaces-py3 and basiciw
# status.register("wireless",
#                 interface="wlan0",
#                 format_up="{essid} {quality:03.0f}%",)

# Shows disk usage of /
# Format:
# 42/128G [86G]
status.register("disk",
                path="/",
                format="{avail}G HD Free",)

# Shows pulseaudio default sink volume
#
# Note: requires libpulseaudio from PyPI
# status.register("alsa",
#                 format="♪{volume}",)


# Shows weather
if my_settings.get('weather'):
    status.register("weather",
                    **my_settings.get('weather')
                    )

# Shows mpd status
# Format:
# Cloud connected▶Reroute to Remain
status.register("mpd",
                format="{title} {status} {album}",
                status={
                    "pause": "▷",
                    "play": "▶",
                    "stop": "◾",
                },)



status.run()
