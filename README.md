# Final 419 Project

**AI-Generated Piano Music: A Music-Theoretical Analysis and Model Comparison**

This repository accompanies a research project on the music-theoretical understanding of AI-generated piano music. It contains analysis tools for the **MAESTRO** (MIDI and Audio Edited for Synchronous Tracks and Organization) dataset, visualization scripts for MIDI files, and supporting materials for the written report.

---

## Research Context (from the PDF Report)

The project originally aimed to **train a neural network** (Google Magenta's Performance RNN or Music Transformer) on the MAESTRO dataset of piano performances and evaluate the outputs for musical coherence—testing whether AI compositions contain sensible chord progressions, key consistency, and cadences.

**Scope Pivot:** Due to technical difficulties configuring Magenta (dependency conflicts, Visual Studio Code setup), the project shifted to **analyzing outputs from existing AI music models** instead:

| Model | Domain | Evaluation Focus |
|-------|--------|------------------|
| **MuseNet** (OpenAI) | Symbolic (MIDI) | Classical piano, ~3 min pieces |
| **Bach Doodle** (Google/Coconet) | Symbolic | 4-part Bach chorale harmonization |
| **MusicLM** (Google) | Audio | Text-conditioned, ~30 s piano |

**Methods:** Qualitative listening combined with computational analysis via the `music21` library. The evaluation focused on:

- **Harmonic elements** — chord progressions, cadences, voice-leading
- **Key consistency** — modulations, tonal center stability
- **Melodic motifs** — motivic development, repetition, structure
- **Structural coherence** — long-term form vs. wandering

**Findings:** Models display rudimentary adherence to music theory. MuseNet maintains stable key and plausible chord progressions (e.g., ii–V–I) but often lacks long-term structure. Bach Doodle achieves near-perfect tonal harmony within its narrow chorale scope. MusicLM produces tonally consistent audio but without classical cadential formulas. The report also discusses **implicit theory learning**, **creativity and authorship**, **data feminism**, **fairness**, and **CARE principles** for Indigenous data governance.

See **`AI-Generated Piano Music_ A Music-Theoretical Analysis and Model Comparison.pdf`** for the full report.

---

## What’s in This Repo

### Python Scripts (Supporting Tools)

- **MAESTRO_graph.py** — Visualizes MIDI files as **pitch–time plots** (hexbin or KDE). Useful for inspecting human or AI-generated piano performances and comparing note density over time.
- **maestro_assessment.py** — Loads MAESTRO metadata, samples entries, extracts MIDI info (duration, instrument count), and assigns quality scores for dataset assessment.

### Other Files

- **`AI-Generated Piano Music_ A Music-Theoretical Analysis and Model Comparison.pdf`** — Full research report (James Nguyen, April 2025)
- **MuseNet improvisation audio** — mp3 examples (Chopin, Mozart, Rachmaninoff styles)
- **bachpiece.mid / bachpiece2.mid** — Sample MIDI files for testing visualization

---

## How the Code Works

### MAESTRO_graph.py (MIDI Visualization)

1. Parses MIDI with `mido`
2. Extracts `note_on` messages (ignoring note-off velocity 0)
3. Builds a DataFrame: `note` (pitch 0–127) vs. `time_elapsed` (cumulative ticks)
4. Plots as either:
   - **Jointplot (hexbin)** — density of notes in pitch–time space (default)
   - **KDE plot** — smoothed density surface
5. Y-axis: pitch (MIDI note numbers); X-axis: elapsed time. Good for seeing register, density, and phrase structure.

### maestro_assessment.py (Metadata & Quality)

1. Loads `maestro-v3.0.0.csv`
2. Randomly samples 10 rows
3. Uses `pretty_midi` to load MIDI files and get duration and instrument count
4. Assigns manual quality scores (0–10) to the sampled subset
5. Prints summary statistics and average quality

---

## Requirements

- Python 3.x
- Dependencies: `mido`, `pretty_midi`, `pandas`, `seaborn`, `matplotlib`

```bash
pip install mido pretty_midi pandas seaborn matplotlib
```

---

## Data Setup

1. Download the [MAESTRO Dataset v3.0.0](https://magenta.tensorflow.org/datasets/maestro)
2. Place in the project folder:
   - `maestro-v3.0.0/` — folder of MIDI files
   - `maestro-v3.0.0.csv` — metadata CSV

---

## Usage

### Visualize a MIDI File

```python
from MAESTRO_graph import MAESTRO_midi_graph

# Hexbin joint plot (default)
MAESTRO_midi_graph('bachpiece.mid', plot_type='jointplot')

# KDE density plot
MAESTRO_midi_graph('bachpiece.mid', plot_type='kdeplot')

# Save to file
MAESTRO_midi_graph('path/to/file.mid', plot_type='jointplot', save_path='output.png')
```

**Parameters:** `plot_type` ('jointplot' | 'kdeplot'), `axes_`, `palette`, `gridsize`, `figwidth`, `figheight`, `save_path`

### Run MAESTRO Assessment

```bash
python maestro_assessment.py
```

---

## Project Structure

```
final_419_project/
├── MAESTRO_graph.py       # MIDI pitch–time visualization
├── maestro_assessment.py  # MAESTRO metadata & quality assessment
├── maestro-v3.0.0.csv     # MAESTRO metadata (download separately)
├── maestro-v3.0.0/        # MAESTRO MIDI files (download separately)
├── AI-Generated Piano Music_ A Music-Theoretical Analysis and Model Comparison.pdf
├── MuseNet improvises *.mp3  # AI-generated audio examples
├── bachpiece.mid, bachpiece2.mid  # Sample MIDI
└── README.md
```

---

## License & Ethics

See the MAESTRO dataset terms for data usage. Project code is for educational purposes (419 course). The report discusses ethical considerations around AI music generation, data governance, and fairness.
