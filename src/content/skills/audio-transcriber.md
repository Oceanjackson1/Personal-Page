---
title: "Audio Transcriber"
description: "Transform audio recordings into professional Markdown documentation with intelligent summaries using LLM integration"
category: "research"
source: "community"
author: "Community"
tags: ["audio", "transcriber"]
date: 2026-03-20
---

## Purpose

This skill automates audio-to-text transcription with professional Markdown output, extracting rich technical metadata (speakers, timestamps, language, file size, duration) and generating structured meeting minutes and executive summaries. It uses Faster-Whisper or Whisper with zero configuration, working universally across projects without hardcoded paths or API keys.

Inspired by tools like Plaud, this skill transforms raw audio recordings into actionable documentation, making it ideal for meetings, interviews, lectures, and content analysis.

## When to Use

Invoke this skill when:

- User needs to transcribe audio/video files to text
- User wants meeting minutes automatically generated from recordings
- User requires speaker identification (diarization) in conversations
- User needs subtitles/captions (SRT, VTT formats)
- User wants executive summaries of long audio content
- User asks variations of "transcribe this audio", "convert audio to text", "generate meeting notes from recording"
- User has audio files in common formats (MP3, WAV, M4A, OGG, FLAC, WEBM)

## Workflow

### Step 0: Discovery (Auto-detect Transcription Tools)

**Objective:** Identify available transcription engines without user configuration.

**Actions:**

Run detection commands to find installed tools:

```bash
# Check for Faster-Whisper (preferred - 4-5x faster)
if python3 -c "import faster_whisper" 2>/dev/null; then
    TRANSCRIBER="faster-whisper"
    echo "✅ Faster-Whisper detected (optimized)"
# Fallback to original Whisper
elif python3 -c "import whisper" 2>/dev/null; then
    TRANSCRIBER="whisper"
    echo "✅ OpenAI Whisper detected"
else
    TRANSCRIBER="none"
    echo "⚠️  No transcription tool found"
fi

# Check for ffmpeg (audio format conversion)
if command -v ffmpeg &>/dev/null; then
    echo "✅ ffmpeg available (format conversion enabled)"
else
    echo "ℹ️  ffmpeg not found (limited format support)"
fi
```

**If no transcriber found:**

Offer automatic installation using the provided script:

```bash
echo "⚠️  No transcription tool found"
echo ""
echo "🔧 Auto-install dependencies? (Recommended)"
read -p "Run installation script? [Y/n]: " AUTO_INSTALL

if [[ ! "$AUTO_INSTALL" =~ ^[Nn] ]]; then
    # Get skill directory (works for both repo and symlinked installations)
    SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    
    # Run installation script
    if [[ -f "$SKILL_DIR/scripts/install-requirements.sh" ]]; then
        bash "$SKILL_DIR/scripts/install-requirements.sh"
    else
        echo "❌ Installation script not found"
        echo ""
        echo "📦 Manual installation:"
        echo "  pip install faster-whisper  # Recommended"
        echo "  pip install openai-whisper  # Alternative"
        echo "  brew install ffmpeg         # Optional (macOS)"
        exit 1
    fi
    
    # Verify installation succeeded
    if python3 -c "import faster_whisper" 2>/dev/null || python3 -c "import whisper" 2>/dev/null; then
        echo "✅ Installation successful! Proceeding with transcription..."
    else
        echo "❌ Installation failed. Please install manually."
        exit 1
    fi
else
    echo ""
    echo "📦 Manual installation required:"
    echo ""
    echo "Recommended (fastest):"
    echo "  pip install faster-whisper"
    echo ""
    echo "Alternative (original):"
    echo "  pip install openai-whisper"
    echo ""
    echo "Optional (format conversion):"
    echo "  brew install ffmpeg  # macOS"
    echo "  apt install ffmpeg   # Linux"
    echo ""
    exit 1
fi
```

This ensures users can install dependencies with one confirmation, or opt for manual installation if preferred.

**If transcriber found:**

Proceed to Step 0b (CLI Detection).


### Step 1: Validate Audio File

**Objective:** Verify file exists, check format, and extract metadata.

**Actions:**

1. **Accept file path or URL** from user:
   - Local file: `meeting.mp3`
   - URL: `https://example.com/audio.mp3` (download to temp directory)

