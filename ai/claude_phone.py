# gemini (via google search)
# pip install fastapi uvicorn twilio
# pip install python-multipart
# uvicorn claude_phone:app --host 0.0.0.0 --port 8000
# cloudflared tunnel --url http://localhost:8000
# Point Twilio to /voice (or just /):
# In your Twilio number's Voice settings ("A call comes in"), set the Webhook URL to https://trycloudflare.com (HTTP POST).
# Add a check on From (Form(...)) in /voice (or /) to verify your own cell number (if From != "+3069...": resp.hangup())

# Alternative to Claude Code:
# Ollama running qwen2.5:7b or llama3.1:8b (4-bit quantized, ~5GB RAM).

import asyncio
import subprocess
from fastapi import FastAPI, Form, Response
from twilio.twiml.voice_response import VoiceResponse, Gather

app = FastAPI()

# Stores pending or completed responses by CallSid
call_tasks = {}
call_results = {}

VOICE_SYSTEM_PROMPT = (
    "You are answering a phone call from the user. "
    "Keep your spoken response brief, natural, and conversational (2-3 sentences max). "
    "Never output markdown, asterisks, bullet points, or raw code blocks."
)

def run_claude_sync(prompt: str, is_first_turn: bool) -> str:
    cmd = [
        "claude",
        "-p", prompt,
        "--append-system-prompt", VOICE_SYSTEM_PROMPT,
        "--allowedTools", "Bash,Read,Edit,Write,Glob,Grep"
    ]
    if not is_first_turn:
        cmd.append("--continue")

    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.stdout.strip() or "Done, though I didn't generate a text response."

async def process_claude(call_sid: str, prompt: str, is_first_turn: bool):
    loop = asyncio.get_running_loop()
    reply = await loop.run_in_executor(None, run_claude_sync, prompt, is_first_turn)
    call_results[call_sid] = reply

@app.post("/")
async def incoming_call():
    resp = VoiceResponse()
    gather = Gather(
        input="speech",          # use Twilio's built-in Speech Recognition & TTS
                                 # Alternative: Speech-to-Text: lightning-whisper-mlx or mlx-whisper
                                 # (using whisper-large-v3-turbo or distil-whisper).
                                 # Text-to-Speech (TTS): Kokoro-82M (via kokoro-onnx or MLX)
        action="/process",
        speech_timeout="auto",
        language="en-US"
    )
    gather.say("Claude Code is ready. What should we work on?", voice="Polly.Joanna-Neural")
    resp.append(gather)
    return Response(content=str(resp), media_type="application/xml")

@app.post("/process")
async def process_speech(CallSid: str = Form(...), SpeechResult: str = Form("")):
    resp = VoiceResponse()
    if not SpeechResult:
        resp.redirect("/")
        return Response(content=str(resp), media_type="application/xml")

    # Start Claude Code in the background so Twilio doesn't time out
    is_first = CallSid not in call_tasks
    call_results.pop(CallSid, None)
    call_tasks[CallSid] = asyncio.create_task(process_claude(CallSid, SpeechResult, is_first))

    resp.say("On it. Give me a moment.", voice="Polly.Joanna-Neural")
    resp.pause(length=4)
    resp.redirect("/poll")
    return Response(content=str(resp), media_type="application/xml")

@app.post("/poll")
async def poll_status(CallSid: str = Form(...)):
    resp = VoiceResponse()
    if CallSid in call_results:
        answer = call_results.pop(CallSid)
        gather = Gather(
            input="speech",
            action="/process",
            speech_timeout="auto",
            language="en-US"
        )
        gather.say(answer, voice="Polly.Joanna-Neural")
        resp.append(gather)
    else:
        # Still running tools/thinking; keep the line alive
        resp.pause(length=4)
        resp.redirect("/poll")
    return Response(content=str(resp), media_type="application/xml")
