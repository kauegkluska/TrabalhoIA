from app.services.sistema_regras import evaluate_rules
from openai import OpenAI

client = OpenAI(api_key="chave")

def get_chat_response(message):
    system_prompt = (
    "Você é um assistente que transforma sintomas descritos em linguagem natural "
    "em fatos no formato sintoma('nome_do_sintoma') para um sistema especialista de manutenção de computadores. "
    "A lista de sintomas válidos inclui: "
    "'tela_preta', 'sem_sinal', 'barulho_hd', 'nao_liga', 'reinicia', 'tela_azul', 'superaquecimento', 'travando', 'lentidao', 'erro_bios'. "
    "Só utilize sintomas dessa lista. Se não identificar nenhum, responda sintoma('nenhum')."
    )

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": message}
        ]
    )

    fatos_extraidos = response.choices[0].message.content
    return evaluate_rules(fatos_extraidos)
