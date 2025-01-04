import pandas as pd
import logging
from dotenv import load_dotenv
import os
from basic_info_processor import BasicInfoProcessor

load_dotenv()

# 設置日誌
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='power_station_converter.log'
)
class PowerStationConverter:
    def __init__(self, api_key):
        self.basic_info_processor = BasicInfoProcessor(api_key)
    
    def convert_csv_to_xlsx(self, input_file: str, provider: str):
        """
        Convert CSV data to XLSX files with device information from specified provider
        """
        try:
            df = pd.read_csv(input_file)
            
            # Select device provider based on input
            device_provider = self._get_device_provider(provider)
            
            for _, row in df.iterrows():
                try:
                    # Process basic information
                    wb = self.basic_info_processor.create_base_template()
                    self.basic_info_processor.fill_station_info(row, wb)
                    
                    # Process device information
                    # device_info = self._process_device_list(row['電站代碼'], device_provider)
                    # self._fill_device_info(wb, device_info)
                    
                    # Save workbook
                    output_filename = f"{row['電站代碼']}.xlsx"
                    wb.save(output_filename)
                    logging.info(f"Successfully processed station {row['電站代碼']}")
                except Exception as e:
                    logging.error(f"Error processing station {row['電站代碼']}: {str(e)}")
                    continue
            
            logging.info("All stations processed")
            
        except Exception as e:
            logging.error(f"Program execution error: {str(e)}")
    
    def _get_device_provider(self, provider: str):
        """
        Factory method to create appropriate device provider
        """
        # providers = {
        #     'AUO': AUODeviceProvider(),
        #     'XXX': XXXDeviceProvider()
        # }
        pass
        # return providers.get(provider)
    
    def _process_device_list(self, station_code: str, provider):
        """
        Fetch device information from provider
        """
        pass
        # return provider.fetch_device_info(station_code)
    
    def _fill_device_info(self, workbook, device_info):
        """
        Fill device information into the workbook
        """
        # Implementation for filling device info into worksheet
        pass

def main():
    CSV_PATH = "template.csv"
    PROVIDER = "AUO"  # or "XXX" depending on your needs
    
    converter = PowerStationConverter(os.getenv("GOOGLE_MAPS_API_KEY"))
    converter.convert_csv_to_xlsx(CSV_PATH, PROVIDER)

if __name__ == "__main__":
    main()