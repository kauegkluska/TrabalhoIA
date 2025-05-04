from experta import *
import re

class Sintoma(Fact):
    """Fato que representa um sintoma relatado pelo usuário."""
    pass

class SistemaRegras(KnowledgeEngine):
    def __init__(self):
        super().__init__()
        self.respostas = []

    @Rule(Sintoma(sintoma='tela_preta'))
    def tratar_tela_preta(self):
        self.respostas.append("Verifique a conexão do monitor e o cabo de energia.")

    @Rule(Sintoma(sintoma='nao_liga'))
    def tratar_nao_liga(self):
        self.respostas.append("Verifique a fonte de alimentação ou a bateria.")

    @Rule(Sintoma(sintoma='barulho'))
    def tratar_barulho(self):
        self.respostas.append("Verifique os ventiladores e possíveis objetos presos.")

    @Rule(Sintoma(sintoma='superaquecendo'))
    def tratar_superaquecendo(self):
        self.respostas.append("Verifique se as ventoinhas estão funcionando e limpe a poeira.")

    @Rule(Sintoma(sintoma='lento'))
    def tratar_lento(self):
        self.respostas.append("Verifique o uso de CPU/memória e programas em segundo plano.")

def evaluate_rules(fatos_str):
    padrao = r"sintoma\('([a-zA-Z0-9_ ]+)'\)"
    sintomas_extraidos = re.findall(padrao, fatos_str)

    engine = SistemaRegras()
    engine.reset()

    for sintoma in sintomas_extraidos:
        engine.declare(Sintoma(sintoma=sintoma))

    engine.run()

    if engine.respostas:
        return "\n".join(f"- {resposta}" for resposta in engine.respostas)
    else:
        return "Não foram encontrados sintomas reconhecíveis."
