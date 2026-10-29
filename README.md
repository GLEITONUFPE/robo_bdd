🤖 Automação de Braço Robótico com BDD & Arquitetura LimpaEste projeto executa testes funcionais do tipo caixa preta sobre manipuladores robóticos através de linguagem natural estruturada (BDD com Gherkin).A camada de teste não precisa conhecer sintaxes de baixo nível, cálculo de matrizes de transformação ou APIs proprietárias de simuladores: os cenários declaram ações espaciais em linguagem humana, enquanto o motor calcula a Cinemática Inversa (IK), avalia as restrições articulares físicas e despacha o movimento para o simulador plugado.📑 SumárioVisão Geral & ConceitosArquitetura do SistemaPré-requisitos e Instalação do AmbienteEstrutura de Pastas e ComponentesMapeamento BDD (Gherkin -> Python)Execução dos Testes e Alternância de SimuladoresSimulação de Falhas e Movimentos ImpossíveisConfiguração de Novos Braços (Niryo, Kinova, KUKA)Boas Práticas de Git e Controle de Versão🎯 Visão Geral & ConceitosO que é o Teste Caixa Preta na Robótica?No teste caixa preta, o analista ou engenheiro de QA valida o que o sistema deve fazer (ex.: pegar um celular na orientação retrato e girá-lo 90 graus para paisagem) sem se acoplar a como os atuadores executam a trajetória.Se o robô colidir, extrapolar o envelope de trabalho ou violar limites mecânicos, a camada de simulação interrompe o fluxo e emite um alerta explícito de violação física.Por que BDD (Behavior-Driven Development)?O BDD unifica os requisitos do time de produto e as asserções de engenharia em arquivos legíveis (.feature). As especificações servem simultaneamente como documentação viva e suite de testes executável.🏛 Arquitetura do SistemaO projeto adota os princípios de Clean Architecture, SOLID e o padrão Ports & Adapters (Arquitetura Hexagonal / Strategy):[ Cenário BDD (.feature) ]
           │
           ▼
[ Step Definitions (robot_steps.py) ]
           │
           ▼  (Inversão de Dependência)
   [ <<interface>> ISimulator ]
           ▲
           ├── [ PyBulletAdapter ]   --> Motor Físico PyBullet (GUI 3D)
           └── [ CoppeliaSimAdapter ] --> Motor Físico CoppeliaSim (ZMQ/Remote API)
Independência de Framework: A lógica de negócio e os cenários de teste não conhecem comandos específicos do PyBullet ou CoppeliaSim.Princípio Aberto/Fechado (OCP): Novos simuladores ou braços industriais podem ser adicionados criando novos adaptadores, sem alterar os testes existentes.💻 Pré-requisitos e Instalação do Ambiente1. Instalação do PythonO projeto requer Python 3.10 ou superior.No Windows:Acesse python.org/downloads e baixe o instalador executável.Obrigatório: Na primeira tela de instalação, marque a caixa de seleção:
☑ Add python.exe to PATH (ou Adicionar Python ao PATH).Conclua a instalação e abra o PowerShell para validar:python --version
pip --version
No Linux (Ubuntu/Debian):sudo apt update
sudo apt install -y python3 python3-pip python3-venv
No macOS:brew install python
2. Configuração do VS CodeBaixe e instale o Visual Studio Code.Abra o VS Code e instale as seguintes extensões pela aba de Extensões (Ctrl + Shift + X):Python (Microsoft)Pylance (Microsoft)Cucumber (Gherkin) Full Support (Steve Purves)3. Configuração do Ambiente Virtual (venv)Recomenda-se isolar os pacotes do projeto para evitar conflitos de dependências globais.Abra a pasta do projeto no VS Code (Arquivo > Abrir Pasta...):# 1. Criação do ambiente virtual
python -m venv .venv

# 2. Ativação do ambiente virtual
# No Windows (PowerShell):
.venv\Scripts\Activate.ps1

