#!/usr/bin/env python3
"""
Test script for battery_snmp.py
"""

import sys
import os

# battery_snmp modülünü import et
sys.path.append(os.path.dirname(__file__))

try:
    from battery_snmp import get_snmp_value
    print("✅ battery_snmp modülü başarıyla import edildi")
except ImportError as e:
    print(f"❌ battery_snmp modülü import edilemedi: {e}")
    sys.exit(1)

# Test OID'leri
test_oids = [
    "1.3.6.1.4.1.99999.1.1.1",  # totalBatteryCount
    "1.3.6.1.4.1.99999.1.1.2",  # totalArmCount
    "1.3.6.1.4.1.99999.1.1.3",  # systemStatus
    "1.3.6.1.4.1.99999.1.1.4",  # lastUpdateTime
    "1.3.6.1.4.1.99999.2.2",    # dataCount
    "1.3.6.1.4.1.99999.3.1.1",  # alarmCount
]

print("\n🧪 SNMP OID Test Sonuçları:")
print("=" * 50)

for oid in test_oids:
    try:
        value = get_snmp_value(oid)
        if value is not None:
            print(f"✅ {oid} = {value} ({type(value).__name__})")
        else:
            print(f"❌ {oid} = None")
    except Exception as e:
        print(f"❌ {oid} = Hata: {e}")

print("\n🔧 Pass Script Format Test:")
print("=" * 50)

# Pass script formatını test et
for oid in test_oids[:3]:  # İlk 3 OID'yi test et
    try:
        value = get_snmp_value(oid)
        if value is not None:
            print(f"OID: {oid}")
            print(f"Tip: {'STRING' if isinstance(value, str) else 'INTEGER'}")
            print(f"Değer: {value}")
            print("---")
        else:
            print(f"❌ {oid} = None")
    except Exception as e:
        print(f"❌ {oid} = Hata: {e}")

print("\n✅ Test tamamlandı!")
