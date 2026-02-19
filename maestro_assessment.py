import os
import pandas as pd
import pretty_midi

# ---------------------------
# Part 1: Load and Inspect MAESTRO Metadata
# ---------------------------

# Load the MAESTRO metadata CSV file
metadata_path = "maestro-v3.0.0.csv"
df = pd.read_csv(metadata_path)
print("First few rows of the metadata:")
print(df.head())

# Randomly sample 10 rows for analysis
sample_df = df.sample(n=10, random_state=42)
print("\nSampled metadata (canonical_title, canonical_composer, duration):")
print(sample_df[['canonical_title', 'canonical_composer', 'duration']])

# ---------------------------
# Part 2: Load MIDI File Information (Optional)
# ---------------------------
def load_midi_info(midi_file_path):
    try:
        midi_data = pretty_midi.PrettyMIDI(midi_file_path)
        duration = midi_data.get_end_time()
        num_instruments = len(midi_data.instruments)
        return {
            "file": os.path.basename(midi_file_path),
            "duration": duration,
            "num_instruments": num_instruments
        }
    except Exception as e:
        print(f"Error processing {midi_file_path}: {e}")
        return None

# Define the base folder that contains the MAESTRO MIDI files (organized in subfolders)
midi_folder = "maestro-v3.0.0"

# For example, process the first sampled performance
midi_filename = sample_df.iloc[0]['midi_filename']
midi_path = os.path.join(midi_folder, midi_filename)
print(f"\nLoading MIDI info for: {midi_path}")
midi_info = load_midi_info(midi_path)
print("\nMIDI File Information for the first sampled performance:")
print(midi_info)

# ---------------------------
# Part 3: MAESTRO Data Assessment
# ---------------------------
# For assessment, we use a subset of the metadata (e.g., title, composer, duration) and manually assign a quality score.
# The quality score is subjective; for instance, you might assess how complete or accurate the metadata appears.

maestro_sample_df = df.sample(n=10, random_state=42)[['canonical_title', 'canonical_composer', 'duration']].reset_index(drop=True)

# Manually assign quality scores (scale 0 to 10)
quality_scores = [8, 7, 9, 6, 8, 7, 8, 7, 8, 7]
maestro_sample_df['quality_score'] = quality_scores

print("\nMAESTRO Dataset Assessment:")
print(maestro_sample_df)
print("\nQuality Scores (0-10):")
print(maestro_sample_df[['canonical_title', 'quality_score']])
print("\nAverage Quality Score for the sampled MAESTRO dataset:")
print(maestro_sample_df['quality_score'].mean())
print("\nMAESTRO Dataset Quality Assessment Complete.")
