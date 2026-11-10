# **Bodycam Video Production Automation**

### *Workflow, Creative Direction & Implementation Plan*

## **01. Existing Setup  -  Google Drive**

We already have the basic case folder structure in Google Drive.

Each case folder contains the available information and assets for that particular case:

- Bodycam footage
- Police reports
- Law enforcement documentation (LP documentation)
- Case summaries
- Other supporting documents and references

We will be using this existing structure rather than creating an entirely new storage system.

A separate **Scripts** folder will also be maintained for generated scripts and related documents.

## **02. Case Research & Context Building**

Before generating the script, the AI agent needs to understand the complete case.

**What the AI agent will do:**

- Analyse all the documents available inside the case folder.
- Analyse the available bodycam footage and understand the events.
- Search Google for additional information about the case.
- Look for existing news coverage, articles and YouTube videos related to the case.
- Collect additional information that helps understand the background, people involved and sequence of events.
- Cross-reference the information gathered from different sources.

The idea is to give the AI agent as much context as possible before it starts writing anything.

### **Single Source of Truth**

Once the research is complete, the AI agent will create a consolidated case document.

This document will contain:

- Complete case background and summary.
- Important facts, dates, names and locations.
- Sequence of events.
- Relevant information extracted from the footage.
- Important details from police reports.
- Additional information gathered online.
- Source links to news articles, reports and other references.
- Any conflicting or unverified information.

This document will act as the **Single Source of Truth (SSOT)** for that particular case and will also be saved in Google Drive.

The reason for doing this is to prevent AI hallucinations.

One of the biggest issues with AI-generated crime storytelling is that it tends to prioritise an engaging narrative, sometimes at the expense of factual accuracy.

By creating a consolidated reference document first, we can make sure the scripting agent works within the available facts rather than inventing details to make the story more interesting.

Any conflicting information will be flagged for manual review.

## **03. Script Generation**

Once the context document is ready, the AI agent moves to the scripting stage.

The objective is to turn the available information into an engaging crime documentary rather than simply narrating what happened in chronological order.

### **Storytelling Direction**

The script should be:

- Dramatic and attention-grabbing.
- Factual, without fabricating information.
- Natural and human-sounding, not like generic AI narration.
- Structured to maintain viewer interest throughout the video.
- Suitable for long-form YouTube content.

### **Non-linear Storytelling**

Instead of following a simple chronological structure:

Event 1 → Event 2 → Event 3 → Event 4

We can experiment with non-linear storytelling.

For example:

- Start with one of the most interesting moments from the case.
- Introduce a question or an important development.
- Go back to the earlier events to explain how things started.
- Gradually build towards the main incident.
- Bring the story back to the present timeline.

This gives us more flexibility to create curiosity and maintain attention.

The objective is to make the existing information more interesting through storytelling, word choice and narrative structure, without changing the actual facts.

### **Footage-Aware Scripting**

An important part of this stage is that the AI agent should already know what footage is available.

The script should be written based on the actual footage and supporting information, not generated independently.

For example:

- If a particular conversation is available, the script can lead into that footage.
- If a news article provides additional context, we can use a screenshot or reference to it.
- If a particular event has no supporting footage, the script should account for that limitation.
- Important dialogue can be retained instead of unnecessarily repeating it through voiceover.

This will help us create an engaging video without writing a script that cannot actually be produced using the available assets.

### **Script Output**

The generated script will be divided into two separate components:

**A. Voiceover (VO)**

The complete narration that will be converted into audio.

**B. Supers**

Supers are the text elements that appear on the video apart from regular subtitles.

Examples:

- Chapter 01 / Chapter 02.
- Date and location information.
- Names and relevant identification details.
- Important statements or dialogue highlights.
- Supporting facts and information.
- Other important contextual details.

The VO and supers will be separately identified in the script so that the editing process can handle both.

## **04. Voiceover Generation**

We have two possible approaches for generating the voiceover.

### **Option A: ElevenLabs**

- Integrate ElevenLabs through its API.
- Use Eleven v4 for expressive and natural-sounding narration.
- Finalise a consistent voice for the channel.

