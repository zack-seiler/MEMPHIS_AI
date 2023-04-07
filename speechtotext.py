from google.cloud import speech
import os
import io
import audio_recorder


def get_text_from_speech():
    credential_path = "E:\\MEMPHIS_AI\\memphis-ai-e42646e3a2e0.json"
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path

    audio_recorder.start()

    # Creates google client
    client = speech.SpeechClient()

    # Path of the audio file
    file_name = os.path.join(os.path.dirname(__file__), "recording_output.wav")

    # Loads the audio file into memory
    with io.open(file_name, "rb") as audio_file:
        content = audio_file.read()
        audio = speech.RecognitionAudio({"content": content})

    config = speech.RecognitionConfig({
        "encoding": speech.RecognitionConfig.AudioEncoding.LINEAR16,
        "audio_channel_count": 1,
        "language_code": "en-US",
    })

    # Sends the request to google for transcription
    response = client.recognize(request={"config": config, "audio": audio})

    # Reads the response
    for result in response.results:
        return result.alternatives[0].transcript

    os.remove("recording_output.wav")