2. **Verify file exists:**

```bash
if [[ ! -f "$AUDIO_FILE" ]]; then
    echo "❌ File not found: $AUDIO_FILE"
    exit 1
fi
```

3. **Extract metadata** using ffprobe or file utilities:

```bash
# Get file size
FILE_SIZE=$(du -h "$AUDIO_FILE" | cut -f1)

# Get duration and format using ffprobe
DURATION=$(ffprobe -v error -show_entries format=duration \
    -of default=noprint_wrappers=1:nokey=1 "$AUDIO_FILE" 2>/dev/null)
FORMAT=$(ffprobe -v error -select_streams a:0 -show_entries \
    stream=codec_name -of default=noprint_wrappers=1:nokey=1 "$AUDIO_FILE" 2>/dev/null)

# Convert duration to HH:MM:SS
DURATION_HMS=$(date -u -r "$DURATION" +%H:%M:%S 2>/dev/null || echo "Unknown")
```

4. **Check file size** (warn if large for cloud APIs):

```bash
SIZE_MB=$(du -m "$AUDIO_FILE" | cut -f1)
if [[ $SIZE_MB -gt 25 ]]; then
    echo "⚠️  Large file ($FILE_SIZE) - processing may take several minutes"
fi
```

5. **Validate format** (supported: MP3, WAV, M4A, OGG, FLAC, WEBM):

```bash
EXTENSION="${AUDIO_FILE##*.}"
SUPPORTED_FORMATS=("mp3" "wav" "m4a" "ogg" "flac" "webm" "mp4")

if [[ ! " ${SUPPORTED_FORMATS[@]} " =~ " ${EXTENSION,,} " ]]; then
    echo "⚠️  Unsupported format: $EXTENSION"
    if command -v ffmpeg &>/dev/null; then
        echo "🔄 Converting to WAV..."
        ffmpeg -i "$AUDIO_FILE" -ar 16000 "${AUDIO_FILE%.*}.wav" -y
        AUDIO_FILE="${AUDIO_FILE%.*}.wav"
    else
        echo "❌ Install ffmpeg to convert formats: brew install ffmpeg"
        exit 1
    fi
fi
```


### Step 3: Generate Markdown Output

**Objective:** Create structured Markdown with metadata, transcription, meeting minutes, and summary.

**Output Template:**

```markdown
# Audio Transcription Report

## 📊 Metadata

| Field | Value |
|-------|-------|
| **File Name** | {filename} |
| **File Size** | {file_size} |
| **Duration** | {duration_hms} |
| **Language** | {language} ({language_code}) |
| **Processed Date** | {process_date} |
| **Speakers Identified** | {num_speakers} |
| **Transcription Engine** | {engine} (model: {model}) |


## 📋 Meeting Minutes

### Participants
- {speaker_1}
- {speaker_2}
- ...

### Topics Discussed
1. **{topic_1}** ({timestamp})
   - {key_point_1}
   - {key_point_2}

2. **{topic_2}** ({timestamp})
   - {key_point_1}

### Decisions Made
- ✅ {decision_1}
- ✅ {decision_2}

### Action Items
- [ ] **{action_1}** - Assigned to: {speaker} - Due: {date_if_mentioned}
- [ ] **{action_2}** - Assigned to: {speaker}


*Generated by audio-transcriber skill v1.0.0*  
*Transcription engine: {engine} | Processing time: {elapsed_time}s*
```

**Implementation:**

Use Python or bash with AI model (Claude/GPT) for intelligent summarization:

```python
def generate_meeting_minutes(segments):
    """Extract topics, decisions, action items from transcription."""
    
    # Group segments by topic (simple clustering by timestamps)
    topics = cluster_by_topic(segments)
    
    # Identify action items (keywords: "should", "will", "need to", "action")
    action_items = extract_action_items(segments)
    
    # Identify decisions (keywords: "decided", "agreed", "approved")
    decisions = extract_decisions(segments)
    
    return {
        "topics": topics,
        "decisions": decisions,
        "action_items": action_items
    }

def generate_summary(segments, max_paragraphs=5):
    """Create executive summary using AI (Claude/GPT via API or local model)."""
    
    full_text = " ".join([s["text"] for s in segments])
    
    # Use Chain of Density approach (from prompt-engineer frameworks)
    summary_prompt = f"""
    Summarize the following transcription in {max_paragraphs} concise paragraphs.
    Focus on key topics, decisions, and action items.
    
    Transcription:
    {full_text}
    """
    
    # Call AI model (placeholder - user can integrate Claude API or use local model)
    summary = call_ai_model(summary_prompt)
    
    return summary
```

