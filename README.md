🤖 Simulação de Braço Robótico com BDD (PyBullet + Behave)
Este projeto permite testar movimentos de um braço robótico em um simulador 3D utilizando a linguagem natural (Gherkin). A ideia principal é permitir que qualquer pessoa escreva testes de "caixa preta" sem precisar saber programar em linguagens complexas de robótica.

O motor do projeto traduz os comandos de texto em coordenadas espaciais, calcula a Cinemática Inversa (IK) e valida se o movimento é fisicamente possível para o robô antes de executá-lo.

📋 1. Pré-requisitos
Antes de começar, você precisa ter o Python e um editor de código instalados no seu computador.

Instalando o Python
Acesse o site oficial do Python: python.org/downloads
Baixe a versão mais recente para o seu sistema operacional (Windows, Mac ou Linux).
MUITO IMPORTANTE (Windows): Durante a instalação, certifique-se de marcar a caixa "Add Python to PATH" (Adicionar Python ao PATH) na primeira tela do instalador. Sem isso, os comandos no terminal não funcionarão.
Conclua a instalação padrão.
Instalando o VS Code (Recomendado)
Baixe o Visual Studio Code em: code.visualstudio.com
Instale o programa.
Sugerimos instalar a extensão Python da Microsoft e a extensão Cucumber (Gherkin) Full Support no VS Code para o código ficar colorido e mais fácil de ler.
🛠️ 2. Configuração do Projeto
Passo 1: Abrir o projeto no VS Code
Extraia o arquivo .zip deste projeto para uma pasta no seu computador.
Abra o VS Code.
Clique em Arquivo > Abrir Pasta... (ou File > Open Folder...).
Selecione a pasta específica chamada meu_robo_bdd (a pasta onde este arquivo README.md e o requirements.txt estão localizados).
Passo 2: Instalar as dependências
Este projeto utiliza bibliotecas externas que precisam ser baixadas.

No VS Code, abra o terminal integrado clicando em Visualizar > Terminal (ou pressione Ctrl + `).
No terminal, certifique-se de que você está dentro da pasta meu_robo_bdd.
Digite o seguinte comando e aperte Enter:
pip install -r requirements.txt

O que isso instala?

behave: A ferramenta que lê os arquivos de texto (Gherkin) e roda os testes (BDD).
pybullet: O simulador de física e robótica 3D.
numpy: Biblioteca de matemática usada nos bastidores pelo PyBullet.
📂 3. Entendendo a Estrutura
requirements.txt: Lista de dependências do projeto.
robot_simulator.py: O coração do projeto em Python. Ele conecta ao PyBullet, carrega o modelo 3D do robô e calcula se os limites físicos (juntas) suportam as coordenadas desejadas.
features/manipular_celular.feature: O arquivo principal para você editar! Aqui ficam os testes em formato de texto simples (Gherkin).
features/steps/robot_steps.py: O "tradutor". Ele conecta as frases escritas no arquivo .feature com as funções matemáticas do robot_simulator.py.
🚀 4. Como Executar os Testes
Com tudo instalado, rodar a simulação é muito simples.

Abra o terminal no VS Code (dentro da pasta meu_robo_bdd).
Digite o comando abaixo e pressione Enter:
behave

O que vai acontecer? Uma janela gráfica em 3D (PyBullet) será aberta. Você verá o braço robótico carregado no cenário se movendo exatamente para as coordenadas XYZ e rotacionando conforme descrito no arquivo manipular_celular.feature.

No terminal, o Behave mostrará quais passos passaram e quais falharam.

🚨 5. Testando Movimentos Impossíveis
Uma das principais funções deste projeto é barrar movimentos que o robô físico não conseguiria fazer (ex: tentar alcançar uma coordenada a 10 metros de distância ou girar uma junta além do seu limite mecânico).

Para testar isso:

Abra o arquivo features/manipular_celular.feature.
Altere uma coordenada Z para um valor absurdo. Exemplo: E o robô levanta a garra para a coordenada X: 0.5, Y: 0.0, Z: 5.0
Salve o arquivo e rode behave novamente no terminal.
A simulação será interrompida e o teste falhará, exibindo no terminal uma mensagem segura alertando sobre o "Movimento Impossível".