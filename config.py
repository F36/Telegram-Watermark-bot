import os

BOT_TOKEN = os.environ.get("BOT_TOKEN")
WATERMARK = str(os.environ.get("WATERMARK", "...watermark..."))
FONT_SIZE = int(os.environ.get("FONT_SIZE", 15))
FONT_NAME = "Space_Age.ttf"  # check tools/fonts
TRANSPARENCY = float(os.environ.get("TRANSPARENCY", 0.75))
QUALITY = int(os.environ.get("QUALITY", 100))
