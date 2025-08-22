#!/usr/bin/env python3
"""
SNMP Test Scripti
Bu script SNMP fonksiyonlarını test eder
"""

import subprocess
import sys

def test_snmp_get(oid):
    """SNMP GET testi"""
    try:
        cmd = ["snmpget", "-v2c", "-c", "public", "localhost", oid]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0:
            print(f"✓ {oid}: {result.stdout.strip()}")
            return True
        else:
            print(f"✗ {oid}: {result.stderr.strip()}")
            return False
            
    except Exception as e:
        print(f"✗ {oid}: Hata - {str(e)}")
        return False

def test_snmp_walk(base_oid):
    """SNMP WALK testi"""
    try:
        cmd = ["snmpwalk", "-v2c", "-c", "public", "localhost", base_oid]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            print(f"✓ WALK {base_oid}: {len(result.stdout.splitlines())} kayıt bulundu")
            return True
        else:
            print(f"✗ WALK {base_oid}: {result.stderr.strip()}")
            return False
            
    except Exception as e:
        print(f"✗ WALK {base_oid}: Hata - {str(e)}")
        return False

def main():
    print("Battery Management System SNMP Testi")
    print("=" * 50)
    
    # Test OID'leri
    test_oids = [
        ".1.3.6.1.4.1.99999.1.1.1",  # Total Battery Count
        ".1.3.6.1.4.1.99999.1.1.2",  # Total Arm Count
        ".1.3.6.1.4.1.99999.1.1.3",  # System Status
        ".1.3.6.1.4.1.99999.1.1.4",  # Last Update Time
        ".1.3.6.1.4.1.99999.2.2",    # Data Count
        ".1.3.6.1.4.1.99999.3.1.1",  # Alarm Count
    ]
    
    # GET testleri
    print("\nSNMP GET Testleri:")
    for oid in test_oids:
        test_snmp_get(oid)
    
    # WALK testleri
    print("\nSNMP WALK Testleri:")
    walk_oids = [
        ".1.3.6.1.4.1.99999.1",      # System Info
        ".1.3.6.1.4.1.99999.2",      # Battery Data
        ".1.3.6.1.4.1.99999.3",      # Alarms
    ]
    
    for oid in walk_oids:
        test_snmp_walk(oid)
    
    print("\nTest tamamlandı!")

if __name__ == "__main__":
    main()