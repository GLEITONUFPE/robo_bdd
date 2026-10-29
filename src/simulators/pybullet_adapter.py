import pybullet as p
import pybullet_data
import math
import time
from src.core.interfaces import ISimulator

class PyBulletAdapter(ISimulator):
    def __init__(self, urdf_path: str):
        self.urdf_path = urdf_path
        self.robot_id = None
        self.physics_client = None
        self.num_joints = 0
        self.end_effector_index = 6

    def connect(self) -> None:
        self.physics_client = p.connect(p.GUI)
        p.setAdditionalSearchPath(pybullet_data.getDataPath())
        p.setGravity(0, 0, -9.81)
        p.loadURDF("plane.urdf")
        self.robot_id = p.loadURDF(self.urdf_path, [0, 0, 0], useFixedBase=True)
        self.num_joints = p.getNumJoints(self.robot_id)

    def move_to_position(self, x: float, y: float, z: float, roll: float, pitch: float, yaw: float) -> None:
        orientation = p.getQuaternionFromEuler([math.radians(roll), math.radians(pitch), math.radians(yaw)])
        joint_poses = p.calculateInverseKinematics(self.robot_id, self.end_effector_index, [x, y, z], orientation)
        
        for i in range(self.num_joints):
            info = p.getJointInfo(self.robot_id, i)
            lower_limit, upper_limit = info[8], info[9]
            if lower_limit < upper_limit:
                if joint_poses[i] < lower_limit or joint_poses[i] > upper_limit:
                    raise ValueError(f"MOVIMENTO IMPOSSÍVEL: A junta {i} excede os limites físicos.")
        
        for i in range(self.num_joints):
            p.setJointMotorControl2(bodyIndex=self.robot_id, jointIndex=i, controlMode=p.POSITION_CONTROL, targetPosition=joint_poses[i])
        
        for _ in range(100):
            p.stepSimulation()
            time.sleep(1./240.)

    def close_gripper(self) -> None:
        print("[PyBullet] Garra fechada.")

    def disconnect(self) -> None:
        if self.physics_client is not None:
            p.disconnect()
