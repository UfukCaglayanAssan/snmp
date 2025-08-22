#!/usr/bin/env python3
"""
Battery Data Shared Module
Bu modül serial reader ile SNMP agent arasında veri paylaşımını sağlar
"""

import time
from datetime import datetime

# Global veri dictionary'si
battery_data = {}

# Veri tipi tanımları - MIB ile uyumlu
DATA_TYPES = {
    # Kol verileri (k=0, dtype=100-199)
    100: "Slave Count",
    101: "Arm Status", 
    102: "Arm Temperature",
    103: "Arm Humidity",
    
    # k=2 verileri (Kol verileri)
    10: "Akım (A)",
    11: "Nem (%)",
    12: "Sıcaklık (°C)",
    
    # k>2 verileri (Batarya verileri)
    126: "SOC (State of Charge)",
    11: "SOH (State of Health)",
    12: "NTC1 (Temperature)",
    13: "NTC2 (Temperature)",
    14: "NTC3 (Temperature)",
    10: "Gerilim (V)"
}

def update_battery_data(arm, k, dtype, data_value, timestamp=None):
    """Battery verisini güncelle"""
    global battery_data
    
    if timestamp is None:
        timestamp = int(time.time() * 1000)
    
    # Veri birimini belirle
    if dtype == 10 and k == 2:  # k=2, Akım
        unit = "A"
    elif dtype == 11 and k == 2:  # k=2, Nem
        unit = "%"
    elif dtype == 12 and k == 2:  # k=2, Sıcaklık
        unit = "°C"
    elif dtype == 10 and k > 2:  # k>2, Gerilim
        unit = "V"
    elif dtype == 11 and k > 2:  # k>2, SOH
        unit = "%"
    elif dtype in [12, 13, 14] and k > 2:  # k>2, NTC sıcaklık
        unit = "°C"
    elif dtype == 126:  # SOC
        unit = "%"
    elif dtype == 100:  # Slave Count
        unit = "Adet"
    elif dtype == 101:  # Arm Status
        unit = "Durum"
    elif dtype in [102, 103]:  # Arm Temperature, Humidity
        unit = "°C" if dtype == 102 else "%"
    else:
        unit = ""
    
    # Veriyi güncelle
    battery_data[(arm, k, dtype)] = (data_value, unit, timestamp)
    
    # Debug için yazdır
    print(f"Veri güncellendi: Kol{arm}, k{k}, {DATA_TYPES.get(dtype, f'Tip{dtype}')}: {data_value} {unit}")

def update_alarm_data(arm, error_code_msb, error_code_lsb, alarm_type, timestamp=None):
    """Alarm verisini güncelle"""
    global battery_data
    
    if timestamp is None:
        timestamp = int(time.time() * 1000)
    
    # Alarm verisi için özel dtype kullan
    alarm_dtype = 200 + hash(alarm_type) % 100  # Benzersiz dtype oluştur
    
    # Alarm verisini kaydet
    battery_data[(arm, 0, alarm_dtype)] = (f"{error_code_msb:02X}{error_code_lsb:02X}", "Alarm", timestamp)
    
    # Debug için yazdır
    print(f"Alarm kaydedildi: Kol{arm}, {alarm_type}, Kod: {error_code_msb:02X}{error_code_lsb:02X}")

def get_battery_data(arm=None, k=None, dtype=None):
    """Battery verisini getir"""
    global battery_data
    
    if arm is None and k is None and dtype is None:
        return battery_data
    
    filtered_data = {}
    for key, value in battery_data.items():
        arm_val, k_val, dtype_val = key
        
        if arm is not None and arm_val != arm:
            continue
        if k is not None and k_val != k:
            continue
        if dtype is not None and dtype_val != dtype:
            continue
            
        filtered_data[key] = value
    
    return filtered_data

def clear_battery_data():
    """Battery verisini temizle"""
    global battery_data
    battery_data.clear()
    print("Battery verisi temizlendi")

def get_data_count():
    """Toplam veri sayısını döndür"""
    return len(battery_data)

