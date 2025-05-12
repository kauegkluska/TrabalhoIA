from app.services.sistema_regras import evaluate_rules, get_missing_symptoms
from openai import OpenAI

# Inicializa o cliente da OpenAI com a chave de API
client = OpenAI(api_key="a")

# Variável global para manter a última pergunta feita ao usuário
ultima_pergunta = ""

# Sintomas válidos
SINTOMAS_VALIDOS = [
    'nao_liga', 'sem_som_ou_luz', 'ventoinhas_paradas',
    'tela_azul', 'travamentos', 'reinicializacao_inesperada',
    'lentidao', 'arquivos_corrompidos', 'erros_leitura_gravacao', 'aquecimento',
    'bip_asrock_1_curto', 'bip_asrock_2_curtos', 'bip_asrock_3_curtos', 'bip_asrock_continuo',
    'bip_gigabyte_1_longo_2_curtos', 'bip_gigabyte_1_longo_3_curtos', 'bip_gigabyte_continuo',
    'bip_asus_1_curto', 'bip_asus_2_curtos', 'bip_asus_3_curtos', 'bip_asus_continuo',
    'bip_colorful_1_longo_2_curtos', 'bip_colorful_1_longo_3_curtos',
    'bip_colorful_3_longos', 'bip_colorful_5_longos', 'bip_colorful_ausente',
    'bateria_nao_carrega', 'bateria_dura_pouco', 'tela_nao_acende', 'teclado_nao_responde',
    'computador_desliga_quando_joga'
]

def extrair_sintomas(texto_usuario):
    print(ultima_pergunta)

    # Monta o prompt baseado se há uma pergunta anterior
    if ultima_pergunta != "":
        system_prompt = (
            "Você é um assistente que transforma sintomas descritos em linguagem natural "
            "em fatos no formato sintoma('nome_do_sintoma'), tipo_computador('pc' ou 'notebook') ou modelo('nome_do_modelo') "
            "para um sistema especialista de manutenção de computadores. "
            f"Os sintomas válidos são: {', '.join(SINTOMAS_VALIDOS)}. "
            "Os modelos válidos são: asus, asrock, gigabyte, colorful. "
            "Se não identificar nenhum fato, responda sintoma('nenhum'). "
            f"Baseando-se na pergunta anterior '{ultima_pergunta}', extraia os fatos do texto: {texto_usuario}"
        )
    else:
        system_prompt = (
            "Você é um assistente que transforma sintomas descritos em linguagem natural "
            "em fatos no formato sintoma('nome_do_sintoma'), tipo_computador('pc' ou 'notebook') ou modelo('nome_do_modelo') "
            "para um sistema especialista de manutenção de computadores. "
            f"Os sintomas válidos são: {', '.join(SINTOMAS_VALIDOS)}. "
            "Os modelos válidos são: asus, asrock, gigabyte, colorful. "
            "Se não identificar nenhum fato, responda sintoma('nenhum'). "
            f"Extraia os fatos do texto: {texto_usuario}"
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
        "Pergunte ao usuário se ele enfrentou problemas com algum destes sintomas: "
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
        f"Com base no diagnóstico '{diagnostico}', explique o problema para o usuário e forneça um passo a passo de como resolvê-lo."
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
    # Extrair sintomas com base no input do usuário
    fatos_texto = extrair_sintomas(user_input)
    novos_fatos = [
        f for f in fatos_texto.splitlines()
        if f not in fatos_anteriores and "nenhum" not in f
    ]
    fatos_anteriores += novos_fatos

    # Realizar a inferência para diagnóstico
    diagnostico = evaluate_rules(fatos_anteriores)

    if diagnostico:
        global ultima_pergunta
        ultima_pergunta = ""  # Resetar pergunta após diagnóstico
        return descrever_diagnostico(diagnostico)
    else:
        # Perguntar pelos sintomas faltando
        sintomas_faltando = get_missing_symptoms(fatos_anteriores)
        if sintomas_faltando:
            return gerar_pergunta(sintomas_faltando)
        else:
            return "Ainda não consigo determinar o problema com base nas informações fornecidas. Você pode descrever mais sintomas?"
