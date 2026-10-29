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
