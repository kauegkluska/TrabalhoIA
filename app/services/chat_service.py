from app.services.sistema_regras import evaluate_rules, get_missing_symptoms
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)

ultima_pergunta = ""
sintoma_em_pergunta = ""  
sintomas_negados = set()

SINTOMAS_VALIDOS = [
    'lentidao_geral', 'travamentos', 'erros_de_arquivo', 'problemas_de_boot',
    'problemas_de_video', 'problemas_de_audio', 'problemas_de_rede',
    'superaquecimento', 'ruidos_estranhos', 'desligamentos_involuntarios',
    'falha_de_componente', 'instabilidade_apos_atualizacao',
    'comportamento_incomum_software', 'reinicializacoes_involuntarias',
    'tela_azul', 'ausencia_de_audio', 'congelamento_de_tela', 'perda_de_dados',
    'aplicativos_nao_respondem', 'teclado_nao_funciona', 'mouse_nao_funciona',
    'leds_piscando', 'barulho_hd_alto', 'imagem_distorcida', 'conexao_lenta',
    'impossibilidade_imprimir', 'camera_nao_funciona', 'microfone_nao_funciona'
]



def _llm_call(prompt):
    """Função auxiliar para fazer chamadas ao modelo de linguagem."""
    response = client.chat.completions.create(
        model="gpt-3.5-turbo", 
        messages=[{"role": "system", "content": prompt}]
    )
    result = response.choices[0].message.content.strip()
    print(f"Response: {result}")
    return result

def extrair_sintomas(texto_usuario):
    """Extrai sintomas válidos do texto do usuário."""
    prompt = (
        "Você é um assistente técnico especializado em diagnosticar problemas de computador.\n"
        f"Considere os seguintes sintomas válidos (use apenas exatamente como listados): {', '.join(SINTOMAS_VALIDOS)}.\n\n"
        "Sua tarefa é analisar a mensagem do usuário e identificar quais desses sintomas estão presentes.\n"
        "Para cada sintoma identificado, você deve retornar **exatamente** no formato:\n"
        "    sintoma('nome_do_sintoma')\n"
        "Exemplo: sintoma('travamentos')\n\n"
        "Não reescreva, resuma ou explique nada. Apenas retorne uma ou mais linhas com os sintomas no formato exato acima.\n\n"
        "Se o usuário negar claramente o a pergunta e o sintoma mencionado usando termos como 'não', 'nunca', ou 'jamais', retorne apenas:\n"
        "    negado\n\n"
        "Se o usuário confirmar claramente o sintoma mencionado usando termos como 'sim', 'exato', 'correto', retorne no formato:\n"
        "   sintoma('nome_do_sintoma')\n\n"
        "Se não houver menção a nenhum dos sintomas válidos, retorne apenas:\n"
        "    sintoma('nenhum')\n\n"
    )

    if ultima_pergunta:
        prompt += f"Considere que a pergunta anterior foi: '{ultima_pergunta}' e o sintoma na pergunta foi '{sintoma_em_pergunta}'.\n\n"

    prompt += f"Mensagem do usuário: '{texto_usuario}'\n\n"
    prompt += "⚠️ Saída obrigatória: uma ou mais linhas com o formato sintoma('nome_do_sintoma'), ou uma única linha com 'negado' ou sintoma('nenhum').\n"
    prompt += "Não inclua explicações ou qualquer outro conteúdo.\n\n"
    prompt += "Sintomas extraídos:"

    return _llm_call(prompt)


def gerar_pergunta(sintomas_faltando):
    """Gera uma pergunta para o usuário com base nos sintomas faltantes."""
    global ultima_pergunta, sintoma_em_pergunta
    if not sintomas_faltando:
        return None
    sintoma_principal = sintomas_faltando[0]
    sintoma_em_pergunta = sintoma_principal 
    prompt = (
        "Você é um assistente que formula perguntas concisas para diagnosticar problemas de computador.\n"
        f"Dado o possível sintoma: '{sintoma_principal}', formule uma pergunta direta ao usuário "
        f"para saber se ele está enfrentando esse problema. Responda apenas com a pergunta."
    )
    ultima_pergunta = _llm_call(prompt)
    return ultima_pergunta

def descrever_diagnostico(diagnostico):
    """Descreve o diagnóstico para o usuário e sugere soluções."""
    prompt = (
        "Você é um técnico de informática explicando problemas de computador e suas soluções.\n"
        "Primeiro, apenas nomeie o diagnóstico. Em seguida, explique o diagnóstico de forma clara e forneça um breve passo a passo para resolução:\n\n"
        f"Diagnóstico: '{diagnostico}'\n\n"
        "Formato de Resposta Esperado:\n"
        "Nome do Diagnóstico: [Nome do Diagnóstico]\n"
        "Explicação e passos para resolução: [Explicação e passos para resolução]"
    )
    return _llm_call(prompt)
def get_chat_response(user_input, fatos_anteriores=set()):
    """Obtém a resposta do chat, integrando extração de sintomas e sistema especialista."""
    global ultima_pergunta, sintoma_em_pergunta

    fatos_texto = extrair_sintomas(user_input)

    if 'negado' in fatos_texto:
        if sintoma_em_pergunta:
            sintomas_negados.add(sintoma_em_pergunta)

    novos_fatos = {f.strip() for f in fatos_texto.splitlines() if "nenhum" not in f}
    fatos_anteriores.update(novos_fatos)

    if not fatos_anteriores:
        return "Olá! Descreva os sintomas do seu computador para que eu possa ajudar."

    resultado_diagnostico = evaluate_rules(list(fatos_anteriores))

    if isinstance(resultado_diagnostico, str) and "Diagnóstico:" in resultado_diagnostico:
        ultima_pergunta = ""
        sintoma_em_pergunta = ""
        fatos_anteriores.clear()
        return descrever_diagnostico(resultado_diagnostico)
    
    sintomas_faltando_dict = get_missing_symptoms(fatos_anteriores)
    if sintomas_faltando_dict:
        sintomas_faltando_dict_filtrado = {}

        for diagnostico, sintomas_lista in sintomas_faltando_dict.items():
            sintomas_filtrados = [s for s in sintomas_lista if s not in sintomas_negados]
            if sintomas_filtrados:
                sintomas_faltando_dict_filtrado[diagnostico] = sintomas_filtrados

        if sintomas_faltando_dict_filtrado:
            primeiro_diagnostico = list(sintomas_faltando_dict_filtrado.keys())[0]
            sintomas_faltando = sintomas_faltando_dict_filtrado[primeiro_diagnostico]
            return gerar_pergunta(sintomas_faltando)

    return "Não consigo diagnosticar o problema com as informações fornecidas. Poderia dar mais detalhes?"
