# Develop a program that uses speech recognition and text to speech to 
# ask questions to an LLM and retrieve answers from it (Use gemini-pro 
# API for this program) 

import speech_recognition as sr
import pyttsx3
import google.generativeai as genai

listener = sr.Recognizer()

engine = pyttsx3.init()

genai.configure(api_key= "AIzaSyBY0rQpSlblpJ5WOsTRROC50Sw8nVXOg6s")

# Setting up Gemini Model 
generation_config = {
  "temperature": 0.9,
  "top_p": 1,
  "top_k": 1,
  "max_output_tokens": 2048,
}

safety_settings = [
  {
    "category": "HARM_CATEGORY_HARASSMENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_HATE_SPEECH",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
]

# function for text to speech operation
def talk(text):
    print(text)
    engine.say(text)
    engine.runAndWait()

def get_info():
    try:
        with sr.Microphone() as source:
            print('listening...')
            voice = listener.listen(source)
            info = listener.recognize_google(voice)
            print(info)
            return info.lower()
    except sr.UnknownValueError:
        print("Could not understand audio.")
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")


def ask_now(query):
    model = genai.GenerativeModel(model_name="gemini-pro",
                                generation_config=generation_config,
                                safety_settings=safety_settings)


    prompt_parts = query

    response = model.generate_content(prompt_parts)
    
    return talk(response.text)

def main():

    while True:
        talk("Ask question")
        question = get_info()
        ask_now(query= question)

if __name__ == "__main__":
    main()

