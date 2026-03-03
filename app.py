import os
from dotenv import load_dotenv
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from openai import OpenAI

load_dotenv()

app = Flask(__name__)

# Configuração correta para a versão nova da OpenAI
client = OpenAI(api_key="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")

@app.route("/whatsapp", methods=['POST'])
def whatsapp_reply():
    user_msg = request.form.get('Body')
    
    try:
        # Sintaxe atualizada para OpenAI 1.0+
        completion = client.chat.completions.create(
            model="gpt-4", # Mais barato e rápido para economizar seu saldo
            messages=[
                {"role": "system", "content": "Você é um assistente financeiro. Extraia item e valor."},
                {"role": "user", "content": user_msg}
            ]
        )
        
        # Acesso correto ao conteúdo
        resposta_ia = completion.choices[0].message.content

    except Exception as e:
        print(f"ERRO NA IA: {e}")
        resposta_ia = f"Erro no cérebro: {e}"

    resp = MessagingResponse()
    resp.message(f"IA FINANCEIRA: {resposta_ia}")
    return str(resp)

if __name__ == "__main__":
    app.run(port=5000)
