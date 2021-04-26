from PIL import Image
import argparse
import os

im = Image.open("thumbnail.webp").convert("RGB")
im.save("thumbnail.jpg","jpeg")
os.remove("thumbnail.webp")