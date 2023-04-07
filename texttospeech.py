import pyttsx3
import os
from google.cloud import texttospeech
from playsound import playsound
import multiprocessing
import sox


def main(text):
    synthesis_input = texttospeech.SynthesisInput(text=text)

    client = texttospeech.TextToSpeechClient()

    voice = texttospeech.VoiceSelectionParams({
        "name": 'en-AU-Neural2-B',
        "language_code": 'en-AU'
    })

    audio_config = texttospeech.AudioConfig({
        "audio_encoding": texttospeech.AudioEncoding.LINEAR16,
        "pitch": 0,
        "speaking_rate": 0.90
    })

    response = client.synthesize_speech(
        input=synthesis_input,
        voice=voice,
        audio_config=audio_config
    )

    with open('google_tts_output.wav', 'wb') as output:
        output.write(response.audio_content)
    output.close()

    tfm = sox.Transformer()
    tfm.flanger(delay=20, phase=100, speed=0.5)
    tfm.reverb(room_scale=90, pre_delay=22, reverberance=25, wet_gain=0.86)
    tfm.flanger(delay=20, phase=100, speed=0.5)

    print("Processing Audio...")
    tfm.build_file(os.path.join(os.getcwd(), "google_tts_output.wav"),
                   os.path.join(os.getcwd(), "google_tts_output_processed.wav"))

    file_name = os.path.join(os.getcwd(), "google_tts_output_processed.wav")
    process = multiprocessing.Process(target=playsound, args=(file_name,))
    process.start()
    process.join()
    process.terminate()
    os.remove(file_name)
    os.remove(os.path.join(os.getcwd(), "google_tts_output.wav"))


def speak(text):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)
    engine.setProperty('rate', 180)
    engine.save_to_file(text, "speech_file.mp3")
    engine.runAndWait()
    engine.stop()

    tfm = sox.Transformer()
    tfm.flanger(delay=20, phase=100, speed=0.5)
    tfm.reverb(room_scale=90, pre_delay=22, reverberance=25, wet_gain=0.86)
    tfm.flanger(delay=20, phase=100, speed=0.5)

    print("Processing Audio...")
    tfm.build_file(os.path.join(os.getcwd(), "speech_file.mp3"),
                   os.path.join(os.getcwd(), "speech_file_processed.wav"))

    file_name = os.path.join(os.getcwd(), "speech_file_processed.wav")
    process = multiprocessing.Process(target=playsound, args=(file_name,))
    process.start()
    process.join()
    process.terminate()
    os.remove(file_name)
    os.remove(os.path.join(os.getcwd(), "speech_file.mp3"))


if __name__ == '__main__':
    main()
