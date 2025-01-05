import os
import requests
from typing import Optional, Dict, List
from urllib.parse import unquote
from src.plant_provider import PlantProvider, Plant, Device
from src.utils.logger import get_logger

logger = get_logger(__name__)

class AUOPlantProvider(PlantProvider):
    _instance = None
    _session: Optional[requests.Session] = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AUOPlantProvider, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not self._session:
            self._session = self._login()
    
    def _login(self) -> Optional[requests.Session]:
        """Login to AUO system and return session"""
        try:
            session = requests.Session()
            login_url = "https://gms.auo.com/MvcWebPortal/Login/Login3"
            headers = {
                "Content-Type": "application/json",
                "Referer": "https://gms.auo.com/MvcWebPortal/",
                "Origin": "https://gms.auo.com",
                "x-requested-with": "XMLHttpRequest"
            }
            login_data = {
                "Act": os.getenv("AUO_GMS_ACCOUNT"),
                "Psw": os.getenv("AUO_GMS_PASSWORD"),
                "RememberMe": True
            }
            
            response = session.post(login_url, headers=headers, json=login_data)
            if response.status_code == 200:
                return session
            return None
        except Exception as e:
            print(f"Login failed: {str(e)}")
            return None

    def _get_plant_no(self, plant_name: str) -> Optional[str]:
        """Get plant number from station code"""
        try:
            headers = {
                "Referer": "https://gms.auo.com/MvcWebPortal/Allsystem/index",
                "Origin": "https://gms.auo.com",
                "x-requested-with": "XMLHttpRequest"
            }
            response = self._session.get(
                "https://gms.auo.com/MvcWebPortal/api/GetPlantsReduce?special_flag=Y",
                headers=headers
            )
            
            if response.status_code == 200:
                plants = response.json()
                for plant in plants:
                    if plant_name in plant["PlantName"]:
                        return unquote(plant["PlantNo"])
            return None
        except Exception as e:
            print(f"Failed to get plant number: {str(e)}")
            return None

    def _get_device_list(self, plant_no: str) -> Optional[Dict]:
        """Get device list for a specific plant"""
        try:
            headers = {
                "Referer": "https://gms.auo.com/MvcWebPortal/Allsystem/index",
                "Origin": "https://gms.auo.com",
                "x-requested-with": "XMLHttpRequest"
            }
            params = {
                "plant_no": plant_no,
                "timeType": "UTC",
                "timeZoneOffSet": "8",
                "SW_Version_User": "ADVANCED",
                "lang": "zh-TW",
                "PlantType": "BENQDL"
            }
            response = self._session.get(
                "https://gms.auo.com/MvcWebPortal/api/GetDeviceTreeData",
                headers=headers,
                params=params
            )
            
            if response.status_code == 200:
                return response.json()
            return None
        except Exception as e:
            print(f"Failed to get device list: {str(e)}")
            return None

    def _get_plant_info(self, plant_no: str) -> Optional[Dict]:
        """Get detailed plant information including grid connection date"""
        try:
            headers = {
                "Referer": "https://gms.auo.com/MvcWebPortal/Allsystem/index",
                "Origin": "https://gms.auo.com",
                "x-requested-with": "XMLHttpRequest"
            }
            params = {
                "plantNo": plant_no,
                "format": "json"
            }
            response = self._session.get(
                "https://gms.auo.com/MvcWebPortal/api/GetOnePlantInfo",
                headers=headers,
                params=params
            )
            
            if response.status_code == 200:
                return response.json()
            return None
        except Exception as e:
            print(f"Failed to get plant info: {str(e)}")
            return None

    def _parse_devices(self, device_data: Dict, plant_info: Dict) -> Plant:
        """Parse device data into Plant object"""
        pyranometers = []
        thermometers = []
        inverters = []
        grid_connection_date = None

        # Get grid connection date from plant info
        if plant_info and "OnGridDate" in plant_info:
            grid_connection_date = plant_info["OnGridDate"].split("T")[0]  # Format: "2021-01-26T00:00:00" -> "2021-01-26"

        # 計數器字典
        device_counters = {
            'PYR': 0,  # 日照計
            'THR': 0,  # 溫度計
            'INV': 0   # 逆變器
        }

        for device in device_data.get("lstDeviceTree", []):
            power_collector_key = device.get('power_collector_key', '')

            if device['unit_type'] == 'MODULE_THERMAL':
                device_counters['THR'] += 1
                device_id = f"{power_collector_key}-THR-{device_counters['THR']:02d}"  # e.g. BDL22206042-THR-01
                thermometers.append(Device(
                    device_name=device['description'],
                    device_serial_number=device['unit_id'],
                    device_id=device_id
                ))
            elif device['unit_type'] == 'INVERTER':
                device_counters['INV'] += 1
                device_id = f"{power_collector_key}-INV-{device_counters['INV']:02d}"
                inverters.append(Device(
                    device_name=device['description'],
                    device_serial_number=device['unit_id'],
                    device_id=device_id
                ))
            elif device['unit_type'] == 'RADIATION':
                device_counters['PYR'] += 1
                device_id = f"{power_collector_key}-PYR-{device_counters['PYR']:02d}"
                pyranometers.append(Device(
                    device_name=device['description'],
                    device_serial_number=device['unit_id'],
                    device_id=device_id
                ))

        return Plant(
            grid_connection_date=grid_connection_date,
            pyranometers=pyranometers,
            thermometers=thermometers,
            inverters=inverters
        )

    def fetch_plant(self, plant_name: str) -> Plant:
        """Fetch device information for a station"""
        if not self._session:
            raise Exception("Not logged in")
            
        plant_no = self._get_plant_no(plant_name)
        if not plant_no:
            raise Exception(f"Plant not found for station: {plant_name}")
        
        plant_info = self._get_plant_info(plant_no)
        if not plant_info:
            raise Exception(f"Failed to get plant info for plant: {plant_no}")

        device_data = self._get_device_list(plant_no)
        if not device_data:
            raise Exception(f"Failed to get device data for plant: {plant_no}")
            

        return self._parse_devices(device_data, plant_info)
