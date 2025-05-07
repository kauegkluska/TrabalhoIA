from app.services.sistema_regras import evaluate_rules, get_missing_symptoms
from openai import OpenAI

client = OpenAI(api_key="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")

ultima_pergunta = ""

SINTOMAS_VALIDOS = [
    'nao_liga', 'sem_som_ou_luz', 'ventoinhas_paradas',
    'tela_azul', 'travamentos', 'reinicializacao_inesperada',
    'lentidao', 'arquivos_corrompidos', 'erros_leitura_gravacao', 'aquecimento'
]

def extrair_sintomas(texto_usuario):
    
    print(ultima_pergunta)
    
    if ultima_pergunta != "":
        system_prompt = (
            "Você é um assistente que transforma sintomas descritos em linguagem natural "
            "em fatos no formato sintoma('nome_do_sintoma') para um sistema especialista de manutenção de computadores. "
            f"Os sintomas válidos são: {', '.join(SINTOMAS_VALIDOS)}. "
            "Se não identificar nenhum sintoma, responda sintoma('nenhum'). "
            f"Baseando-se na pergunta anterior '{ultima_pergunta}', extraia os sintomas do texto: {texto_usuario}"
        )
    
    else:
        system_prompt = (
            "Você é um assistente que transforma sintomas descritos em linguagem natural "
            "em fatos no formato sintoma('nome_do_sintoma') para um sistema especialista de manutenção de computadores. "
            f"Os sintomas válidos são: {', '.join(SINTOMAS_VALIDOS)}. "
            "Se não identificar nenhum sintoma, responda sintoma('nenhum')."
            f"Extraia os sintomas do texto: {texto_usuario}"
            
        )
    
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",  
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": texto_usuario}
        ]
    )
    
    return response.choices[0].message.content.strip()


def gerar_pergunta(sintomas_faltando):
    
    print(sintomas_faltando)
    system_prompt = (
        "Você é um assistente que faz perguntas para ajudar a diagnosticar problemas de computador. "
        "pergunte se o usuario enfrentou problema com esse sintoma: "
        f"{', '.join(sintomas_faltando)}. "
    )
    
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": "Formule uma pergunta baseada nesses sintomas."}
        ]
    )
    global ultima_pergunta
    ultima_pergunta = response.choices[0].message.content.strip()
    
    return response.choices[0].message.content.strip()


def descrever_diagnostico(diagnostico):
    system_prompt = (
        "Você é um assistente técnico que explica problemas de computador e sugere soluções. "
        f"Com base no diagnóstico '{diagnostico}', fale o problema para o usuário, e de um passo a passo de como resolver-lo"
    )
    
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": diagnostico}
        ]
    )
    
    
    return response.choices[0].message.content.strip()


def get_chat_response(user_input, fatos_anteriores=[]):
    
    fatos_texto = extrair_sintomas(user_input)
    
    novos_fatos = [f for f in fatos_texto.splitlines() if f not in fatos_anteriores and "nenhum" not in f]
    fatos_anteriores += novos_fatos

    diagnostico = evaluate_rules(fatos_anteriores)

    if diagnostico:
        global ultima_pergunta
        ultima_pergunta = ""
        return descrever_diagnostico(diagnostico)
    else:
        sintomas_faltando = get_missing_symptoms(fatos_anteriores)
        if sintomas_faltando:
            return gerar_pergunta(sintomas_faltando)
        else:
            return "Ainda não consigo determinar o problema com base nas informações fornecidas. Você pode descrever mais sintomas?"
