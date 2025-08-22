#!/usr/bin/env python3
"""
Gelişmiş Alarm Sistemi Test Scripti
"""

from scripts.alarm_manager import AlarmManager
import time
from datetime import datetime

def test_complete_alarm_system():
    """Tam alarm sistemini test et"""
    print("=== GELİŞMİŞ ALARM SİSTEMİ TESTİ ===")
    
    alarm_mgr = AlarmManager()
    
    # Test 1: Tüm batarya alarmları
    print("\n1. BATARYA ALARMLARI TEST EDİLİYOR...")
    print("-" * 50)
    
    # Kritik alarmlar (Seviye 4)
    print("Kritik alarmlar (Seviye 4):")
    alarm_mgr.process_battery_alarm(1, 2, 1, 0, int(time.time() * 1000))  # Pozitif kutup başı
    alarm_mgr.process_battery_alarm(2, 1, 2, 0, int(time.time() * 1000))  # Negatif kutup başı sıcaklık
    alarm_mgr.process_battery_alarm(3, 1, 0, 64, int(time.time() * 1000)) # Modül sıcaklık
    
    # Yüksek alarmlar (Seviye 3)
    print("\nYüksek alarmlar (Seviye 3):")
    alarm_mgr.process_battery_alarm(1, 3, 0, 8, int(time.time() * 1000))  # Düşük gerilim
    alarm_mgr.process_battery_alarm(2, 2, 0, 32, int(time.time() * 1000)) # Yüksek gerilim
    
    # Orta alarmlar/Uyarılar (Seviye 2)
    print("\nOrta alarmlar/Uyarılar (Seviye 2):")
    alarm_mgr.process_battery_alarm(1, 4, 0, 4, int(time.time() * 1000))  # Düşük gerilim uyarısı
    alarm_mgr.process_battery_alarm(2, 3, 0, 16, int(time.time() * 1000)) # Yüksek gerilim uyarısı
    
    # Test 2: Tüm kol alarmları
    print("\n2. KOL ALARMLARI TEST EDİLİYOR...")
    print("-" * 50)
    
    # Kritik alarmlar (Seviye 4)
    print("Kritik alarmlar (Seviye 4):")
    alarm_mgr.process_arm_alarm(1, 2, 9, int(time.time() * 1000))  # Yüksek akım
    
    # Yüksek alarmlar (Seviye 3)
    print("\nYüksek alarmlar (Seviye 3):")
    alarm_mgr.process_arm_alarm(2, 16, 9, int(time.time() * 1000)) # Yüksek kol sıcaklığı
    
    # Orta alarmlar/Uyarılar (Seviye 2)
    print("\nOrta alarmlar/Uyarılar (Seviye 2):")
    alarm_mgr.process_arm_alarm(3, 4, 9, int(time.time() * 1000))  # Yüksek nem
    alarm_mgr.process_arm_alarm(4, 8, 9, int(time.time() * 1000))  # Yüksek ortam sıcaklığı
    
    # Test 3: Alarm düzeltme
    print("\n3. ALARM DÜZELTME TEST EDİLİYOR...")
    print("-" * 50)
    
    print("Batarya alarmları düzeltiliyor...")
    alarm_mgr.process_battery_alarm(1, 2, 1, 1, int(time.time() * 1000))  # Kol1, Batarya2 düzeldi
    alarm_mgr.process_battery_alarm(2, 1, 1, 1, int(time.time() * 1000))  # Kol2, Batarya1 düzeldi
    alarm_mgr.process_battery_alarm(3, 1, 1, 1, int(time.time() * 1000))  # Kol3, Batarya1 düzeldi
    
    print("Kol alarmları düzeltiliyor...")
    alarm_mgr.process_arm_alarm(1, 0, 9, int(time.time() * 1000))  # Kol1 alarmı düzeldi
    alarm_mgr.process_arm_alarm(2, 0, 9, int(time.time() * 1000))  # Kol2 alarmı düzeldi
    
    # Test 4: Sonuçları göster
    print("\n4. TEST SONUÇLARI")
    print("=" * 60)
    
    # Genel özet
    summary = alarm_mgr.get_alarm_summary()
    print(f"Toplam aktif alarm: {summary['active_alarms']}")
    print(f"Toplam geçmiş kayıt: {summary['total_history']}")
    print(f"Batarya alarmları: {summary['battery_alarms']}")
    print(f"Kol alarmları: {summary['arm_alarms']}")
    
    # Kritiklik seviyesine göre özet
    print(f"\nKritiklik seviyesine göre:")
    print(f"  Kritik (Seviye 4): {summary['critical_alarms']}")
    print(f"  Yüksek (Seviye 3): {summary['high_alarms']}")
    print(f"  Orta (Seviye 2): {summary['medium_alarms']}")
    print(f"  Düşük (Seviye 1): {summary['low_alarms']}")
    
    # Aktif alarmlar
    print(f"\n5. AKTİF ALARMLAR:")
    print("-" * 60)
    active_alarms = alarm_mgr.get_active_alarms()
    
    if not active_alarms:
        print("Aktif alarm yok!")
    else:
        for key, (timestamp, desc, status, severity) in active_alarms.items():
            severity_name = alarm_mgr.get_severity_name(severity)
            time_str = datetime.fromtimestamp(timestamp/1000).strftime('%H:%M:%S')
            print(f"  {time_str} - {key}: {desc} - {status} - {severity_name}")
    
    # Son alarm geçmişi
    print(f"\n6. SON ALARM GEÇMİŞİ (Son 15 kayıt):")
    print("-" * 60)
    alarm_history = alarm_mgr.get_alarm_history(15)
    
    for alarm in alarm_history:
        time_str = datetime.fromtimestamp(alarm['timestamp']/1000).strftime('%H:%M:%S')
        status_icon = "🔴" if alarm['status'] == "Devam Ediyor" else "🟢"
        severity_color = {
            1: "🟢",  # Düşük
            2: "��",  # Orta (Uyarı)
            3: "🟠",  # Yüksek
            4: "🔴"   # Kritik
        }.get(alarm['severity'], "⚪")
        
        print(f"  {status_icon} {severity_color} {time_str} - Kol{alarm['arm']}, {alarm['battery']}")
        print(f"      {alarm['description']} - {alarm['status']} - {alarm['severity_name']}")
        print()

