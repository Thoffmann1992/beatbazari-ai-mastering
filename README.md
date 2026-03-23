# beatbazari-ai-mastering
Analyzer 
# BeatBazarı AI Mastering Engineer

Audio faylları (WAV/MP3) qəbul edib avtomatik analiz edən və mastering edən FastAPI-based servisdən istifadə edin.

## Məqsəd
- BPM, key, LUFS, dynamic range, frequency balance analizi
- Rule-based mastering chain (EQ, multiband compression, saturation, limiter)
- Railway.app üzərində deploy üçün optimallaşdırılıb

## Texnologiyalar
- FastAPI
- Librosa (analiz)
- Pedalboard (DSP effektləri)
- Pydub / SoundFile (audio I/O)

## Quraşdırma
```bash
git clone https://github.com/Thoffmann1992/beatbazari-ai-mastering.git
cd beatbazari-ai-mastering
python -m venv venv
source venv/bin/activate    # Windows-da: venv\Scripts\activate
pip install -r requirements.txt
