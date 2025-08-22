#!/usr/bin/env python3
"""
Battery Data Shared Module Test Scripti
"""

from battery_data_shared import *

def test_shared_module():
    """Paylaşılan modülü test et"""
    print("=== BATTERY DATA SHARED MODULE TEST ===")
    
    # Test verisi ekle
    print("1. Test verisi ekleniyor...")
    add_test_data()
    
    # Özeti yazdır
    print("\n2. Veri özeti:")
    print_data_summary()
    
    # Filtreleme testleri
    print("\n3. Filtreleme testleri:")
    
    print("\nKol1 verileri:")
    kol1_data = get_battery_data(arm=1)
    for key, value in kol1_data.items():
        print(f"  {key}: {value}")
    
    print("\nSıcaklık verileri:")
    temp_data = get_battery_data(dtype=13)
    for key, value in temp_data.items():
        print(f"  {key}: {value}")
    
    print("\nKol1, Batarya1 verileri:")
    kol1_bat1_data = get_battery_data(arm=1, k=1)
    for key, value in kol1_bat1_data.items():
        print(f"  {key}: {value}")
    
    # Sistem özeti
    print("\n4. Sistem özeti:")
    summary = get_system_summary()
    for key, value in summary.items():
        print(f"  {key}: {value}")
    
    # Veri sayısı
    print(f"\n5. Toplam veri sayısı: {get_data_count()}")
    
    # Son güncelleme zamanı
    last_update = get_last_update_time()
    if last_update > 0:
        from datetime import datetime
        last_update_str = datetime.fromtimestamp(last_update/1000).strftime('%Y-%m-%d %H:%M:%S')
        print(f"6. Son güncelleme zamanı: {last_update_str}")

def test_data_manipulation():
    """Veri manipülasyon testleri"""
    print("\n=== VERİ MANİPÜLASYON TESTLERİ ===")
    
    # Veriyi temizle
    print("1. Veri temizleniyor...")
    clear_battery_data()
    print(f"Temizleme sonrası veri sayısı: {get_data_count()}")
    
    # Yeni veri ekle
    print("\n2. Yeni veri ekleniyor...")
    current_time = int(time.time() * 1000)
    
    update_battery_data(1, 1, 13, 30.5, current_time)    # Yeni sıcaklık
    update_battery_data(1, 1, 10, 90.0, current_time)    # Yeni SOC
    update_battery_data(2, 1, 15, 12.8, current_time)    # Yeni voltaj
    
    print(f"Yeni veri ekleme sonrası veri sayısı: {get_data_count()}")
    
    # Güncelleme testi
    print("\n3. Veri güncelleniyor...")
    update_battery_data(1, 1, 13, 31.0, current_time)    # Sıcaklık güncellendi
    
    print("\n4. Güncel veri:")
    print_data_summary()

if __name__ == "__main__":
    test_shared_module()
    test_data_manipulation()
    
    print("\n=== TÜM TESTLER TAMAMLANDI ===")