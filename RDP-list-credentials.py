"""
Companion script to test RDP-set-credentials.py
"""

import gi
gi.require_version('Secret', '1')

from gi.repository import Secret, GLib

RDP_SCHEMA = Secret.Schema.new("org.gnome.RemoteDesktop.RdpCredentials",
	Secret.SchemaFlags.NONE,
	{
		"credentials": Secret.SchemaAttributeType.STRING,
                "NULL": 0
	}
)

vdict = Secret.password_lookup_sync(RDP_SCHEMA, { "credentials": "username" }, None)
gvd = GLib.Variant.parse(None, vdict, None, None)

assert isinstance(gvd, GLib.Variant)

uname = gvd.lookup_value("username", None)
print(uname)
pwd = gvd.lookup_value("password", None)
print(pwd)


