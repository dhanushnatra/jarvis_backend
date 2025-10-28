from pathlib import Path
import speech_recognition as sr 

class SpeechToText:
    def __init__(self):
        self.recognizer = sr.Recognizer()
    def transcribe_from_file(self, filename: Path|str) -> str:
        if isinstance(filename, Path):
            filename = str(filename.absolute().resolve())
        with sr.AudioFile(filename) as source:
            audio_data = self.recognizer.record(source)
            try:
                text = self.recognizer.recognize_google(audio_data) # type: ignore
                return text
            except sr.UnknownValueError:
                return "Could not understand the audio"
            except sr.RequestError as e:
                return f"Could not request results; {e}"
            finally:
                del audio_data

if __name__ == "__main__":
    stt = SpeechToText()
    result = stt.transcribe_from_file("output.wav")
    print("Transcription:", result)