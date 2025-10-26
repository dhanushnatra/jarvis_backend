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
        wav_file = wave.open(str(filename), "wb")
        self.voice.synthesize_wav(text=text,wav_file=wav_file,syn_config=self.syn_config)
        wav_file.close()
        
        
if __name__ == "__main__":
    tts = TextToSpeech()
    tts.speak_to_file("Hello, this is a test of the text to speech synthesis.")