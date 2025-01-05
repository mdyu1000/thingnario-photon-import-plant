from abc import ABC, abstractmethod
from typing import List
from dataclasses import dataclass

@dataclass
class Device:
    device_name: str
    device_serial_no: str

@dataclass
class Plant:
    grid_connection_date: str
    pyranometers: List[Device]
    thermometers: List[Device]
    inverters: List[Device]

class PlantProvider(ABC):
    @abstractmethod
    def fetch_plant(self, station_code: str) -> Plant:
        pass
