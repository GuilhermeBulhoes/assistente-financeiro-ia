import os
from dotenv import load_dotenv
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from openai import OpenAI

load_dotenv()

app = Flask(__name__)


import os
api_key = os.getenv("OPENAI_API_KEY")

@app.route("/whatsapp", methods=['POST'])
def whatsapp_reply():
    user_msg = request.form.get('Body')
    
    try:
       
        completion = client.chat.completions.create(
            model="gpt-4", 
            messages=[
                {"role": "system", "content": "Você é um assistente financeiro. Extraia item e valor."},
                {"role": "user", "content": user_msg}
            ]
        )
        
        
        resposta_ia = completion.choices[0].message.content

    except Exception as e:
        print(f"ERRO NA IA: {e}")
        resposta_ia = f"Erro no cérebro: {e}"

    resp = MessagingResponse()
    resp.message(f"IA FINANCEIRA: {resposta_ia}")
    return str(resp)

if __name__ == "__main__":
    app.run(port=5000)
