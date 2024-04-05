import pyaudio
import speech_recognition as sr


def transcribe_audio():
    # Set up the PyAudio stream
    p = pyaudio.PyAudio()
    chunk_size = 1024
    sample_format = pyaudio.paInt16
    channels = 1
    fs = 44100

    stream = p.open(format=sample_format,
                    channels=channels,
                    rate=fs,
                    frames_per_buffer=chunk_size,
                    input=True)

    # Set up the speech recognition
    recognizer = sr.Recognizer()

    try:
        print("Listening for audio...")
        while True:
            # Capture audio from the stream
            data = stream.read(chunk_size)
            audio_data = sr.AudioData(data, fs, sample_format)

            # Recognize speech using Google Web Speech API
            text = recognizer.recognize_google(audio_data)

            # Print the transcribed text
            print("Transcription:", text)

    except KeyboardInterrupt:
        print("Stopping transcription.")
    finally:
        # Stop the stream and close PyAudio
        stream.stop_stream()
        stream.close()
        p.terminate()


if __name__ == "__main__":
    transcribe_audio()