def get_last_update_time():
    """Son güncelleme zamanını döndür"""
    if not battery_data:
        return 0
    
    latest_time = max([v[2] for v in battery_data.values()])
    return latest_time

def get_last_update_time_formatted():
    """Son güncelleme zamanını formatlanmış olarak döndür"""
    summary = get_system_summary()
    timestamp = summary.get('last_update', 0)
    
    if timestamp > 0:
        dt = datetime.fromtimestamp(timestamp/1000)
        return dt.strftime('%Y-%m-%d %H:%M:%S')
    else:
        return "Veri yok"

def get_system_summary():
    """Sistem özetini döndür"""
    if not battery_data:
        return {
            'total_records': 0,
            'arm_count': 0,
            'battery_count': 0,
            'last_update': 0
        }
    
    arms = set([k[0] for k in battery_data.keys()])
    batteries = set([k[1] for k in battery_data.keys() if k[1] > 2])  # k>2 = batarya
    last_update = get_last_update_time()
    
    return {
        'total_records': len(battery_data),
        'arm_count': len(arms),
        'battery_count': len(batteries),
        'last_update': last_update
    }

# Test verisi ekle
def add_test_data():
    """Test verisi ekle"""
    current_time = int(time.time() * 1000)
    
    # Kol verileri
    update_battery_data(1, 0, 100, 4, current_time)      # Kol1, Slave sayısı
    update_battery_data(1, 0, 101, 1, current_time)      # Kol1, Durum (Aktif)
    update_battery_data(2, 0, 100, 3, current_time)      # Kol2, Slave sayısı
    update_battery_data(2, 0, 101, 1, current_time)      # Kol2, Durum (Aktif)
    
    # k=2 verileri (Kol verileri)
    update_battery_data(1, 2, 10, 25.5, current_time)    # Kol1, k=2, Akım
    update_battery_data(1, 2, 11, 65.2, current_time)    # Kol1, k=2, Nem
    update_battery_data(1, 2, 12, 28.1, current_time)    # Kol1, k=2, Sıcaklık
    
    # k>2 verileri (Batarya verileri)
    update_battery_data(1, 3, 10, 12.8, current_time)    # Kol1, Batarya1, Gerilim
    update_battery_data(1, 3, 126, 85.2, current_time)   # Kol1, Batarya1, SOC
    update_battery_data(1, 3, 11, 92.1, current_time)    # Kol1, Batarya1, SOH
    update_battery_data(1, 3, 12, 25.5, current_time)    # Kol1, Batarya1, NTC1
    update_battery_data(1, 3, 13, 26.1, current_time)    # Kol1, Batarya1, NTC2
    update_battery_data(1, 3, 14, 24.8, current_time)    # Kol1, Batarya1, NTC3

# Modül import edildiğinde test verisi ekle
add_test_data()

def print_data_summary():
    """Veri özetini yazdır"""
    summary = get_system_summary()
    
    print("\n=== BATTERY DATA SUMMARY ===")
    print(f"Toplam kayıt: {summary['total_records']}")
    print(f"Kol sayısı: {summary['arm_count']}")
    print(f"Batarya sayısı: {summary['battery_count']}")
    
    if summary['last_update'] > 0:
        last_update_str = datetime.fromtimestamp(summary['last_update']/1000).strftime('%Y-%m-%d %H:%M:%S')
        print(f"Son güncelleme: {last_update_str}")
    
    print("\nDetaylı veri:")
    for (arm, k, dtype), (value, unit, timestamp) in battery_data.items():
        dtype_name = DATA_TYPES.get(dtype, f"Tip{dtype}")
        time_str = datetime.fromtimestamp(timestamp/1000).strftime('%H:%M:%S')
        print(f"  {time_str} - Kol{arm}, k{k}, {dtype_name}: {value} {unit}")

# Test için
if __name__ == "__main__":
    print("Battery Data Shared Module Test")
    print("=" * 40)
    
    # Test verisi ekle
    # add_test_data() # This line is now redundant as it's called at module level
    
    # Özeti yazdır
    print_data_summary()