import os
import librosa
import soundfile as sf
import numpy as np

def split_audio(input_file, output_folder):
    # Create output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Load audio using librosa
    y, sr = librosa.load(input_file, sr=None)

    # Split an audio signal into non-silent intervals.
    intervals = librosa.effects.split(y, top_db=50)

    # Save each segment separately
    for i, interval in enumerate(intervals):
        start_sample = interval[0]
        end_sample = interval[1]
        duration = librosa.samples_to_time(end_sample - start_sample, sr=sr)
        if duration >= 0.5:  # Keep intervals longer than 0.5 seconds
            segment = y[start_sample:end_sample]
            output_file = os.path.join(output_folder, f"{os.path.splitext(input_file)[0]}_{i}.mp3")
            sf.write(output_file, segment, sr)
            print(f"Segment {i}:{duration} saved at: {output_file}")
        else: print(f"Segment {i}:{duration} discarded.")

# Example usage
input_file = "audio.aac"
output_folder = "segmented_audio"
split_audio(input_file, output_folder)
