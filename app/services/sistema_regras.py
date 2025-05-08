from experta import *

# Lista de sintomas válidos, incluindo códigos de bips para ASRock, Gigabyte e ASUS
SINTOMAS_VALIDOS = [
    'nao_liga', 'sem_som_ou_luz', 'ventoinhas_paradas',
    'tela_azul', 'travamentos', 'reinicializacao_inesperada',
    'lentidao', 'arquivos_corrompidos', 'erros_leitura_gravacao', 'aquecimento',
    # Beeps ASRock
    'bip_asrock_1_curto', 'bip_asrock_2_curto', 'bip_asrock_3_curto', 'bip_asrock_continuo',
    # Beeps Gigabyte
    'bip_gigabyte_1_longo_2_curto', 'bip_gigabyte_1_longo_3_curto', 'bip_gigabyte_continuo',
    # Beeps ASUS
    'bip_asus_1_curto', 'bip_asus_2_curto', 'bip_asus_3_curto', 'bip_asus_continuo'
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

    # Regras existentes
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

    # Regras para beeps ASRock
    @Rule(Sintoma(bip_asrock_1_curto=True))
    def asrock_dram_refresh(self):
        self.diagnostico_final = "Falha de renovação DRAM (ASRock)"

    @Rule(Sintoma(bip_asrock_2_curto=True))
    def asrock_parity(self):
        self.diagnostico_final = "Falha de circuito de paridade (ASRock)"

    @Rule(Sintoma(bip_asrock_3_curto=True))
    def asrock_ram_64k(self):
        self.diagnostico_final = "Falha de 64K de RAM base (ASRock)"

    @Rule(Sintoma(bip_asrock_continuo=True))
    def asrock_power(self):
        self.diagnostico_final = "Problema de fonte ou placa-mãe (ASRock)"

    # Regras para beeps Gigabyte
    @Rule(Sintoma(bip_gigabyte_1_longo_2_curto=True))
    def gigabyte_vga(self):
        self.diagnostico_final = "Falha de placa de vídeo (Gigabyte)"

    @Rule(Sintoma(bip_gigabyte_1_longo_3_curto=True))
    def gigabyte_memory(self):
        self.diagnostico_final = "Falha de memória (Gigabyte)"

    @Rule(Sintoma(bip_gigabyte_continuo=True))
    def gigabyte_power(self):
        self.diagnostico_final = "Erro de energia ou placa-mãe (Gigabyte)"

    # Regras para beeps ASUS
    @Rule(Sintoma(bip_asus_1_curto=True))
    def asus_normal(self):
        self.diagnostico_final = "Inicialização bem-sucedida (ASUS)"

    @Rule(Sintoma(bip_asus_2_curto=True))
    def asus_ram(self):
        self.diagnostico_final = "Erro de memória RAM (ASUS)"

    @Rule(Sintoma(bip_asus_3_curto=True))
    def asus_vga(self):
        self.diagnostico_final = "Falha de placa de vídeo (ASUS)"

    @Rule(Sintoma(bip_asus_continuo=True))
    def asus_power(self):
        self.diagnostico_final = "Problema de fonte de alimentação (ASUS)"

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
