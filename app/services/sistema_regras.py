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
    'desliga_apos_ligar', 'bios_indica_falha_na_ventoinha', 'cpu_queimada', 'Wifi_não_funciona_após_formatação',
    'não_aparece_redes_wifi_para_se_conectar', 'ruido_alto_cooler', 'aquecimento_sem_uso', 'pasta_termica_ressecada',
    'poeira_acumulada', 'ventilacao_obstruida', 'ruido_metalico_ventoinha', 'vibracao_anormal_cooler',
    'rotacao_irregular_ventoinha'
]

class Sintoma(Fact):
    """Fato representando um sintoma do computador."""
    pass

class BaseRegras(KnowledgeEngine):
    def __init__(self):
        super().__init__()
        self.diagnostico_final = None
        self.fatos_relevantes = []
        self.sintomas_por_regra = {}
        self.regras_por_sintoma = {}
        self._mapear_sintomas()

    def _mapear_sintomas(self):
        """Mapeia os sintomas para suas respectivas regras e vice-versa."""
        pass

    def reset(self):
        super().reset()
        self.diagnostico_final = None
        self.fatos_relevantes = []

    def run_with_facts(self, fatos_dict):
        try:
            self.reset()
            self.fatos_relevantes = fatos_dict
            
            # Se não houver sintomas, retorna mensagem de boas-vindas
            if not fatos_dict:
                return "Olá! Sou um sistema especialista em diagnóstico de problemas de computador. Por favor, descreva em detalhes o problema que você está enfrentando. Quanto mais detalhes você fornecer, melhor poderei ajudar!"
            
            # Verifica se algum dos sintomas é único para uma regra
            for sintoma in fatos_dict.keys():
                regras_do_sintoma = self.regras_por_sintoma.get(sintoma, set())
                if len(regras_do_sintoma) == 1:  # Se o sintoma é único para uma regra
                    regra = list(regras_do_sintoma)[0]
                    # Declara todos os sintomas necessários para essa regra
                    for sintoma_necessario in self.sintomas_por_regra[regra]:
                        self.declare(Sintoma(sintoma=sintoma_necessario))
                    self.run()
                    if self.diagnostico_final:
                        return self.diagnostico_final
            
            # Se não encontrou regra única, continua com o processo normal
            primeiro_sintoma = list(fatos_dict.keys())[0]
            regras_possiveis = self.regras_por_sintoma.get(primeiro_sintoma, set())
            
            if not regras_possiveis:
                return "Não foi possível identificar nenhum sintoma conhecido no seu relato. Por favor, descreva o problema de outra forma, fornecendo mais detalhes sobre os sintomas que seu computador está apresentando. Quanto mais específico você for, melhor poderei ajudar!"
            
            # Para cada regra possível, verifica quais sintomas ainda faltam
            sintomas_faltantes = {}
            for regra in regras_possiveis:
                sintomas_necessarios = self.sintomas_por_regra[regra]
                faltantes = sintomas_necessarios - set(fatos_dict.keys())
                if faltantes:
                    sintomas_faltantes[regra] = faltantes
            
            # Se já tiver todos os sintomas de alguma regra, executa o diagnóstico
            for sintoma in fatos_dict:
                self.declare(Sintoma(sintoma=sintoma))
            
            try:
                self.run()
                if self.diagnostico_final:
                    return self.diagnostico_final
            except Exception as e:
                return f"Erro ao processar as regras: {str(e)}"
            
            # Se não chegou a um diagnóstico, retorna os próximos sintomas a verificar
            if sintomas_faltantes:
                return {"sintomas_faltantes": sintomas_faltantes}
            
            return "Preciso de mais informações para fazer um diagnóstico preciso. Pode me contar mais sobre o problema?"
            
        except Exception as e:
            return f"Erro ao processar os fatos: {str(e)}"

