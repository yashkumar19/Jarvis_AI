import datetime
import os
import subprocess
import Openai
from config import apikey
import pyttsx3     # so this is text to speech conversion library which is used in windows
import speech_recognition as sr
import webbrowser
import openai
import datetime

def say(text):
    engine = pyttsx3.init()  # Here we are initialize the pyttsx
    engine.say(text)     #Adds the text to the speech engine's queue.
    engine.runAndWait()

def takeCommand():
    r = sr.Recognizer()      # this is used to recognize the speech
    with sr.Microphone() as source:   # we use microphone as audio source
        #print("Adjusting for ambient noise...")
        r.adjust_for_ambient_noise(source, duration=1)  # Helps to adjust for ambient noise to improve the accuracy
        print("Listening...")
        audio = r.listen(source)   #this is used to listen the audio
    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language="en-in")   # we are using  Google's speech recognition service to recognize the audio
        print(f"User said: {query}")
    except sr.UnknownValueError:
        print("Sorry, I did not understand that.")
        query = "Sorry, I did not understand that."   # if it didn't hear anything then it comes in picture
        say(query)
    return query

def get_openai_response(user_text):
    openai.api_key = apikey
    response_text = f"OpenAI response for Prompt: {user_text} \n *************************\n\n"    # heading text in the file where prompt generate
    try:
        response = openai.Completion.create(
            model="davinci-002",
            prompt=user_text,
            temperature=0.7,
            max_tokens=256,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        # todo: Wrap this inside of a  try catch block
        # print(response["choices"][0]["text"])
        response_text += response["choices"][0]["text"]
        if not os.path.exists("Openai"):  # when Openai doesn't exists so it create the directory
            os.mkdir("Openai")
        file_name = f"Openai/{''.join(user_text.split('intelligence')[1:]).strip()}.txt" # Here we define the fine name and also we can show the
                                                                                         # prompt name after the word intellignece and use if strip
                                                                                         # will help us to remove the starting and ending space

        # Save the response text to the file
        with open(file_name, "w") as f:   # here we write the content in the file
            f.write(response_text)

        print(f"Response saved to {file_name}")
    except Exception as e:
        print(f"Failed to get response from OpenAI: {e}")
        return "Sorry, I could not process your request."

chatStr = ""
def chat(query):
    global chatStr
    print(chatStr)
    openai.api_key = apikey
    chatStr += f"Yash: {query}\n Jarvis: "

    response = openai.Completion.create(
        model="davinci-002",
        prompt= chatStr,
        temperature=0.7,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    # todo: Wrap this inside of a  try catch block
    say(response["choices"][0]["text"])
    chatStr += f"{response['choices'][0]['text']}\n"
    return response["choices"][0]["text"]

if __name__ == '__main__':
    print("""
          JJJJJJJ  AAAAAAA   RRRRRRRR   VV   VV  IIIIIII    SSSSSSSSS
            JJ    AA     AA  RR   RR    VV   VV    III      SSS
            JJ    AAAAAAAAA  RRRRRRR    VV   VV    III        SSSSSSS
        JJ   JJ   AA     AA  RR    RR    VV VV     III            SSS
         JJJJJ    AA     AA  RR     RR     VV    IIIIIII    SSSSSSSSS
    """)

    say("Hello Yash, I am Jarvis AI")
    say("How may i help you")
    while True :
        query = takeCommand()

        # here we store some link which he directly oen the link
        sites = [["youtube","https://www.youtube.com"],["google","https://www.google.com"],["hdmovie2","https://hdmovie2.bike/"],
                 ["music Ve kamliya","https://music.youtube.com/watch?v=GkJ_wZy0iB4&list=RDAMVMGkJ_wZy0iB4"],
                 ["music husn","https://music.youtube.com/watch?v=_deqdZmKzyg&list=RDAMVMGkJ_wZy0iB4"],
                 ["music hovega", "https://music.youtube.com/watch?v=zLpVIKpSiGI&list=RDAMVMzLpVIKpSiGI"],
                 ["google","https://www.google.com"],["chatgpt","https://chatgpt.com/"],
                 ["resume","file:///C:/Users/yashk/OneDrive/Desktop/yash_resume.pdf"]]
        for site in sites:
            if f"Open {site[0]}".lower() in query.lower():    # in this here we just compare our query with the sites list
                say(f"Opening{site[0]} sir....")
                webbrowser.open(site[1])

        if "the time" in query:
            time = datetime.datetime.now().strftime("%H %M %S")
            say(f"sir time is {time}")

        elif "java".lower() in query.lower():
            intell_path = r"C:\Users\Public\Desktop\IntelliJ IDEA Community Edition 2023.1.2.lnk"    #path of intellij
            try:
                subprocess.Popen([intell_path],shell=True)    # By this we can open the application of the window
                say("Opening IntelliJ IDEA")
            except Exception as e:
                print(f"Failed to open IntelliJ IDEA: {e}");
                say("Failed to open IntelliJ IDEA")

        elif "using artificial intelligence".lower() in query.lower():
            get_openai_response(query)

        elif "exit ai".lower() in query.lower():
            say("Goodbye, have a great day!")
            exit()

        else:
            print("Chatting...")
            chat(query)