def test_alarm_resolution():
    """Alarm düzeltme sistemini test et"""
    print("\n=== ALARM DÜZELTME SİSTEMİ TESTİ ===")
    
    alarm_mgr = AlarmManager()
    
    # Test senaryosu: Bir alarm oluştur, sonra düzelt
    print("1. Test alarmı oluşturuluyor...")
    alarm_mgr.process_battery_alarm(1, 1, 1, 0, int(time.time() * 1000))  # Pozitif kutup başı
    
    print("2. Alarm durumu kontrol ediliyor...")
    active_count = alarm_mgr.get_alarm_count()
    print(f"Aktif alarm sayısı: {active_count}")
    
    print("3. Alarm düzeltiliyor...")
    alarm_mgr.process_battery_alarm(1, 1, 1, 1, int(time.time() * 1000))  # Düzeldi
    
    print("4. Düzeltme sonrası kontrol...")
    active_count_after = alarm_mgr.get_alarm_count()
    print(f"Düzeltme sonrası aktif alarm sayısı: {active_count_after}")
    
    print("5. Geçmiş kayıt kontrolü...")
    history = alarm_mgr.get_alarm_history(5)
    for alarm in history:
        time_str = datetime.fromtimestamp(alarm['timestamp']/1000).strftime('%H:%M:%S')
        print(f"  {time_str} - {alarm['description']} - {alarm['status']}")

def test_severity_levels():
    """Kritiklik seviyelerini test et"""
    print("\n=== KRİTİKLİK SEVİYELERİ TESTİ ===")
    
    alarm_mgr = AlarmManager()
    
    # Tüm seviyelerde alarm oluştur
    print("1. Tüm kritiklik seviyelerinde alarm oluşturuluyor...")
    
    # Seviye 4 - Kritik
    alarm_mgr.process_battery_alarm(1, 1, 1, 0, int(time.time() * 1000))  # Pozitif kutup başı
    
    # Seviye 3 - Yüksek
    alarm_mgr.process_battery_alarm(1, 2, 0, 8, int(time.time() * 1000))  # Düşük gerilim
    
    # Seviye 2 - Orta (Uyarı)
    alarm_mgr.process_battery_alarm(1, 3, 0, 4, int(time.time() * 1000))  # Düşük gerilim uyarısı
    
    # Seviye 1 - Düşük
    # Bu seviyede özel bir alarm yok, genel bilgilendirme olarak kullanılabilir
    
    print("2. Kritiklik seviyesine göre alarm sayıları:")
    severity_counts = alarm_mgr.get_alarm_count_by_severity()
    
    for level in range(1, 5):
        count = severity_counts.get(level, 0)
        level_name = alarm_mgr.get_severity_name(level)
        print(f"  Seviye {level} ({level_name}): {count} alarm")
    
    print("3. Aktif alarmlar:")
    active_alarms = alarm_mgr.get_active_alarms()
    for key, (timestamp, desc, status, severity) in active_alarms.items():
        severity_name = alarm_mgr.get_severity_name(severity)
        print(f"  {key}: {desc} - {severity_name}")

if __name__ == "__main__":
    # Ana test
    test_complete_alarm_system()
    
    # Ek testler
    test_alarm_resolution()
    test_severity_levels()
    
    print("\n=== TÜM TESTLER TAMAMLANDI ===")