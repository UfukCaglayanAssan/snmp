# Battery Management System - Veri Tipi Tanımları

## Kol Verileri (k=0, dtype=100-199)

| Dtype | Açıklama | Birim | Kritiklik | Örnek |
|-------|----------|-------|-----------|-------|
| 100 | Slave Count | Adet | - | 4 |
| 101 | Arm Status | - | - | 1=Aktif, 2=Pasif, 3=Hata |
| 102 | Arm Temperature | °C | - | 25.5 |
| 103 | Arm Humidity | % | - | 45.2 |

## Batarya Verileri (k=1,2,3..., dtype=10-99)

| Dtype | Açıklama | Birim | Kritiklik | Örnek |
|-------|----------|-------|-----------|-------|
| 10 | SOC (State of Charge) | % | - | 85.2 |
| 11 | SOH (State of Health) | % | - | 92.1 |
| 13 | Temperature | °C | - | 25.5 |
| 14 | Temperature (Alt) | °C | - | 24.8 |
| 15 | Voltage | V | - | 12.80 |
| 16 | Current | A | - | 2.15 |

## Alarm Sistemi

### Kritiklik Seviyeleri

| Seviye | Açıklama | Renk | Örnek |
|--------|----------|-------|--------|
| 1 | Düşük | Yeşil | Genel bilgilendirme |
| 2 | Orta (Uyarı) | Sarı | Dikkat edilmesi gereken durum |
| 3 | Yüksek | Turuncu | Acil müdahale gerekli |
| 4 | Kritik | Kırmızı | Anında müdahale gerekli |

### Batarya Alarmları

| Error Code | Açıklama | Kritiklik | Durum |
|------------|----------|-----------|-------|
| MSB:1, LSB:0 | Pozitif kutup başı alarmı | 4 (Kritik) | Alarm |
| MSB:2, LSB:0 | Negatif kutup başı sıcaklık alarmı | 4 (Kritik) | Alarm |
| MSB:0, LSB:4 | Düşük batarya gerilim uyarısı | 2 (Orta) | Uyarı |
| MSB:0, LSB:8 | Düşük batarya gerilimi alarmı | 3 (Yüksek) | Alarm |
| MSB:0, LSB:16 | Yüksek batarya gerilimi uyarısı | 2 (Orta) | Uyarı |
| MSB:0, LSB:32 | Yüksek batarya gerilimi alarmı | 3 (Yüksek) | Alarm |
| MSB:0, LSB:64 | Modül sıcaklık alarmı | 4 (Kritik) | Alarm |

### Kol Alarmları

| Error Code | Açıklama | Kritiklik | Durum |
|------------|----------|-----------|-------|
| MSB:2, LSB:9 | Yüksek akım alarmı | 4 (Kritik) | Alarm |
| MSB:4, LSB:9 | Yüksek nem uyarısı | 2 (Orta) | Uyarı |
| MSB:8, LSB:9 | Yüksek ortam sıcaklığı uyarısı | 2 (Orta) | Uyarı |
| MSB:16, LSB:9 | Yüksek kol sıcaklığı alarmı | 3 (Yüksek) | Alarm |

### Alarm Düzeltme

| Durum | Açıklama | Error Code |
|-------|----------|------------|
| Batarya Alarmı Düzeldi | errorCodeMsb:1, errorCodeLsb:1 | 1,1 |
| Kol Alarmı Düzeldi | errorCodeMsb:0, errorCodeLsb:9 | 0,9 |

## OID Yapısı
