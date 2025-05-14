from experta import *

SINTOMAS_VALIDOS = [
    'lentidao_geral', 'travamentos', 'erros_de_arquivo', 'problemas_de_boot',
    'problemas_de_video', 'problemas_de_audio', 'problemas_de_rede',
    'superaquecimento', 'ruidos_estranhos', 'desligamentos_involuntarios',
    'instabilidade_apos_atualizacao',
    'comportamento_incomum_software', 'reinicializacoes_involuntarias',
    'tela_azul', 'ausencia_de_audio', 'congelamento_de_tela', 'perda_de_dados',
    'aplicativos_nao_respondem', 'teclado_nao_funciona', 'mouse_nao_funciona',
    'leds_piscando', 'barulho_hd_alto', 'imagem_distorcida', 'conexao_lenta',
    'impossibilidade_imprimir', 'camera_nao_funciona', 'microfone_nao_funciona',
    'ordem_de_boot_errada', 'nao_detecta_hd', 'conexao_intermittente',
    'sem_acesso_internet', 'Wifi_nao_funciona',
    'nao_aparece_redes_wifi_para_se_conectar', 'pendrive_nao_reconhecido',
    'nao_detecta_dispositivo_usb', 'boot_loop', 'sistema_nao_encontra_disco',
    'mensagem_de_erro_inicial', 'bloqueio_de_programas_legitimos',
    'avisos_na_tela', 'desativacao_de_funcionalidades',
    'restricao_de_configuracoes'
]

class Sintoma(Fact):
    """Fato representando um sintoma do computador."""
    pass

