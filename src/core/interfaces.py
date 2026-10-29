from abc import ABC, abstractmethod

class ISimulator(ABC):
    @abstractmethod
    def connect(self) -> None:
        pass

    @abstractmethod
    def move_to_position(self, x: float, y: float, z: float, roll: float, pitch: float, yaw: float) -> None:
        pass

    @abstractmethod
    def close_gripper(self) -> None:
        pass

    @abstractmethod
    def disconnect(self) -> None:
        pass
