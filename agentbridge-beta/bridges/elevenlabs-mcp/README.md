# elevenlabs-mcp-bridge

Same pattern as Manus MCP bridge:

- **Server holds** `ELEVEN_LABS_KEY` (from GitHub Actions secret / host env)
- **Client holds** only `BRIDGE_TOKEN`
- `/health` probes ElevenLabs `/v1/user` without exposing the key
- `/tts` generates MP3 for mapped personas (Kenji=Louis, Rex=Hank, Zagan=Guy)

## Deploy env

```
ELEVEN_LABS_KEY=...          # GitHub Secret → host env
BRIDGE_TOKEN=...             # different long random secret
PORT=8000
```

## Test key holds up

```bash
curl -s https://YOUR_HOST/health
# expect chip green, user_me_status 200, key_configured true
```

Run GitHub Action `elevenlabs-tts-kenji` — if KEY_HOLD_UP=true the secret works.

**This chat cannot read GitHub Actions secret values.**
