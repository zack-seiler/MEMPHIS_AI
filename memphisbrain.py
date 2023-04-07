import speechtotext
import gpt_responses
import elevenlabstts
import texttospeech
import os


def main():
    cont = True
    input("Press ENTER to begin")
    while cont:

        print("Removing previous recordings.")
        try:
            os.remove(os.path.join(os.getcwd(), "recording_output.wav"))
        except FileNotFoundError:
            print("No previous recordings found")
        except PermissionError as e:
            print("Permission error, cannot remove file")
            print(e)

        query = speechtotext.get_text_from_speech()
        print("Query: ", query)
        # query = input("Input: ")

        if query == " None " or query == "None" or query == "" or query == " " or query is None:
            print("Query failed")
            # texttospeech.main("I didn't get that, please try again.")
            # elevenlabstts.convert_text_to_speech("I didn't quite understand that. Could you try again?")
            texttospeech.speak("Request invalid, please try again.")
            continue
        if query.casefold() == "echo charlie".casefold():
            print("Ending conversation")
            break

        print("Getting response")
        response = gpt_responses.get_response(query)
        print("Response: ", response)

        print("Beginning text to speech...")
        # texttospeech.main(response)
        # elevenlabstts.convert_text_to_speech(response)
        texttospeech.speak(response)
        print("Done")

        # user_input = input("Continue? (Y/N)")
        # if user_input == "N".casefold():
        #     cont = False
        # elif user_input == "Y".casefold():
        #     continue
        # else:
        #     print("Invalid response, exiting.")
        #     cont = False


if __name__ == '__main__':
    main()
