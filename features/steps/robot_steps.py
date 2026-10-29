from behave import given, when, then
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from robot_simulator import RobotSimulator

@given('que o braço robótico está inicializado no simulador')
def step_init_sim(context):
    context.robot = RobotSimulator()
    context.current_x = 0
    context.current_y = 0
    context.current_z = 0
    context.current_roll = 0
    context.current_pitch = 0
    context.current_yaw = 0
    context.error = None

@given('a garra está aberta')
def step_garra_aberta(context):
    pass # Estado inicial padrão

@when('o robô move a garra para a coordenada X: {x:f}, Y: {y:f}, Z: {z:f}')
def step_move_xyz(context, x, y, z):
    context.current_x, context.current_y, context.current_z = x, y, z
    try:
        context.robot.move_to_position(x, y, z, context.current_roll, context.current_pitch, context.current_yaw)
    except ValueError as e:
        context.error = str(e)

@when('o robô fecha a garra')
def step_fecha_garra(context):
    context.robot.close_gripper()

@when('o robô levanta a garra para a coordenada X: {x:f}, Y: {y:f}, Z: {z:f}')
def step_levanta_garra(context, x, y, z):
    context.current_x, context.current_y, context.current_z = x, y, z
    try:
        context.robot.move_to_position(x, y, z, context.current_roll, context.current_pitch, context.current_yaw)
    except ValueError as e:
        context.error = str(e)

@when('o robô rotaciona o pulso em {angulo:d} graus no eixo Z')
def step_rotaciona_pulso(context, angulo):
    context.current_yaw += angulo
    try:
        context.robot.move_to_position(context.current_x, context.current_y, context.current_z, 
                                       context.current_roll, context.current_pitch, context.current_yaw)
    except ValueError as e:
        context.error = str(e)

@then('a ação deve ser executada com sucesso')
def step_sucesso(context):
    assert context.error is None, f"Falha na execução. Erro registrado: {context.error}"

@then('nenhuma mensagem de "movimento impossível" deve ser exibida')
def step_sem_erro_impossivel(context):
    context.robot.disconnect() # Limpa a simulação no final
    assert context.error is None, "Um movimento impossível foi detectado durante o teste!"