class RegrasSoftware(BaseRegras):
    def sintomas_necessarios(self, max_faltantes=3):
        """Retorna os sintomas relevantes que podem levar a diagnósticos."""
        sintomas_relevantes = set()
        for sintomas in self.sintomas_por_regra.values():
            sintomas_relevantes.update(sintomas)
        return list(sintomas_relevantes)

    def _mapear_sintomas(self):
        self.sintomas_por_regra = {
            "Sistema Operacional Corrompido": {
                "loop_de_boot", "arquivos_de_sistema_ausentes",
                "menu_iniciar_nao_funciona", "travamentos_apos_atualizacao"
            },
            "Driver de Vídeo com Problema": {
                "tela_preta_pos_boot", "resolucao_incorreta", "travamento_em_jogos",
                "erro_no_driver_de_video", "so_funciona_no_modo_seguro"
            },
            "Malware ou Vírus": {
                "lentidao_anormal", "popups_no_navegador", "arquivos_somem",
                "programas_abrem_sozinhos", "acesso_a_sites_estranhos"
            },
            "Falta do Driver Wifi": {
                "Wifi_não_funciona_após_formatação", "não_aparece_redes_wifi_para_se_conectar"
            }
        }
        self._criar_mapa_reverso()

    def _criar_mapa_reverso(self):
        self.regras_por_sintoma = {}
        for regra, sintomas in self.sintomas_por_regra.items():
            for sintoma in sintomas:
                if sintoma not in self.regras_por_sintoma:
                    self.regras_por_sintoma[sintoma] = set()
                self.regras_por_sintoma[sintoma].add(regra)

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

    @Rule(Sintoma(sintoma="Wifi_não_funciona_após_formatação"),
          Sintoma(sintoma="não_aparece_redes_wifi_para_se_conectar"))
    def diagnostico_rede(self):
        self.diagnostico_final = "Diagnóstico: Falta do driver Wifi"

class RegrasHardware(BaseRegras):
    def sintomas_necessarios(self, max_faltantes=3):
        """Retorna os sintomas relevantes que podem levar a diagnósticos."""
        sintomas_relevantes = set()
        for sintomas in self.sintomas_por_regra.values():
            sintomas_relevantes.update(sintomas)
        return list(sintomas_relevantes)

    def _mapear_sintomas(self):
        self.sintomas_por_regra = {
            "HD com Setores Defeituosos": {
                "lentidao_ao_abrir_arquivos", "arquivos_corrompidos",
                "erro_ao_copiar_arquivos", "travamento_ao_inicializar", "clique_vindo_do_hd"
            },
            "Superaquecimento da CPU": {
                "desligamento_repentino", "travamento_em_uso_intenso",
                "cooler_em_alta_velocidade", "temperatura_acima_de_80", "lentidao_sem_motivo"
            },
            "Fonte de Alimentação com Defeito": {
                "nao_liga", "reinicializacoes_aleatorias", "componentes_sem_energia",
                "queima_frequente_de_componentes", "cheiro_de_queimado"
            },
            "Memória RAM Defeituosa": {
                "tela_azul", "aplicacoes_fechando_sozinhas", "travamentos_aleatorios",
                "falha_na_instalacao_do_sistema", "ram_mostrando_menos_que_instalada"
            },
            "Placa-mãe Danificada": {
                "nao_da_video", "hardware_nao_reconhecido", "usb_nao_funciona",
                "erros_de_post", "instabilidade_geral"
            },
            "Placa de Vídeo com Falha": {
                "artefatos_na_tela", "sem_sinal_de_video", "travamento_em_graficos",
                "cooler_da_gpu_nao_gira", "driver_da_gpu_falha"
            },
            "CPU Queimada": {
                "aumento_rapido_de_temperatura", "cooler_silencioso_ou_com_ruido",
                "desliga_apos_ligar", "bios_indica_falha_na_ventoinha", "cpu_queimada"
            },
            "Pasta Térmica Ressecada": {
                "temperatura_acima_de_80", "cooler_em_alta_velocidade",
                "aquecimento_sem_uso", "pasta_termica_ressecada", "ruido_alto_cooler"
            },
            "Ventilação Obstruída": {
                "temperatura_acima_de_80", "ruido_alto_cooler",
                "aquecimento_sem_uso", "poeira_acumulada", "ventilacao_obstruida"
            },
            "Falta de Lubrificação na Ventoinha": {
                "ruido_metalico_ventoinha", "vibracao_anormal_cooler",
                "rotacao_irregular_ventoinha", "ruido_alto_cooler", "aquecimento_sem_uso"
            }
        }
        self._criar_mapa_reverso()

    def _criar_mapa_reverso(self):
        self.regras_por_sintoma = {}
        for regra, sintomas in self.sintomas_por_regra.items():
            for sintoma in sintomas:
                if sintoma not in self.regras_por_sintoma:
                    self.regras_por_sintoma[sintoma] = set()
                self.regras_por_sintoma[sintoma].add(regra)

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

    @Rule(Sintoma(sintoma="temperatura_acima_de_80"),
          Sintoma(sintoma="cooler_em_alta_velocidade"),
          Sintoma(sintoma="aquecimento_sem_uso"),
          Sintoma(sintoma="pasta_termica_ressecada"),
          Sintoma(sintoma="ruido_alto_cooler"))
    def diagnostico_pasta_termica(self):
        self.diagnostico_final = "Diagnóstico: Pasta térmica ressecada"

    @Rule(Sintoma(sintoma="temperatura_acima_de_80"),
          Sintoma(sintoma="ruido_alto_cooler"),
          Sintoma(sintoma="aquecimento_sem_uso"),
          Sintoma(sintoma="poeira_acumulada"),
          Sintoma(sintoma="ventilacao_obstruida"))
    def diagnostico_ventilacao(self):
        self.diagnostico_final = "Diagnóstico: Ventilação obstruída"

    @Rule(Sintoma(sintoma="ruido_metalico_ventoinha"),
          Sintoma(sintoma="vibracao_anormal_cooler"),
          Sintoma(sintoma="rotacao_irregular_ventoinha"),
          Sintoma(sintoma="ruido_alto_cooler"),
          Sintoma(sintoma="aquecimento_sem_uso"))
    def diagnostico_lubrificacao_ventoinha(self):
        self.diagnostico_final = "Diagnóstico: Falta de lubrificação na ventoinha"

