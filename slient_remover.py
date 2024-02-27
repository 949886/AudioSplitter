import os
import librosa
import soundfile as sf
import numpy as np

def remove_silence(input_file, output_folder):
    # Create output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Load audio using librosa
    y, sr = librosa.load(input_file, sr=None)

    # Split an audio signal into non-silent intervals.
    intervals = librosa.effects.split(y, top_db=50)

    # Handle each intervals.
    trimmed_audio = []
    for interval in intervals:
        start_time = librosa.samples_to_time(interval[0], sr=sr)
        end_time = librosa.samples_to_time(interval[1], sr=sr)
        duration = end_time - start_time
        if duration >= 2:  # Keep intervals longer than 2 seconds
            trimmed_audio.append(y[interval[0]:interval[1]])

    # Concatenate continuous sound parts
    trimmed_audio = np.concatenate(trimmed_audio)

    # Save continuous sound parts
    output_file = os.path.join(output_folder, os.path.splitext(input_file)[0] + "_trimmed.wav")
    sf.write(output_file, trimmed_audio, sr)
    print("Trimmed audio saved at:", output_file)

# Example usage
input_file = "audio.aac"
output_folder = "trimmed_audio"
remove_silence(input_file, output_folder)
