"""
Set credentials for GNOME Remote Desktop
A quick hack.
"""

import sys
import gi
gi.require_version('Secret', '1')
from gi.repository import Secret

RDP_SCHEMA = Secret.Schema.new("org.gnome.RemoteDesktop.RdpCredentials",
	Secret.SchemaFlags.NONE,
	{
		"credentials": Secret.SchemaAttributeType.STRING,
                "NULL": 0
	}
)

attributes = {
	"credentials": "username",
}


def main(username,password):
    Secret.password_store_sync(RDP_SCHEMA, attributes, Secret.COLLECTION_DEFAULT,
                               "RDP username", "{{\"username\":\"{}\",\"password\":\"{}\"}}".format(username,password), None)

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Usage:\n python {} username password'.format(__file__))
    else:
        main(sys.argv[1], sys.argv[2])
