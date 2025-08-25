#!/usr/bin/env python3
"""
Battery Management System SNMP Pass Script
Bu script SNMP pass direktifi için kullanılır
"""

import sys
import os

def get_snmp_value(oid):
    """SNMP OID için değer döndür"""
    try:
        # OID'den .0 son ekini kaldır
        oid = oid.rstrip('.0')
        
        # Sistem bilgileri - sabit değerler (test için)
        if oid == "1.3.6.1.4.1.99999.1.1.1":  # totalBatteryCount
            return 1
        elif oid == "1.3.6.1.4.1.99999.1.1.2":  # totalArmCount
            return 2
        elif oid == "1.3.6.1.4.1.99999.1.1.3":  # systemStatus
            return 1
        elif oid == "1.3.6.1.4.1.99999.1.1.4":  # lastUpdateTime
            return "2025-08-25 09:00:00"
        
        # Veri sayısı
        elif oid == "1.3.6.1.4.1.99999.2.2":  # dataCount
            return 13
        
        # Alarm sayısı
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
    # SNMPD stdin'den veri bekliyor
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