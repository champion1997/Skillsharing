# Agnes Video V2.0 API Reference

## Endpoint
`POST https://apihub.agnes-ai.com/v1/videos`

## Auth
`Authorization: Bearer ***

## Submit Task Params
- `model`: `agnes-video-v2.0`
- `prompt`: Description
- `width`: Default 1152
- `height`: Default 768
- `num_frames`: Max 441, must follow `8n + 1` rule
- `frame_rate`: 1-60
- `mode`: `ti2vid` (text-to-video), `keyframes`

## Polling
- Endpoint: `GET https://apihub.agnes-ai.com/agnesapi?video_id=***`
- Note: `/agnesapi` does NOT have `/v1` prefix!
- Strip `/v1` from base_url before polling.

## Status Flow
`queued` → `in_progress` → `completed` (or `failed`)

## Completed Response
`remixed_from_video_id`: Direct URL to the MP4 file

## Video Duration
`seconds = num_frames / frame_rate`
Default: 121 / 24 ≈ 5 seconds

## Prompt Structure
`[Subject] + [Action] + [Scene] + [Camera Movement] + [Lighting] + [Style]`