**Advantages:**

- High-quality voice generation.
- Good emotional expression.
- More natural delivery, especially for dramatic storytelling.

**Limitations:**

- Credit limitations.
- Regenerating entire voiceovers can become expensive.
- Usage costs need to be considered.

### **Option B: Open-source Models**

Explore open-source voice generation models that can produce quality close to ElevenLabs.

**Advantages:**

- No dependency on a recurring voice generation subscription.
- More control over usage.
- Can be hosted and run independently.
- Potentially lower costs at higher volumes.

**Limitations:**

- Requires computational resources.
- Initial setup and testing.
- Voice quality and emotional expression need to be evaluated.

I can share a few open-source model references that we can test.

**Decision:** We will test both approaches, compare the output quality and costs, finalise a voice and use it consistently across the channel.

## **05. Subtitles & Styling**

Once the voiceover is generated, subtitles will be created using the final voiceover audio.

**Process:**

- Match the voiceover with the approved script.
- Generate word-level or phrase-level timestamps.
- Synchronise subtitles with the audio.
- Apply the final subtitle style.
- Add emphasis to important words where required.

We will need to finalise the subtitle design separately.

The idea is to have a consistent subtitle style that can be reused across videos.

## **06. Sound Effects & Audio Design**

We will create a collection of high-quality sound effects that can be reused across videos.

Some examples:

- Cinematic booms.
- Whooshes and transitions.
- Camera capture sounds.
- Impact sounds.
- Subtle tension-building effects.

I can share a collection of SFX for approval. Once finalised, these can be reused across the editing workflow.

### **Background Music**

I don't think background music will work particularly well for this type of content.

Most established bodycam channels rely primarily on original footage audio, narration and sound effects rather than background music.

Adding music could actually take away from the seriousness and realism of the incidents, especially when the footage itself is intense.

I'd suggest keeping the videos music-free by default and using sound effects selectively wherever they add value.

## **07. Video Assembly & Editing**

Once the individual components are ready, they will be stitched together into the final video timeline.

This includes:

- Original bodycam footage.
- AI-generated voiceover.
- Original dialogue and audio.
- Subtitles.
- Supers.
- Sound effects.
- Transitions and motion graphics.

The editing will follow a predefined structure, with the AI agent selecting and arranging footage based on the approved script and timestamps.

### **Look & Feel**

We will need to finalise the overall visual style based on the channel's branding.

This includes:

- Channel colours.
- Fonts and typography.
- Subtitle styling.
- Chapter title styling.
- Lower thirds and supers.
- Motion graphics.
- Sound effects and transitions.

The advantage here is that bodycam videos are primarily footage-driven.

There isn't a huge requirement for complex typography or motion graphics throughout the video.

We can create a reusable editing template and establish the look and feel of each individual element once.

After that, the same system can be reused across cases without making every video look overly templated.

The focus should remain on the actual footage and storytelling.

## **08. Reference Channels & Editing Styles**

We have analysed four established channels in the bodycam and crime documentary space to understand how they structure their hooks, visuals, subtitles and pacing.

### **A. Dr Insanity (@DrInsanityCrime)**

**Format:** Long-form crime documentaries (35 - 55 minutes).

**Hook & Structure:**

- Starts with a 15 - 30 second cold open using the most tense exchange from the bodycam or interrogation room.
- Immediately follows with a narrator setup explaining what detectives are trying to uncover.

**Visuals & Editing Style:**

- Uses a dark blue and black particle wave background when playing 911 calls or audio recordings, with a clean audio waveform box in the centre.
- Displays floating evidence cards on screen, such as missing person posters, detective ID cards and family photos.
- Uses clean teal lower-third boxes for subject names and ages, and bottom-left tags for dates and locations.
- Subtitles are placed inside a solid black rectangular box at the bottom in white or cyan text.

### **B. Code Blue Cam (@CodeBlueCam)**

**Format:** Mid-form bodycam videos (15 - 25 minutes) and vertical Shorts (30 - 60 seconds).

**Hook & Structure:**

