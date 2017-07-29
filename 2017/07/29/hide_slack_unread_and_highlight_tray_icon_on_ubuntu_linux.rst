Hide Slack unread and highlight Tray Icon on Ubuntu/Linux
=========================================================

The Slack Ubuntu/Linux application doesn't provide a way to disable the tray
icon and that means the unread or highlight notification bubbles will distract
you whenever somebody writes something in ANY channel that you are in, even
when the messages are not even interesting for you.

I wrote to Slack support to make a feature request and they suggested to make
clever use of an upstream Electron bug that makes the tray icon disappear in
17.04 as a workaround. This gave me the idea for a  more stable workaround.

I poked around in the list of files of the `slack-desktop` package and found
out that you can just exchange the files for the tray icons , so that the Slack
app is fooled into thinking it is showing the unread or highlight icons.

    sudo -i
    cd /usr/lib/slack/resources/app.asar.unpacked/src/static
    mv slack-taskbar-highlight.png slack-taskbar-highlight-backup.png
    mv slack-taskbar-unread.png slack-taskbar-unread-backup.png
    cp slack-taskbar-rest.png slack-taskbar-highlight.png
    cp slack-taskbar-rest.png slack-taskbar-unread.png

Since I probably need to re-run this after every update to the Slack app, I
packed this into a shell script `slack-quiet`.

.. author:: default
.. categories:: none
.. tags:: none
.. comments::
