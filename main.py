import pandas as pd
import logging
from dotenv import load_dotenv
from src.basic_info_processor import BasicInfoProcessor
from src.auo_plant_provider import AUOPlantProvider
from src.utils.logger import setup_logger
from openpyxl.workbook.workbook import Workbook
import openpyxl

load_dotenv()
setup_logger()

class PowerStationConverter:
    def __init__(self, provider: str):
        self.basic_info_processor = BasicInfoProcessor()
        self.device_provider = self._get_device_provider(provider)
    
    def convert_csv_to_xlsx(self, input_file: str):
        try:
            df = pd.read_csv(input_file)
            
            for _, row in df.iterrows():
                try:
                    workbook = openpyxl.Workbook()
                    self._process_basic_info(workbook, row)
                    self._process_device_list(row['電站名稱'])

                    output_filename = f"{row['電站代碼']}.xlsx"
                    workbook.save(output_filename)
                    logging.info(f"Successfully processed station {row['電站代碼']}")
                except Exception as e:
                    logging.error(f"Error processing station {row['電站代碼']}: {str(e)}")
                    continue
            
            logging.info("All stations processed")
            
        except Exception as e:
            logging.error(f"Program execution error: {str(e)}")
    
    def _get_device_provider(self, provider: str):
        providers = {
            'AUO': AUOPlantProvider(),
            # 'XXX': XXXDeviceProvider()
        }
        return providers.get(provider)
    
    def _process_basic_info(self, workbook: Workbook, row: dict):
        ws = self.basic_info_processor.setup_basic_info_sheet(workbook)
        self.basic_info_processor.fill_station_info(ws, row)

    def _process_device_list(self, plant_name: str):
        plant = self.device_provider.fetch_plant(plant_name)
        logging.info(plant)
        

def main():
    CSV_PATH = "template.csv"
    PROVIDER = "AUO"  # or "XXX" depending on your needs
    
    converter = PowerStationConverter(PROVIDER)
    converter.convert_csv_to_xlsx(CSV_PATH)

if __name__ == "__main__":
    main()