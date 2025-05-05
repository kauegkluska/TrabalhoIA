from experta import *
import re

class Sintoma(Fact):
    """Fato que representa um sintoma relatado pelo usuário."""
    pass

class SistemaRegras(KnowledgeEngine):
    def __init__(self):
        super().__init__()
        self.respostas = []

    @Rule(Sintoma(sintoma='nao_liga'))
    def regra_energia(self):
        self.respostas.append("Verifique se o cabo de energia está conectado e a fonte está funcionando.")

    @Rule(Sintoma(sintoma='tela_azul'))
    def regra_tela_azul(self):
        self.respostas.append("A tela azul pode ser causada por erro de driver ou falha na memória RAM.")

    @Rule(Sintoma(sintoma='lento'))
    def regra_lentidao(self):
        self.respostas.append("O sistema pode estar sobrecarregado. Verifique processos em segundo plano ou vírus.")

    @Rule(Sintoma(sintoma='superaquecendo'))
    def regra_aquecimento(self):
        self.respostas.append("Limpe as ventoinhas e verifique se o cooler está funcionando.")

    @Rule(Sintoma(sintoma='bips'))
    def regra_bips(self):
        self.respostas.append("Verifique memória RAM, processador e placa de vídeo.")

    @Rule(AND(Sintoma(sintoma='nao_liga'), Sintoma(sintoma='led_piscando')))
    def regra_fonte_defeituosa(self):
        self.respostas.append("Possível falha na fonte de alimentação. Teste com outra fonte ou meça a tensão.")

    @Rule(AND(Sintoma(sintoma='tela_azul'), Sintoma(sintoma='ram_quente')))
    def regra_ram_aquecida(self):
        self.respostas.append("RAM com temperatura elevada. Verifique dissipadores e posição dos módulos.")

    @Rule(AND(Sintoma(sintoma='lento'), Sintoma(sintoma='cpu_quente')))
    def regra_cpu_aquecida(self):
        self.respostas.append("CPU aquecida. Limpe o cooler e aplique nova pasta térmica.")

    @Rule(
        OR(
            AND(Sintoma(sintoma='nao_liga'), Sintoma(sintoma='cheiro_queimado')),
            AND(Sintoma(sintoma='superaquecendo'), Sintoma(sintoma='desliga_sozinho'))
        )
    )
    def regra_curto_circuito(self):
        self.respostas.append("Há indícios de curto-circuito. Desligue imediatamente e inspecione placa-mãe e cabos.")

def evaluate_rules(fatos_str):
    padrao = r"sintoma\('([a-zA-Z0-9_ ]+)'\)"
    sintomas_extraidos = re.findall(padrao, fatos_str)

    engine = SistemaRegras()
    engine.reset()

    for sintoma in sintomas_extraidos:
        engine.declare(Sintoma(sintoma=sintoma.strip().lower()))

    engine.run()

    if engine.respostas:
        return "\n".join(f"- {resposta}" for resposta in engine.respostas)
    else:
        return "Não foram encontrados sintomas reconhecíveis."
