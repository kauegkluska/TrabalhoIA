from experta import *

# Lista de sintomas válidos, incluindo códigos de bips para ASRock, Gigabyte e ASUS e Colorful
SINTOMAS_VALIDOS = [
    # Sintomas genéricos
    'nao_liga', 'sem_som_ou_luz', 'ventoinhas_paradas',
    'tela_azul', 'travamentos', 'reinicializacao_inesperada',
    'lentidao', 'arquivos_corrompidos', 'erros_leitura_gravacao', 'aquecimento',
    # Beeps ASRock (1 curto, 2 curtos, 3 curtos, contínuo)
    'bip_asrock_1_curto', 'bip_asrock_2_curtos', 'bip_asrock_3_curtos', 'bip_asrock_continuo',
    # Beeps Gigabyte (1 longo + X curtos, contínuo)
    'bip_gigabyte_1_longo_2_curtos', 'bip_gigabyte_1_longo_3_curtos', 'bip_gigabyte_continuo',
    # Beeps ASUS (1 curto, 2 curtos, 3 curtos, contínuo)
    'bip_asus_1_curto', 'bip_asus_2_curtos', 'bip_asus_3_curtos', 'bip_asus_continuo',
    # Beeps Colorful (1 longo + X curtos, múltiplos longos, sem bip)
    'bip_colorful_1_longo_2_curtos', 'bip_colorful_1_longo_3_curtos',
    'bip_colorful_3_longos', 'bip_colorful_5_longos', 'bip_colorful_ausente'
]

class Sintoma(Fact):
    """Fato representando um sintoma do computador."""
    pass

