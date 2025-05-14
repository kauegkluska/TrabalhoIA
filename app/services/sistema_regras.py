from experta import *

SINTOMAS_VALIDOS = [
    'lentidao_geral', 'travamentos', 'erros_de_arquivo', 'problemas_de_boot',
    'problemas_de_video', 'problemas_de_audio', 'problemas_de_rede',
    'superaquecimento', 'ruidos_estranhos', 'desligamentos_involuntarios',
    'falha_de_componente', 'instabilidade_apos_atualizacao',
    'comportamento_incomum_software', 'reinicializacoes_involuntarias'
]



class Sintoma(Fact):
    """Fato representando um sintoma do computador."""
    pass

class RegrasDiagnostico(KnowledgeEngine):
    def __init__(self):
        super().__init__()
        self.diagnostico_final = None
        self.regras_sintomas = {  
            # Diagnóstico: Falha Crítica no Disco
            "Falha Crítica no Disco": {"erros_de_arquivo", "lentidao_geral"},

            # Diagnóstico: Falha Crítica no Disco (variante)
            "Falha Crítica no Disco": {"erros_de_arquivo", "ruidos_estranhos", "desligamentos_involuntarios"},

            # Diagnóstico: Vírus ou Malware
            "Vírus ou Malware": {"comportamento_incomum_software", "lentidao_geral"},

            # Diagnóstico: Vírus ou Malware (variante)
            "Vírus ou Malware": {"travamentos", "comportamento_incomum_software", "instabilidade_apos_atualizacao"},

            # Diagnóstico: Problemas de Driver
            "Problemas de Driver": {"problemas_de_video", "instabilidade_apos_atualizacao"},

            # Diagnóstico: Problemas de Driver (variante)
            "Problemas de Driver": {"problemas_de_audio", "instabilidade_apos_atualizacao", "travamentos"},

            # Diagnóstico: Memória com Falhas
            "Memória com Falhas": {"travamentos", "reinicializacoes_involuntarias"},  # Novo sintoma? se sim, adicione no seu `SINTOMAS_VALIDOS`

            # Diagnóstico: Superaquecimento Grave
            "Superaquecimento Grave": {"superaquecimento", "desligamentos_involuntarios", "ruidos_estranhos"},

            # Diagnóstico: Fonte de Energia Instável
            "Fonte de Energia Instável": {"desligamentos_involuntarios", "problemas_de_boot"},

            # Diagnóstico: Sistema Corrompido
            "Sistema Corrompido": {"problemas_de_boot", "erros_de_arquivo", "instabilidade_apos_atualizacao"},

            # Diagnóstico: Conflito de Software
            "Conflito de Software": {"comportamento_incomum_software", "travamentos", "instabilidade_apos_atualizacao"},

            # Diagnóstico: Placa de Vídeo com Problemas
            "Placa de Vídeo com Problemas": {"problemas_de_video", "travamentos", "ruidos_estranhos"},

            # Diagnóstico: Falha de RAM
            "Falha de RAM": {"travamentos", "erros_de_arquivo", "lentidao_geral"},

            # Diagnóstico: Sistema Operacional Desatualizado
            "Sistema Operacional Desatualizado": {"instabilidade_apos_atualizacao", "lentidao_geral", "problemas_de_rede"},

            # Diagnóstico: BIOS Corrompida
            "BIOS Corrompida": {"problemas_de_boot", "falha_de_componente", "instabilidade_apos_atualizacao"},
        }
        self.fatos_relevantes = {} 

    def reset(self):
        super().reset()
        self.diagnostico_final = None 
        self.fatos_relevantes = {}

    def run_with_facts(self, fatos_dict):
        try:
            self.reset()
            self.fatos_relevantes = fatos_dict

            if not fatos_dict:
                return "Olá! Descreva o problema do seu computador para que eu possa ajudar."

            for sintoma in fatos_dict.keys():
                self.declare(Sintoma(sintoma=sintoma))

            self.run()
            return self.diagnostico_final if self.diagnostico_final else self.sintomas_necessarios() 

        except Exception as e:
            return f"Erro ao processar as regras: {str(e)}"

    def sintomas_necessarios(self):
        pendentes = {}
        sintomas_informados = set(self.fatos_relevantes.keys())

        for diagnostico, sintomas in self.regras_sintomas.items():
            sintomas_faltando = [s for s in sintomas if s not in sintomas_informados]
            if sintomas_faltando and len(sintomas_faltando) < len(sintomas):
                pendentes[diagnostico] = sintomas_faltando
        

        return pendentes

    @Rule(Sintoma(sintoma="lentidao_geral"),
          Sintoma(sintoma="travamentos"))
    def diagnostico_desempenho(self):
        self.diagnostico_final = "Diagnóstico: Possíveis problemas de desempenho geral do sistema."

    @Rule(Sintoma(sintoma="erros_de_arquivo"),
          Sintoma(sintoma="lentidao_geral"))
    def diagnostico_falha_disco(self):
        self.diagnostico_final = "Diagnóstico: Falha crítica no disco rígido ou SSD."

    @Rule(Sintoma(sintoma="erros_de_arquivo"),
          Sintoma(sintoma="ruidos_estranhos"),
          Sintoma(sintoma="desligamentos_involuntarios"))
    def diagnostico_falha_disco_avancada(self):
        self.diagnostico_final = "Diagnóstico: Indícios graves de falha no disco rígido."

    @Rule(Sintoma(sintoma="problemas_de_boot"),
          Sintoma(sintoma="lentidao_geral"))
    def diagnostico_falha_boot(self):
        self.diagnostico_final = "Diagnóstico: Problemas ao iniciar o sistema operacional."

    @Rule(Sintoma(sintoma="problemas_de_video"),
          Sintoma(sintoma="travamentos"))
    def diagnostico_video_driver(self):
        self.diagnostico_final = "Diagnóstico: Problemas com driver de vídeo ou placa gráfica."

    @Rule(Sintoma(sintoma="problemas_de_audio"),
          Sintoma(sintoma="instabilidade_apos_atualizacao"))
    def diagnostico_audio_driver(self):
        self.diagnostico_final = "Diagnóstico: Problemas com driver de áudio após atualização."

    @Rule(Sintoma(sintoma="superaquecimento"),
          Sintoma(sintoma="desligamentos_involuntarios"))
    def diagnostico_superaquecimento(self):
        self.diagnostico_final = "Diagnóstico: Superaquecimento do sistema causando desligamentos."

    @Rule(Sintoma(sintoma="superaquecimento"),
          Sintoma(sintoma="ruidos_estranhos"),
          Sintoma(sintoma="desligamentos_involuntarios"))
    def diagnostico_superaquecimento_grave(self):
        self.diagnostico_final = "Diagnóstico: Superaquecimento grave – verifique ventoinhas ou dissipadores."

    @Rule(Sintoma(sintoma="falha_de_componente"),
          Sintoma(sintoma="problemas_de_boot"))
    def diagnostico_falha_hardware_boot(self):
        self.diagnostico_final = "Diagnóstico: Falha de hardware impactando o processo de boot."

    @Rule(Sintoma(sintoma="comportamento_incomum_software"),
          Sintoma(sintoma="lentidao_geral"))
    def diagnostico_malware(self):
        self.diagnostico_final = "Diagnóstico: Sistema pode estar infectado por vírus ou malware."

    @Rule(Sintoma(sintoma="comportamento_incomum_software"),
          Sintoma(sintoma="instabilidade_apos_atualizacao"),
          Sintoma(sintoma="travamentos"))
    def diagnostico_conflito_software(self):
        self.diagnostico_final = "Diagnóstico: Conflito entre softwares ou atualizações recentes."

    @Rule(Sintoma(sintoma="problemas_de_rede"),
          Sintoma(sintoma="instabilidade_apos_atualizacao"))
    def diagnostico_rede_driver(self):
        self.diagnostico_final = "Diagnóstico: Problemas de rede causados por drivers após atualização."

    @Rule(Sintoma(sintoma="travamentos"),
          Sintoma(sintoma="reinicializacoes_involuntarias"))
    def diagnostico_memoria_defeituosa(self):
        self.diagnostico_final = "Diagnóstico: Falhas em módulos de memória RAM."

    @Rule(Sintoma(sintoma="problemas_de_boot"),
          Sintoma(sintoma="falha_de_componente"),
          Sintoma(sintoma="instabilidade_apos_atualizacao"))
    def diagnostico_bios_corrompida(self):
        self.diagnostico_final = "Diagnóstico: Possível corrupção de BIOS ou firmware."

    @Rule(Sintoma(sintoma="instabilidade_apos_atualizacao"),
          Sintoma(sintoma="lentidao_geral"),
          Sintoma(sintoma="problemas_de_rede"))
    def diagnostico_sistema_desatualizado(self):
        self.diagnostico_final = "Diagnóstico: Sistema operacional desatualizado ou incompatível."

    @Rule(Sintoma(sintoma="problemas_de_boot"),
          Sintoma(sintoma="desligamentos_involuntarios"))
    def diagnostico_fonte_inestavel(self):
        self.diagnostico_final = "Diagnóstico: Fonte de energia instável pode estar causando falhas no boot."

    @Rule(Sintoma(sintoma="problemas_de_audio"))
    def diagnostico_audio_simples(self):
        self.diagnostico_final = "Diagnóstico: Problemas com a saída ou driver de áudio."

    @Rule(Sintoma(sintoma="problemas_de_video"))
    def diagnostico_video_simples(self):
        self.diagnostico_final = "Diagnóstico: Problemas com a saída de vídeo ou driver gráfico."

    @Rule(Sintoma(sintoma="problemas_de_rede"))
    def diagnostico_rede_simples(self):
        self.diagnostico_final = "Diagnóstico: Problemas com a conexão de rede (Wi-Fi ou Ethernet)."

    @Rule(Sintoma(sintoma="instabilidade_apos_atualizacao"))
    def diagnostico_atualizacao_simples(self):
        self.diagnostico_final = "Diagnóstico: Instabilidade do sistema após uma atualização de software."

def evaluate_rules(fatos_lista):
    """Avalia os fatos e retorna um diagnóstico ou os sintomas pendentes."""
    fatos_dict = {}
    for fato in fatos_lista:
        if "sintoma(" in fato:
            nome = fato.replace("sintoma(", "").replace(")", "").replace("'", "").strip()
            if nome in SINTOMAS_VALIDOS:
                fatos_dict[nome] = True

    engine = RegrasDiagnostico()
    return engine.run_with_facts(fatos_dict)

def get_missing_symptoms(fatos_lista):
    """Retorna os sintomas faltantes para completar diagnósticos."""
    fatos_dict = {}
    for fato in fatos_lista:
        if "sintoma(" in fato:
            nome = fato.replace("sintoma(", "").replace(")", "").replace("'", "").strip()
            if nome in SINTOMAS_VALIDOS:
                fatos_dict[nome] = True

    engine = RegrasDiagnostico()
    engine.fatos_relevantes = fatos_dict 
    return engine.sintomas_necessarios()