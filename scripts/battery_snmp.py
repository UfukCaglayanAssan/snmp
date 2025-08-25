#!/usr/bin/env python3
"""
Battery Management System SNMP Pass Script
Bu script SNMP pass direktifi için kullanılır ve gerçek batarya verilerini döndürür
"""

import sys
import os

# battery_data_shared modülünü import et
try:
    from battery_data_shared import get_battery_data, DATA_TYPES
except ImportError:
    # Eğer import edilemezse, basit fallback kullan
    DATA_TYPES = {}
    def get_battery_data(*args, **kwargs):
        return {}

def get_snmp_value(oid):
    """SNMP OID için değer döndür"""
    try:
        # OID'den .0 son ekini kaldır
        oid = oid.rstrip('.0')
        
        # Sistem bilgileri - gerçek verilerden hesapla
        if oid == "1.3.6.1.4.1.99999.1.1.1":  # totalBatteryCount
            # Toplam batarya sayısını hesapla
            data = get_battery_data()
            battery_count = 0
            for (arm, k, dtype) in data.keys():
                if k > 2:  # k>2 olanlar batarya verisi
                    battery_count += 1
            return battery_count if battery_count > 0 else 1
            
        elif oid == "1.3.6.1.4.1.99999.1.1.2":  # totalArmCount
            # Toplam kol sayısını hesapla
            data = get_battery_data()
            arms = set()
            for (arm, k, dtype) in data.keys():
                arms.add(arm)
            return len(arms) if arms else 2
            
        elif oid == "1.3.6.1.4.1.99999.1.1.3":  # systemStatus
            # Sistem durumu - varsayılan olarak 1 (normal)
            return 1
            
        elif oid == "1.3.6.1.4.1.99999.1.1.4":  # lastUpdateTime
            # Son güncelleme zamanı
            from datetime import datetime
            return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Veri sayısı
        elif oid == "1.3.6.1.4.1.99999.2.2":  # dataCount
            data = get_battery_data()
            return len(data) if data else 13
        
        # Alarm sayısı
        elif oid == "1.3.6.1.4.1.99999.3.1.1":  # alarmCount
            data = get_battery_data()
            alarm_count = 0
            for (arm, k, dtype) in data.keys():
                if dtype >= 200:  # Alarm verileri
                    alarm_count += 1
            return alarm_count
        
        # Alarm kritiklik özeti
        elif oid == "1.3.6.1.4.1.99999.3.1.2.1":  # criticalAlarms
            return 0  # Şimdilik sabit
        elif oid == "1.3.6.1.4.1.99999.3.1.2.2":  # highAlarms
            return 0  # Şimdilik sabit
        elif oid == "1.3.6.1.4.1.99999.3.1.2.3":  # mediumAlarms
            return 0  # Şimdilik sabit
        elif oid == "1.3.6.1.4.1.99999.3.1.2.4":  # lowAlarms
            return 0  # Şimdilik sabit
        
        # Gerçek batarya verileri - OID'den arm, k, dtype çıkar
        elif oid.startswith("1.3.6.1.4.1.99999.4."):
            # Format: 1.3.6.1.4.1.99999.4.{arm}.{k}.{dtype}
            parts = oid.split('.')
            if len(parts) >= 8:
                arm = int(parts[6])
                k = int(parts[7])
                dtype = int(parts[8]) if len(parts) > 8 else 0
                
                data = get_battery_data(arm, k, dtype)
                if data:
                    # İlk veriyi al
                    for key, value in data.items():
                        if key[0] == arm and key[1] == k and key[2] == dtype:
                            return value[0]  # data_value
                return 0
        
        else:
            return None
            
    except Exception as e:
        print(f"Error in get_snmp_value: {e}", file=sys.stderr)
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
        # Stdin mode
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