from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
import shutil
import os
from pathlib import Path
import librosa
import soundfile as sf
from pedalboard import Pedalboard, Compressor, LowShelfFilter, HighShelfFilter, Limiter
from pedalboard.io import AudioFile

app = FastAPI(title="BeatBazarı AI Mastering")

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

@app.post("/master")
async def master_audio(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(('.wav', '.mp3', '.flac')):
        raise HTTPException(400, "Yalnız WAV/MP3/FLAC qəbul edilir")

    input_path = UPLOAD_DIR / file.filename
    with input_path.open("wb") as f:
        shutil.copyfileobj(file.file, f)

    try:
        # 1. Analiz (sadə)
        y, sr = librosa.load(input_path, sr=None)
        tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
        rms = librosa.feature.rms(y=y)
        # ... daha çox analiz əlavə edə bilərsən (LUFS approx, spektr)

        # 2. Mastering chain (pedalboard ilə)
        board = Pedalboard([
            LowShelfFilter(cutoff_frequency_hz=120, gain_db=3.0, q=0.7),     # bass boost
            Compressor(threshold_db=-18, ratio=4, attack_ms=5, release_ms=100),
            HighShelfFilter(cutoff_frequency_hz=8000, gain_db=2.0, q=0.7),   # air
            Limiter(threshold_db=-3.0, release_ms=50)
        ])

        output_path = UPLOAD_DIR / f"mastered_{file.filename}"
        with AudioFile(str(input_path), 'r') as f:
            with AudioFile(str(output_path), 'w', f.samplerate, f.num_channels) as o:
                while f.tell() < f.frames:
                    chunk = f.read(f.frames)
                    effected = board(chunk, f.samplerate)
                    o.write(effected)

        return FileResponse(output_path, filename=f"mastered_{file.filename}")

    finally:
        # Təmizlə (storage limit üçün)
        if input_path.exists(): input_path.unlink()
        if output_path.exists(): output_path.unlink()   # production-da saxla və ya S3-ə yüklə

@app.get("/")
def root():
    return {"message": "BeatBazarı AI Mastering API — /master endpoint-ə POST audio göndər"}