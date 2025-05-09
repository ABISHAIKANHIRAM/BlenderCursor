import speech_recognition as sr
import wave
import pyaudio
import os
import re
import threading

class VoiceToTextCorrector:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.audio = pyaudio.PyAudio()
        self.format = pyaudio.paInt16
        self.channels = 1
        self.rate = 44100
        self.chunk = 1024
        self.frames = []
        self.recording = False
        self.stream = None
        self.temp_audio_file = "temp_recording.wav"

    def start_recording(self):
        print("Recording started... Click 'Stop' to finish.")
        self.frames = []
        self.recording = True
        self.stream = self.audio.open(format=self.format, channels=self.channels,
                                      rate=self.rate, input=True,
                                      frames_per_buffer=self.chunk)
        threading.Thread(target=self._record).start()

    def _record(self):
        while self.recording:
            data = self.stream.read(self.chunk)
            self.frames.append(data)

    def stop_recording_and_process(self):
        self.recording = False
        self.stream.stop_stream()
        self.stream.close()
        print("Recording stopped.")

        # Save audio
        with wave.open(self.temp_audio_file, 'wb') as wf:
            wf.setnchannels(self.channels)
            wf.setsampwidth(self.audio.get_sample_size(self.format))
            wf.setframerate(self.rate)
            wf.writeframes(b''.join(self.frames))

        # Convert and delete
        text = self.audio_to_text()
        os.remove(self.temp_audio_file)
        return self.correct_grammar(text)

    def audio_to_text(self):
        try:
            with sr.AudioFile(self.temp_audio_file) as source:
                self.recognizer.adjust_for_ambient_noise(source)
                audio_data = self.recognizer.record(source)
                print("Converting speech to text...")
                return self.recognizer.recognize_google(audio_data, language="en-US")
        except sr.UnknownValueError:
            print("Speech not understood.")
            return ""
        except sr.RequestError as e:
            print(f"API Error: {e}")
            return ""

    def correct_grammar(self, text):
        if not text:
            return ""
        original = text
        corrections = [
            (r'(\w)\.(\w)', r'\1. \2'),
            (r'(\w),(\w)', r'\1, \2'),
            (r'^([a-z])', lambda m: m.group(1).upper()),
            (r'([.!?]\s+)([a-z])', lambda m: m.group(1) + m.group(2).upper()),
            (r'\bi\b', 'I'),
            (r'\bdont\b', "don't"),
            (r'\bcant\b', "can't"),
            (r'\bim\b', "I'm"),
            (r'\bthats\b', "that's"),
            (r'\btheres\b', "there's"),
            (r'\bwont\b', "won't"),
            (r'\bwerent\b', "weren't"),
            (r'\bwouldnt\b', "wouldn't"),
            (r'\bcouldnt\b', "couldn't"),
            (r'\bshouldnt\b', "shouldn't"),
            (r'\baint\b', "ain't"),
            (r'\bgonna\b', "going to"),
            (r'\bwanna\b', "want to"),
            (r'\s+', ' '),
        ]
        for pattern, replacement in corrections:
            text = re.sub(pattern, replacement, text)
        if text and not text.endswith(('.', '!', '?')):
            text += '.'
        return text.strip()

# Simulating button usage
if __name__ == "__main__":
    vtt = VoiceToTextCorrector()

    input("Press Enter to START recording...")
    vtt.start_recording()

    input("Press Enter to STOP recording...")
    final_text = vtt.stop_recording_and_process()

    print("\nFinal output:\n", final_text)
