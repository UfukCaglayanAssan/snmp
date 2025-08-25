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
        print(f"DEBUG: get_snmp_value called with OID: {oid}", file=sys.stderr)
        
        # OID'den .0 son ekini kaldır
        oid = oid.rstrip('.0')
        print(f"DEBUG: OID after stripping .0: {oid}", file=sys.stderr)

        # Sistem bilgileri - gerçek verilerden hesapla
        if oid == "1.3.6.1.4.1.99999.1.1.1":  # totalBatteryCount
            print("DEBUG: Matched totalBatteryCount", file=sys.stderr)
            # Toplam batarya sayısını hesapla
            data = get_battery_data()
            battery_count = 0
            for (arm, k, dtype) in data.keys():
                if k > 2:  # k>2 olanlar batarya verisi
                    battery_count += 1
            result = battery_count if battery_count > 0 else 1
            print(f"DEBUG: Returning battery count: {result}", file=sys.stderr)
            return result

        elif oid == "1.3.6.1.4.1.99999.1.1.2":  # totalArmCount
            print("DEBUG: Matched totalArmCount", file=sys.stderr)
            # Toplam kol sayısını hesapla
            data = get_battery_data()
            arms = set()
            for (arm, k, dtype) in data.keys():
                arms.add(arm)
            result = len(arms) if arms else 2
            print(f"DEBUG: Returning arm count: {result}", file=sys.stderr)
            return result

        elif oid == "1.3.6.1.4.1.99999.1.1.3":  # systemStatus
            print("DEBUG: Matched systemStatus", file=sys.stderr)
            # Sistem durumu - varsayılan olarak 1 (normal)
            result = 1
            print(f"DEBUG: Returning system status: {result}", file=sys.stderr)
            return result

        elif oid == "1.3.6.1.4.1.99999.1.1.4":  # lastUpdateTime
            print("DEBUG: Matched lastUpdateTime", file=sys.stderr)
            # Son güncelleme zamanı
            from datetime import datetime
            result = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"DEBUG: Returning last update time: {result}", file=sys.stderr)
            return result

        # Veri sayısı
        elif oid == "1.3.6.1.4.1.99999.2.2":  # dataCount
            print("DEBUG: Matched dataCount", file=sys.stderr)
            data = get_battery_data()
            result = len(data) if data else 13
            print(f"DEBUG: Returning data count: {result}", file=sys.stderr)
            return result

        # Alarm sayısı
        elif oid == "1.3.6.1.4.1.99999.3.1.1":  # alarmCount
            print("DEBUG: Matched alarmCount", file=sys.stderr)
            data = get_battery_data()
            alarm_count = 0
            for (arm, k, dtype) in data.keys():
                if dtype >= 200:  # Alarm verileri
                    alarm_count += 1
            result = alarm_count
            print(f"DEBUG: Returning alarm count: {result}", file=sys.stderr)
            return result

        # Alarm kritiklik özeti
        elif oid == "1.3.6.1.4.1.99999.3.1.2.1":  # criticalAlarms
            print("DEBUG: Matched criticalAlarms", file=sys.stderr)
            result = 0  # Şimdilik sabit
            print(f"DEBUG: Returning critical alarms: {result}", file=sys.stderr)
            return result
        elif oid == "1.3.6.1.4.1.99999.3.1.2.2":  # highAlarms
            print("DEBUG: Matched highAlarms", file=sys.stderr)
            result = 0  # Şimdilik sabit
            print(f"DEBUG: Returning high alarms: {result}", file=sys.stderr)
            return result
        elif oid == "1.3.6.1.4.1.99999.3.1.2.3":  # mediumAlarms
            print("DEBUG: Matched mediumAlarms", file=sys.stderr)
            result = 0  # Şimdilik sabit
            print(f"DEBUG: Returning medium alarms: {result}", file=sys.stderr)
            return result
        elif oid == "1.3.6.1.4.1.99999.3.1.2.4":  # lowAlarms
            print("DEBUG: Matched lowAlarms", file=sys.stderr)
            result = 0  # Şimdilik sabit
            print(f"DEBUG: Returning low alarms: {result}", file=sys.stderr)
            return result

        # Gerçek batarya verileri - OID'den arm, k, dtype çıkar
        elif oid.startswith("1.3.6.1.4.1.99999.4."):
            print("DEBUG: Matched real battery data OID", file=sys.stderr)
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
                            result = value[0]  # data_value
                            print(f"DEBUG: Returning real battery data value for OID {oid}: {result}", file=sys.stderr)
                            return result
                result = 0
                print(f"DEBUG: Returning 0 for real battery data OID {oid}", file=sys.stderr)
                return result

        else:
            print(f"DEBUG: No match for OID: {oid}", file=sys.stderr)
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