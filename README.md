# Clap Detection System

A small Python system that listens through your microphone, detects a clap, and triggers an action (e.g. opening an application) when one is heard.

Built as a learning project focused on understanding audio signal processing and basic system architecture — not just wiring together library calls.

## How it works

Instead of pitch-tracking (which is meant for tonal/periodic sounds like voice or music), this system detects a clap using two properties that actually define it:

- **Loudness** — measured via RMS (Root Mean Square) of each audio chunk.
- **Suddenness** — the *change* in RMS between consecutive chunks, so a sharp spike (clap) is distinguished from a gradual increase (e.g. turning up music).

```
prev_rms = 0
for each audio chunk:
    rms = sqrt(mean(chunk^2))
    jump = rms - prev_rms
    if jump > threshold:
        trigger()
    prev_rms = rms
```

## Architecture

The system is split into stages, each independently testable:

1. **Capture** — continuous audio stream from the microphone (`sounddevice.InputStream`)
2. **Feature extraction** — raw audio chunk → RMS value (pure function)
3. **Decision** — RMS jump vs. threshold → clap or not (pure function)
4. **Action** — dispatch to the configured application (`application_open.py`)

Keeping steps 2 and 3 as pure functions (no I/O, no side effects) means they can be tested against saved `.wav` samples without a live microphone.

## Setup

```bash
pip install sounddevice numpy
```

## Usage

```bash
python main.py
```

Clap near your microphone — the configured application will launch.

Set the target application path in `application_open.py`:

```python
path = r"C:\path\to\your\app.exe"
```

## Calibration

The detection `threshold` is not a magic number — it should be measured, not guessed. Run a quick script that prints RMS values while you clap and while the room is silent, then set the threshold between the two ranges with some margin. Values will vary by microphone and environment.

## Known limitations / next steps

- Single detection only — no cooldown period, so the loop currently exits after one trigger. Adding a cooldown window would allow continuous listening without double-triggering on the tail of a clap.
- Threshold is fixed rather than adaptive to ambient noise level.
- No spectral flatness check yet — adding one would help distinguish a clap (broadband/noisy) from other sudden loud sounds (e.g. a single tonal bang), reducing false positives.
- Config (target app, threshold, sample rate) is currently hardcoded — could move to a small config file for easier changes.

## What I learned

- Why pitch-tracking is the wrong tool for a transient, non-tonal sound like a clap.
- The difference between "loud" and "sudden," and why the latter is the actual signal that defines a clap.
- Sample rate and buffer size are tradeoffs, not arbitrary constants — they need to match the frequency content and time resolution of the sound you're detecting.
- Separating pure decision logic from I/O (capture, action) makes a system testable and easier to reason about as it grows.
- 
