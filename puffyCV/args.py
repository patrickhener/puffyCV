import argparse
from puffyCV._version import __version__

global args

parser = argparse.ArgumentParser(
    description="Software to recognise Steel Darts thrown to a board using multiple cameras and openCV"
)

parser.add_argument(
    dest="MODE",
    type=str,
    help="which mode to use: either 'run' for recognising darts or 'cal' for calibration of webcams"
)

parser.add_argument(
    'DEVICE_IDS',
    type=int,
    nargs='+',
    help='device ids for the devices that should be used'
)

parser.add_argument(
    '-rw',
    '--resolution-width',
    dest="WIDTH",
    default=1920,
    type=int,
    help="Resolution width of cameras in use (default: 1920)"
)

parser.add_argument(
    '-rh',
    '--resolution-height',
    dest="HEIGHT",
    default=1080,
    type=int,
    help="Resolution height of cameras in use (default: 1080)"
)

parser.add_argument(
    '-pf',
    '--pixel-format',
    dest="PIXELFORMAT",
    default="MJPG",
    type=str,
    help="Pixelformat of cameras in use (default: 'MJPG')"
)

parser.add_argument(
    '-sh',
    '--scoreboard-host',
    dest="SB-HOST",
    default="127.0.0.1",
    type=str,
    help="the hostname or IP address where the scoreboard is hosted (default: 127.0.0.1)"
)

parser.add_argument(
    '-sp',
    '--scoreboard-port',
    dest="SB-PORT",
    default="5000",
    type=str,
    help="the port on which the scoreboard is hosted (default: 5000)"
)

parser.add_argument(
    '-d',
    '--debug',
    dest="DEBUG",
    default=False,
    action="store_true",
    help="show debug messages"
)

parser.add_argument(
    '-ob',
    '--omit-banner',
    dest="OBANNER",
    default=False,
    action="store_true",
    help="Omit print of puffyCV Banner"
)

parser.add_argument(
    '-v',
    '--version',
    action='version',
    version='puffyCV ' + __version__
)

args = parser.parse_args()
