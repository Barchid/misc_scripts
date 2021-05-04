# Import everything needed to edit video clips
import click
from moviepy.editor import *
import argparse
import youtube_dl
import os
from PIL import Image, ImageDraw, ImageFont
from unsplash_image import get_random_picture

# CONSTANTS
HOUR_IN_SECS = 60 * 1 * 3
FILENAME_THUMB = "thumbnail"
FILENAME_SONG = "tmp_song"
DEST_DIR = "one_hour_vids"

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source_url", help="Youtube URL of audio to make one hour vid")
    parser.add_argument("--destination_file", help="Filename of the resulting 1-hour video", default="result.mp4")
    # parser.add_argument("--artist", help="Artist name", required=True)
    # parser.add_argument("--title", help="Title of the song.", required=True)
    return parser.parse_args()


def download_youtube_vid(url):
    ydl_opts = {}
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])


def download_youtube_thumb(url):
    os.system(f"youtube-dl --write-thumbnail --skip-download -o {FILENAME_THUMB} {url}")


def download_youtube_audio(url):
    ydl_opts = {
        'format': 'worstaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': FILENAME_SONG + '.%(ext)s'
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])



def audio_loop(song, duration):
    print('AUDIO LOOP')
    nloops = int(duration/ song.duration)+1
    return afx.audio_loop(song, nloops=nloops)


def vid_to_1hour():
    # One-hour audio
    source_song = AudioFileClip(FILENAME_SONG + ".mp3")
    hour_song = audio_loop(source_song, HOUR_IN_SECS)

    # Image
    print('Image Clip')
    one_hour = ImageClip(FILENAME_THUMB + ".jpg", duration=hour_song.duration)

    one_hour.audio = hour_song
    return one_hour

def write_text(artist, title, im):
    draw = ImageDraw.Draw(im)

    font = ImageFont.truetype('Roboto-Bold.ttf', size=45)
    # choose color of font
    if click.confirm('White font with this picture ?', default=True):
        print('Using white font.')
        color = 'rgb(255, 255, 255)' # black color
    else:
        print('Using black font.')
        color = 'rgb(0, 0, 0)' # black color

    # Write title
    (x, y) = (50, 50)
    draw.text((x, y), title.upper(), fill=color, font=font)

    # Write artist
    font = ImageFont.truetype('Roboto-Bold.ttf', size=37)
    (x, y) = (60, 150)
    draw.text((x, y), artist, fill=color, font=font)

    return im

if __name__ == "__main__":
    # im = get_random_picture()
    # im.show()
    # exit()
    args = get_args()

    if not os.path.exists(FILENAME_THUMB + ".jpg"):
        print('No thumbnail found. Bye bye.')
        exit()

    download_youtube_audio(args.source_url)
    one_hour = vid_to_1hour()
    print('Saving video')
    one_hour.write_videofile(os.path.join(DEST_DIR, args.destination_file), fps=1)