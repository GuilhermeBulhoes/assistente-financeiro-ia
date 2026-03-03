# 💰 Assistente Financeiro Pessoal - WhatsApp + IA (GPT-4)

Este projeto é um bot de automação financeira que recebe mensagens de gastos pelo **WhatsApp**, utiliza Processamento de Linguagem Natural (NLP) via **OpenAI** para entender o valor e a categoria, e processa tudo através de um servidor **Flask**.

## 🛠️ Tecnologias e Ferramentas
*   **Python 3.14**: Linguagem principal do projeto.
*   **OpenAI API (GPT-4-mini)**: Cérebro da IA para interpretar mensagens naturais.
*   **Twilio API**: Interface de comunicação para o WhatsApp.
*   **Flask (Python)**: Framework para criação do servidor Webhook.
*   **ngrok**: Túnel seguro para expor o servidor local para a internet.
*   **python-dotenv**: Segurança para gerenciar chaves de API.

## 🚀 Como Funciona (Fluxo de Dados)
1. O usuário envia: *"Gastei 50 com pizza"* no WhatsApp.
2. O **Twilio** recebe e envia um `POST` para a URL do **ngrok**.
3. O servidor **Flask** no meu PC processa a mensagem.
4. A **IA da OpenAI** extrai: `Item: Pizza` | `Valor: R$ 50,00`.
5. O robô responde formatado de volta no WhatsApp.

## 📸 Demonstração
![Screenshot do WhatsApp](./whatsapp-demo.png)
*(Aqui você deve subir um print da conversa que você teve hoje com o robô)*

---
### 🔒 Segurança
O projeto utiliza um arquivo `.env` para proteger a `OPENAI_API_KEY`, garantindo que credenciais sensíveis não sejam expostas publicamente no repositório.
