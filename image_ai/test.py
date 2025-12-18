import pyaudio
import wave
import requests

# Constants
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024
RECORD_SECONDS = 5  # Adjust the duration of the recording
FILE_NAME = "recording.wav"  # Name of the file to save locally
SERVER_URL = "http://your-server-url.com/upload"  # URL of your server endpoint to upload the audio file

def record_audio(file_name):
    audio = pyaudio.PyAudio()
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True,
                        frames_per_buffer=CHUNK)
    print("Recording...")

    frames = []

    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

    print("Finished recording.")

    stream.stop_stream()
    stream.close()
    audio.terminate()

    # Save recorded audio to a file
    with wave.open(file_name, 'wb') as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(audio.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))

def upload_to_server(file_name, server_url):
    files = {'file': open(file_name, 'rb')}
    response = requests.post(server_url, files=files)
    if response.status_code == 200:
        print("Upload successful.")
    else:
        print("Upload failed.")

if __name__ == "__main__":
    record_audio(FILE_NAME)
    upload_to_server(FILE_NAME, SERVER_URL)
