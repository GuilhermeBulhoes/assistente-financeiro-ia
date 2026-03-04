import os
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from openai import OpenAI

app = Flask(__name__)


client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route("/whatsapp", methods=['POST'])
def whatsapp_reply():
    user_msg = request.form.get('Body')
    
    try:
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo", 
            messages=[
                {"role": "system", "content": "Você é um assistente financeiro. Extraia item e valor."},
                {"role": "user", "content": user_msg}
            ]
        )
        resposta_ia = completion.choices[0].message.content

    except Exception as e:
        print(f"ERRO NA IA: {e}")
        resposta_ia = "Ops, tive um problema para processar isso agora."

    resp = MessagingResponse()
    resp.message(f"IA FINANCEIRA: {resposta_ia}")
    return str(resp)

# 
@app.route("/")
def home():
    return "Robô Financeiro Rodando com Sucesso!"

if __name__ == "__main__":
    
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
