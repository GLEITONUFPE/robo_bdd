import pybullet as p
import pybullet_data
import time
import math

class RobotSimulator:
    def __init__(self):
        # Conecta ao simulador com interface gráfica
        self.physicsClient = p.connect(p.GUI)
        p.setAdditionalSearchPath(pybullet_data.getDataPath())
        p.setGravity(0, 0, -9.81)
        
        # Carrega um plano e um braço robótico padrão (Franka Panda ou KUKA)
        self.planeId = p.loadURDF("plane.urdf")
        self.robotId = p.loadURDF("kuka_iiwa/model.urdf", [0, 0, 0], useFixedBase=True)
        self.num_joints = p.getNumJoints(self.robotId)
        self.end_effector_index = 6 # Índice da garra no modelo KUKA
        
    def move_to_position(self, x, y, z, roll, pitch, yaw):
        # Converte graus para radianos
        orientation = p.getQuaternionFromEuler([math.radians(roll), math.radians(pitch), math.radians(yaw)])
        
        # Cinemática Inversa: Calcula os ângulos necessários para as juntas
        joint_poses = p.calculateInverseKinematics(
            self.robotId, 
            self.end_effector_index, 
            [x, y, z], 
            orientation
        )
        
        # Validação de Movimento Impossível (Limites Físicos)
        for i in range(self.num_joints):
            info = p.getJointInfo(self.robotId, i)
            lower_limit, upper_limit = info[8], info[9]
            # Se o limite inferior for menor que o superior, existe restrição
            if lower_limit < upper_limit:
                if joint_poses[i] < lower_limit or joint_poses[i] > upper_limit:
                    raise ValueError(f"MOVIMENTO IMPOSSÍVEL: A junta {i} excede os limites físicos para atingir esta coordenada.")
        
        # Executa o movimento no simulador
        for i in range(self.num_joints):
            p.setJointMotorControl2(bodyIndex=self.robotId, jointIndex=i, 
                                    controlMode=p.POSITION_CONTROL, 
                                    targetPosition=joint_poses[i])
        
        # Avança a simulação para o robô se mover
        for _ in range(100):
            p.stepSimulation()
            time.sleep(1./240.)
            
    def close_gripper(self):
        # Lógica simulada de fechamento da garra
        print("Garra fechada.")
        
    def disconnect(self):
        p.disconnect()
