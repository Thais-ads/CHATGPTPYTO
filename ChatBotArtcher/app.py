from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import openai

app = Flask(__name__)
CORS(app)  # Configuração do CORS para permitir solicitações de qualquer origem

# Chave de API do OpenAI
openai.api_key = "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"

# Função para enviar mensagens para o ChatGPT usando a API da OpenAI
def send_message_to_chatgpt(conversation):
    api_url = "https://api.openai.com/v1/engines/gpt-3.5-turbo/completions"
    headers = {
        "Authorization": f"Bearer {openai.api_keyEY}",
        "Content-Type": "application/json",
    }
    data = {
        "messages": conversation,
    }
    response = requests.post(api_url, headers=headers, json=data)
    return response.json()

@app.route("/chat", methods=["POST"])
def chat():
    try:
        # Recebe a entrada do usuário da página da web
        user_input = request.json.get("user_input")
        print("User Input:", user_input)

        # Acessa o conteúdo do arquivo de texto
        with open("contexto.txt", "r") as file:
            context = file.read()

        # Crie uma conversa
        conversation = [
            {"role": "system", "content": "Você é um chatbot chamado Arthur que indica restaurantes para os usuários. Use somente o artigo fornecido para responder às perguntas"},
            {"role": "system", "content": "Caso não possua os dados no artigo escreva: Me desculpe não possuo sugestões para esse assunto."},
            {"role": "user", "content": context},
            {"role": "user", "content": user_input},  # Adicionar a entrada do usuário
        ]

        # Parâmetros da solicitação
        params = {
            "model": "gpt-3.5-turbo",
            "messages": conversation,
            "max_tokens": 300,  # Número máximo de tokens na resposta
            "temperature": 0.9  # Temperatura da resposta (quanto maior, mais aleatória)
    }

        # Enviar a solicitação para a API do ChatGPT
        resposta = openai.ChatCompletion.create(**params)
        print("Resposta da API:", resposta)

        # A resposta da API do ChatGPT está dentro da chave 'choices'
        choices = resposta.choices[0].message['content']
        print(choices)

        if choices:
            # Acesse a primeira escolha (pode haver várias, mas pegaremos a primeira)
            #first_choice = choices[0]

            #my_list = list(first_choice)

            #json_data = json.dumps(my_list)

            # Retorne a resposta para a página da web
            return choices
        else:
            # Se 'choices' estiver ausente ou vazio, retorne uma resposta vazia
            return jsonify({"assistant_response": ""})
    except Exception as e:
        print("Erro:", str(e))
        return jsonify({"error": str(e)})
    
if __name__ == "__main__":
    app.run()