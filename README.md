
# README

Este projeto foi desenvolvido utilizando **Python 3.9**.  
Certifique-se de ter o Python 3.9 instalado em seu sistema. Caso ainda não tenha, baixe e instale a versão correta do [site oficial do Python](https://www.python.org/downloads/release/python-390/).

### Criação e ativação do ambiente virtual:

1. **Criação do ambiente virtual:**

No Windows, use o comando abaixo para criar o ambiente virtual chamado `venv`:

```bash
python -m venv venv
```

2. **Ativação do ambiente virtual:**

- No Windows:

```bash
.env\Scriptsctivate
```

- No macOS/Linux:

```bash
source venv/bin/activate
```

Após ativar o ambiente virtual, todas as dependências serão instaladas de forma isolada, sem interferir nas configurações globais do Python.

### Instalando as dependências:

Com o ambiente virtual ativado, instale as dependências necessárias com o comando:

```bash
pip install -r requirements.txt
```


## 2 - Fazer pushs para o repositório remoto

### Etapas para enviar alterações locais ao repositório remoto:

1. **Adicionar arquivos alterados ao stage:**

```bash
git add .
```

2. **Criar um commit com uma mensagem descritiva:**

```bash
git commit -m "sua mensagem"
```

3. **Enviar as alterações para o repositório remoto:**

```bash
git push origin main
```

> Substitua `"sua mensagem"` por algo descritivo, como `feat: adiciona nova funcionalidade` ou `fix: corrige bug no login`.
 
