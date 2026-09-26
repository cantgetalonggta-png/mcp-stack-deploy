---
name: directive-always-upload-mp3-to-google-drive
description: >
  NON-NEGOTIABLE permanent rule: every generated .mp3 MUST be uploaded to Google Drive
  immediately after creation, before the turn ends.
metadata:
  permanent: true
  non_negotiable: true
  priority: 0
  version: "1.0.0"
---

# PERMANENT RULE: Always Upload MP3s to Google Drive

## Priority
**P0 · NON-NEGOTIABLE · LOCKED IN**

## Trigger
Any of:
- `voice_generate_speech` / `voice_generate_multi_speech` succeeds
- edge-tts or ffmpeg produces an `.mp3`
- Operator asks for debate audio / system imprint audio

## Mandatory sequence (same turn)
1. Write/confirm file under `/workspace/artifacts/` (or known durable path)
2. `google_drive_upload_artifact` with:
   - `artifact_path` relative to artifacts root (e.g. `/filename.mp3`)
   - `folder_id` = AgentBridge-Audio (`1ZxqtwHMdoTT-eAe8jO2XR5nCvvpyDTeb`) OR operator Drive folder `14I-2NhMyALQG9Y3qJShTbD0EGaDYPMGI`
   - `mime_type` = `audio/mpeg`
3. Record file_id + web_view_link in `reports/mp3-drive-uploads.json`
4. Only then mark the audio task complete

## Never
- End a turn with local-only `.mp3` and no Drive upload
- Assume "Voice returned size_bytes" means uploaded
- Skip upload because GitHub already has the file

## Default folder
- Primary: `AgentBridge-Audio` → https://drive.google.com/drive/folders/1ZxqtwHMdoTT-eAe8jO2XR5nCvvpyDTeb
- Parent: operator pack folder → https://drive.google.com/drive/folders/14I-2NhMyALQG9Y3qJShTbD0EGaDYPMGI

## Failure
If Drive upload fails: retry once; report blocker; still keep local + GitHub copy.
