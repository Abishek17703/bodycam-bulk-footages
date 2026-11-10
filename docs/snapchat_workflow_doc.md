# **Snapchat Video Production Automation**

### *Reference Analysis, Creative Direction & Workflow Plan*

## **01. Overview & Formats**

We are building a repeatable production workflow for vertical Snapchat content (9:16 aspect ratio).

Based on the reference links shared, there are two distinct Snapchat formats we need to support:

- **Format A: Snapchat Show / Highlight Episodes (3 - 5 minutes)**  -  Narrator-driven, multi-chapter storytelling episodes.
- **Format B: Snapchat Spotlight Clips (30 - 60 seconds)**  -  Fast-paced, raw viral clips with minimal narration and bold on-screen captions.

Both formats can be produced using the same core pipeline by switching the editing and subtitle configuration.

## **02. Reference Analysis**

We analysed both reference videos to break down what is happening in the video, how the story is structured and how the editing is handled.

### **Reference 1: Stay Curious (@staycurioustv)**

**Video Analysed:** One Hit Wonders, Where Are They Now?

**Duration & Format:** 4 minutes 35 seconds (9:16 vertical show episode).

**Context & Story Structure:**

- The video covers multiple subjects in a single episode (such as Gotye, Rebecca Black and Carly Rae Jepsen).
- Each subject is treated as a short mini-chapter lasting roughly 45 - 60 seconds.
- For each person, the narrator quickly covers their viral peak, what happened right after and what they are doing today.

**Visuals & Editing Style:**

- **Chapter Title Cards:** Every new subject is introduced with a darkened freeze-frame portrait and a large, bold cyan uppercase title right in the centre of the screen (for example, GOTYE or CARLY RAE JEPSEN).
- **Paper-Rip Transitions:** Uses a jagged white paper-tear wipe effect paired with a camera shutter sound when moving between chapters or archival clips.
- **Constant Motion & Pacing:** Cuts happen every 1.5 - 2.5 seconds across music videos, interviews and B-roll. Every static image or talking-head clip has a slow continuous zoom-in (100% to 112%) so the frame never feels static.
- **Subtitles:** Clean, small, single-line white sans-serif text with a thin black outline, placed in the lower-middle area (kept safely above Snapchat's bottom UI buttons), showing 3 - 5 words at a time.

**Audio Design:**

- Driven 100% by a fast, upbeat narrator voiceover.
- Original clip audio and background music are kept low underneath the voiceover, briefly ducking up only for 1 - 2 second punchlines.

### **Reference 2: The Fugitive (@t.fugitive)**

**Video Analysed:** Cop Just Wanted to Enjoy Some Ice Cream

**Duration & Format:** 41 seconds (9:16 vertical Spotlight clip).

**Context & Story Structure:**

- Shows a lighthearted interaction between a uniformed police officer (Officer A. Ramos) and a Turkish ice cream vendor playing the classic cone trick.
- There is no intro bumper or narrator setup. The video starts at 0.0 seconds right in the middle of the interaction.

**Visuals & Editing Style:**

- **Zero-Intro Hook:** Opens immediately on the action with short on-screen context labels (THIS COP / ICE CREAM MAN).
- **Jump-Cut Pacing:** All dead air and pauses longer than half a second are cut out to keep the interaction moving quickly.
- **Subtitles:** Large uppercase bold comic-style font placed near the centre of the screen with a thick black outline.
- **Speaker Colour-Coding:** Different colours are used to separate speakers (White for the vendor, Yellow and Green for the officer's reactions like WHAT IS THIS? and HAVE A GOOD NIGHT).

**Audio Design:**

- Uses the original real-life audio from the clip as the main track.
- Adds a very light background audio bed underneath to fill out the sound without overpowering the dialogue.

### **Reference Comparison**

| **Feature** | **Stay Curious (Show Format)** | **The Fugitive (Spotlight Format)** |
| :---: | :---: | :---: |
| Duration | 3 - 5 minutes | 30 - 60 seconds |
| Structure | Multi-chapter narrated compilation | Single continuous viral interaction |
| Opening Hook | Fast narrator question + title card | Immediate action at 0.0s with no intro |
| Transitions | Paper-rip wipes & shutter effects | Hard jump-cuts removing pauses |
| Subtitles | Small white lower-middle text (3 - 5 words) | Large centred uppercase text (Yellow / White) |
| Audio | Continuous voiceover + ducked B-roll | Original clip audio + subtle background bed |

## **03. Automated Production Workflow**

We can support both Snapchat styles using a clean, modular workflow.

### **Step 1  -  Source Selection & Context**

- For **Show Episodes**, the AI agent researches 4 - 5 related cases or subjects and builds a short fact sheet for each chapter.
- For **Spotlight Clips**, the AI agent scans raw bodycam or viral footage to find a self-contained 30 - 60 second interaction with a clear hook and payoff.

### **Step 2  -  Scripting & Trimming**

- **Show Format:** The AI agent writes a tight 450 - 650 word voiceover script broken into chapters, along with chapter title supers and B-roll cues.
- **Spotlight Format:** No narrator script is needed. The agent identifies exact timestamps from the raw video, trims out pauses and generates short hook labels.

### **Step 3  -  Voiceover & Audio**

- Generate fast-paced voiceover audio for Show episodes (using ElevenLabs or open-source voice models).
- For Spotlight clips, clean and normalise the original footage audio so dialogue is clear.

### **Step 4  -  Vertical Cropping & Visual Assembly**

- Convert horizontal 16:9 footage into 9:16 vertical format by tracking the active subject in the frame.
- Apply continuous slow zoom keyframes on static shots.
- Insert freeze-frame cyan chapter cards and paper-rip transitions for Show episodes.

### **Step 5  -  Subtitles & Safe Zones**

- Generate word-aligned timestamps from the audio track.
- Apply the respective preset (clean lower-middle white text for Shows, or centred colour-coded bold text for Spotlight).
- Keep all text and supers inside the central vertical safe zone so nothing is covered by Snapchat's top profile bar or bottom UI controls.

---

# **04. Overall Snapchat Pipeline**

| **SHOW FORMAT (3 - 5 MINS)** | **SPOTLIGHT FORMAT (30 - 60 SECS)** |
| :---: | :---: |
| 1. Topic & Multi-Subject Research | 1. Raw Footage Highlight Detection |
| 2. Chapter-Based Script & Supers | 2. Silence & Pause Trimming |
| 3. Fast-Paced Voiceover Generation | 3. Smart 9:16 Subject Cropping |
| 4. B-Roll Assembly & Slow Zooms | 4. Original Audio Cleanup |
| 5. Freeze-Frame Cyan Title Cards | 5. Speaker Colour-Coded Centred Captions |
| 6. Paper-Rip Transitions & Shutter SFX | 6. Safe-Zone Check & Export |
| 7. Lower-Middle Subtitles & Final Export |  |

---

## **Next Steps**

We will first build one sample for the **Show Format** and one sample for the **Spotlight Format** to lock in the fonts, subtitle placement, transitions and pacing.

Once approved, the same templates can be reused to produce daily Snapchat episodes and Spotlight clips automatically.
