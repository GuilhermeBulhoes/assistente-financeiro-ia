import os
import psycopg2
from dotenv import load_dotenv
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from openai import OpenAI

load_dotenv()

app = Flask(__name__)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
DATABASE_URL = os.getenv("DATABASE_URL")
TWILIO_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")

@app.route("/whatsapp", methods=['POST'])
def whatsapp_reply():
    user_msg = request.form.get('Body')
    confirmacao_banco = ""

    try:
        
        completion = client.chat.completions.create(
            model="gpt-4o-mini", #Depois trocar progpt-4o-mini
            messages=[
                {"role": "system", "content": "Você é um assistente financeiro. Extraia item e valor."},
                {"role": "user", "content": user_msg}
            ]
        )
        
        
        resposta_ia = completion.choices[0].message.content

        #Bloco Banco de Dados
        try:
             conn = psycopg2.connect(DATABASE_URL)
             cur = conn.cursor()
             # Cria a tabela se ela ainda não existir
             cur.execute("CREATE TABLE IF NOT EXISTS historico (id SERIAL PRIMARY KEY, descricao TEXT, data TIMESTAMP DEFAULT CURRENT_TIMESTAMP);")
             # Insere a resposta da IA no banco
             cur.execute("INSERT INTO historico (descricao) VALUES (%s)", (resposta_ia,))
             # Isso adiciona novas colunas sem apagar a 'descricao' que você já tem
             cur.execute("ALTER TABLE historico ADD COLUMN IF NOT EXISTS valor NUMERIC;")
             cur.execute("ALTER TABLE historico ADD COLUMN IF NOT EXISTS categoria TEXT;")
             conn.commit()
             cur.close()
             conn.close()
        
        except Exception as db_error:
             print(f"Erro ao salvar no Neon: {db_error}")
             confirmacao_banco = "\n(Erro ao salvar no banco, mas processei o texto.)"

    except Exception as e:
        print(f"ERRO NA IA: {e}")
        resposta_ia = f"Erro no cérebro: {e}"

    resp = MessagingResponse()
    resp.message(f"GPTech: {resposta_ia} {confirmacao_banco}")
    return str(resp)

if __name__ == "__main__":
    app.run(port=5000) 
