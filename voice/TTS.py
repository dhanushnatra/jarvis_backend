from pathlib import Path
import wave

from piper import PiperVoice,SynthesisConfig

class TextToSpeech:
    def __init__(self,model_path: Path|str = Path("voice/tts_model/Jarvis.onnx")):
        if isinstance(model_path, Path):
            model_path = model_path.absolute().resolve()
        self.voice = PiperVoice.load(model_path)

        self.syn_config = SynthesisConfig(
            volume=0.5,  # half as loud
            length_scale=1.0,  # normal speed
        )

    def speak_to_file(self, text, filename:str|Path="output.wav"):
        if isinstance(filename, Path):
            filename = filename.absolute().resolve()
        try:
            wav_file = wave.open(str(filename), "wb")
            self.voice.synthesize_wav(text=text,wav_file=wav_file,syn_config=self.syn_config)
            return True,f"voice generated at {filename}"
        except Exception as e:
            print(f"Error occurred while synthesizing speech: {e}")
        finally:
            wav_file.close()

if __name__ == "__main__":
    tts = TextToSpeech()
    out = tts.speak_to_file("Hello, this is a test of the text to speech synthesis.",Path("output.wav"))
    if out:
        print(out[1])