class RegrasDiagnostico(KnowledgeEngine):
    def __init__(self):
        super().__init__()
        self.diagnostico_final = None
        self.regras_sintomas = {
            "Falha Crítica no Disco": {"erros_de_arquivo", "lentidao_geral"},
            "Falha Crítica no Disco (variante)": {"erros_de_arquivo", "ruidos_estranhos", "desligamentos_involuntarios"},
            "Falha Crítica no Disco (Grave)": {"erros_de_arquivo", "barulho_hd_alto", "perda_de_dados", "desligamentos_involuntarios"},
            "Vírus ou Malware": {"comportamento_incomum_software", "lentidao_geral"},
            "Vírus ou Malware (variante)": {"travamentos", "comportamento_incomum_software", "instabilidade_apos_atualizacao"},
            "Vírus ou Malware (Extremo)": {"comportamento_incomum_software", "aplicativos_nao_respondem", "tela_azul", "perda_de_dados"},
            "Problemas de Driver": {"problemas_de_video", "instabilidade_apos_atualizacao"},
            "Problemas de Driver (variante)": {"problemas_de_audio", "instabilidade_apos_atualizacao", "travamentos"},
            "Problemas de Driver (Gráfico)": {"problemas_de_video", "imagem_distorcida", "congelamento_de_tela"},
            "Memória com Falhas": {"travamentos", "reinicializacoes_involuntarias"},
            "Memória com Falhas (Grave)": {"travamentos", "reinicializacoes_involuntarias", "tela_azul", "perda_de_dados"},
            "Superaquecimento Grave": {"superaquecimento", "desligamentos_involuntarios", "ruidos_estranhos"},
            "Superaquecimento Extremo": {"superaquecimento", "desligamentos_involuntarios", "ruidos_estranhos", "congelamento_de_tela"},
            "Fonte de Energia Instável": {"desligamentos_involuntarios", "problemas_de_boot"},
            "Fonte de Energia Instável (Grave)": {"desligamentos_involuntarios", "problemas_de_boot", "reinicializacoes_involuntarias", "leds_piscando"},
            "Sistema Corrompido": {"problemas_de_boot", "erros_de_arquivo", "instabilidade_apos_atualizacao"},
            "Sistema Corrompido (Grave)": {"problemas_de_boot", "erros_de_arquivo", "instabilidade_apos_atualizacao", "tela_azul"},
            "Conflito de Software": {"comportamento_incomum_software", "travamentos", "instabilidade_apos_atualizacao"},
            "Conflito de Software (Grave)": {"comportamento_incomum_software", "travamentos", "instabilidade_apos_atualizacao", "aplicativos_nao_respondem"},
            "Placa de Vídeo com Problemas": {"problemas_de_video", "travamentos", "ruidos_estranhos"},
            "Placa de Vídeo com Problemas (Grave)": {"problemas_de_video", "travamentos", "ruidos_estranhos", "imagem_distorcida"},
            "Falha de RAM": {"travamentos", "erros_de_arquivo", "lentidao_geral"},
            "Falha de RAM (Grave)": {"travamentos", "erros_de_arquivo", "lentidao_geral", "tela_azul"},
            "Sistema Operacional Desatualizado": {"instabilidade_apos_atualizacao", "lentidao_geral", "problemas_de_rede"},
            "Sistema Operacional Desatualizado (Grave)": {"instabilidade_apos_atualizacao", "lentidao_geral", "problemas_de_rede", "comportamento_incomum_software"},
            "BIOS Corrompida": {"problemas_de_boot", "instabilidade_apos_atualizacao"},
            "BIOS Corrompida (Grave)": {"problemas_de_boot", "instabilidade_apos_atualizacao", "tela_azul"},
            "Problemas de Conectividade": {"problemas_de_rede", "conexao_lenta"},
            "Falha Periféricos": {"teclado_nao_funciona", "mouse_nao_funciona"},
            "Problemas de Impressão": {"impossibilidade_imprimir", "erros_de_arquivo"},
            "Falha de Áudio/Vídeo": {"ausencia_de_audio", "camera_nao_funciona", "microfone_nao_funciona"},
            "Instabilidade do Sistema": {"tela_azul", "reinicializacoes_involuntarias", "congelamento_de_tela"},
            "Desempenho Lento": {"lentidao_geral", "aplicativos_nao_respondem", "travamentos"},
            "Ruídos Excessivos": {"ruidos_estranhos", "barulho_hd_alto"},
            "Problemas de Inicialização": {"problemas_de_boot", "leds_piscando"},
            "Corrupção de Dados": {"erros_de_arquivo", "perda_de_dados"},
            "Falha na Placa-Mãe": {"nao_liga", "sem_som_ou_luz", "leds_piscando"},
            "Falha na Placa-Mãe (Grave)": {"nao_liga", "sem_som_ou_luz", "leds_piscando", "ventoinhas_paradas"},
            "Erro de Configuração da BIOS": {"problemas_de_boot", "ordem_de_boot_errada"},
            "Erro de Configuração da BIOS (Avançado)": {"problemas_de_boot", "nao_detecta_hd", "instabilidade_apos_atualizacao"},
            "SSD com Problemas de Firmware": {"travamentos", "erros_de_arquivo", "desligamentos_involuntarios"},
            "SSD com Problemas de Firmware (Grave)": {"travamentos", "erros_de_arquivo", "desligamentos_involuntarios", "perda_de_dados"},
            "Conflito de IP na Rede": {"problemas_de_rede", "conexao_intermittente", "sem_acesso_internet"},
            "Conflito de IP na Rede (Persistente)": {"problemas_de_rede", "conexao_intermittente", "sem_acesso_internet", "wifi_nao_funciona"},
            "Driver de Rede sem Fio com Falha": {"Wifi_nao_funciona", "nao_aparece_redes_wifi_para_se_conectar", "instabilidade_apos_atualizacao"},
            "Driver de Rede sem Fio com Falha (Grave)": {"Wifi_nao_funciona", "nao_aparece_redes_wifi_para_se_conectar", "problemas_de_rede", "comportamento_incomum_software"},
            "Porta USB com Falha": {"pendrive_nao_reconhecido", "teclado_nao_funciona", "mouse_nao_funciona"},
            "Porta USB com Falha (Placa-Mãe)": {"pendrive_nao_reconhecido", "teclado_nao_funciona", "nao_detecta_dispositivo_usb"},
            "Problemas com Atualização do Windows": {"instabilidade_apos_atualizacao", "tela_azul", "boot_loop"},
            "Problemas com Atualização do Windows (Crítico)": {"instabilidade_apos_atualizacao", "tela_azul", "boot_loop", "perda_de_dados"},
            "Erro Pós-Formatação": {"problemas_de_boot", "sistema_nao_encontra_disco", "mensagem_de_erro_inicial"},
            "Erro Pós-Formatação (Drivers)": {"problemas_de_rede", "Wifi_nao_funciona", "ausencia_de_audio", "camera_nao_funciona"},
            "Antivírus Bloqueando Sistema": {"comportamento_incomum_software", "aplicativos_nao_respondem", "lentidao_geral"},
            "Antivírus Bloqueando Sistema (Paranoico)": {"comportamento_incomum_software", "aplicativos_nao_respondem", "lentidao_geral", "bloqueio_de_programas_legitimos"},
            "Licença do Windows Expirada": {"avisos_na_tela", "desativacao_de_funcionalidades", "comportamento_incomum_software"},
            "Licença do Windows Expirada (Grave)": {"avisos_na_tela", "comportamento_incomum_software", "restricao_de_configuracoes", "instabilidade_apos_atualizacao"}
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

    @Rule(Sintoma(sintoma="instabilidade_apos_atualizacao"))
    def diagnostico_atualizacao_simples(self):
        self.diagnostico_final = "Diagnóstico: Instabilidade do sistema após uma atualização de software."

    @Rule(Sintoma(sintoma="problemas_de_rede"),
          Sintoma(sintoma="conexao_lenta"))
    def diagnostico_problemas_conectividade(self):
        self.diagnostico_final = "Diagnóstico: Problemas de conectividade de rede."

    @Rule(Sintoma(sintoma="teclado_nao_funciona"),
          Sintoma(sintoma="mouse_nao_funciona"))
    def diagnostico_falha_perifericos(self):
        self.diagnostico_final = "Diagnóstico: Falha em periféricos de entrada (teclado/mouse)."

    @Rule(Sintoma(sintoma="impossibilidade_imprimir"),
          Sintoma(sintoma="erros_de_arquivo"))
    def diagnostico_problemas_impressao(self):
        self.diagnostico_final = "Diagnóstico: Problemas com a impressão de arquivos."

    @Rule(Sintoma(sintoma="ausencia_de_audio"),
          Sintoma(sintoma="camera_nao_funciona"),
          Sintoma(sintoma="microfone_nao_funciona"))
    def diagnostico_falha_audio_video(self):
        self.diagnostico_final = "Diagnóstico: Falha em dispositivos de áudio e vídeo."

    @Rule(Sintoma(sintoma="tela_azul"),
          Sintoma(sintoma="reinicializacoes_involuntarias"),
          Sintoma(sintoma="congelamento_de_tela"))
    def diagnostico_instabilidade_sistema(self):
        self.diagnostico_final = "Diagnóstico: Instabilidade crítica do sistema."

    @Rule(Sintoma(sintoma="lentidao_geral"),
          Sintoma(sintoma="aplicativos_nao_respondem"),
          Sintoma(sintoma="travamentos"))
    def diagnostico_desempenho_lento(self):
        self.diagnostico_final = "Diagnóstico: Desempenho geral do sistema muito lento."

    @Rule(Sintoma(sintoma="ruidos_estranhos"),
          Sintoma(sintoma="barulho_hd_alto"))
    def diagnostico_ruidos_excessivos(self):
        self.diagnostico_final = "Diagnóstico: Ruídos excessivos provenientes do hardware."

    @Rule(Sintoma(sintoma="problemas_de_boot"),
          Sintoma(sintoma="leds_piscando"))
    def diagnostico_problemas_inicializacao(self):
        self.diagnostico_final = "Diagnóstico: Problemas na inicialização do sistema."

    @Rule(Sintoma(sintoma="erros_de_arquivo"),
          Sintoma(sintoma="perda_de_dados"))
    def diagnostico_corrupcao_dados(self):
        self.diagnostico_final = "Diagnóstico: Corrupção de dados ou perda de arquivos."

    @Rule(Sintoma(sintoma="erros_de_arquivo"),
          Sintoma(sintoma="lentidao_geral"),
          Sintoma(sintoma="perda_de_dados"))
    def diagnostico_falha_disco_grave(self):
        self.diagnostico_final = "Diagnóstico: Falha crítica no disco rígido ou SSD."

    @Rule(Sintoma(sintoma="comportamento_incomum_software"),
          Sintoma(sintoma="lentidao_geral"),
          Sintoma(sintoma="conexao_lenta"))
    def diagnostico_virus_avancado(self):
        self.diagnostico_final = "Diagnóstico: Sistema pode estar infectado por vírus ou malware."

    @Rule(Sintoma(sintoma="problemas_de_video"),
          Sintoma(sintoma="instabilidade_apos_atualizacao"),
          Sintoma(sintoma="tela_azul"))
    def diagnostico_driver_video_grave(self):
        self.diagnostico_final = "Diagnóstico: Problemas com driver de vídeo ou placa gráfica."

    @Rule(Sintoma(sintoma="travamentos"),
          Sintoma(sintoma="reinicializacoes_involuntarias"),
          Sintoma(sintoma="perda_de_dados"))
    def diagnostico_memoria_falha_grave(self):
        self.diagnostico_final = "Diagnóstico: Falhas em módulos de memória RAM."

    @Rule(Sintoma(sintoma="nao_liga"),
          Sintoma(sintoma="sem_som_ou_luz"),
          Sintoma(sintoma="leds_piscando"))
    def diagnostico_placa_mae(self):
        self.diagnostico_final = "Diagnóstico: Falha na placa-mãe."

    @Rule(Sintoma(sintoma="nao_liga"),
          Sintoma(sintoma="sem_som_ou_luz"),
          Sintoma(sintoma="leds_piscando"),
          Sintoma(sintoma="ventoinhas_paradas"))
    def diagnostico_placa_mae_grave(self):
        self.diagnostico_final = "Diagnóstico: Falha grave na placa-mãe."


    @Rule(Sintoma(sintoma="problemas_de_boot"),
          Sintoma(sintoma="nao_detecta_hd"),
          Sintoma(sintoma="instabilidade_apos_atualizacao"))
    def diagnostico_bios_configuracao_grave(self):
        self.diagnostico_final = "Diagnóstico: Configuração incorreta ou corrompida da BIOS."

    @Rule(Sintoma(sintoma="travamentos"),
          Sintoma(sintoma="erros_de_arquivo"),
          Sintoma(sintoma="desligamentos_involuntarios"))
    def diagnostico_firmware_ssd(self):
        self.diagnostico_final = "Diagnóstico: Problemas de firmware no SSD."

    @Rule(Sintoma(sintoma="travamentos"),
          Sintoma(sintoma="erros_de_arquivo"),
          Sintoma(sintoma="desligamentos_involuntarios"),
          Sintoma(sintoma="perda_de_dados"))
    def diagnostico_firmware_ssd_grave(self):
        self.diagnostico_final = "Diagnóstico: Falha grave no firmware do SSD."

    @Rule(Sintoma(sintoma="problemas_de_rede"),
          Sintoma(sintoma="conexao_intermittente"),
          Sintoma(sintoma="sem_acesso_internet"))
    def diagnostico_conflito_ip(self):
        self.diagnostico_final = "Diagnóstico: Conflito de IP na rede."

    @Rule(Sintoma(sintoma="problemas_de_rede"),
          Sintoma(sintoma="conexao_intermittente"),
          Sintoma(sintoma="sem_acesso_internet"),
          Sintoma(sintoma="Wifi_nao_funciona"))
    def diagnostico_conflito_ip_persistente(self):
        self.diagnostico_final = "Diagnóstico: Conflito de IP persistente afetando conexão."

    @Rule(Sintoma(sintoma="Wifi_nao_funciona"),
          Sintoma(sintoma="nao_aparece_redes_wifi_para_se_conectar"),
          Sintoma(sintoma="instabilidade_apos_atualizacao"))
    def diagnostico_driver_wifi(self):
        self.diagnostico_final = "Diagnóstico: Falha no driver de rede sem fio."

    @Rule(Sintoma(sintoma="Wifi_nao_funciona"),
          Sintoma(sintoma="nao_aparece_redes_wifi_para_se_conectar"),
          Sintoma(sintoma="problemas_de_rede"),
          Sintoma(sintoma="comportamento_incomum_software"))
    def diagnostico_driver_wifi_grave(self):
        self.diagnostico_final = "Diagnóstico: Falha grave no driver de rede sem fio."

    @Rule(Sintoma(sintoma="pendrive_nao_reconhecido"),
          Sintoma(sintoma="teclado_nao_funciona"),
          Sintoma(sintoma="mouse_nao_funciona"))
    def diagnostico_usb_falha(self):
        self.diagnostico_final = "Diagnóstico: Portas USB com falha."

    @Rule(Sintoma(sintoma="pendrive_nao_reconhecido"),
          Sintoma(sintoma="teclado_nao_funciona"),
          Sintoma(sintoma="nao_detecta_dispositivo_usb"))
    def diagnostico_usb_placa_mae(self):
        self.diagnostico_final = "Diagnóstico: Falha na controladora USB da placa-mãe."

    @Rule(Sintoma(sintoma="instabilidade_apos_atualizacao"),
          Sintoma(sintoma="tela_azul"),
          Sintoma(sintoma="boot_loop"))
    def diagnostico_windows_update(self):
        self.diagnostico_final = "Diagnóstico: Problemas após atualização do Windows."

    @Rule(Sintoma(sintoma="instabilidade_apos_atualizacao"),
          Sintoma(sintoma="tela_azul"),
          Sintoma(sintoma="boot_loop"),
          Sintoma(sintoma="perda_de_dados"))
    def diagnostico_windows_update_grave(self):
        self.diagnostico_final = "Diagnóstico: Atualização crítica do Windows causou falhas graves."

    @Rule(Sintoma(sintoma="problemas_de_boot"),
          Sintoma(sintoma="sistema_nao_encontra_disco"),
          Sintoma(sintoma="mensagem_de_erro_inicial"))
    def diagnostico_erro_formatacao(self):
        self.diagnostico_final = "Diagnóstico: Erro de configuração após formatação."

    @Rule(Sintoma(sintoma="problemas_de_rede"),
          Sintoma(sintoma="Wifi_nao_funciona"),
          Sintoma(sintoma="ausencia_de_audio"),
          Sintoma(sintoma="camera_nao_funciona"))
    def diagnostico_drivers_pos_formatacao(self):
        self.diagnostico_final = "Diagnóstico: Drivers ausentes após formatação."

    @Rule(Sintoma(sintoma="comportamento_incomum_software"),
          Sintoma(sintoma="aplicativos_nao_respondem"),
          Sintoma(sintoma="lentidao_geral"))
    def diagnostico_antivirus_bloqueando(self):
        self.diagnostico_final = "Diagnóstico: Antivírus está interferindo no funcionamento do sistema."

    @Rule(Sintoma(sintoma="comportamento_incomum_software"),
          Sintoma(sintoma="aplicativos_nao_respondem"),
          Sintoma(sintoma="lentidao_geral"),
          Sintoma(sintoma="bloqueio_de_programas_legitimos"))
    def diagnostico_antivirus_paranoico(self):
        self.diagnostico_final = "Diagnóstico: Antivírus excessivamente restritivo bloqueando processos legítimos."

    @Rule(Sintoma(sintoma="avisos_na_tela"),
          Sintoma(sintoma="desativacao_de_funcionalidades"),
          Sintoma(sintoma="comportamento_incomum_software"))
    def diagnostico_licenca_expirada(self):
        self.diagnostico_final = "Diagnóstico: Licença do Windows expirada."

    @Rule(Sintoma(sintoma="avisos_na_tela"),
          Sintoma(sintoma="comportamento_incomum_software"),
          Sintoma(sintoma="restricao_de_configuracoes"),
          Sintoma(sintoma="instabilidade_apos_atualizacao"))
    def diagnostico_licenca_expirada_grave(self):
        self.diagnostico_final = "Diagnóstico: Licença expirada causando instabilidade e restrições no sistema."

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