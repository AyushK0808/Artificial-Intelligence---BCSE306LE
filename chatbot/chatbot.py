import os
import google.generativeai as genai


GOOGLE_API_KEY=os.getenv('GOOGLE_API_KEY') #Add a Gemini API key to .env file. 
genai.configure(api_key=GOOGLE_API_KEY)

model = genai.GenerativeModel('gemini-pro')
chat = model.start_chat(history=[])

while True:
    prompt = input("Ask me anything: ")
    if (prompt == "exit"):
        break
    response = chat.send_message(prompt, stream=True)
    for chunk in response:
        if chunk.text:
          print(chunk.text)