**Output file naming:**

```bash
# v1.1.0: Use timestamp para evitar sobrescrever
TIMESTAMP=$(date +%Y%m%d-%H%M%S)
TRANSCRIPT_FILE="transcript-${TIMESTAMP}.md"
ATA_FILE="ata-${TIMESTAMP}.md"

echo "$TRANSCRIPT_CONTENT" > "$TRANSCRIPT_FILE"
echo "✅ Transcript salvo: $TRANSCRIPT_FILE"

if [[ -n "$ATA_CONTENT" ]]; then
    echo "$ATA_CONTENT" > "$ATA_FILE"
    echo "✅ Ata salva: $ATA_FILE"
fi
```


#### **SCENARIO A: User Provided Custom Prompt**

**Workflow:**

1. **Display user's prompt:**
   ```
   📝 Prompt fornecido pelo usuário:
   ┌──────────────────────────────────┐
   │ [User's prompt preview]          │
   └──────────────────────────────────┘
   ```

2. **Automatically improve with prompt-engineer (if available):**
   ```bash
   🔧 Melhorando prompt com prompt-engineer...
   [Invokes: gh copilot -p "melhore este prompt: {user_prompt}"]
   ```

3. **Show both versions:**
   ```
   ✨ Versão melhorada:
   ┌──────────────────────────────────┐
   │ Role: Você é um documentador...  │
   │ Instructions: Transforme...      │
   │ Steps: 1) ... 2) ...             │
   │ End Goal: ...                    │
   └──────────────────────────────────┘

   📝 Versão original:
   ┌──────────────────────────────────┐
   │ [User's original prompt]         │
   └──────────────────────────────────┘
   ```

4. **Ask which to use:**
   ```bash
   💡 Usar versão melhorada? [s/n] (default: s):
   ```

5. **Process with selected prompt:**
   - If "s": use improved
   - If "n": use original


#### **LLM Processing (Both Scenarios)**

Once prompt is finalized:

```python
from rich.progress import Progress, SpinnerColumn, TextColumn

def process_with_llm(transcript, prompt, cli_tool='claude'):
    full_prompt = f"{prompt}\n\n---\n\nTranscrição:\n\n{transcript}"
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True
    ) as progress:
        progress.add_task(
            description=f"🤖 Processando com {cli_tool}...",
            total=None
        )
        
        if cli_tool == 'claude':
            result = subprocess.run(
                ['claude', '-'],
                input=full_prompt,
                capture_output=True,
                text=True,
                timeout=300  # 5 minutes
            )
        elif cli_tool == 'gh-copilot':
            result = subprocess.run(
                ['gh', 'copilot', 'suggest', '-t', 'shell', full_prompt],
                capture_output=True,
                text=True,
                timeout=300
            )
    
    if result.returncode == 0:
        return result.stdout.strip()
    else:
        return None
```

**Progress output:**
```
🤖 Processando com claude... ⠋
[After completion:]
✅ Ata gerada com sucesso!
```


#### **Final Output**

**Success (both files):**
```bash
💾 Salvando arquivos...

✅ Arquivos criados:
  - transcript-20260203-023045.md  (transcript puro)
  - ata-20260203-023045.md         (processado com LLM)

🧹 Removidos arquivos temporários: metadata.json, transcription.json

✅ Concluído! Tempo total: 3m 45s
```

**Transcript only (user declined LLM):**
```bash
💾 Salvando arquivos...

✅ Arquivo criado:
  - transcript-20260203-023045.md

ℹ️  Ata não gerada (processamento LLM recusado pelo usuário)

🧹 Removidos arquivos temporários: metadata.json, transcription.json

✅ Concluído!
```


### Step 5: Display Results Summary

**Objective:** Show completion status and next steps.

**Output:**

