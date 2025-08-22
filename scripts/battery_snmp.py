#!/usr/bin/env python3
"""
Battery Management System SNMP Script
Bu script SNMP OID'leri için veri döndürür
"""

import sys
import time
import json
import os

# Gerçek veriyi oku
try:
    from battery_data_shared import battery_data, DATA_TYPES, get_data_count, get_system_summary
except ImportError:
    print("HATA: battery_data_shared modülü bulunamadı!")
    sys.exit(1)

def get_battery_count():
    """Batarya sayısını döndür"""
    summary = get_system_summary()
    return summary['battery_count'] or 0

def get_arm_count():
    """Kol sayısını döndür"""
    summary = get_system_summary()
    return summary['arm_count'] or 4

def get_system_status():
    """Sistem durumunu döndür"""
    if battery_data:
        return 1  # Normal
    return 4  # Hata

def get_last_update_time():
    """Son güncelleme zamanını döndür"""
    if battery_data:
        latest_time = max([v[2] for v in battery_data.values()])
        return int((time.time() * 1000 - latest_time) / 10)  # centiseconds
    return 0

def get_snmp_value(oid):
    """SNMP OID için değer döndür"""
    try:
        # Sistem bilgileri
        if oid == "1.3.6.1.4.1.99999.1.1.1.0":  # totalBatteryCount
            return get_battery_count()
        elif oid == "1.3.6.1.4.1.99999.1.1.2.0":  # totalArmCount
            return get_arm_count()
        elif oid == "1.3.6.1.4.1.99999.1.1.3.0":  # systemStatus
            return get_system_status()
        elif oid == "1.3.6.1.4.1.99999.1.1.4.0":  # lastUpdateTime
            return get_last_update_time()
        
        # Veri sayısı
        elif oid == "1.3.6.1.4.1.99999.2.1.2.0":  # dataCount
            return get_data_count()
        
        # Alarm sayısı (şimdilik 0)
        elif oid == "1.3.6.1.4.1.99999.3.1.1.0":  # alarmCount
            return 0
        
        # Alarm kritiklik özeti
        elif oid == "1.3.6.1.4.1.99999.3.2.1.0":  # criticalAlarms
            return 0
        elif oid == "1.3.6.1.4.1.99999.3.2.2.0":  # highAlarms
            return 0
        elif oid == "1.3.6.1.4.1.99999.3.2.3.0":  # mediumAlarms
            return 0
        elif oid == "1.3.6.1.4.1.99999.3.2.4.0":  # lowAlarms
            return 0
        
        else:
            print(f"Bilinmeyen OID: {oid}")
            return 0
            
    except Exception as e:
        print(f"SNMP değer alma hatası: {e}")
        return 0

def main():
    """Ana fonksiyon"""
    print("Battery SNMP Agent başlatıldı...")
    print("=" * 40)
    
    # Sistem özetini göster
    summary = get_system_summary()
    print(f"Toplam kayıt: {summary['total_records']}")
    print(f"Kol sayısı: {summary['arm_count']}")
    print(f"Batarya sayısı: {summary['battery_count']}")
    
    # Test OID'leri
    test_oids = [
        "1.3.6.1.4.1.99999.1.1.1.0",  # Batarya sayısı
        "1.3.6.1.4.1.99999.1.1.2.0",  # Kol sayısı
        "1.3.6.1.4.1.99999.1.1.3.0",  # Sistem durumu
        "1.3.6.1.4.1.99999.2.1.2.0",  # Veri sayısı
    ]
    
    print("\nSNMP Test OID'leri:")
    for oid in test_oids:
        value = get_snmp_value(oid)
        print(f"  {oid}: {value}")
    
    print("\nSNMP Agent hazır. Veri bekleniyor...")
    print("Ctrl+C ile durdurun.")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nSNMP Agent durduruldu.")

if __name__ == "__main__":
    main()