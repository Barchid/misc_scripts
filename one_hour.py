import argparse
from moviepy.audio.io.AudioFileClip import AudioFileClip
from moviepy.video.VideoClip import ImageClip
import youtube_dl
import os

# CONSTANTS
TMP_SONG = "tmp_song"
TMP_VIDEO = "tmp_video.mp4"
TARGET_SECONDS_DURATION = 60 * 60 * 1 # One hour in seconds here

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--youtube_url", "-y", help="Youtube URL of audio to make one hour vid")
    parser.add_argument("--output", "-o", help="Filename of the resulting 1-hour video", default="result.mp4")
    parser.add_argument("--thumbnail", "-t", help="File URL of the picture to use as a youtube video")
    # parser.add_argument("--artist", help="Artist name", required=True)
    # parser.add_argument("--title", help="Title of the song.", required=True)
    return parser.parse_args()

def download_youtube_audio(url):
    print(f"DOWNLOAD YOUTUBE VIDEO TO LOOP : {url}")
    ydl_opts = {
        'format': 'worstaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': TMP_SONG + '.%(ext)s'
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    print(f"YOUTUBE VIDEO LOCATED IN FILE {TMP_SONG}.mp3")

def get_number_of_loops(audio: AudioFileClip):
    """Computes the number of loops needed to obtain a one-hour video

    Args:
        audio (AudioFileClip): The Audio Clip to loop
    """
    return int(TARGET_SECONDS_DURATION/audio.duration)
    

def thumb_audio_fusion(thumbnail_url: str):
    """Merges the tmp audio file from Youtube with a picture (its file URL in parameter) and saves the result into a .mp4 file

    Args:
        thumbnail_url (str): file URL of the thumbnail
    """
    source_song = AudioFileClip(f"{TMP_SONG}.mp3")

    # Image Clip
    fusion = ImageClip(thumbnail_url, duration=source_song.duration)

    # attach audio to image clip
    fusion.audio = source_song

    print(f'SAVING FUSION OF AUDIO AND THUMBNAIL IN FILE {TMP_VIDEO}')
    fusion.write_videofile(TMP_VIDEO, fps=1)

    return fusion

def create_one_hour(video, output):
    """Creates a one-hour loop of the video located in the URL of the constant TMP_VIDEO using ffmpeg

    Args:
        video (AudioFileClip): the video to loop
        output (str): the output URL of the resulting one-hour video
    """
    loop_number = get_number_of_loops(video)
    print(loop_number)
    print(f"CREATING ONE-HOUR LOOP IN FILE {output}")
    os.system(f"ffmpeg -stream_loop {loop_number} -i {TMP_VIDEO} -c copy {output}")

def remove_tmp_files():
    """Empty disk by removing TMP files to prepare the next run
    """
    if os.path.exists(TMP_VIDEO):
        print(f'REMOVING TMP FILE {TMP_VIDEO}')
        os.remove(TMP_VIDEO)
    
    if os.path.exists(TMP_SONG + ".mp3"):
        print(f'REMOVING TMP FILE {TMP_SONG}.mp3')
        os.remove(f"{TMP_SONG}.mp3")

if __name__ == "__main__":
    args = get_args()

    download_youtube_audio(args.youtube_url)
    video = thumb_audio_fusion(args.thumbnail)
    create_one_hour(video, args.output)
    remove_tmp_files()
    print('\n\n\nEND OF SCRIPT\n\n\n')