# No Windows (Prompt de Comando CMD):
.venv\Scripts\activate.bat

# No Linux / macOS:
source .venv/bin/activate
Dica Windows: Se o PowerShell bloquear a ativação por política de execução, execute uma vez como Administrador:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser4. Instalação das DependênciasCom o terminal ativo no diretório raiz do projeto, instale os pacotes necessários:pip install --upgrade pip
pip install -r requirements.txt
O arquivo requirements.txt contempla:behave: Motor de orquestração BDD para Python.pybullet: Motor de física rígida, renderização 3D e cinemática inversa.numpy: Manipulação vetorial e cálculos matriciais.📁 Estrutura de Pastas e Componentesmeu_robo_bdd/
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
📝 Mapeamento BDD (Gherkin -> Python)O teste inicial simula o reposicionamento de uma garra sobre um dispositivo móvel, fechamento da pinça, elevação e rotação em 90 graus no eixo Z (transição Portrait -> Landscape).O Cenário Gherkin (features/manipular_celular.feature)# language: pt
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
O Contrato da Interface (src/core/interfaces.py)Garante que qualquer simulador exponha os mesmos métodos de controle:from abc import ABC, abstractmethod

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
🚀 Execução dos Testes e Alternância de SimuladoresA seleção do simulador ocorre dinamicamente por meio da variável de ambiente SIMULATOR.1. Execução Padrão com PyBullet (Visual 3D Ativo)Por padrão, o PyBullet inicializa com a janela gráfica GUI:behave
Uma janela do PyBullet será aberta exibindo o plano cartesiano, o manipulador robótico e o movimento correspondente a cada passo do Gherkin.2. Alternando para CoppeliaSim (Mock/Adaptador Secundário)Sem modificar uma única linha do arquivo .feature, alterne o motor via variável de ambiente:No Windows (PowerShell):$env:SIMULATOR="coppeliasim"; behave
No Windows (CMD):set SIMULATOR=coppeliasim && behave
No Linux / macOS:SIMULATOR=coppeliasim behave
🚨 Simulação de Falhas e Movimentos ImpossíveisO motor de cinemática inversa calcula os ângulos articulares $q_i$ para que o efetuador alcance a pose alvo $(X, Y, Z, \phi, \theta, \psi)$. Caso o ponto requisitado viole os limites mínimos ou máximos das juntas ($q_i < q_{min}$ ou $q_i > q_{max}$), uma exceção física é disparada.Como induzir o erro de teste:Abra o arquivo features/manipular_celular.feature.Altere uma das coordenadas para um valor fora do envelope de trabalho do braço:Quando o robô levanta a garra para a coordenada X: 5.0, Y: 0.0, Z: 8.0
Execute novamente:behave
Resultado esperado: O Behave interrompe o cenário no passo afetado e acusa a violação mecânica calculada pelo motor:AssertionError: Falha na execução. Erro registrado: MOVIMENTO IMPOSSÍVEL: A junta 2 excede os limites físicos.
🔧 Configuração de Novos Braços (Niryo, Kinova, KUKA)O arquivo config/robot_config.json centraliza os caminhos dos arquivos de descrição cinemática (URDF) e os índices das extremidades (End-Effectors):{
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
Para carregar o Niryo One ou o Kinova, basta transferir a pasta do URDF correspondente para a raiz do projeto e atualizar o caminho relativo no JSON. O PyBulletAdapter consome essa configuração diretamente.🛡 Boas Práticas de Git e Controle de VersãoPara manter a branch main protegida e estável, todo o desenvolvimento deve ocorrer na branch dev:Garantir que está trabalhando na branch dev:git checkout dev
Registrar alterações locais:git add .
git commit -m "feat: implementa validacao de limites articulares para Niryo One"
git push origin dev
Promover alterações para a main após testes aprovados:git checkout main
git pull origin main
git merge dev
git push origin main
git checkout dev
