import tkinter as tk
from tkinter import filedialog
import random
from moviepy.editor import *

#open file manager for images
def get_image():
    print("Please select a thumbnail image.")
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.bmp")])
    return file_path

#open file manager for audio
def get_audio_files():
    print("Please select the audio files to play.")
    file_paths = filedialog.askopenfilenames(filetypes=[("Audio files", "*.mp3;*.wav")])
    return file_paths

# TODO: use sound effects that have not been used first, and refresh options when empty.
#Select and add a random sound from the ones chosen
def add_random_sound(clip, audio_effects):
    sound_effect = audio_effects[random.randint(0, len(audio_effects) - 1)]
    start_time = random.uniform(0, clip.duration - sound_effect.duration)
    return clip.set_audio(sound_effect.set_start(start_time))

def create_video():
    # Get background image
    image_path = get_image()
    if not image_path:
        return

    # Get audio files
    audio_paths = get_audio_files()
    if not audio_paths:
        return

    # Create video clip with the background image
    clip_duration = 3600  # seconds
    amount_of_sounds = random.randrange(20,24)
    
    clip = ImageClip(image_path).set_duration(clip_duration)

    # Load audio clips
    audio_effects = [AudioFileClip(path) for path in audio_paths]

    # TODO: instead of 20-24 subclips, prompt the user for this range (or specific amount?)
    # Split the clip into smaller subclips for random sound effects, and add a random delay between each
    subclip_duration = (clip_duration / amount_of_sounds)
    subclips = [clip.subclip(t, t + subclip_duration + random.randrange(1,(clip_duration*0.01))) for t in range(0, clip_duration, int(subclip_duration)+random.randrange(1,(clip_duration*0.01)))]

    # Add random sound effects to each subclip
    final_clip = concatenate_videoclips([add_random_sound(subclip, audio_effects) for subclip in subclips])

    # Save the final video
    output_filename = "output.mp4"
    final_clip.write_videofile(output_filename, fps=1)

    print("Video created successfully as " + output_filename)

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    create_video()