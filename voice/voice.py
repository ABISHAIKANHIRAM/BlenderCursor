import speech_recognition as sr
import language_tool_python
import os
import time
import wave
import pyaudio

class VoiceToTextCorrector:
    def __init__(self):
        # Initialize speech recognizer
        self.recognizer = sr.Recognizer()
        
        # Initialize grammar correction tool
        self.grammar_tool = language_tool_python.LanguageTool('en-US')
        
        # Audio recording parameters
        self.format = pyaudio.paInt16
        self.channels = 1
        self.rate = 44100
        self.chunk = 1024
        self.record_seconds = 5  # Default recording time
        self.temp_audio_file = "temp_recording.wav"
    
    def record_audio(self, duration=None):
        """Record audio from microphone for specified duration"""
        if duration:
            self.record_seconds = duration
            
        print(f"Recording for {self.record_seconds} seconds...")
        
        audio = pyaudio.PyAudio()
        
        # Start recording
        stream = audio.open(format=self.format, channels=self.channels,
                            rate=self.rate, input=True,
                            frames_per_buffer=self.chunk)
        
        frames = []
        
        for i in range(0, int(self.rate / self.chunk * self.record_seconds)):
            data = stream.read(self.chunk)
            frames.append(data)
            
            # Display recording progress
            if i % 10 == 0:
                seconds_passed = i * self.chunk / self.rate
                progress = int(seconds_passed / self.record_seconds * 20)
                print(f"\r[{'#' * progress}{' ' * (20-progress)}] {seconds_passed:.1f}s", end="")
        
        print("\nFinished recording.")
        
        # Stop and close the stream
        stream.stop_stream()
        stream.close()
        audio.terminate()
        
        # Save the recorded audio as a WAV file
        with wave.open(self.temp_audio_file, 'wb') as wf:
            wf.setnchannels(self.channels)
            wf.setsampwidth(audio.get_sample_size(self.format))
            wf.setframerate(self.rate)
            wf.writeframes(b''.join(frames))
        
        return self.temp_audio_file
    
    def audio_to_text(self, audio_file=None):
        """Convert audio to text using speech recognition"""
        if audio_file is None:
            audio_file = self.temp_audio_file
            
        print("Converting speech to text...")
        
        try:
            with sr.AudioFile(audio_file) as source:
                # Adjust for ambient noise
                self.recognizer.adjust_for_ambient_noise(source)
                
                # Record audio from the file
                audio_data = self.recognizer.record(source)
                
                # Recognize speech using Google Speech Recognition
                text = self.recognizer.recognize_google(audio_data)
                print(f"Original text: {text}")
                return text
                
        except sr.UnknownValueError:
            print("Speech recognition could not understand the audio")
            return ""
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")
            return ""
    
    def correct_grammar(self, text):
        """Correct grammar in the provided text"""
        print("Correcting grammar...")
        
        if not text:
            return ""
            
        # Use LanguageTool to correct the text
        corrected_text = self.grammar_tool.correct(text)
        print(f"Corrected text: {corrected_text}")
        
        return corrected_text
    
    def process_from_file(self, audio_file):
        """Process an existing audio file"""
        text = self.audio_to_text(audio_file)
        return self.correct_grammar(text)
        
    def process(self, duration=None):
        """Record audio and convert to grammatically correct text"""
        # Record audio
        self.record_audio(duration)
        
        # Convert to text
        text = self.audio_to_text()
        
        # Correct grammar
        corrected_text = self.correct_grammar(text)
        
        # Clean up temporary file
        if os.path.exists(self.temp_audio_file):
            os.remove(self.temp_audio_file)
            
        return corrected_text

def main():
    processor = VoiceToTextCorrector()
    
    while True:
        print("\n=== Voice to Text with Grammar Correction ===")
        print("1. Record and process voice")
        print("2. Process existing audio file")
        print("3. Change recording duration")
        print("4. Exit")
        
        choice = input("Enter your choice (1-4): ")
        
        if choice == '1':
            result = processor.process()
            print("\nFinal result:")
            print(f"'{result}'")
            
        elif choice == '2':
            file_path = input("Enter the path to your audio file (.wav format): ")
            if os.path.exists(file_path):
                result = processor.process_from_file(file_path)
                print("\nFinal result:")
                print(f"'{result}'")
            else:
                print("File not found!")
                
        elif choice == '3':
            try:
                new_duration = float(input("Enter new recording duration in seconds: "))
                if new_duration > 0:
                    processor.record_seconds = new_duration
                    print(f"Recording duration set to {new_duration} seconds")
                else:
                    print("Duration must be greater than 0")
            except ValueError:
                print("Please enter a valid number")
                
        elif choice == '4':
            print("Exiting program...")
            break
            
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()