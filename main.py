import pandas as pd
import openpyxl
from openpyxl.styles import PatternFill, Font, Alignment
import requests
import logging
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()

# 設置日誌
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='power_station_converter.log'
)

def get_coordinates_from_google(address, api_key):
    """
    從 Google Maps API 獲取地址的經緯度
    """
    try:
        base_url = "https://maps.googleapis.com/maps/api/geocode/json"
        params = {
            "address": address,
            "key": api_key
        }
        response = requests.get(base_url, params=params)
        data = response.json()
        
        if data["status"] == "OK":
            location = data["results"][0]["geometry"]["location"]
            return location["lat"], location["lng"]
        else:
            logging.error(f"無法獲取地址'{address}'的經緯度: {data['status']}")
            return None, None
    except Exception as e:
        logging.error(f"調用 Google Maps API 時發生錯誤: {str(e)}")
        return None, None

def create_base_template(workbook):
    """
    創建基本模板，包含固定的表格結構和格式
    """
    sheet = workbook.active
    sheet.title = "電站基本資訊 v8"

    sheet.column_dimensions['A'].width = 20
    sheet.column_dimensions['B'].width = 40
    sheet.column_dimensions['C'].width = 40
    
    # 設置標題行
    headers = [
        ("電站資訊", "A1"),
        ("答案", "B1"),
    ]
    
    for header_text, cell in headers:
        sheet[cell] = header_text
        sheet[cell].font = Font(bold=True, color="FFFFFF")
        sheet[cell].fill = PatternFill(start_color="1C4587", end_color="1C4587", fill_type="solid")
    
    # 設置基本資訊欄位
    info_fields = [
        ("地區", "A2"),
        ("電站代碼", "A3"),
        ("電站名稱", "A4"),
        ("地址", "A5"),
        ("緯度", "A6"),
        ("經度", "A7"),
        ("併聯日期", "A8"),
        ("電力結構", "A9"),
        ("註冊碼", "A10")
    ]
    
    for field, cell in info_fields:
        sheet[cell] = field

def process_power_station(csv_row, api_key):
    """
    處理單個電站資料
    """
    wb = openpyxl.Workbook()
    create_base_template(wb)
    ws = wb.active
    
    # 填充動態資料
    ws["B2"] = csv_row["地區"]
    ws["B3"] = csv_row["電站代碼"]
    ws["B4"] = csv_row["電站名稱"]
    ws["B5"] = csv_row["地址"]
    
    # 處理經緯度
    full_address = f"{csv_row['地區']}{csv_row['CITY']}{csv_row['地址']}"
    lat, lng = get_coordinates_from_google(full_address, api_key)
    if lat and lng:
        ws["B6"] = lat
        ws["B7"] = lng
    
    # 設置固定值
    ws["B9"] = "純光電"  # 電力結構
    ws["B10"] = csv_row["註冊碼"]
    
    return wb

def main(csv_path, api_key):
    """
    主函數
    """
    try:
        # 讀取 CSV 檔案
        df = pd.read_csv(csv_path)
        
        # 處理每個電站
        for _, row in df.iterrows():
            try:
                wb = process_power_station(row, api_key)
                output_filename = f"{row['電站代碼']}.xlsx"
                wb.save(output_filename)
                logging.info(f"成功處理電站 {row['電站代碼']}")
            except Exception as e:
                logging.error(f"處理電站 {row['電站代碼']} 時發生錯誤: {str(e)}")
                continue
                
        logging.info("所有電站處理完成")
        
    except Exception as e:
        logging.error(f"程式執行時發生錯誤: {str(e)}")

if __name__ == "__main__":
    CSV_PATH = "template.csv"
    main(CSV_PATH, os.getenv("GOOGLE_MAPS_API_KEY"))
