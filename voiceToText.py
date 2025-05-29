import os
import speech_recognition as sr
from pydub import AudioSegment

def convert_m4a_to_wav(m4a_path, wav_path):
    audio = AudioSegment.from_file(m4a_path, format="m4a")
    audio.export(wav_path, format="wav")

def transcribe_audio(file_path):
    recognizer = sr.Recognizer()

    # Convert m4a to wav
    wav_path = file_path.replace(".m4a", ".wav")
    convert_m4a_to_wav(file_path, wav_path)

    # Load and recognize
    with sr.AudioFile(wav_path) as source:
        audio_data = recognizer.record(source)

    try:
        text = recognizer.recognize_google(audio_data)
        return text
    except sr.UnknownValueError:
        return "[Unintelligible or silent audio]"
    except sr.RequestError as e:
        return f"[Could not request results; {e}]"
    finally:
        if os.path.exists(wav_path):
            os.remove(wav_path)  # Clean up

# Example usage:
text = transcribe_audio("D:/SUB/NubeEra_work/CalllogsAIProj/record_out.m4a")
print("Transcript:\n", text)
