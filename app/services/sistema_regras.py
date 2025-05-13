from experta import *


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
    'desliga_apos_ligar', 'bios_indica_falha_na_ventoinha', 'cpu_queimada'


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

    def run_with_facts(self, fatos_dict):
        self.reset()
        self.fatos_relevantes = fatos_dict
        for sintoma in fatos_dict:
            self.declare(Sintoma(sintoma=sintoma))

        self.run()
        return self.diagnostico_final
    
    def sintomas_necessarios(self, max_faltantes=3):
        """
        Retorna os sintomas relevantes que podem levar a diagnósticos,
        filtrando os que ainda não foram fornecidos.
        Considera como relevante uma regra da qual faltam até 'max_faltantes' sintomas.
        """
        regras_sintomas = [
            {"lentidao_ao_abrir_arquivos", "arquivos_corrompidos", "erro_ao_copiar_arquivos", "travamento_ao_inicializar", "clique_vindo_do_hd"},
            {"desligamento_repentino", "travamento_em_uso_intenso", "cooler_em_alta_velocidade", "temperatura_acima_de_80", "lentidao_sem_motivo"},
            {"nao_liga", "reinicializacoes_aleatorias", "componentes_sem_energia", "queima_frequente_de_componentes", "cheiro_de_queimado"},
            {"tela_azul", "aplicacoes_fechando_sozinhas", "travamentos_aleatorios", "falha_na_instalacao_do_sistema", "ram_mostrando_menos_que_instalada"},
            {"nao_da_video", "hardware_nao_reconhecido", "usb_nao_funciona", "erros_de_post", "instabilidade_geral"},
            {"loop_de_boot", "arquivos_de_sistema_ausentes", "menu_iniciar_nao_funciona", "travamentos_apos_atualizacao"},
            {"tela_preta_pos_boot", "resolucao_incorreta", "travamento_em_jogos", "erro_no_driver_de_video", "so_funciona_no_modo_seguro"},
            {"lentidao_anormal", "popups_no_navegador", "arquivos_somem", "programas_abrem_sozinhos", "acesso_a_sites_estranhos"},
            {"artefatos_na_tela", "sem_sinal_de_video", "travamento_em_graficos", "cooler_da_gpu_nao_gira", "driver_da_gpu_falha"},
            {"aumento_rapido_de_temperatura", "cooler_silencioso_ou_com_ruido", "desliga_apos_ligar", "bios_indica_falha_na_ventoinha", "cpu_queimada"},
            {"Wifi_não_funciona_após_formatação","não_aparece_redes_wifi_para_se_conectar"}
        ]
        
        fornecidos = set(self.fatos_relevantes.keys())
        sintomas_faltando = set()

        for regra in regras_sintomas:
            faltam = regra - fornecidos
            if 0 < len(faltam) <= max_faltantes: 
                sintomas_faltando.update(faltam)
                
        return list(sintomas_faltando)
    


    @Rule(Sintoma(sintoma="lentidao_ao_abrir_arquivos"),
          Sintoma(sintoma="arquivos_corrompidos"),
          Sintoma(sintoma="erro_ao_copiar_arquivos"),
          Sintoma(sintoma="travamento_ao_inicializar"),
          Sintoma(sintoma="clique_vindo_do_hd"))
    def diagnostico_hd_ruim(self):
        self.diagnostico_final = "Diagnóstico: HD com setores defeituosos"

    @Rule(Sintoma(sintoma="desligamento_repentino"),
          Sintoma(sintoma="travamento_em_uso_intenso"),
          Sintoma(sintoma="cooler_em_alta_velocidade"),
          Sintoma(sintoma="temperatura_acima_de_80"),
          Sintoma(sintoma="lentidao_sem_motivo"))
    def diagnostico_superaquecimento(self):
        self.diagnostico_final = "Diagnóstico: Superaquecimento da CPU"

    @Rule(Sintoma(sintoma="nao_liga"),
          Sintoma(sintoma="reinicializacoes_aleatorias"),
          Sintoma(sintoma="componentes_sem_energia"),
          Sintoma(sintoma="queima_frequente_de_componentes"),
          Sintoma(sintoma="cheiro_de_queimado"))
    def diagnostico_fonte_energia(self):
        self.diagnostico_final = "Diagnóstico: Fonte de alimentação com defeito"

    @Rule(Sintoma(sintoma="tela_azul"),
          Sintoma(sintoma="aplicacoes_fechando_sozinhas"),
          Sintoma(sintoma="travamentos_aleatorios"),
          Sintoma(sintoma="falha_na_instalacao_do_sistema"),
          Sintoma(sintoma="nao_da_video"),
          Sintoma(sintoma="ram_mostrando_menos_que_instalada"))
    def diagnostico_ram_defeituosa(self):
        self.diagnostico_final = "Diagnóstico: Memória RAM defeituosa"

    @Rule(Sintoma(sintoma="nao_da_video"),
          Sintoma(sintoma="hardware_nao_reconhecido"),
          Sintoma(sintoma="usb_nao_funciona"),
          Sintoma(sintoma="erros_de_post"),
          Sintoma(sintoma="instabilidade_geral"))
    def diagnostico_placa_mae(self):
        self.diagnostico_final = "Diagnóstico: Placa-mãe danificada"

    @Rule(Sintoma(sintoma="loop_de_boot"),
          Sintoma(sintoma="arquivos_de_sistema_ausentes"),
          Sintoma(sintoma="menu_iniciar_nao_funciona"),
          Sintoma(sintoma="travamentos_apos_atualizacao"))
    def diagnostico_sistema_operacional(self):
        self.diagnostico_final = "Diagnóstico: Sistema operacional corrompido"

    @Rule(Sintoma(sintoma="tela_preta_pos_boot"),
          Sintoma(sintoma="resolucao_incorreta"),
          Sintoma(sintoma="travamento_em_jogos"),
          Sintoma(sintoma="erro_no_driver_de_video"),
          Sintoma(sintoma="so_funciona_no_modo_seguro"))
    def diagnostico_driver_video(self):
        self.diagnostico_final = "Diagnóstico: Driver de vídeo com problema"

    @Rule(Sintoma(sintoma="lentidao_anormal"),
          Sintoma(sintoma="popups_no_navegador"),
          Sintoma(sintoma="arquivos_somem"),
          Sintoma(sintoma="programas_abrem_sozinhos"),
          Sintoma(sintoma="acesso_a_sites_estranhos"))
    def diagnostico_malware(self):
        self.diagnostico_final = "Diagnóstico: Malware ou vírus"

    @Rule(Sintoma(sintoma="artefatos_na_tela"),
          Sintoma(sintoma="sem_sinal_de_video"),
          Sintoma(sintoma="travamento_em_graficos"),
          Sintoma(sintoma="cooler_da_gpu_nao_gira"),
          Sintoma(sintoma="driver_da_gpu_falha"))
    def diagnostico_placa_video(self):
        self.diagnostico_final = "Diagnóstico: Placa de vídeo com falha"

    @Rule(Sintoma(sintoma="aumento_rapido_de_temperatura"),
          Sintoma(sintoma="cooler_silencioso_ou_com_ruido"),
          Sintoma(sintoma="desliga_apos_ligar"),
          Sintoma(sintoma="bios_indica_falha_na_ventoinha"),
          Sintoma(sintoma="cpu_queimada"))
    def diagnostico_cpu(self):
        self.diagnostico_final = "Diagnóstico: CPU queimada"
        
    @Rule(Sintoma(sintoma="Wifi_não_funciona_após_formatação"),
         Sintoma(sintoma="não_aparece_redes_wifi_para_se_conectar"))
    def diagnostico_rede(self):
        self.diagnostico_final = "Diagnostico: Falta do driver Wifi"
        


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
    print(f"Fatos recebidos: {fatos_dict}")
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