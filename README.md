# Uninstall Android

## Descrição

Aplicativo desktop em **Python/Tkinter** para gerenciamento e desinstalação de aplicativos Android conectados via **ADB (Android Debug Bridge)**. Ideal para remover aplicativos do usuário 0 sem necessidade de root.

## 🚀 Tecnologias Utilizadas

* **Python 3.11+** - Linguagem de programação
* **Tkinter** - Interface gráfica
* **asyncio** - Execução assíncrona
* **ADB (Platform Tools)** - Comunicação com dispositivos Android

## 📋 Pré-requisitos

* Python >= 3.11
* Windows / Linux / macOS
* ADB incluído na pasta `tools/`
* uv (gerenciador de pacotes Python)

## 🛠️ Configuração do Ambiente

### 1. Preparação do Ambiente Virtual

```bash
# Inicializar projeto com uv
uv init

# Criar ambiente virtual
uv venv .venv

# Ativar ambiente virtual (Windows)
.venv\Scripts\activate

# Ativar ambiente virtual (Linux/Mac)
source .venv/bin/activate
```

### 2. Instalação das Dependências

```bash
# Adicionar dependências principais
uv add asyncio tk
```

### 3. Configuração do ADB

Certifique-se que o executável **ADB** está localizado em `tools/adb.exe`.

## 🏗️ Estrutura do Projeto

```
Uninstall_Android/
├── core/
│   ├── adb_manager.py   # Gerencia comandos ADB assíncronos
│   └── logger.py        # Gerencia logs da interface
├── tools/
│   └── adb.exe          # Executável do ADB
├── ui/
│   └── app.py           # Interface Tkinter principal
├── uv.toml              # Configurações do projeto UV
└── README.md            # Este arquivo
```

## 🚀 Executando a Aplicação

### Desenvolvimento Local

```bash
python ui/app.py
```

1. Conecte seu dispositivo Android via USB e habilite a **Depuração USB**.
2. Use a barra de pesquisa para filtrar pacotes.
3. Selecione os aplicativos que deseja desinstalar e clique em **"Desinstalar Selecionados"**.
4. Acompanhe o log no painel inferior.

## 📝 Funcionalidades Implementadas

* Verificação automática da instalação do ADB
* Conexão com dispositivos Android
* Listagem de todos os pacotes do usuário 0
* Pesquisa por nome de pacote
* Seleção múltipla e desinstalação de aplicativos
* Log em tempo real das operações ADB
* Scroll da lista de pacotes via roda do mouse

## 🏛️ Arquitetura do Projeto

* **core/**: Lógica de comunicação com ADB e logging
* **ui/**: Interface gráfica Tkinter
* **tools/**: Contém o executável ADB
* **uv.toml**: Configurações do gerenciador de pacotes UV

## 🔧 Comandos Úteis

```bash
# Executar aplicação
python ui/app.py
```

## 📄 Licença

Este projeto está sob a licença MIT.

## 👨‍💻 Desenvolvedor

Bruno Wilson - BrunoWil
