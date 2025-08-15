import os
import gradio as gr
from groq import Groq
from dotenv import load_dotenv
from gtts import gTTS
import tempfile

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

chat_history = []

def chatbot(message, history):
    history.append({"role": "user", "content": message})

    messages = [{"role": "system", "content": "You are a friendly AI assistant that answers clearly."}]
    messages.extend(history)

    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages,
        temperature=0.7
    )
    reply = completion.choices[0].message.content  

    history.append({"role": "assistant", "content": reply})

    tts = gTTS(reply)
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
    tts.save(temp_file.name)

    return history, history, temp_file.name

with gr.Blocks() as demo:
    gr.Markdown("## 🎙️ Groq Conversational Chatbot with Voice")

    chatbot_ui = gr.Chatbot(type="messages") 
    msg = gr.Textbox(label="Type your message and press Enter")
    audio_output = gr.Audio(label="AI Voice", type="filepath")
    clear_btn = gr.Button("Clear Chat")

    msg.submit(chatbot, [msg, chatbot_ui], [chatbot_ui, chatbot_ui, audio_output])
    clear_btn.click(lambda: ([], [], None), None, [chatbot_ui, msg, audio_output])

if __name__ == "__main__":
    demo.launch()
