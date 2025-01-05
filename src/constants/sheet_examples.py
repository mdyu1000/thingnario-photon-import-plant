from dataclasses import dataclass


@dataclass
class SheetExamples:
    LOGGER_EXAMPLE = [
        ("範例", "A"),
        ("06:77:80:40:5B:F8", "B"),
        ("PE-1000", "C"),
    ]

    PYRANOMETER_EXAMPLE = [
        ("範例", "A"),
        ("KH018-PYR-01", "B"),
        ("ABB_VSN800", "C"),
        ("4", "D"),
        ("9600, N, 8, 1", "E"),
        ("KH018-TCP-01", "F"),
        ("192.168.2.1", "G"),
        ("1", "H"),
        ("NW", "I"),
    ]

    THERMOMETER_EXAMPLE = [
        ("範例", "A"),
        ("KH018-THR-01", "B"),
        ("ABB_VSN800", "C"),
        ("4", "D"),
        ("9600, N, 8, 1", "E"),
        ("KH018-TCP-01", "F"),
        ("192.168.2.1", "G"),
        ("2", "H"),
        ("NW", "I"),
    ]

    ANEMOMETER_EXAMPLE = [
        ("範例", "A"),
        ("KH018-ANE-01", "B"),
        ("ABB_VSN800", "C"),
        ("4", "D"),
        ("9600, N, 8, 1", "E"),
        ("KH018-TCP-01", "F"),
        ("192.168.2.1", "G"),
        ("3", "H"),
    ]

    POWER_METER_EXAMPLE = [
        ("範例", "A"),
        ("KH018-PWR-01", "B"),
        ("ABB_B24", "C"),
        ("3", "D"),
        ("9600, N, 8, 1", "E"),
        ("KH018-TCP-01", "F"),
        ("192.168.2.1", "G"),
        ("1", "H"),
        ("光電端", "I"),
    ]

    PROTECTION_RELAY_EXAMPLE = [
        ("範例", "A"),
        ("KH018-PTR-01", "B"),
        ("AQTIVATE_AQ200", "C"),
        ("3", "D"),
        ("9600, N, 8, 1", "E"),
        ("KH018-TCP-01", "F"),
        ("192.168.2.1", "G"),
        ("2", "H"),
    ]

    INVERTER_EXAMPLE = [
        ("範例", "A"),
        ("KH018-INV-A01", "B"),
        ("ABB_PVS-100-TL-WB-SX", "C"),
        ("1", "D"),
        ("9600, N, 8, 1", "E"),
        ("KH018-TCP-01", "F"),
        ("192.168.2.1", "G"),
        ("1", "H"),
        ("2017_10_28", "I"),
        ("15.2", "J"),
        ("NW", "K"),
        ("10", "L"),
    ]
