#!/usr/bin/env python3
"""
Alarm Management System - battery_data_shared.py ile entegre
Batarya ve kol alarmlarını yönetir
"""

import time
from datetime import datetime

class AlarmManager:
    def __init__(self):
        # Aktif alarmları tut: key=(arm, battery, alarm_type), value=(timestamp, description, status, severity)
        self.active_alarms = {}
        
        # Alarm geçmişi
        self.alarm_history = []
        
        # Alarm ID sayacı
        self.alarm_id_counter = 1
    
    def get_alarm_description_and_severity(self, error_code_msb, error_code_lsb, is_battery=True):
        """Alarm açıklamasını ve kritiklik seviyesini döndür"""
        if is_battery:
            # Batarya alarmları
            if error_code_lsb != 1 and error_code_msb >= 1:
                switch_msb = {
                    1: ("Pozitif kutup başı alarmı", 4),      # Kritik
                    2: ("Negatif kutup başı sıcaklık alarmı", 4)  # Kritik
                }
                if error_code_msb in switch_msb:
                    return switch_msb[error_code_msb]
                return (f"Bilinmeyen batarya alarmı (MSB:{error_code_msb})", 1)
            
            switch_lsb = {
                4: ("Düşük batarya gerilim uyarısı", 2),      # Orta
                8: ("Düşük batarya gerilimi alarmı", 3),      # Yüksek
                16: ("Yüksek batarya gerilimi uyarısı", 2),   # Orta
                32: ("Yüksek batarya gerilimi alarmı", 3),    # Yüksek
                64: ("Modül sıcaklık alarmı", 4)              # Kritik
            }
            if error_code_lsb in switch_lsb:
                return switch_lsb[error_code_lsb]
            return (f"Bilinmeyen batarya alarmı (LSB:{error_code_lsb})", 1)
        else:
            # Kol alarmları
            if error_code_lsb == 9:
                switch_msb = {
                    2: ("Yüksek akım alarmı", 4),              # Kritik
                    4: ("Yüksek nem uyarısı", 2),              # Orta
                    8: ("Yüksek ortam sıcaklığı uyarısı", 2),  # Orta
                    16: ("Yüksek kol sıcaklığı alarmı", 3)     # Yüksek
                }
                if error_code_msb in switch_msb:
                    return switch_msb[error_code_msb]
                return (f"Bilinmeyen kol alarmı (MSB:{error_code_msb})", 1)
            return (f"Bilinmeyen kol alarmı (LSB:{error_code_lsb})", 1)
    
    def get_severity_name(self, severity):
        """Kritiklik seviyesi adını döndür"""
        severity_names = {
            1: "Düşük",
            2: "Orta (Uyarı)",
            3: "Yüksek",
            4: "Kritik"
        }
        return severity_names.get(severity, "Bilinmeyen")
    
    def process_battery_alarm(self, arm, battery, error_code_msb, error_code_lsb, timestamp):
        """Batarya alarmını işle"""
        # Alarm düzeldi mi kontrol et (errorCodeMsb:1, errorCodeLsb:1)
        if error_code_msb == 1 and error_code_lsb == 1:
            # Bu batarya için tüm alarmları düzelt
            self.resolve_battery_alarms(arm, battery, timestamp)
            return
        
        # Yeni alarm mı kontrol et
        alarm_type = f"BAT_{error_code_msb}_{error_code_lsb}"
        alarm_key = (arm, battery, alarm_type)
        
        if alarm_key not in self.active_alarms:
            # Yeni alarm
            description, severity = self.get_alarm_description_and_severity(error_code_msb, error_code_lsb, True)
            self.active_alarms[alarm_key] = (timestamp, description, "Devam Ediyor", severity)
            
            # Alarm geçmişine ekle
            self.alarm_history.append({
                'id': self.alarm_id_counter,
                'timestamp': timestamp,
                'arm': arm,
                'battery': battery,
                'description': description,
                'status': "Devam Ediyor",
                'severity': severity,
                'severity_name': self.get_severity_name(severity),
                'type': 'Battery'
            })
            self.alarm_id_counter += 1
            
            severity_name = self.get_severity_name(severity)
            print(f"YENİ BATARYA ALARMI: Kol{arm}, Batarya{battery}, {description} - {severity_name}")
    
    def process_arm_alarm(self, arm, error_code_msb, error_code_lsb, timestamp):
        """Kol alarmını işle"""
        # Kol alarmı düzeldi mi kontrol et (errorCodeLsb:9, errorCodeMsb:0)
        if error_code_lsb == 9 and error_code_msb == 0:
            # Bu kol için tüm alarmları düzelt
            self.resolve_arm_alarms(arm, timestamp)
            return
        
        # Yeni kol alarmı mı kontrol et
        if error_code_lsb == 9 and error_code_msb >= 1:
            alarm_type = f"ARM_{error_code_msb}_{error_code_lsb}"
            alarm_key = (arm, "Kol", alarm_type)
            
            if alarm_key not in self.active_alarms:
                # Yeni kol alarmı
                description, severity = self.get_alarm_description_and_severity(error_code_msb, error_code_lsb, False)
                self.active_alarms[alarm_key] = (timestamp, description, "Devam Ediyor", severity)
                
                # Alarm geçmişine ekle
                self.alarm_history.append({
                    'id': self.alarm_id_counter,
                    'timestamp': timestamp,
                    'arm': arm,
                    'battery': "Kol",
                    'description': description,
                    'status': "Devam Ediyor",
                    'severity': severity,
                    'severity_name': self.get_severity_name(severity),
                    'type': 'Arm'
                })
                self.alarm_id_counter += 1
                
                severity_name = self.get_severity_name(severity)
                print(f"YENİ KOL ALARMI: Kol{arm}, {description} - {severity_name}")
    
    def resolve_battery_alarms(self, arm, battery, timestamp):
        """Batarya alarmlarını düzelt"""
        resolved_count = 0
        
        for alarm_key, (alarm_timestamp, description, status, severity) in list(self.active_alarms.items()):
            if alarm_key[0] == arm and alarm_key[1] == battery and status == "Devam Ediyor":
                # Alarmı düzelt
                self.active_alarms[alarm_key] = (timestamp, description, "Düzeldi", severity)
                
                # Alarm geçmişine ekle
                self.alarm_history.append({
                    'id': self.alarm_id_counter,
                    'timestamp': timestamp,
                    'arm': arm,
                    'battery': battery,
                    'description': description,
                    'status': "Düzeldi",
                    'severity': severity,
                    'severity_name': self.get_severity_name(severity),
                    'type': 'Battery'
                })
                self.alarm_id_counter += 1
                
                resolved_count += 1
                severity_name = self.get_severity_name(severity)
                print(f"BATARYA ALARMI DÜZELDİ: Kol{arm}, Batarya{battery}, {description} - {severity_name}")
        
        if resolved_count > 0:
            print(f"Toplam {resolved_count} batarya alarmı düzeltildi")
    
    def resolve_arm_alarms(self, arm, timestamp):
        """Kol alarmlarını düzelt"""
        resolved_count = 0
        
        for alarm_key, (alarm_timestamp, description, status, severity) in list(self.active_alarms.items()):
            if alarm_key[0] == arm and alarm_key[1] == "Kol" and status == "Devam Ediyor":
                # Alarmı düzelt
                self.active_alarms[alarm_key] = (timestamp, description, "Düzeldi", severity)
                
                # Alarm geçmişine ekle
                self.alarm_history.append({
                    'id': self.alarm_id_counter,
                    'timestamp': timestamp,
                    'arm': arm,
                    'battery': "Kol",
                    'description': description,
                    'status': "Düzeldi",
                    'severity': severity,
                    'severity_name': self.get_severity_name(severity),
                    'type': 'Arm'
                })
                self.alarm_id_counter += 1
                
                resolved_count += 1
                severity_name = self.get_severity_name(severity)
                print(f"KOL ALARMI DÜZELDİ: Kol{arm}, {description} - {severity_name}")
        
        if resolved_count > 0:
            print(f"Toplam {resolved_count} kol alarmı düzeltildi")
    
    def get_active_alarms(self):
        """Aktif alarmları döndür"""
        return self.active_alarms
    
    def get_alarm_history(self, limit=100):
        """Alarm geçmişini döndür"""
        return self.alarm_history[-limit:]
    
    def get_alarm_count(self):
        """Aktif alarm sayısını döndür"""
        return len([a for a in self.active_alarms.values() if a[2] == "Devam Ediyor"])
    
    def get_alarm_count_by_severity(self):
        """Kritiklik seviyesine göre alarm sayılarını döndür"""
        severity_counts = {1: 0, 2: 0, 3: 0, 4: 0}
        
        for alarm_key, (timestamp, description, status, severity) in self.active_alarms.items():
            if status == "Devam Ediyor":
                severity_counts[severity] += 1
        
        return severity_counts
    
    def get_alarm_summary(self):
        """Alarm özetini döndür"""
        active_count = self.get_alarm_count()
        total_history = len(self.alarm_history)
        severity_counts = self.get_alarm_count_by_severity()
        
        return {
            'active_alarms': active_count,
            'total_history': total_history,
            'battery_alarms': len([a for a in self.active_alarms.values() if a[2] == "Devam Ediyor" and "Kol" not in str(a)]),
            'arm_alarms': len([a for a in self.active_alarms.values() if a[2] == "Devam Ediyor" and "Kol" in str(a)]),
            'severity_counts': severity_counts,
            'critical_alarms': severity_counts[4],
            'high_alarms': severity_counts[3],
            'medium_alarms': severity_counts[2],
            'low_alarms': severity_counts[1]
        }

