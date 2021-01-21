## RDP at Home

We want to operate the firefox on the desktop in the study (connected
to the TV with an HDMI cable)...

_... from the couch in the living room._

Why is this an issue? Well, our study is separated from the living
room by a sliding door that includes the TV - so pausing a movie or
changing the volume involves a walk to the study (and the shortest
route involves sliding away the TV), an inconvenient interruption.

A straightforward solution should be to connect our (Windows)
laptop(s) to the (Linux) desktop using Remote Desktop. GNOME Remote
Desktop should enable just that, but it is, well, _pre-alpha_; not yet
ready for use in my desktop environment (FC33).

_Here's the steps to make this work!_

### Sharing settings

The first step is to turn GNOME Remote Desktop on/off through the
Screen Sharing dialogue, under `Settings / Sharing / Screen Sharing`
in the menu. 

Choose a password, pick one that is different from your normal login
password.

Switching the slider in the Sharing settings is equivalent to
entering the following from the command-line:

    systemctl --user start|stop gnome-remote-desktop.service

### TLS settings

The second step is to make the Windows client connect to the Linux
server without connection errors. I did not yet find out whether it is
the Windows RDP client that forces the use of TLS 2.0 or whether this
is a requirement in the GNOME Remote Desktop server, but you must
provide a key for the server.

The following is a workaround that needs improvement. I have -
temporarilly - [created self-signed certificates](keys.md)
`server.crt` and `server.key`. 

Getting things to actually work creates a minor security issue:
because the _user_ runs `gnome-remote-desktop` (and not `root`), 
the file storing the server's _private_ key must be user-readable:

    sudo chown $USER /etc/pki/tls/private/server.key

Use `dconf-editor` to set the following values, or use the CLI:

    gsettings set org.gnome.desktop.remote-desktop.rdp tls-cert  '/etc/pki/tls/certs/server.crt'
    gsettings set org.gnome.desktop.remote-desktop.rdp tls-key   '/etc/pki/tls/private/server.key'
    gsettings set org.gnome.desktop.remote-desktop.rdp view-only "false"

### RDP credentials

Once I got this far, I discovered that the UI/UX for controlling
access is unfinished or missing.

When trying to connect to GNOME Remote Desktop you see the following
errors in the log (`journalctl -rx`): 
`gnome-remote-de[XXX]: Couldn't retrieve RDP username: Credentials not set`.

The problem is that `grd-settings.c` [(code)][grd-settings-c]
looks for user credentials using `libsecret`; the VNC password in
`org.gnome.RemoteDesktop.VncPassword` is set correctly using the
Screen Sharing dialogue mentioned above, but the option to control
`org.gnome.RemoteDesktop.RdpCredentials` is still missing from the
UI.

Initially, I attempted to mimic the VNC values using `seahorse` and/or
`secret-tool`, but to no avail. After trying many different failed
methods to get the credentials into the user environment in the right
way, I ended up reverse engineering the solution from the code and
writing a simple _yet-not-robust_ python script to create these
values correctly (the server code is still fragile and crashes upon
incorrect values).

Download `RDP-set-credentials.py` [from this repository][repo] and
issue the following command:

    python RDP-set-credentials.py $USER vnc-password

The password should correspond to the one given under Access Options
in the Sharing dialogue.

### Next steps

Use-case watching online films from the couch has been solved!
Unfortunately, only mouse input works - I have yet to find out how to
fix keyboard input. _Stay tuned..._

[grd-settings-c]:	https://gitlab.gnome.org/GNOME/gnome-remote-desktop/-/blob/master/src/grd-settings.c	"grd-settings.c"
[repo]:				https://github.com/arjenpdevries/RDP													"arjenpdevries/RDP"
