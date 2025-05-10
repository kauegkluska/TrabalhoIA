from experta import *

SINTOMAS_VALIDOS = [
    'nao_liga', 'sem_som_ou_luz', 'ventoinhas_paradas',
    'tela_azul', 'travamentos', 'reinicializacao_inesperada',
    'lentidao', 'arquivos_corrompidos', 'erros_leitura_gravacao', 'aquecimento',
    'bip_asrock_1_curto', 'bip_asrock_2_curtos', 'bip_asrock_3_curtos', 'bip_asrock_continuo',
    'bip_gigabyte_1_longo_2_curtos', 'bip_gigabyte_1_longo_3_curtos', 'bip_gigabyte_continuo',
    'bip_asus_1_curto', 'bip_asus_2_curtos', 'bip_asus_3_curtos', 'bip_asus_continuo',
    'bip_colorful_1_longo_2_curtos', 'bip_colorful_1_longo_3_curtos',
    'bip_colorful_3_longos', 'bip_colorful_5_longos', 'bip_colorful_ausente'
]

TIPOS_COMPUTADOR = ['tipo_computador("notebook")', 'tipo_computador("pc")']
    
MODELOS_VALIDOS = [
    'modelo("asus")', 'modelo("asrock")', 'modelo("gigabyte")', 'modelo("colorful")'
]

SINTOMAS_BEEP = [
    s for s in SINTOMAS_VALIDOS if s.startswith("bip_")
]

SINTOMAS_GENERICOS = [
    f"sintoma('{s}')" for s in SINTOMAS_VALIDOS if not s.startswith("bip_")
]

MODELOS_NOTEBOOK = [
    'Dell', 'Lenovo', 'Acer', 'HP', 'Samsung', 'vaio'
]

class Sintoma(Fact):
    """Fato representando um sintoma do computador."""
    pass

class Modelo_placa_mae(Fact):
    """Fato representando o modelo da placa mãe."""
    pass

class Modelo_notebook(Fact):
    """Fato representando o modelo do notebook."""
    pass

class Tipo_computador(Fact):
    """Fato representando o tipo de computador."""
    pass

class SistemaRegras(KnowledgeEngine):
    def __init__(self):
        super().__init__()
        self.diagnosticos = []
        self.fatos_relevantes = []

    def reset(self):
        super().reset()
        self.diagnosticos = []
        self.fatos_relevantes = []

    # ----- Regras com sintomas genéricos -----
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

    # ----- Regras específicas para placas-mãe -----
    @Rule(Sintoma(bip_asrock_1_curto=True), Modelo_placa_mae(modelo='ASRock'))
    def asrock_dram_refresh(self):
        self.diagnosticos.append("Falha de renovação DRAM (ASRock)")

    @Rule(Sintoma(bip_asrock_2_curtos=True), Modelo_placa_mae(modelo='ASRock'))
    def asrock_parity(self):
        self.diagnosticos.append("Falha de circuito de paridade (ASRock)")

    @Rule(Sintoma(bip_asrock_3_curtos=True), Modelo_placa_mae(modelo='ASRock'))
    def asrock_ram_64k(self):
        self.diagnosticos.append("Falha de 64K de RAM base (ASRock)")

    @Rule(Sintoma(bip_asrock_continuo=True), Modelo_placa_mae(modelo='ASRock'))
    def asrock_power(self):
        self.diagnosticos.append("Problema de fonte ou placa-mãe (ASRock)")

    # ----- Regras para notebooks -----
    @Rule(Sintoma(bateria_nao_carrega=True), Tipo_computador(tipo='notebook'))
    def defeito_bateria(self):
        self.diagnosticos.append("Bateria com defeito ou conector de carga ruim")

    @Rule(Sintoma(bateria_dura_pouco=True), Sintoma(aquecimento=True), Tipo_computador(tipo='notebook'))
    def aquecimento_afeta_bateria(self):
        self.diagnosticos.append("Superaquecimento reduz capacidade da bateria")

    @Rule(Sintoma(tela_nao_acende=True), Sintoma(sem_som_ou_luz=True), Tipo_computador(tipo='notebook'))
    def problema_backlight(self):
        self.diagnosticos.append("Inverter ou backlight da tela com defeito")

    @Rule(Sintoma(teclado_nao_responde=True), Tipo_computador(tipo='notebook'))
    def defeito_teclado(self):
        self.diagnosticos.append("Falha no teclado – possível mau contato ou driver")

    @Rule(Sintoma(computador_desliga_quando_joga=True), Tipo_computador(tipo='notebook'))
    def troca_pastatermica(self):
        self.diagnosticos.append("Fazer limpeza do notebook e troca da pasta térmica")

    def run_with_facts(self, fatos_dict):
        self.reset()
        self.fatos_relevantes = fatos_dict
        for chave, valor in fatos_dict.items():
            if chave in SINTOMAS_VALIDOS:
                self.declare(Sintoma(**{chave: True}))
            elif chave in MODELOS_PLACA_MAE:
                self.declare(Modelo_placa_mae(modelo=chave))
            elif chave in MODELOS_NOTEBOOK:
                self.declare(Modelo_notebook(modelo=chave))
            elif chave in TIPOS_DE_COMPUTADOR:
                self.declare(Tipo_computador(tipo=chave))
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
            {'nao_liga', 'sem_som_ou_luz'},
            {'bateria_dura_pouco', 'aquecimento'},
            {'tela_nao_acende', 'sem_som_ou_luz'},
            {'bip_asrock_1_curto'},
            {'bip_asrock_2_curtos'},
            {'bip_asrock_3_curtos'},
            {'bip_asrock_continuo'},
            {'bip_gigabyte_1_longo_2_curtos'},
            {'bip_gigabyte_1_longo_3_curtos'},
            {'bip_gigabyte_continuo'},
            {'bip_asus_1_curto'},
            {'bip_asus_2_curtos'},
            {'bip_asus_3_curtos'},
            {'bip_asus_continuo'},
            {'bip_colorful_1_longo_2_curtos'},
            {'bip_colorful_1_longo_3_curtos'},
            {'bip_colorful_3_longos'},
            {'bip_colorful_5_longos'},
            {'bip_colorful_ausente'},
            {'bateria_nao_carrega'},
            {'tela_nao_acende', 'sem_som_ou_luz'},
            {'teclado_nao_responde'},
            {'computador_desliga_quando_joga'}
        ]
        fornecidos = set(self.fatos_relevantes.keys())
        faltando = set()
        for regra in regras_pares:
            diff = regra - fornecidos
            if len(diff) == 1:
                faltando.update(diff)
        return list(faltando)
        

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


def get_missing_symptoms(fatos):
    if not any(fato.startswith("tipo_computador(") for fato in fatos):
        return TIPOS_COMPUTADOR

    if not any(fato.startswith("modelo(") for fato in fatos):
        return MODELOS_VALIDOS

    if not any(fato.startswith("sintoma('bip_") for fato in fatos):
        return [f"sintoma('{s}')" for s in SINTOMAS_BEEP]

    sintomas_presentes = set(fato for fato in fatos if fato.startswith("sintoma("))
    sintomas_faltando = [s for s in SINTOMAS_GENERICOS if s not in sintomas_presentes]

    return sintomas_faltando
