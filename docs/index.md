## RDP at Home

We want to operate firefox in the study (connected to the TV with an HDMI cable)...

_... from the couch in the living room._

This would let us pause a movie or adapt the volume without walking to the study.
A straightforward solution should be to connect our (Windows) laptop(s) to the 
desktop with Remote Desktop.

GNOME Remote Desktop should do what we want, but is, well, pre-alpha;
it is not yet completely integrated in the desktop environment (FC33).

### Sharing settings

You can turn GNOME Remote Desktop on/off through the Screen Sharing dialogue: 
Settings / Sharing / Screen Sharing. Switching the slider is equivalent to 
issuing `systemctl --user start|stop gnome-remote-desktop.service`.

Choose a password, pick one that is different from your normal login password.

### TLS settings

I did not find out whether it is the Windows RDP client that forces the use of TLS, 
or it is a requirement in the GNOME Remote Desktop server, but you need a key for the server.
I have - temporarilly - created self-signed certificates `server.crt` and `server.key`.

You either use `dconf-editor` to set these values, or use the CLI:

    gsettings set org.gnome.desktop.remote-desktop.rdp tls-cert  '/etc/pki/tls/certs/server.crt'
    gsettings set org.gnome.desktop.remote-desktop.rdp tls-key   '/etc/pki/tls/private/server.key'
    gsettings set org.gnome.desktop.remote-desktop.rdp view-only "false"

The current way to get it to work creates a minor security issue, because it is the user who runs
`gnome-remote-desktop` and not `root`; the file storing the server's private key must be 
user-readable:

    sudo chown $USER /etc/pki/tls/private/server.key

### RDP credentials

Once I got this far, I discovered that the UI/UX for controlling access is unfinished.

When trying to connect to GNOME Remote Desktop you see the following errors (`journalctl -rx`):
`gnome-remote-de[XXX]: Couldn't retrieve RDP username: Credentials not set`.

The problem is that 
[`grd-settings.c`](https://gitlab.gnome.org/GNOME/gnome-remote-desktop/-/blob/master/src/grd-settings.c)
looks for user credentials using `libsecret`; the VNC password in `org.gnome.RemoteDesktop.VncPassword` 
is set correctly using the Screen Sharing dialogue mentioned above, but the option to control 
`org.gnome.RemoteDesktop.RdpCredentials` is still missing from the UI.

Initially, I attempted to mimic the VNC values using `seahorse` and/or `secret-tool`, but to no avail.
After trying many different failed methods to get the credentials into the user environment in the right way,
I ended up reverse engineering the solution from the code and writing a simple _yet-not-robust_ python script 
to create these values correctly (the server code is still fragile and crashes upon incorrect values).

You find the scripts in this repository.
