import os
import json
import psycopg2
from dotenv import load_dotenv
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from openai import OpenAI

load_dotenv()
app = Flask(__name__)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
DATABASE_URL = os.getenv("DATABASE_URL")

# --- CONFIGURAÇÃO INICIAL DO BANCO (Roda apenas quando o app inicia) ---
def inicializar_banco():
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        # Cria a tabela já com todas as colunas corretas se não existirem
        cur.execute("""
            CREATE TABLE IF NOT EXISTS historico (
                id SERIAL PRIMARY KEY,
                descricao TEXT,
                valor NUMERIC,
                categoria TEXT,
                data TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        conn.commit()
        cur.close()
        conn.close()
        print("Banco de dados verificado com sucesso!")
    except Exception as e:
        print(f"Erro ao inicializar o banco: {e}")

# Executa a criação da estrutura antes do app rodar
inicializar_banco()


@app.route("/whatsapp", methods=['POST'])
def whatsapp_reply():
    user_msg = request.form.get('Body')
    confirmacao_banco = ""
    resposta_para_usuario = ""

    try:
        # Pedimos para a IA responder estritamente em formato JSON para podermos separar os dados
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            response_format={ "type": "json_object" }, # Força a IA a devolver um JSON válido
            messages=[
                {
                    "role": "system", 
                    "content": (
                        "Você é um assistente financeiro. Extraia as informações do texto do usuário "
                        "e responda estritamente no seguinte formato JSON:\n"
                        '{"descricao": "nome do item", "valor": 0.00, "categoria": "categoria do gasto"}\n'
                        "Se o usuário não disser a categoria, defina uma padrão."
                    )
                },
                {"role": "user", "content": user_msg}
            ]
        )
        
        # Transforma o texto da IA em um dicionário do Python
        dados_ia = json.loads(completion.choices[0].message.content)
        descricao = dados_ia.get("descricao")
        valor = dados_ia.get("valor")
        categoria = dados_ia.get("categoria")

        # Texto que vai aparecer no WhatsApp do usuário
        resposta_para_usuario = f"Gasto registrado!\n• Item: {descricao}\n• Valor: R$ {valor:.2f}\n• Categoria: {categoria}"

        # --- BLOCO DO BANCO DE DADOS ---
        try:
            conn = psycopg2.connect(DATABASE_URL)
            cur = conn.cursor()
            
            # Insere cada dado na sua respectiva coluna
            cur.execute(
                "INSERT INTO historico (descricao, valor, categoria) VALUES (%s, %s, %s)", 
                (descricao, valor, categoria)
            )
            
            conn.commit()
            cur.close()
            conn.close()
            confirmacao_banco = "\n\n Salvo no banco Neon!"
        except Exception as db_error:
            print(f"Erro ao salvar no Neon: {db_error}")
            confirmacao_banco = "\n\n⚠️ (Erro ao salvar no banco, mas a IA processou)."

    except Exception as e:
        print(f"ERRO GERAL: {e}")
        resposta_para_usuario = f"Erro ao processar mensagem."

    # Resposta final do Twilio para o WhatsApp
    resp = MessagingResponse()
    resp.message(f"GPTech:\n{resposta_para_usuario}{confirmacao_banco}")
    return str(resp)


if __name__ == "__main__":
    app.run(port=5000)

