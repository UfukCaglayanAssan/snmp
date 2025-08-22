#!/bin/bash
# Battery Management System SNMP Kurulum Scripti

echo "Battery Management System SNMP Kurulumu Başlıyor..."
echo "=================================================="

# Net-SNMP kurulumu
echo "1. Net-SNMP kuruluyor..."
sudo apt-get update
sudo apt-get install -y snmpd snmp

# Script dosyalarını çalıştırılabilir yap
echo "2. SNMP script dosyaları çalıştırılabilir yapılıyor..."
chmod +x scripts/battery_snmp.py
chmod +x scripts/alarm_manager.py
chmod +x scripts/battery_data_shared.py

# MIB dosyasını kopyala
echo "3. MIB dosyası kopyalanıyor..."
sudo cp mibs/BATTERY-MANAGEMENT-MIB.mib /usr/share/snmp/mibs/

# SNMP konfigürasyonunu güncelle
echo "4. SNMP konfigürasyonu güncelleniyor..."
sudo cp config/snmpd.conf /etc/snmp/snmpd.conf

# SNMP servisini yeniden başlat
echo "5. SNMP servisini yeniden başlatılıyor..."
sudo systemctl restart snmpd
sudo systemctl enable snmpd

# Test
echo "6. SNMP test ediliyor..."
sleep 3

echo "   Sistem bilgileri test ediliyor..."
snmpget -v2c -c public localhost .1.3.6.1.4.1.99999.1.1.1

echo "   Alarm sayısı test ediliyor..."
snmpget -v2c -c public localhost .1.3.6.1.4.1.99999.3.1.1

echo "   Kritik alarm sayısı test ediliyor..."
snmpget -v2c -c public localhost .1.3.6.1.4.1.99999.3.1.2.1

echo ""
echo "✓ Kurulum tamamlandı!"
echo ""
echo "Test komutları:"
echo "  python3 test_shared_module.py"
echo "  python3 test_alarm_system.py"
echo "  snmpwalk -v2c -c public localhost .1.3.6.1.4.1.99999"
echo "  snmpget -v2c -c public localhost .1.3.6.1.4.1.99999.1.1.1"
echo "  snmpget -v2c -c public localhost .1.3.6.1.4.1.99999.3.1.1"