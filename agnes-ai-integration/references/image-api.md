# Agnes Image 2.1 Flash API Reference

## Endpoint
`POST https://apihub.agnes-ai.com/v1/images/generations`

## Auth
`Authorization: Bearer <API_KEY>`

## Required Params
- `model`: `agnes-image-2.1-flash` or `agnes-image-2.0-flash`
- `prompt`: Text description
- `size`: e.g. `1024x768`, `1024x1024`

## Optional Params
- `image`: Array of URLs/Base64 for img2img (inside `extra_body`)
- `return_base64`: true for Base64 output
- `extra_body.response_format`: `"url"` or `"b64_json"`

## Critical Rule
`response_format` MUST be inside `extra_body`, NOT at top level. Top-level causes 400 error.

## Image-to-Image
```json
{
  "model": "agnes-image-2.1-flash",
  "prompt": "Transform into cyberpunk style",
  "size": "1024x768",
  "extra_body": {
    "image": ["https://example.com/input.png"],
    "response_format": "url"
  }
}
```

## Response
- URL mode: `data[0].url`
- Base64 mode: `data[0].b64_json`

## Prompt Structure
`[Subject] + [Scene] + [Style] + [Lighting] + [Composition] + [Quality]`
