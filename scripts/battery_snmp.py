#!/usr/bin/env python3
"""
Battery Management System SNMP Pass Script
Bu script SNMP pass direktifi için kullanılır
"""

import sys
import os

# Gerçek veriyi oku
try:
    from battery_data_shared import battery_data, DATA_TYPES, get_data_count, get_system_summary, get_last_update_time_formatted
except ImportError:
    print("NONE", file=sys.stderr)
    sys.exit(1)

def get_battery_count():
    """Batarya sayısını döndür"""
    try:
        summary = get_system_summary()
        return summary['battery_count'] or 0
    except:
        return 0

def get_arm_count():
    """Kol sayısını döndür"""
    try:
        summary = get_system_summary()
        return summary['arm_count'] or 0
    except:
        return 0

def get_system_status():
    """Sistem durumunu döndür"""
    try:
        if battery_data:
            return 1  # Normal
        return 4  # Hata
    except:
        return 4

def get_last_update_time():
    """Son güncelleme zamanını döndür"""
    try:
        return get_last_update_time_formatted()
    except:
        return "Unknown"

def get_snmp_value(oid):
    """SNMP OID için değer döndür"""
    try:
        # OID'den .0 son ekini kaldır
        oid = oid.rstrip('.0')
        
        # Sistem bilgileri
        if oid == "1.3.6.1.4.1.99999.1.1.1":  # totalBatteryCount
            return get_battery_count()
        elif oid == "1.3.6.1.4.1.99999.1.1.2":  # totalArmCount
            return get_arm_count()
        elif oid == "1.3.6.1.4.1.99999.1.1.3":  # systemStatus
            return get_system_status()
        elif oid == "1.3.6.1.4.1.99999.1.1.4":  # lastUpdateTime
            return get_last_update_time()
        
        # Veri sayısı
        elif oid == "1.3.6.1.4.1.99999.2.2":  # dataCount
            return get_data_count()
        
        # Alarm sayısı (şimdilik 0)
        elif oid == "1.3.6.1.4.1.99999.3.1.1":  # alarmCount
            return 0
        
        # Alarm kritiklik özeti
        elif oid == "1.3.6.1.4.1.99999.3.1.2.1":  # criticalAlarms
            return 0
        elif oid == "1.3.6.1.4.1.99999.3.1.2.2":  # highAlarms
            return 0
        elif oid == "1.3.6.1.4.1.99999.3.1.2.3":  # mediumAlarms
            return 0
        elif oid == "1.3.6.1.4.1.99999.3.1.2.4":  # lowAlarms
            return 0
        
        else:
            return None
            
    except Exception as e:
        return None

def main():
    """Ana fonksiyon - pass direktifi için"""
    if len(sys.argv) > 1 and sys.argv[1] == "-g":
        # SNMP GET mode - SNMPD tarafından çağrılır
        oid = sys.argv[2] if len(sys.argv) > 2 else ""
        value = get_snmp_value(oid)
        
        if value is None:
            print("NONE")
        else:
            # SNMP pass formatı: OID, tip, değer
            print(oid)
            if isinstance(value, str):
                print("STRING")
                print(value)
            else:
                print("INTEGER")
                print(value)
                
    elif len(sys.argv) > 1 and sys.argv[1] == "-n":
        # SNMP GETNEXT mode
        print("NONE")
        
    else:
        # Eski stdin mode (geriye uyumluluk için)
        for line in sys.stdin:
            line = line.strip()
            if not line:
                continue
            parts = line.split()
            if len(parts) >= 2:
                command = parts[0].upper()
                oid = parts[1]
                if command == "GET":
                    value = get_snmp_value(oid)
                    if value is None:
                        print("NONE")
                    else:
                        if isinstance(value, str):
                            print("STRING")
                            print(value)
                        else:
                            print("INTEGER")
                            print(value)
                    sys.stdout.flush()
                elif command == "GETNEXT":
                    print("NONE")
                    sys.stdout.flush()
                else:
                    print("NONE")
                    sys.stdout.flush()

if __name__ == "__main__":
    main()