- Opens with 2 - 3 fast action clips from the incident (such as a foot chase or taser deployment).
- Transitions into a 3D satellite map fly-in with red and blue radar dots showing where the pursuit or incident took place.

**Visuals & Editing Style:**

- Uses tactical red tracking boxes and circular spotlight highlights that dim the surrounding frame to point out distant suspects or vehicles.
- Displays the officer's name in the top-left corner so the viewer knows whose camera perspective is playing.
- Subtitles sit inside a semi-transparent black pill box and are colour-coded by speaker (White for officers, Red or Yellow for suspects, Cyan for dispatch).
- For Shorts, the footage is centre-cropped into 9:16 vertical over a blurred background fill, with brief narrator context leading into the raw interaction.

### **C. Midwest Safety (@MidwestSafety)**

**Format:** Mid-form bodycam videos (18 - 35 minutes) and high-retention Shorts (15 - 45 seconds).

**Hook & Structure:**

- Skips the raw cold open and starts immediately at 0:00 with the narrator explaining the exact action happening on screen.
- Pairs the opening narration with an animated red arrow and a bold uppercase label pointing directly at the subject or vehicle.

**Visuals & Editing Style:**

- Uses a clean blue pill tag in the top-left corner (such as Officer #1) and a location pin tag when switching scenes.
- Subtitles use a dark box with two-tone keyword highlighting, keeping standard words in white and highlighting key action words in bold red.
- For Shorts, a permanent red banner headline stays pinned in the top third of the screen throughout the entire clip so viewers immediately understand the context.

### **D. Red File (@redfilechannel)**

**Format:** Long-form psychological interrogation and bodycam breakdowns (25 - 48 minutes).

**Hook & Structure:**

- Uses a contradiction hook in the first 30 - 45 seconds.
- Plays the suspect's initial 911 call or excuse first, and then the narrator immediately reveals how phone records or forensic evidence contradict what they just said.

**Visuals & Editing Style:**

- Uses a dark 3D wireframe building or crime-scene background during 911 calls, placing caller and dispatcher portraits on either side of a live glowing waveform.
- Places floating transcript text directly above the audio waveform during phone calls, and switches to black-box subtitles during interrogation and bodycam scenes.
- Uses red circular callouts to highlight small physical details on bodycam, such as a weapon or holster.

### **Comparison Summary**

| **Channel** | **Format** | **Opening Hook** | **Visual Elements** | **Subtitle Style** |
| :---: | :---: | :---: | :---: | :---: |
| Dr Insanity | Long-form (35 - 55m) | Tense 15 - 30s exchange followed by narrator setup | Dark waveform canvas, floating evidence cards, teal lower thirds | White / cyan text in solid black box |
| Code Blue Cam | Mid-form (15 - 25m) & Shorts | Fast action montage into 3D satellite map fly-in | Red tracking boxes, circular spotlight dimmers, officer camera tags | Speaker colour-coded text in dark pill box |
| Midwest Safety | Mid-form (18 - 35m) & Shorts | Immediate narrator hook at 0:00 with red arrow callout | Blue officer tags, location pins, permanent top red banner on Shorts | White text with bold red action keywords |
| Red File | Long-form (25 - 48m) | Suspect's excuse contrasted with contradicting evidence | 3D crime scene background, split caller-dispatcher waveform, red circle callouts | Floating text over waveform & black-box captions |

We can combine the strongest elements from these references when finalising our own channel templates for both long-form videos and vertical Shorts.

## **09. Thumbnail Generation**

Once the video is ready, the AI agent will generate thumbnail variations.

**Process:**

- Analyse the case and identify the most interesting visual moments.
- Select suitable frames from the available footage.
- Generate three thumbnail variations.
- Apply the channel's established visual style.
- Save the variations to Google Drive.
- Share them for selection and approval.

We will also finalise a reusable thumbnail style based on the channel's branding.

For image generation, we can explore both paid APIs and locally hosted open-source models, depending on output quality and processing costs.

## **10. YouTube Upload & Publishing**

Once the video and thumbnail are approved, we can integrate the YouTube Data API.

**Process:**

- Upload the final video to YouTube.
- Add the title and description.
- Add the selected thumbnail.
- Set visibility to Private or Unlisted.
- Share the uploaded video with the client for review.
- Client can log into YouTube and publish the video manually.

The YouTube Data API supports video uploads and metadata management. Upload quotas and account restrictions will need to be considered during implementation.

### **Other Platforms**

We can also explore publishing to Instagram, Facebook, TikTok and X.

Each platform has its own API and publishing requirements.

Alternatively, we can use a third-party publishing platform that integrates multiple social media APIs, although this would involve an additional subscription.

For now, YouTube will be our primary focus.

## **11. Scalability & Customisation**

Although we are initially building this for one channel, we should keep multiple channels and clients in mind from the beginning.

The system should allow us to customise:

- Channel colours and fonts.
- Subtitle styles.
- Voiceover selection.
- Sound effects and audio presets.
- Motion graphics and supers.
- Thumbnail styles.
- Editing templates.

The idea is to build a common backend and allow individual channel-specific settings.

Once the first channel's look and feel are finalised, we can use the same system for other channels by changing the respective configurations rather than rebuilding the entire workflow.

The initial target is to establish a reliable system that can eventually support 5 - 10 channels or more.

---

# **12. Testing & Feedback Process**

Initially, everything will go through manual review. I will personally review the generated outputs and share individual components for approval.

We can follow this process:

**Step 1  -  Individual Component Approval**

I will generate and share samples of:

- Case context document.
- Script.
- Voiceover.
- Subtitle style.
- Sound effects.
- Motion graphics and supers.
- Thumbnail style.

We can finalise each element individually before building the complete video.

**Step 2  -  First Case Video**

Once the individual styles are approved, we will build the first complete video.

The client can review the video and share feedback on storytelling, pacing, voiceover, editing and overall presentation.

**Step 3  -  Second Case Video**

Based on the feedback from the first video, we will make improvements and generate the second video.

We can identify anything that needs further refinement.

**Step 4  -  Third Case Video**

The third video will incorporate the additional feedback from the second video.

At this stage, we should be able to finalise most of the workflow, editing style and output quality.

**Step 5  -  Finalise & Scale**

Once the workflow is stable, we can reduce manual intervention and move towards a more automated production process.

---

# **13. Cost Considerations**

The final operating cost will depend on the models and processing methods we choose.

| **Component** | **Options to Evaluate** | **Cost** |
| :---: | :---: | :---: |
| AI Research & Scripting | LLM APIs / Open-source models | TBD |
| Transcription & Analysis | Speech-to-text / AI APIs | TBD |
| Voiceover | ElevenLabs / Open-source models | TBD |
| Video Processing | Local / Cloud processing | TBD |
| Subtitle Generation | Speech alignment tools | TBD |
| Thumbnail Image Generation | Image generation APIs / Open-source models | TBD |
| Storage & Infrastructure | Google Drive / Cloud | TBD |
| Publishing | YouTube Data API | TBD |

We will compare the available options and finalise the costs after testing.

The priority is to keep recurring costs as low as possible without compromising the output quality.

---

# **14. Overall Workflow**

| **CASE RESEARCH & SCRIPTING** | **VIDEO PRODUCTION & PUBLISHING** |
| :---: | :---: |
| 1. Existing Google Drive Case Folder | 1. Voiceover Generation |
| 2. AI Research & Case Analysis | 2. Supers & Subtitle Generation |
| 3. Single Source of Truth Document | 3. Sound Effects & Audio Design |
| 4. AI Script Generation | 4. Automated Video Assembly |
| 5. Client Script Approval | 5. Thumbnail Generation |
|  | 6. Final Video Review |
|  | 7. YouTube Private / Unlisted Upload |
|  | 8. Client Reviews & Publishes |

---

## **Final Approach**

The initial focus is to get the quality right rather than immediately trying to automate everything.

We will first establish the storytelling style, voice, subtitles, sound design and overall look and feel.

Once these individual elements are finalised, we can build the complete workflow and test it across three case videos.

The feedback from each video will help improve the next one.

Once the output is consistent, we can automate more of the process and scale the same system across multiple channels.
