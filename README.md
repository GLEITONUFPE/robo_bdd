# 🤖 Automação de Braço Robótico com BDD & Arquitetura Limpa

[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)
[![Testing Engine](https://img.shields.io/badge/BDD-Behave%20(Gherkin)-green.svg)](https://behave.readthedocs.io/)
[![Simulators](https://img.shields.io/badge/Simulators-PyBullet%20%7C%20CoppeliaSim-orange.svg)](https://pybullet.org/)
[![Architecture](https://img.shields.io/badge/Architecture-Hexagonal%20%2F%20Ports%20%26%20Adapters-purple.svg)]()

Este projeto executa testes funcionais do tipo **caixa preta** sobre manipuladores robóticos através de linguagem natural estruturada (**BDD com Gherkin**). 

A camada de teste não precisa conhecer sintaxes de baixo nível, cálculo de matrizes de transformação ou APIs proprietárias de simuladores: os cenários declaram ações espaciais em linguagem humana, enquanto o motor calcula a **Cinemática Inversa (IK)**, avalia as restrições articulares físicas e despacha o movimento para o simulador plugado.

---

## 📑 Sumário

1. [Visão Geral & Conceitos](#-visão-geral--conceitos)
2. [Arquitetura do Sistema](#-arquitetura-do-sistema)
3. [Pré-requisitos e Instalação do Ambiente](#-pré-requisitos-e-instalação-do-ambiente)
4. [Estrutura de Pastas e Componentes](#-estrutura-de-pastas-e-componentes)
5. [Mapeamento BDD (Gherkin -> Python)](#-mapeamento-bdd-gherkin---python)
6. [Execução dos Testes e Alternância de Simuladores](#-execução-dos-testes-e-alternância-de-simuladores)
7. [Simulação de Falhas e Movimentos Impossíveis](#-simulação-de-falhas-e-movimentos-impossíveis)
8. [Configuração de Novos Braços (Niryo, Kinova, KUKA)](#-configuração-de-novos-braços-niryo-kinova-kuka)
9. [Boas Práticas de Git e Controle de Versão](#-boas-práticas-de-git-e-controle-de-versão)

---

## 🎯 Visão Geral & Conceitos

### O que é o Teste Caixa Preta na Robótica?
No teste caixa preta, o analista ou engenheiro de QA valida **o que** o sistema deve fazer (ex.: *pegar um celular na orientação retrato e girá-lo 90 graus para paisagem*) sem se acoplar a **como** os atuadores executam a trajetória. 

Se o robô colidir, extrapolar o envelope de trabalho ou violar limites mecânicos, a camada de simulação interrompe o fluxo e emite um alerta explícito de violação física.

### Por que BDD (Behavior-Driven Development)?
O BDD unifica os requisitos do time de produto e as asserções de engenharia em arquivos legíveis (`.feature`). As especificações servem simultaneamente como documentação viva e suite de testes executável.

---

## 🏛 Arquitetura do Sistema

O projeto adota os princípios de **Clean Architecture**, **SOLID** e o padrão **Ports & Adapters (Arquitetura Hexagonal / Strategy)**:

```
[ Cenário BDD (.feature) ]
           │
           ▼
[ Step Definitions (robot_steps.py) ]
           │
           ▼  (Inversão de Dependência)
   [ <<interface>> ISimulator ]
           ▲
           ├── [ PyBulletAdapter ]   --> Motor Físico PyBullet (GUI 3D)
           └── [ CoppeliaSimAdapter ] --> Motor Físico CoppeliaSim (ZMQ/Remote API)
```

- **Independência de Framework:** A lógica de negócio e os cenários de teste não conhecem comandos específicos do PyBullet ou CoppeliaSim.
- **Princípio Aberto/Fechado (OCP):** Novos simuladores ou braços industriais podem ser adicionados criando novos adaptadores, sem alterar os testes existentes.

---

## 💻 Pré-requisitos e Instalação do Ambiente

### 1. Instalação do Python

O projeto requer **Python 3.10 ou superior**.

#### No Windows:
1. Acesse [python.org/downloads](https://www.python.org/downloads/) e baixe o instalador executável.
2. **Obrigatório:** Na primeira tela de instalação, marque a caixa de seleção:
   `☑ Add python.exe to PATH` (ou `Adicionar Python ao PATH`).
3. Conclua a instalação e abra o PowerShell para validar:
   ```powershell
   python --version
   pip --version
   ```

#### No Linux (Ubuntu/Debian):
```bash
sudo apt update
sudo apt install -y python3 python3-pip python3-venv
```

#### No macOS:
```bash
brew install python
```

---

### 2. Configuração do VS Code

1. Baixe e instale o [Visual Studio Code](https://code.visualstudio.com/).
2. Abra o VS Code e instale as seguintes extensões pela aba de Extensões (`Ctrl + Shift + X`):
   - **Python** (Microsoft)
   - **Pylance** (Microsoft)
   - **Cucumber (Gherkin) Full Support** (Steve Purves)

---

### 3. Configuração do Ambiente Virtual (`venv`)

Recomenda-se isolar os pacotes do projeto para evitar conflitos de dependências globais.

Abra a pasta do projeto no VS Code (`Arquivo` > `Abrir Pasta...`):

```bash
# 1. Criação do ambiente virtual
python -m venv .venv

# 2. Ativação do ambiente virtual
# No Windows (PowerShell):
.venv\Scripts\Activate.ps1

# No Windows (Prompt de Comando CMD):
.venv\Scripts\activate.bat

# No Linux / macOS:
source .venv/bin/activate
```

> **Dica Windows:** Se o PowerShell bloquear a ativação por política de execução, execute uma vez como Administrador:
> `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`

---

### 4. Instalação das Dependências

Com o terminal ativo no diretório raiz do projeto, instale os pacotes necessários:

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

O arquivo `requirements.txt` contempla:
- `behave`: Motor de orquestração BDD para Python.
- `pybullet`: Motor de física rígida, renderização 3D e cinemática inversa.
- `numpy`: Manipulação vetorial e cálculos matriciais.

---

## 📁 Estrutura de Pastas e Componentes

```text
meu_robo_bdd/
├── .gitignore
├── README.md
├── pyproject.toml              # Metadados do projeto e configurações de empacotamento
├── requirements.txt            # Dependências com versões controladas
├── config/
│   └── robot_config.json       # Parâmetros de juntas, URDFs e offsets por modelo
├── features/
│   ├── manipular_celular.feature  # Cenários declarativos em Gherkin
│   └── steps/
│       └── robot_steps.py      # Tradução dos passos para chamadas da interface
└── src/
    ├── __init__.py
    ├── core/
    │   ├── __init__.py
    │   └── interfaces.py       # Contrato abstrato ISimulator
    └── simulators/
        ├── __init__.py
        ├── pybullet_adapter.py    # Adaptador com motor PyBullet + IK
        └── coppeliasim_adapter.py # Adaptador com motor CoppeliaSim
```

---

## 📝 Mapeamento BDD (Gherkin -> Python)

O teste inicial simula o reposicionamento de uma garra sobre um dispositivo móvel, fechamento da pinça, elevação e rotação em 90 graus no eixo Z (transição Portrait -> Landscape).

### O Cenário Gherkin (`features/manipular_celular.feature`)

```gherkin
# language: pt
Funcionalidade: Teste de Manipulação de Celular com Braço Robótico

  Cenário: Rotacionar o celular da posição Portrait para Landscape (90 graus)
    Dado que o braço robótico está inicializado no simulador
    E a garra está aberta
    Quando o robô move a garra para a coordenada X: 0.5, Y: 0.0, Z: 0.1
    E o robô fecha a garra
    E o robô levanta a garra para a coordenada X: 0.5, Y: 0.0, Z: 0.4
    E o robô rotaciona o pulso em 90 graus no eixo Z
    Então a ação deve ser executada com sucesso
    E nenhuma mensagem de "movimento impossível" deve ser exibida
```

### O Contrato da Interface (`src/core/interfaces.py`)

Garante que qualquer simulador exponha os mesmos métodos de controle:

```python
from abc import ABC, abstractmethod

class ISimulator(ABC):
    @abstractmethod
    def connect(self) -> None:
        """Inicializa contexto físico e carrega o modelo do manipulador."""
        pass

    @abstractmethod
    def move_to_position(self, x: float, y: float, z: float, roll: float, pitch: float, yaw: float) -> None:
        """Aplica Cinemática Inversa e move o efetuador final."""
        pass

    @abstractmethod
    def close_gripper(self) -> None:
        """Aciona os atuadores da garra."""
        pass

    @abstractmethod
    def disconnect(self) -> None:
        """Finaliza a conexão e desaloca recursos."""
        pass
```

---

## 🚀 Execução dos Testes e Alternância de Simuladores

A seleção do simulador ocorre dinamicamente por meio da variável de ambiente `SIMULATOR`.

### 1. Execução Padrão com PyBullet (Visual 3D Ativo)

Por padrão, o PyBullet inicializa com a janela gráfica GUI:

```bash
behave
```

Uma janela do PyBullet será aberta exibindo o plano cartesiano, o manipulador robótico e o movimento correspondente a cada passo do Gherkin.

---

### 2. Alternando para CoppeliaSim (Mock/Adaptador Secundário)

Sem modificar uma única linha do arquivo `.feature`, alterne o motor via variável de ambiente:

#### No Windows (PowerShell):
```powershell
$env:SIMULATOR="coppeliasim"; behave
```

#### No Windows (CMD):
```cmd
set SIMULATOR=coppeliasim && behave
```

#### No Linux / macOS:
```bash
SIMULATOR=coppeliasim behave
```

---

## 🚨 Simulação de Falhas e Movimentos Impossíveis

O motor de cinemática inversa calcula os ângulos articulares $q_i$ para que o efetuador alcance a pose alvo $(X, Y, Z, \phi, \theta, \psi)$. Caso o ponto requisitado viole os limites mínimos ou máximos das juntas ($q_i < q_{min}$ ou $q_i > q_{max}$), uma exceção física é disparada.

### Como induzir o erro de teste:

1. Abra o arquivo `features/manipular_celular.feature`.
2. Altere uma das coordenadas para um valor fora do envelope de trabalho do braço:
   ```gherkin
   Quando o robô levanta a garra para a coordenada X: 5.0, Y: 0.0, Z: 8.0
   ```
3. Execute novamente:
   ```bash
   behave
   ```
4. **Resultado esperado:** O Behave interrompe o cenário no passo afetado e acusa a violação mecânica calculada pelo motor:
   ```text
   AssertionError: Falha na execução. Erro registrado: MOVIMENTO IMPOSSÍVEL: A junta 2 excede os limites físicos.
   ```

---

## 🔧 Configuração de Novos Braços (Niryo, Kinova, KUKA)

O arquivo `config/robot_config.json` centraliza os caminhos dos arquivos de descrição cinemática (**URDF**) e os índices das extremidades (**End-Effectors**):

```json
{
    "default_simulator": "pybullet",
    "robots": {
        "kuka": {
            "urdf_path": "kuka_iiwa/model.urdf",
            "end_effector_index": 6
        },
        "niryo_one": {
            "urdf_path": "niryo_one/niryo_one.urdf",
            "end_effector_index": 7
        },
        "kinova": {
            "urdf_path": "kinova/j2s7s300.urdf",
            "end_effector_index": 8
        }
    }
}
```

Para carregar o **Niryo One** ou o **Kinova**, basta transferir a pasta do URDF correspondente para a raiz do projeto e atualizar o caminho relativo no JSON. O `PyBulletAdapter` consome essa configuração diretamente.

---

## 🛡 Boas Práticas de Git e Controle de Versão

Para manter a branch `main` protegida e estável, todo o desenvolvimento deve ocorrer na branch `dev`:

1. **Garantir que está trabalhando na branch `dev`:**
   ```bash
   git checkout dev
   ```

2. **Registrar alterações locais:**
   ```bash
   git add .
   git commit -m "feat: implementa validacao de limites articulares para Niryo One"
   git push origin dev
   ```

3. **Promover alterações para a `main` após testes aprovados:**
   ```bash
   git checkout main
   git pull origin main
   git merge dev
   git push origin main
   git checkout dev
   ```