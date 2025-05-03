from experta import *

class Sintoma(Fact):
    """Fato que representa um sintoma informado pelo usuário."""
    pass

class SistemaManutencao(KnowledgeEngine):
    def __init__(self):
        super().__init__()
        self.resposta = None

    @Rule(Sintoma(desc='computador não liga'))
    def regra_energia(self):
        self.resposta = "Verifique se o cabo de energia está conectado e a fonte está funcionando."

    @Rule(Sintoma(desc='tela azul'))
    def regra_tela_azul(self):
        self.resposta = "A tela azul pode ser causada por erro de driver ou falha na memória RAM."

    @Rule(Sintoma(desc='muito lento'))
    def regra_lentidao(self):
        self.resposta = "O sistema pode estar sobrecarregado. Verifique processos em segundo plano ou vírus."

    @Rule(Sintoma(desc='superaquecendo'))
    def regra_aquecimento(self):
        self.resposta = "Limpe as ventoinhas e verifique se o cooler está funcionando."

def evaluate_rules(mensagem):
    engine = SistemaManutencao()
    engine.reset()
    engine.declare(Sintoma(desc=mensagem.lower()))
    engine.run()
    return engine.resposta
