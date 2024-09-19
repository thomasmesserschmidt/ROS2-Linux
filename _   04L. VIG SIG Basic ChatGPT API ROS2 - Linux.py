# Basic ChatGPT Voice I/O for ROS2 on Linux
# Thomas Messerschmidt

import speech_recognition as sr  # Import the speech recognition library
import os  # Import the os library for using espeak
import openai  # Import the OpenAI library

# Initialize the recognizer
recognizer = sr.Recognizer()  # Create an instance of the recognizer

def speak_response(response):
    os.system(f'espeak "{response}"')  # Use espeak to say the response

speak_response("Starting Chatbot")  # Announce that the chatbot code is running
speak_response("To quit, say the word exit")  # Tell user that to stop running, you say the word "exit"

# Set your OpenAI API key
openai.api_key = 'sk-xx-xx'  # Replace with your actual OpenAI API key

# Function to get voice input
def get_voice_input():
    with sr.Microphone() as source:  # Use the microphone as the audio source
        print("Listening...")  # Inform the user that the program is listening
        audio = recognizer.listen(source)  # Listen for the audio input
        try:
            text = recognizer.recognize_google(audio)  # Convert the audio to text using Google's speech recognition
            print(f"You said: {text}")  # Print the recognized text
            return text  # Return the recognized text
        except sr.UnknownValueError:
            print("Sorry, I didn't understand that.")  # Handle the case where the speech was not understood
            speak_response("Sorry, I didn't understand that.")
            return None  # Return None if the speech was not understood
        except sr.RequestError as e:
            print(f"Could not request results; {e}")  # Handle the case where there was an error with the request
            speak_response("Sorry, I am having problems. Please repeat.")
            return None  # Return None if there was an error with the request

# Function to get response from ChatGPT-4
def get_chatgpt_response(prompt, conversation_history, system="You are a ROS 2 robot. You are located in Riverside, California. Your name is Hal. Your answers are terse. Never more than a sentence.", temperature=0.7, max_tokens=150, stop=None):
    conversation_history.append({"role": "system", "content": system})  # Add the system message to the conversation history
    conversation_history.append({"role": "user", "content": prompt})  # Add the user's prompt to the conversation history
    response = openai.ChatCompletion.create(
        model="gpt-4",  # Specify the model to use
        messages=conversation_history,  # Provide the conversation history
        temperature=temperature,  # Set the temperature for the response
        max_tokens=max_tokens,  # Set the maximum number of tokens for the response
        stop=stop  # Specify the stop sequence for the response
    )
    reply = response.choices[0].message['content']  # Extract the reply from the response
    conversation_history.append({"role": "assistant", "content": reply})  # Add the assistant's reply to the conversation history
    return reply  # Return the assistant's reply

# Main function to run the chat
def chat_with_gpt():
    conversation_history = []  # Initialize an empty conversation history
    while True:
        user_input = get_voice_input()  # Get the user's voice input
        if user_input:
            if user_input.lower() in ["exit", "quit", "stop"]:   # Check if the user wants to exit
                print("Shutting down Chatbot.")  # Inform the user that the program is exiting
                break  # Exit the loop
            response = get_chatgpt_response(user_input, conversation_history)  # Get the response from ChatGPT-4
            print(f"ChatGPT-4: {response}")  # Print the response
            speak_response(response)  # Speak the response

if __name__ == "__main__":
    chat_with_gpt()  # Run the main function if the script is executed directly

speak_response("Shutting down Chatbot")  # Announce that the chatbot code is stopping
