from src.core.interfaces import ISimulator

class CoppeliaSimAdapter(ISimulator):
    def __init__(self, scene_path: str):
        self.scene_path = scene_path
        
    def connect(self) -> None:
        print(f"[CoppeliaSim] Conectado na cena: {self.scene_path}")

    def move_to_position(self, x: float, y: float, z: float, roll: float, pitch: float, yaw: float) -> None:
        print(f"[CoppeliaSim] Movendo para X:{x} Y:{y} Z:{z} Roll:{roll} Pitch:{pitch} Yaw:{yaw}")

    def close_gripper(self) -> None:
        print("[CoppeliaSim] Garra fechada via atuador local.")

    def disconnect(self) -> None:
        print("[CoppeliaSim] Desconectado.")
