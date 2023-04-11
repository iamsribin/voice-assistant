import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import openai

openai.api_key = "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"

engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0')

r = sr.Recognizer()
mic = sr.Microphone(device_index=1)

conversation = ""
user_name = "Sri"
bot_name = "Alexa"

while True:
    with mic as source:
        print("\n Listening...")
        r.adjust_for_ambient_noise(source, duration=0.2)
        audio = r.listen(source, phrase_time_limit=5)

    try:
        user_input = r.recognize_google(audio)
        user_input = user_input.lower().replace("alexa", "")
        print(f"User said: {user_input}")
        if "stop" in user_input.lower():
            print("Goodbye...")
            engine.say("Goodbye")
            engine.runAndWait()
            exit()
    except sr.UnknownValueError:
        print("Could not understand audio")
        continue
    except sr.RequestError as e:
        print("Could not request results; {0}".format(e))
        continue

    prompt = user_name + ":" + user_input + "\n" + bot_name + ":"
    conversation += prompt

    if "play" in user_input.lower():
        video_name = user_input.lower().replace("play", "")
        pywhatkit.playonyt(video_name)
        response_str = f"Playing {video_name} on YouTube"
        print("Goodbye! enjoy " + video_name + " video...")
        engine.say("enjoy " + video_name + " video Goodbye...")
        engine.runAndWait()
        exit()

    elif "what time it is" in user_input.lower():
        now = datetime.datetime.now()
        time_str = now.strftime("%H:%M:%S")
        response_str = f"The time is {time_str}"
        print(f"{bot_name}: {response_str}")
        engine.say(response_str)
        engine.runAndWait()

    elif "what is today's date" in user_input.lower():
        now = datetime.datetime.now()
        date_str = now.strftime("%B %d, %Y")
        response_str = f"Today's date is {date_str}"
        print(f"{bot_name}: {response_str}")
        engine.say(response_str)
        engine.runAndWait()

    else:

        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=conversation,
            temperature=0.7,
            max_tokens=256,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )

        response_str = response["choices"][0]["text"].replace("\n", "")
        response_str = response_str.split(user_name + ":", 1)[0].split(bot_name + ":", 1)[0]

        conversation += response_str + "\n"
        print(f"{bot_name}: {response_str}")

        engine.say(response_str)

        engine.runAndWait()
