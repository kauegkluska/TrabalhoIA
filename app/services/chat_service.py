from app.services.sistema_regras import evaluate_rules, get_missing_symptoms
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
AP = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=AP)

ultima_pergunta = ""

SINTOMAS_VALIDOS = [
    'lentidao_ao_abrir_arquivos', 'arquivos_corrompidos', 'erro_ao_copiar_arquivos',
    'travamento_ao_inicializar', 'clique_vindo_do_hd', 'desligamento_repentino',
    'travamento_em_uso_intenso', 'cooler_em_alta_velocidade', 'temperatura_acima_de_80',
    'lentidao_sem_motivo', 'nao_liga', 'reinicializacoes_aleatorias', 'componentes_sem_energia',
    'queima_frequente_de_componentes', 'cheiro_de_queimado', 'tela_azul', 'aplicacoes_fechando_sozinhas',
    'falha_na_instalacao_do_sistema', 'ram_mostrando_menos_que_instalada', 'nao_da_video',
    'hardware_nao_reconhecido', 'usb_nao_funciona', 'erros_de_post', 'instabilidade_geral',
    'loop_de_boot', 'arquivos_de_sistema_ausentes', 'menu_iniciar_nao_funciona',
    'travamentos_apos_atualizacao', 'tela_preta_pos_boot', 'resolucao_incorreta',
    'travamento_em_jogos', 'erro_no_driver_de_video', 'so_funciona_no_modo_seguro',
    'popups_no_navegador', 'arquivos_somem', 'programas_abrem_sozinhos', 'acesso_a_sites_estranhos',
    'artefatos_na_tela', 'sem_sinal_de_video', 'travamento_em_graficos', 'cooler_da_gpu_nao_gira',
    'driver_da_gpu_falha', 'aumento_rapido_de_temperatura', 'cooler_silencioso_ou_com_ruido',
    'desliga_apos_ligar', 'bios_indica_falha_na_ventoinha', 'cpu_queimada','Wifi_não_funciona_após_formatação','não_aparece_redes_wifi_para_se_conectar'
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
    
    print(response.choices[0].message.content.strip())
    
    return response.choices[0].message.content.strip()


def gerar_pergunta(sintomas_faltando):
    
    print(sintomas_faltando)
    system_prompt = (
        "Você é um assistente que faz perguntas para ajudar a diagnosticar problemas de computador. "
        "pergunte se o usuario enfrentou problema com esse sintoma (apenas e somente o primeiro item): "
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
    # Se não houver fatos anteriores, significa que é a primeira interação
    if not fatos_anteriores:
        # Extrair os sintomas do input inicial do usuário
        fatos_texto = extrair_sintomas(user_input)
        novos_fatos = [f for f in fatos_texto.splitlines() if "nenhum" not in f]
        fatos_anteriores += novos_fatos
        
        # Obter diagnóstico inicial ou próximos passos
        resultado = evaluate_rules(fatos_anteriores)
        
        # Se for a primeira mensagem e não houver sintomas identificados
        if not novos_fatos:
            return "Olá! Sou um sistema especialista em diagnóstico de problemas de computador. Para ajudá-lo melhor, preciso que você descreva os sintomas que seu computador está apresentando. Por exemplo: se está lento, travando, fazendo barulhos estranhos, não liga, etc. Quanto mais detalhes você fornecer, mais preciso será meu diagnóstico!"
    else:
        # Extrair os sintomas do input do usuário
        fatos_texto = extrair_sintomas(user_input)
        novos_fatos = [f for f in fatos_texto.splitlines() if f not in fatos_anteriores and "nenhum" not in f]
        fatos_anteriores += novos_fatos
        
        # Obter diagnóstico ou próximos passos
        resultado = evaluate_rules(fatos_anteriores)
    
    # Se o resultado for um dicionário com sintomas faltantes
    if isinstance(resultado, dict) and "sintomas_faltantes" in resultado:
        # Escolher a primeira regra e seus sintomas faltantes
        primeira_regra = list(resultado["sintomas_faltantes"].keys())[0]
        sintomas = list(resultado["sintomas_faltantes"][primeira_regra])[0]
        return gerar_pergunta([sintomas])
    
    # Se for um diagnóstico final
    elif isinstance(resultado, str) and "Diagnóstico:" in resultado:
        global ultima_pergunta
        ultima_pergunta = ""  # Resetar a pergunta anterior após diagnóstico
        fatos_anteriores.clear()  # Limpar o histórico de fatos após o diagnóstico
        return descrever_diagnostico(resultado)
    
    # Se for uma mensagem de orientação
    else:
        return resultado
