from dataclasses import dataclass

COMMON_HEADERS = [
    ("裝置代碼", "B"),
    ("裝置型號", "C"),
    ("RS485埠", "D"),
    ("RS485設定", "E"),
    ("TCP代碼", "F"),
    ("TCP地址", "G"),
    ("Modbus ID", "H"),
]


@dataclass
class SheetHeaders:
    LOGGER_HEADERS = [
        ("資料搜集器", "A"),
        ("MAC地址", "B"),
        ("資料蒐集器型號", "C"),
    ]

    PYRANOMETER_HEADERS = [
        ("日照計", "A"),
        *COMMON_HEADERS,
        ("方位", "I"),
    ]

    THERMOMETER_HEADERS = [
        ("溫度計", "A"),
        *COMMON_HEADERS,
        ("方位", "I"),
    ]

    ANEMOMETER_HEADERS = [
        ("風速計", "A"),
        *COMMON_HEADERS,
    ]

    POWER_METER_HEADERS = [
        ("電表", "A"),
        *COMMON_HEADERS,
        ("電表位置", "I"),
    ]

    PROTECTION_RELAY_HEADERS = [
        ("保護電驛", "A"),
        *COMMON_HEADERS,
    ]

    INVERTER_HEADERS = [
        ("變流器", "A"),
        *COMMON_HEADERS,
        ("安裝日期", "I"),
        ("MPPT1 安裝容量", "J"),
        ("MPPT1 方位", "K"),
        ("MPPT1 傾角", "L"),
    ]