```bash
echo ""
echo "✅ Transcription Complete!"
echo ""
echo "📊 Results:"
echo "  File: $OUTPUT_FILE"
echo "  Language: $LANGUAGE"
echo "  Duration: $DURATION_HMS"
echo "  Speakers: $NUM_SPEAKERS"
echo "  Words: $WORD_COUNT"
echo "  Processing time: ${ELAPSED_TIME}s"
echo ""
echo "📝 Generated:"
echo "  - $OUTPUT_FILE (Markdown report)"
[if alternative formats:]
echo "  - ${OUTPUT_FILE%.*}.srt (Subtitles)"
echo "  - ${OUTPUT_FILE%.*}.json (Structured data)"
echo ""
echo "🎯 Next steps:"
echo "  1. Review meeting minutes and action items"
echo "  2. Share report with participants"
echo "  3. Track action items to completion"
```


## Example Usage

### **Example 1: Basic Transcription**

**User Input:**
```bash
copilot> transcribe audio to markdown: meeting-2026-02-02.mp3
```

**Skill Output:**

```bash
✅ Faster-Whisper detected (optimized)
✅ ffmpeg available (format conversion enabled)

📂 File: meeting-2026-02-02.mp3
📊 Size: 12.3 MB
⏱️  Duration: 00:45:32

🎙️  Processing...
[████████████████████] 100%

✅ Language detected: Portuguese (pt-BR)
👥 Speakers identified: 4
📝 Generating Markdown output...

✅ Transcription Complete!

📊 Results:
  File: meeting-2026-02-02.md
  Language: pt-BR
  Duration: 00:45:32
  Speakers: 4
  Words: 6,842
  Processing time: 127s

📝 Generated:
  - meeting-2026-02-02.md (Markdown report)

🎯 Next steps:
  1. Review meeting minutes and action items
  2. Share report with participants
  3. Track action items to completion
```


### **Example 3: Batch Processing**

**User Input:**
```bash
copilot> transcreva estes áudios: recordings/*.mp3
```

**Skill Output:**

```bash
📦 Batch mode: 5 files found
  1. team-standup.mp3
  2. client-call.mp3
  3. brainstorm-session.mp3
  4. product-demo.mp3
  5. retrospective.mp3

🎙️  Processing batch...

[1/5] team-standup.mp3 ✅ (2m 34s)
[2/5] client-call.mp3 ✅ (15m 12s)
[3/5] brainstorm-session.mp3 ✅ (8m 47s)
[4/5] product-demo.mp3 ✅ (22m 03s)
[5/5] retrospective.mp3 ✅ (11m 28s)

✅ Batch Complete!
📝 Generated 5 Markdown reports
⏱️  Total processing time: 6m 15s
```


### **Example 5: Large File Warning**

**User Input:**
```bash
copilot> transcribe audio to markdown: conference-keynote.mp3
```

**Skill Output:**

```bash
✅ Faster-Whisper detected (optimized)

📂 File: conference-keynote.mp3
📊 Size: 87.2 MB
⏱️  Duration: 02:15:47
⚠️  Large file (87.2 MB) - processing may take several minutes

Continue? [Y/n]:
```

**User:** `Y`

```bash
🎙️  Processing... (this may take 10-15 minutes)
[████░░░░░░░░░░░░░░░░] 20% - Estimated time remaining: 12m
```


This skill is **platform-agnostic** and works in any terminal context where GitHub Copilot CLI is available. It does not depend on specific project configurations or external APIs, following the zero-configuration philosophy.

---

## Reference: Tools Comparison

# Transcription Tools Comparison

Comprehensive comparison of audio transcription engines supported by the audio-transcriber skill.

## Overview

| Tool | Type | Speed | Quality | Cost | Privacy | Offline | Languages |
|------|------|-------|---------|------|---------|---------|-----------|
| **Faster-Whisper** | Open-source | ⚡⚡⚡⚡⚡ | ⭐⭐⭐⭐⭐ | Free | 100% | ✅ | 99 |
| **Whisper** | Open-source | ⚡⚡⚡ | ⭐⭐⭐⭐⭐ | Free | 100% | ✅ | 99 |
| Google Speech-to-Text | Commercial API | ⚡⚡⚡⚡ | ⭐⭐⭐⭐⭐ | $0.006/15s | Partial | ❌ | 125+ |
| Azure Speech | Commercial API | ⚡⚡⚡⚡ | ⭐⭐⭐⭐ | $1/hour | Partial | ❌ | 100+ |
| AssemblyAI | Commercial API | ⚡⚡⚡⚡ | ⭐⭐⭐⭐⭐ | $0.00025/s | Partial | ❌ | 99 |

