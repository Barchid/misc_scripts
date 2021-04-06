# Import everything needed to edit video clips
from moviepy.editor import *
import argparse
import youtube_dl
import os
from PIL import Image

# CONSTANTS
HOUR_IN_SECS = 4 * 60
FILENAME_THUMB = "tmp_thumbnail"
FILENAME_SONG = "tmp_song"
DEST_DIR = "one_hour_vids"

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source_url", help="Youtube URL of audio to make one hour vid")
    parser.add_argument("--destination_file", help="Filename of the resulting 1-hour video")
    return parser.parse_args()


def download_youtube_vid(url):
    ydl_opts = {}
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])


def download_youtube_thumb(url):
    os.system(f"youtube-dl --write-thumbnail --skip-download -o {FILENAME_THUMB} {url}")


def download_youtube_audio(url):
    ydl_opts = {
        'format': 'bestaudio/best',
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
    nloops = int(duration/ song.duration)+1
    return afx.audio_loop(song, nloops=nloops)


def vid_to_1hour():
    source_song = AudioFileClip(FILENAME_SONG + ".mp3")
    hour_song = audio_loop(source_song, HOUR_IN_SECS)
    one_hour = ImageClip(FILENAME_THUMB + ".jpg", duration=hour_song.duration)
    one_hour.audio = hour_song
    return one_hour

def webp2jpg():
    im = Image.open(FILENAME_THUMB + ".webp").convert('RGB')
    im.save(FILENAME_THUMB + ".jpg", 'jpeg')

if __name__ == "__main__":
    args = get_args()
    download_youtube_audio(args.source_url)
    download_youtube_thumb(args.source_url)
    webp2jpg()
    one_hour = vid_to_1hour()
    one_hour.write_videofile(os.path.join(DEST_DIR, args.destination_file), fps=1)