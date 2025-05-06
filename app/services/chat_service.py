from app.services.sistema_regras import evaluate_rules
from openai import OpenAI

client = OpenAI(api_key="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")

def get_chat_response(message):
    system_prompt = (
    "Você é um assistente que transforma sintomas descritos em linguagem natural "
    "em fatos no formato sintoma('nome_do_sintoma') para um sistema especialista de manutenção de computadores. "
    "A lista de sintomas válidos inclui: "
    "'nao_liga','sem_som_ou_luz','ventoinhas_paradas'"
    "'tela_azul','travamentos','reinicializacao_inesperada',"
    "'lentidao','arquivos_corrompidos','erros_leitura_gravacao',"
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
    print(fatos_extraidos)
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