class SistemaRegras(KnowledgeEngine):
    def __init__(self):
        super().__init__()
        self.hardware_rules = RegrasHardware()
        self.software_rules = RegrasSoftware()
        self.diagnostico_final = None

    def run_with_facts(self, fatos_dict):
        # Tenta primeiro as regras de hardware
        self.diagnostico_final = self.hardware_rules.run_with_facts(fatos_dict)
        
        # Se não encontrou diagnóstico, tenta as regras de software
        if not self.diagnostico_final:
            self.diagnostico_final = self.software_rules.run_with_facts(fatos_dict)
        
        return self.diagnostico_final

    def sintomas_necessarios(self, max_faltantes=3):
        """Retorna os sintomas relevantes que podem levar a diagnósticos."""
        sintomas_hardware = set(self.hardware_rules.sintomas_necessarios(max_faltantes))
        sintomas_software = set(self.software_rules.sintomas_necessarios(max_faltantes))
        return list(sintomas_hardware | sintomas_software)

def evaluate_rules(fatos_lista):
    """Avalia os fatos e retorna um diagnóstico."""
    fatos_dict = {}
    for fato in fatos_lista:
        if "sintoma(" in fato:
            nome = fato.replace("sintoma(", "").replace(")", "").replace("'", "").strip()
            if nome in SINTOMAS_VALIDOS:
                fatos_dict[nome] = True

    engine = SistemaRegras()
    return engine.run_with_facts(fatos_dict)

def get_missing_symptoms(fatos_lista):
    """Retorna sintomas faltantes para completar diagnósticos."""
    fatos_dict = {}
    for fato in fatos_lista:
        if "sintoma(" in fato:
            nome = fato.replace("sintoma(", "").replace(")", "").replace("'", "").strip()
            if nome in SINTOMAS_VALIDOS:
                fatos_dict[nome] = True

    engine = SistemaRegras()
    return engine.sintomas_necessarios()