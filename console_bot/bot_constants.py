import os
import sys


APPDATA_DIRNAME = ".ConsoleBot"
if sys.platform == "win32":
    APPDATA_PATH = os.path.join(os.environ.get("USERPROFILE"), APPDATA_DIRNAME)
elif sys.platform == "linux":
    APPDATA_PATH = os.path.join(os.path.expanduser("~"), APPDATA_DIRNAME)
elif sys.platform == "darwin":
    APPDATA_PATH = os.path.join(os.path.expanduser("~"), APPDATA_DIRNAME)
else:
    raise Exception("Unsupported platform: {}".format(sys.platform))

if not os.path.exists(APPDATA_PATH):
    os.makedirs(APPDATA_PATH)

BOT_STATE_FILE = os.path.join(APPDATA_PATH, "bot_data.json")
