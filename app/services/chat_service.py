from app.services.sistema_regras import evaluate_rules
from openai import OpenAI

client = OpenAI(api_key="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")

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
    diagnostico = evaluate_rules(fatos_extraidos)
    
    system_prompt = (
    "Você é um assistente que descreve um diagnóstico de computador em linguagem natural "
    "a partir do diagnóstico {diagnostico}. "
    )
    
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": diagnostico}
        ]
    )
    
    resposta = response.choices[0].message.content
    return resposta
