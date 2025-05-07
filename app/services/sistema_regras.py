from experta import *

# Lista de sintomas válidos
SINTOMAS_VALIDOS = [
    'nao_liga', 'sem_som_ou_luz', 'ventoinhas_paradas',
    'tela_azul', 'travamentos', 'reinicializacao_inesperada',
    'lentidao', 'arquivos_corrompidos', 'erros_leitura_gravacao', 'aquecimento'
]

class Sintoma(Fact):
    """Fato representando um sintoma do computador."""
    pass

class SistemaRegras(KnowledgeEngine):
    def __init__(self):
        super().__init__()
        self.diagnostico_final = None
        self.fatos_relevantes = []

    def reset(self):
        super().reset()
        self.diagnostico_final = None
        self.fatos_relevantes = []

    @Rule(Sintoma(nao_liga=True), Sintoma(ventoinhas_paradas=True))
    def fonte_alimentacao(self):
        self.diagnostico_final = "Fonte de alimentação com defeito"

    @Rule(Sintoma(tela_azul=True), Sintoma(reinicializacao_inesperada=True))
    def memoria_defeituosa(self):
        self.diagnostico_final = "Problema na memória RAM"

    @Rule(Sintoma(lentidao=True), Sintoma(erros_leitura_gravacao=True))
    def hd_com_defeito(self):
        self.diagnostico_final = "Disco rígido (HD) com defeito"

    @Rule(Sintoma(travamentos=True), Sintoma(aquecimento=True))
    def superaquecimento(self):
        self.diagnostico_final = "Processador superaquecendo"

    @Rule(Sintoma(nao_liga=True), Sintoma(sem_som_ou_luz=True))
    def placa_mae(self):
        self.diagnostico_final = "Problema na placa-mãe"
    

    def run_with_facts(self, fatos_dict):
        self.reset()
        self.fatos_relevantes = fatos_dict
        for sintoma in fatos_dict:
            self.declare(Sintoma(**{sintoma: True}))
        self.run()
        return self.diagnostico_final

    def sintomas_necessarios(self):
        """
        Retorna os sintomas relevantes que podem levar a diagnósticos,
        filtrando os que ainda não foram fornecidos.
        """
        regras_sintomas = [
            {'nao_liga', 'ventoinhas_paradas'},
            {'tela_azul', 'reinicializacao_inesperada'},
            {'lentidao', 'erros_leitura_gravacao'},
            {'travamentos', 'aquecimento'},
            {'nao_liga', 'sem_som_ou_luz'}
        ]
        fornecidos = set(self.fatos_relevantes.keys())
        sintomas_faltando = set()

        for regra in regras_sintomas:
            faltam = regra - fornecidos
            if len(faltam) == 1:  
                sintomas_faltando.update(faltam)
        return list(sintomas_faltando)


# Funções públicas para integração

def evaluate_rules(fatos_lista):
    """
    fatos_lista: lista de strings no formato sintoma('nome')
    Retorna o diagnóstico ou None
    """
    fatos_dict = {}
    for fato in fatos_lista:
        if "sintoma(" in fato:
            nome = fato.replace("sintoma(", "").replace(")", "").replace("'", "").strip()
            if nome in SINTOMAS_VALIDOS:
                fatos_dict[nome] = True

    engine = SistemaRegras()
    return engine.run_with_facts(fatos_dict)


def get_missing_symptoms(fatos_lista):
    fatos_dict = {}
    for fato in fatos_lista:
        if "sintoma(" in fato:
            nome = fato.replace("sintoma(", "").replace(")", "").replace("'", "").strip()
            if nome in SINTOMAS_VALIDOS:
                fatos_dict[nome] = True

    engine = SistemaRegras()
    engine.run_with_facts(fatos_dict)
    return engine.sintomas_necessarios()
