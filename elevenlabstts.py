from elevenlabslib import *
import pydub
import pydub.playback
import io
import sox
import os
import multiprocessing
from playsound import playsound
import requests
import texttospeech


def read_token():
    file_name = "ElevenLabs_API_Key.txt"
    current_dir = os.getcwd()
    file_path = os.path.join(current_dir, file_name)
    with open(file_path, 'r') as file:
        token = file.readline().strip()
    return token


def play_tts_audio(bytes_data):
    sound = pydub.AudioSegment.from_file_using_temporary_files(io.BytesIO(bytes_data))
    sound.export(out_f="elevenlabstts_output.wav", format="wav", bitrate="128")

    tfm = sox.Transformer()
    tfm.flanger(delay=20, phase=100, speed=0.5)
    tfm.reverb(room_scale=90, pre_delay=22, reverberance=25, wet_gain=0.86)
    tfm.flanger(delay=20, phase=100, speed=0.5)

    print("Processing Audio...")
    tfm.build_file(os.path.join(os.getcwd(), "elevenlabstts_output.wav"),
                   os.path.join(os.getcwd(), "elevenlabstts_output_processed.wav"))
    print("Playing Audio...")
    file_name = os.path.join(os.getcwd(), "elevenlabstts_output_processed.wav")
    process = multiprocessing.Process(target=playsound, args=(file_name,))
    process.start()
    process.join()
    process.terminate()
    os.remove(file_name)
    os.remove(os.path.join(os.getcwd(), "elevenlabstts_output.wav"))

    # pydub.playback.play(sound)
    return


def convert_text_to_speech(tts_message):
    user = ElevenLabsUser(read_token())
    voice = user.get_voices_by_name("Winslow")[0]
    try:
        play_tts_audio(voice.generate_audio_bytes(tts_message))
    except requests.exceptions.HTTPError as e:
        print(e)
        print("Switching to Google Voice API")
        texttospeech.main(tts_message)
    # the ai to say as a string