# Global alarm manager instance
alarm_manager = AlarmManager()

# Test fonksiyonları
def test_alarm_system():
    """Alarm sistemini test et"""
    print("=== ALARM SİSTEMİ TESTİ ===")
    
    # Test batarya alarmları
    print("\n1. Batarya alarmları test ediliyor...")
    alarm_manager.process_battery_alarm(1, 2, 1, 0, int(time.time() * 1000))  # Pozitif kutup başı (Kritik)
    alarm_manager.process_battery_alarm(1, 3, 0, 8, int(time.time() * 1000))  # Düşük gerilim (Yüksek)
    alarm_manager.process_battery_alarm(1, 4, 0, 4, int(time.time() * 1000))  # Düşük gerilim uyarısı (Orta)
    alarm_manager.process_battery_alarm(2, 1, 0, 64, int(time.time() * 1000)) # Modül sıcaklık (Kritik)
    
    # Test kol alarmları
    print("\n2. Kol alarmları test ediliyor...")
    alarm_manager.process_arm_alarm(1, 2, 9, int(time.time() * 1000))  # Yüksek akım (Kritik)
    alarm_manager.process_arm_alarm(2, 4, 9, int(time.time() * 1000))  # Yüksek nem (Orta)
    alarm_manager.process_arm_alarm(3, 8, 9, int(time.time() * 1000))  # Yüksek ortam sıcaklığı (Orta)
    alarm_manager.process_arm_alarm(4, 16, 9, int(time.time() * 1000)) # Yüksek kol sıcaklığı (Yüksek)
    
    # Test alarm düzeltme
    print("\n3. Alarm düzeltme test ediliyor...")
    alarm_manager.process_battery_alarm(1, 2, 1, 1, int(time.time() * 1000))  # Batarya alarmı düzeldi
    alarm_manager.process_arm_alarm(1, 0, 9, int(time.time() * 1000))  # Kol alarmı düzeldi
    
    # Sonuçları göster
    print("\n4. Sonuçlar:")
    print(f"Aktif alarm sayısı: {alarm_manager.get_alarm_count()}")
    print(f"Toplam geçmiş: {len(alarm_manager.get_alarm_history())}")
    
    summary = alarm_manager.get_alarm_summary()
    print(f"Kritik alarmlar: {summary['critical_alarms']}")
    print(f"Yüksek alarmlar: {summary['high_alarms']}")
    print(f"Orta alarmlar (Uyarı): {summary['medium_alarms']}")
    print(f"Düşük alarmlar: {summary['low_alarms']}")
    
    print("\n5. Aktif alarmlar:")
    for key, (timestamp, desc, status, severity) in alarm_manager.get_active_alarms().items():
        severity_name = alarm_manager.get_severity_name(severity)
        print(f"  {key}: {desc} - {status} - {severity_name}")
    
    print("\n6. Son alarm geçmişi:")
    for alarm in alarm_manager.get_alarm_history(10):
        time_str = datetime.fromtimestamp(alarm['timestamp']/1000).strftime('%H:%M:%S')
        print(f"  {time_str} - Kol{alarm['arm']}, {alarm['battery']}, {alarm['description']}, {alarm['status']}, {alarm['severity_name']}")

if __name__ == "__main__":
    test_alarm_system()