---

## Faster-Whisper (Recommended)

### Pros
✅ **4-5x faster** than original Whisper  
✅ **Same quality** as original Whisper  
✅ **Lower memory usage** (50-60% less RAM)  
✅ **Free and open-source**  
✅ **100% offline** (privacy guaranteed)  
✅ **Easy installation** (`pip install faster-whisper`)  
✅ **Drop-in replacement** for Whisper

### Cons
❌ Requires Python 3.8+  
❌ Initial model download (~100MB-1.5GB)  
❌ GPU optional but speeds up significantly

### Installation

```bash
pip install faster-whisper
```

### Usage Example

```python
from faster_whisper import WhisperModel

# Load model (auto-downloads on first run)
model = WhisperModel("base", device="cpu", compute_type="int8")

# Transcribe
segments, info = model.transcribe("audio.mp3", language="pt")

# Print results
for segment in segments:
    print(f"[{segment.start:.2f}s -> {segment.end:.2f}s] {segment.text}")
```

### Model Sizes

| Model | Size | RAM | Speed (CPU) | Quality |
|-------|------|-----|-------------|---------|
| `tiny` | 39 MB | ~1 GB | Very fast (~10x realtime) | Basic |
| `base` | 74 MB | ~1 GB | Fast (~7x realtime) | Good |
| `small` | 244 MB | ~2 GB | Moderate (~4x realtime) | Very good |
| `medium` | 769 MB | ~5 GB | Slow (~2x realtime) | Excellent |
| `large` | 1550 MB | ~10 GB | Very slow (~1x realtime) | Best |

**Recommendation:** `small` or `medium` for production use.

---

## Whisper (Original)

### Pros
✅ **Official OpenAI model**  
✅ **Excellent quality**  
✅ **Free and open-source**  
✅ **100% offline**  
✅ **Well-documented**  
✅ **Large community**

### Cons
❌ **Slower** than Faster-Whisper (4-5x)  
❌ **Higher memory usage**  
❌ Requires PyTorch (large dependency)  
❌ GPU highly recommended for larger models

### Installation

```bash
pip install openai-whisper
```

### Usage Example

```python
import whisper

# Load model
model = whisper.load_model("base")

# Transcribe
result = model.transcribe("audio.mp3", language="pt")

# Print results
print(result["text"])
```

### When to Use Whisper vs. Faster-Whisper

**Use Faster-Whisper if:**
- Speed is important
- Limited RAM available
- Processing many files

**Use Original Whisper if:**
- Faster-Whisper installation issues
- Need exact OpenAI implementation
- Already have Whisper in project dependencies

---

## Google Cloud Speech-to-Text

### Pros
✅ **Very accurate** (industry-leading)  
✅ **Fast processing** (cloud infrastructure)  
✅ **125+ languages**  
✅ **Word-level timestamps**  
✅ **Punctuation & capitalization**  
✅ **Speaker diarization** (premium)

### Cons
❌ **Requires internet** (cloud-only)  
❌ **Costs money** (after free tier)  
❌ **Privacy concerns** (audio uploaded to Google)  
❌ Requires GCP account setup  
❌ Complex authentication

### Pricing

- **Free tier:** 60 minutes/month
- **Standard:** $0.006 per 15 seconds ($1.44/hour)
- **Premium:** $0.009 per 15 seconds (with diarization)

### Installation

```bash
pip install google-cloud-speech
```

### Setup

1. Create GCP project
2. Enable Speech-to-Text API
3. Create service account & download JSON key
4. Set environment variable:
   ```bash
   export GOOGLE_APPLICATION_CREDENTIALS="path/to/key.json"
   ```

### Usage Example

```python
from google.cloud import speech

client = speech.SpeechClient()

with open("audio.wav", "rb") as audio_file:
    content = audio_file.read()

audio = speech.RecognitionAudio(content=content)
config = speech.RecognitionConfig(
    encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
    sample_rate_hertz=16000,
    language_code="pt-BR",
)

response = client.recognize(config=config, audio=audio)

for result in response.results:
    print(result.alternatives[0].transcript)
```

---

## Azure Speech Services

