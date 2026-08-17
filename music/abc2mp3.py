import argparse
import tempfile
from pathlib import Path

import lameenc
import music21
import numpy as np
import pretty_midi


def parse_abc_to_midi(abc_path: Path, temp_midi_path: Path) -> None:
    """Parses an ABC file and outputs a temporary MIDI stream."""
    score = music21.converter.parse(str(abc_path))
    if score is not None:
        score = score.makeMeasures()
        score.write("midi", fp=str(temp_midi_path))


def synthesize_midi_to_mp3(
    midi_path: Path,
    mp3_path: Path,
    sample_rate: int = 44100,
    bitrate: int = 192,
) -> None:
    """Synthesizes MIDI events to audio and encodes directly to MP3."""
    pm = pretty_midi.PrettyMIDI(str(midi_path))
    total_time = pm.get_end_time() + 1.5
    total_samples = int(total_time * sample_rate)
    audio = np.zeros(total_samples, dtype=np.float32)

    for instrument in pm.instruments:
        for note in instrument.notes:
            freq = pretty_midi.note_number_to_hz(note.pitch)
            start_sample = int(note.start * sample_rate)
            duration = note.end - note.start
            ring_out = 0.8
            total_duration = duration + ring_out
            num_samples = int(total_duration * sample_rate)

            t = np.linspace(0, total_duration, num_samples, endpoint=False)

            # Harmonic structure simulating piano timbres
            fundamental = np.sin(2 * np.pi * freq * t)
            h2 = 0.50 * np.sin(2 * np.pi * freq * 2 * t)
            h3 = 0.25 * np.sin(2 * np.pi * freq * 3 * t)
            h4 = 0.10 * np.sin(2 * np.pi * freq * 4 * t)
            tone = fundamental + h2 + h3 + h4

            # Percussive attack & decay envelope
            velocity_scale = note.velocity / 127.0
            envelope = np.exp(-3.5 * t / total_duration) * velocity_scale
            note_wave = tone * envelope

            end_sample = min(start_sample + num_samples, total_samples)
            actual_len = end_sample - start_sample
            audio[start_sample:end_sample] += note_wave[:actual_len]

    # Normalize audio peak
    if np.max(np.abs(audio)) > 0:
        audio = (audio / np.max(np.abs(audio))) * 0.9

    pcm_bytes = (audio * 32767).astype(np.int16).tobytes()

    # Encode directly to MP3
    encoder = lameenc.Encoder()
    encoder.set_bit_rate(bitrate)
    encoder.set_in_sample_rate(sample_rate)
    encoder.set_channels(1)
    encoder.set_quality(2)

    mp3_data = encoder.encode(pcm_bytes) + encoder.flush()
    mp3_path.write_bytes(mp3_data)


def main():
    parser = argparse.ArgumentParser(
        description="Convert an ABC notation file directly to an MP3 audio file."
    )
    parser.add_argument(
        "input",
        type=Path,
        help="Path to the input .abc file (e.g., inputs/piece_name.abc).",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        help="Optional explicit path for output MP3.",
    )

    args = parser.parse_args()
    input_path = args.input.resolve()

    if not input_path.exists():
        parser.error(f"Input file not found: {input_path}")

    # Set default output path to outputs/piece_name.mp3
    if args.output:
        output_path = args.output.resolve()
    else:
        output_dir = Path("outputs")
        output_path = output_dir / f"{input_path.stem}.mp3"

    # Ensure output directory exists
    output_path.parent.mkdir(parents=True, exist_ok=True)

    print(f"Converting '{input_path}' -> '{output_path}'...")

    # Process via temporary MIDI file
    with tempfile.NamedTemporaryFile(suffix=".mid", delete=False) as tmp:
        temp_midi_path = Path(tmp.name)

    try:
        parse_abc_to_midi(input_path, temp_midi_path)
        synthesize_midi_to_mp3(temp_midi_path, output_path)
        print(f"Done! Created: {output_path}")
    finally:
        if temp_midi_path.exists():
            temp_midi_path.unlink()


if __name__ == "__main__":
    main()
