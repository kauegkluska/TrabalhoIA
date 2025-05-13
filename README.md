
# README

Este projeto foi desenvolvido utilizando **Python 3.9**.  
Certifique-se de ter o Python 3.9 instalado em seu sistema. Caso ainda não tenha, baixe e instale a versão correta no [site oficial do Python](https://www.python.org/downloads/release/python-390/).

---

### Etapas de preparação do ambiente

#### 1. Clone o projeto

```bash
git clone https://github.com/kauegkluska/TrabalhoIA.git
```

#### 2. Verifique se o Python 3.9 está instalado

```bash
py -3.9 --version
```

#### 3. Crie o ambiente virtual com Python 3.9

```bash
py -3.9 -m venv venv
```

#### 4. Ative o ambiente virtual

- No Windows:

```bash
.\venv\Scripts\activate
```

Se a ativação for bem-sucedida, aparecerá `(venv)` antes da linha de comando.

---

#### ⚠️ Possível erro ao ativar o ambiente

Se ocorrer o erro:

> "não pode ser carregado porque a execução de scripts foi desabilitada neste sistema"

Use este comando no PowerShell para habilitar a execução temporária de scripts:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

Depois, execute novamente o comando de ativação do ambiente virtual.

---

#### 5. Verifique a versão do Python no ambiente

```bash
python --version
```

#### 6. Instale as dependências

```bash
pip install -r requirements.txt
```

> Após ativar o ambiente virtual, todas as dependências serão instaladas de forma isolada, sem interferir nas configurações globais do Python.

---

## 2 - Enviar alterações para o repositório remoto

### Etapas para enviar alterações locais ao GitHub:

1. Adicionar arquivos modificados ao stage:

```bash
git add .
```

2. Criar um commit com uma mensagem descritiva:

```bash
git commit -m "sua mensagem"
```

3. Enviar as alterações para o repositório remoto:

```bash
git push origin main
```

4. Para puxar alterações do repositório remoto:

```bash
git pull origin main
```

> Substitua `"sua mensagem"` por algo descritivo.