### Pros
✅ **High accuracy**  
✅ **100+ languages**  
✅ **Real-time transcription**  
✅ **Custom models** (train on your data)  
✅ **Good Microsoft ecosystem integration**

### Cons
❌ **Requires internet**  
❌ **Costs money** (after free tier)  
❌ **Privacy concerns** (cloud processing)  
❌ Requires Azure account  
❌ Complex setup

### Pricing

- **Free tier:** 5 hours/month
- **Standard:** $1.00 per audio hour

### Installation

```bash
pip install azure-cognitiveservices-speech
```

### Setup

1. Create Azure account
2. Create Speech resource
3. Get API key and region
4. Set environment variables:
   ```bash
   export AZURE_SPEECH_KEY="your-key"
   export AZURE_SPEECH_REGION="your-region"
   ```

### Usage Example

```python
import azure.cognitiveservices.speech as speechsdk

speech_config = speechsdk.SpeechConfig(
    subscription=os.environ.get('AZURE_SPEECH_KEY'),
    region=os.environ.get('AZURE_SPEECH_REGION')
)

audio_config = speechsdk.audio.AudioConfig(filename="audio.wav")
speech_recognizer = speechsdk.SpeechRecognizer(
    speech_config=speech_config,
    audio_config=audio_config
)

result = speech_recognizer.recognize_once()
print(result.text)
```

---

## AssemblyAI

### Pros
✅ **Modern, developer-friendly API**  
✅ **Excellent accuracy**  
✅ **Advanced features** (sentiment, topic detection, PII redaction)  
✅ **Speaker diarization** (included)  
✅ **Fast processing**  
✅ **Good documentation**

### Cons
❌ **Requires internet**  
❌ **Costs money** (no free tier, only trial credits)  
❌ **Privacy concerns** (cloud processing)  
❌ Requires API key

### Pricing

- **Free trial:** $50 credits
- **Standard:** $0.00025 per second (~$0.90/hour)

### Installation

```bash
pip install assemblyai
```

### Setup

1. Sign up at assemblyai.com
2. Get API key
3. Set environment variable:
   ```bash
   export ASSEMBLYAI_API_KEY="your-key"
   ```

### Usage Example

```python
import assemblyai as aai

aai.settings.api_key = os.environ["ASSEMBLYAI_API_KEY"]

transcriber = aai.Transcriber()
transcript = transcriber.transcribe("audio.mp3")

print(transcript.text)

# Speaker diarization
for utterance in transcript.utterances:
    print(f"Speaker {utterance.speaker}: {utterance.text}")
```

---

## Recommendation Matrix

### Use Faster-Whisper if:
- ✅ Privacy is critical (local processing)
- ✅ Want zero cost (free forever)
- ✅ Need offline capability
- ✅ Processing many files (speed matters)
- ✅ Limited budget

### Use Google Speech-to-Text if:
- ✅ Need absolute best accuracy
- ✅ Have budget for cloud services
- ✅ Want advanced features (punctuation, diarization)
- ✅ Already using GCP ecosystem

### Use Azure Speech if:
- ✅ In Microsoft ecosystem
- ✅ Need custom model training
- ✅ Want real-time transcription
- ✅ Have Azure credits

### Use AssemblyAI if:
- ✅ Need advanced features (sentiment, topics)
- ✅ Want easiest API experience
- ✅ Need automatic PII redaction
- ✅ Value developer experience

---

## Performance Benchmarks

**Test:** 1-hour podcast (MP3, 44.1kHz, stereo)

| Tool | Processing Time | Accuracy | Cost |
|------|----------------|----------|------|
| Faster-Whisper (small) | 8 min | 94% | $0 |
| Whisper (small) | 32 min | 94% | $0 |
| Google Speech | 2 min | 96% | $1.44 |
| Azure Speech | 3 min | 95% | $1.00 |
| AssemblyAI | 4 min | 96% | $0.90 |

*Benchmarks run on MacBook Pro M1, 16GB RAM*

---

## Conclusion

**For the audio-transcriber skill:**

1. **Primary:** Faster-Whisper (best balance of speed, quality, privacy, cost)
2. **Fallback:** Whisper (if Faster-Whisper unavailable)
3. **Optional:** Cloud APIs (user choice for premium features)

This ensures the skill works out-of-the-box for most users while allowing advanced users to integrate commercial services if needed.