class SistemaRegras(KnowledgeEngine):
    def __init__(self):
        super().__init__()
        # Lista para armazenar múltiplos diagnósticos
        self.diagnosticos = []
        self.fatos_relevantes = []

    def reset(self):
        super().reset()
        self.diagnosticos = []
        self.fatos_relevantes = []

    # ----- Regras base (necessitam de pares de sintomas) -----
    @Rule(Sintoma(nao_liga=True), Sintoma(ventoinhas_paradas=True))
    def fonte_alimentacao(self):
        self.diagnosticos.append("Fonte de alimentação com defeito")

    @Rule(Sintoma(tela_azul=True), Sintoma(reinicializacao_inesperada=True))
    def memoria_defeituosa(self):
        self.diagnosticos.append("Problema na memória RAM")

    @Rule(Sintoma(lentidao=True), Sintoma(erros_leitura_gravacao=True))
    def hd_com_defeito(self):
        self.diagnosticos.append("Disco rígido (HD) com defeito")

    @Rule(Sintoma(travamentos=True), Sintoma(aquecimento=True))
    def superaquecimento(self):
        self.diagnosticos.append("Processador superaquecendo")

    @Rule(Sintoma(nao_liga=True), Sintoma(sem_som_ou_luz=True))
    def placa_mae(self):
        self.diagnosticos.append("Problema na placa-mãe")

    # ----- Regras de bips ASRock -----
    @Rule(Sintoma(bip_asrock_1_curto=True))
    def asrock_dram_refresh(self):
        self.diagnosticos.append("Falha de renovação DRAM (ASRock)")

    @Rule(Sintoma(bip_asrock_2_curtos=True))
    def asrock_parity(self):
        self.diagnosticos.append("Falha de circuito de paridade (ASRock)")

    @Rule(Sintoma(bip_asrock_3_curtos=True))
    def asrock_ram_64k(self):
        self.diagnosticos.append("Falha de 64K de RAM base (ASRock)")

    @Rule(Sintoma(bip_asrock_continuo=True))
    def asrock_power(self):
        self.diagnosticos.append("Problema de fonte ou placa-mãe (ASRock)")

    # ----- Regras de bips Gigabyte -----
    @Rule(Sintoma(bip_gigabyte_1_longo_2_curtos=True))
    def gigabyte_vga(self):
        self.diagnosticos.append("Falha de placa de vídeo (Gigabyte)")

    @Rule(Sintoma(bip_gigabyte_1_longo_3_curtos=True))
    def gigabyte_memory(self):
        self.diagnosticos.append("Falha de memória (Gigabyte)")

    @Rule(Sintoma(bip_gigabyte_continuo=True))
    def gigabyte_power(self):
        self.diagnosticos.append("Erro de energia ou placa-mãe (Gigabyte)")

    # ----- Regras de bips ASUS -----
    @Rule(Sintoma(bip_asus_1_curto=True))
    def asus_normal(self):
        self.diagnosticos.append("Inicialização bem-sucedida (ASUS)")

    @Rule(Sintoma(bip_asus_2_curtos=True))
    def asus_ram(self):
        self.diagnosticos.append("Erro de memória RAM (ASUS)")

    @Rule(Sintoma(bip_asus_3_curtos=True))
    def asus_vga(self):
        self.diagnosticos.append("Falha de placa de vídeo (ASUS)")

    @Rule(Sintoma(bip_asus_continuo=True))
    def asus_power(self):
        self.diagnosticos.append("Problema de fonte de alimentação (ASUS)")

    # ----- Regras de bips Colorful -----
    @Rule(Sintoma(bip_colorful_1_longo_2_curtos=True))
    def colorful_erro_video(self):
        self.diagnosticos.append("Erro na placa de vídeo ou BIOS (Colorful)")

    @Rule(Sintoma(bip_colorful_1_longo_3_curtos=True))
    def colorful_problema_agp(self):
        self.diagnosticos.append("Problema no slot AGP ou placa de vídeo (Colorful)")

    @Rule(Sintoma(bip_colorful_3_longos=True))
    def colorful_memoria_ram(self):
        self.diagnosticos.append("Falha na memória RAM (Colorful)")

    @Rule(Sintoma(bip_colorful_5_longos=True))
    def colorful_processador(self):
        self.diagnosticos.append("Falha no processador (Colorful)")

    @Rule(Sintoma(bip_colorful_ausente=True))
    def colorful_placa_mae_fonte(self):
        self.diagnosticos.append("Falha na placa-mãe ou fonte (Colorful)")

    def run_with_facts(self, fatos_dict):
        """
        Executa o motor com fatos fornecidos e retorna lista de diagnósticos ou None.
        """
        self.reset()
        self.fatos_relevantes = fatos_dict
        for sintoma in fatos_dict:
            self.declare(Sintoma(**{sintoma: True}))
        self.run()
        return self.diagnosticos if self.diagnosticos else None

    def sintomas_necessarios(self):
        """
        Retorna sintomas genéricos pendentes para completar pares de diagnóstico.
        """
        regras_pares = [
            {'nao_liga', 'ventoinhas_paradas'},
            {'tela_azul', 'reinicializacao_inesperada'},
            {'lentidao', 'erros_leitura_gravacao'},
            {'travamentos', 'aquecimento'},
            {'nao_liga', 'sem_som_ou_luz'}
        ]
        fornecidos = set(self.fatos_relevantes.keys())
        faltando = set()
        for regra in regras_pares:
            diff = regra - fornecidos
            if len(diff) == 1:
                faltando.update(diff)
        return list(faltando)

# Funções públicas para integração

def evaluate_rules(fatos_lista):
    """
    fatos_lista: lista de strings no formato sintoma('nome')
    Retorna lista de diagnósticos ou None.
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
    """
    Retorna sintomas genéricos que ainda faltam para formar pares diagnósticos.
    """
    fatos_dict = {}
    for fato in fatos_lista:
        if "sintoma(" in fato:
            nome = fato.replace("sintoma(", "").replace(")", "").replace("'", "").strip()
            if nome in SINTOMAS_VALIDOS:
                fatos_dict[nome] = True
    engine = SistemaRegras()
    engine.run_with_facts(fatos_dict)
    return engine.sintomas_necessarios()