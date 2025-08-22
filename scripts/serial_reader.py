#!/usr/bin/env python3
"""
Serial Port Reader - Pigpio UART ile veri oku ve RAM'de tut
mainkod.py'deki okuma mantığını kullan
"""

import pigpio
import time
import threading
from battery_data_shared import update_battery_data, update_alarm_data

# GPIO Pin tanımları
RX_PIN = 16  # UART RX GPIO pini
TX_PIN = 26  # UART TX GPIO pini
BAUD_RATE = 9600

# Global buffer
buffer = bytearray()

def read_serial(pi):
    """Bit-banging ile GPIO üzerinden seri veri oku"""
    global buffer
    print("\nBit-banging UART veri alımı başladı...")
    
    # Başlangıçta buffer'ı temizle
    buffer.clear()

    while True:
        try:
            (count, data) = pi.bb_serial_read(RX_PIN)
            if count > 0:
                # Yeni verileri buffer'a ekle
                buffer.extend(data)
                while len(buffer) > 0:
                    try:
                        # Header (0x80 veya 0x81) bul
                        header_index = -1
                        for i, byte in enumerate(buffer):
                            if byte == 0x80 or byte == 0x81:
                                header_index = i
                                break
                        
                        if header_index == -1:
                            buffer.clear()
                            break

                        if header_index > 0:
                            buffer = buffer[header_index:]

                        if len(buffer) >= 3:
                            dtype = buffer[2]
                            
                            # Paket uzunluğunu belirle
                            if dtype == 0x7F and len(buffer) >= 5:
                                packet_length = 5  # Missing data
                            elif len(buffer) >= 6 and (buffer[2] == 0x0F or buffer[1] == 0x7E or (buffer[2] == 0x7D and buffer[1] == 2)):
                                packet_length = 6  # Balans, armslavecounts, Hatkon alarm
                            elif dtype == 0x7D and len(buffer) >= 7 and buffer[1] > 2:
                                packet_length = 7  # Batkon alarm
                            else:
                                packet_length = 11  # Normal veri

                            if len(buffer) >= packet_length:
                                packet = buffer[:packet_length]
                                buffer = buffer[packet_length:]
                                
                                # Paketi işle
                                process_packet(packet)
                            else:
                                break
                        else:
                            break

                    except Exception as e:
                        print(f"Paket işleme hatası: {e}")
                        buffer.clear()
                        continue

            time.sleep(0.01)

        except Exception as e:
            print(f"Veri okuma hatası: {e}")
            time.sleep(1)

def process_packet(packet):
    """Paketi işle ve RAM'e kaydet"""
    try:
        # Paket tipini belirle
        if len(packet) == 11:
            process_11byte_packet(packet)
        elif len(packet) == 7:
            process_7byte_packet(packet)
        elif len(packet) == 6:
            process_6byte_packet(packet)
        elif len(packet) == 5:
            process_5byte_packet(packet)
        else:
            print(f"Bilinmeyen paket uzunluğu: {len(packet)}")
            
    except Exception as e:
        print(f"Paket işleme hatası: {e}")

def process_11byte_packet(packet):
    """11 byte'lık normal veri paketini işle"""
    try:
        arm_value = packet[3]
        dtype = packet[2]
        k_value = packet[1]
        
        # Veri hesaplama
        if dtype == 11 and k_value == 2:  # Nem hesaplama
            onlar = packet[5]
            birler = packet[6]
            kusurat1 = packet[7]
            kusurat2 = packet[8]
            tam_kisim = (onlar * 10 + birler)
            kusurat_kisim = (kusurat1 * 0.1 + kusurat2 * 0.01)
            salt_data = tam_kisim + kusurat_kisim
            salt_data = round(salt_data, 4)
        else:
            # Normal hesaplama
            saltData = packet[4] * 100 + packet[5] * 10 + packet[6] + packet[7] * 0.1 + packet[8] * 0.01 + packet[9] * 0.001
            salt_data = round(saltData, 4)
        
        # RAM'e kaydet
        timestamp = int(time.time() * 1000)
        update_battery_data(arm_value, k_value, dtype, salt_data, timestamp)
        
        # Debug
        print(f"Veri kaydedildi: Kol{arm_value}, k{k_value}, dtype{dtype}: {salt_data}")
        
    except Exception as e:
        print(f"11 byte paket işleme hatası: {e}")

def process_7byte_packet(packet):
    """7 byte'lık Batkon alarm paketini işle"""
    try:
        # Batkon alarm verisi
        arm_value = packet[3]
        error_code_msb = packet[4]
        error_code_lsb = packet[5]
        
        # Alarm işle
        update_alarm_data(arm_value, error_code_msb, error_code_lsb, "Battery", int(time.time() * 1000))
        
        print(f"Batkon alarm: Kol{arm_value}, MSB:{error_code_msb}, LSB:{error_code_lsb}")
        
    except Exception as e:
        print(f"7 byte paket işleme hatası: {e}")

def process_6byte_packet(packet):
    """6 byte'lık paketleri işle"""
    try:
        if packet[2] == 0x7D:  # Hatkon alarm
            arm_value = packet[3]
            error_code_msb = packet[4]
            error_code_lsb = 9  # Sabit değer
            
            # Alarm işle
            update_alarm_data(arm_value, error_code_msb, error_code_lsb, "Arm", int(time.time() * 1000))
            
            print(f"Hatkon alarm: Kol{arm_value}, MSB:{error_code_msb}")
            
        elif packet[1] == 0x7E:  # Armslavecounts
            arm1, arm2, arm3, arm4 = packet[2], packet[3], packet[4], packet[5]
            
            # Kol bilgilerini RAM'e kaydet
            timestamp = int(time.time() * 1000)
            update_battery_data(1, 0, 100, arm1, timestamp)  # Kol1 slave sayısı
            update_battery_data(2, 0, 100, arm2, timestamp)  # Kol2 slave sayısı
            update_battery_data(3, 0, 100, arm3, timestamp)  # Kol3 slave sayısı
            update_battery_data(4, 0, 100, arm4, timestamp)  # Kol4 slave sayısı
            
            print(f"Armslavecounts: Kol1:{arm1}, Kol2:{arm2}, Kol3:{arm3}, Kol4:{arm4}")
            
    except Exception as e:
        print(f"6 byte paket işleme hatası: {e}")

def process_5byte_packet(packet):
    """5 byte'lık missing data paketini işle"""
    try:
        arm_value = packet[3]
        slave = packet[1]
        status = packet[4]
        
        # Missing data bilgisini RAM'e kaydet
        timestamp = int(time.time() * 1000)
        update_battery_data(arm_value, 0, 101, status, timestamp)  # Kol durumu
        
        print(f"Missing data: Kol{arm_value}, Slave{slave}, Status{status}")
        
    except Exception as e:
        print(f"5 byte paket işleme hatası: {e}")

def main():
    try:
        # Pigpio başlat
        pi = pigpio.pi()
        if not pi.connected:
            print("Pigpio bağlantısı sağlanamadı!")
            return
        
        # TX pin'i hazırla
        pi.set_mode(TX_PIN, pigpio.OUTPUT)
        pi.write(TX_PIN, 1)
        
        # UART okuma başlat
        pi.bb_serial_read_open(RX_PIN, BAUD_RATE)
        print(f"GPIO{RX_PIN} bit-banging UART başlatıldı @ {BAUD_RATE} baud.")
        
        # Okuma thread'i başlat
        read_thread = threading.Thread(target=read_serial, args=(pi,), daemon=True)
        read_thread.start()
        print("Serial okuma thread'i başlatıldı.")
        
        print("Program çalışıyor... (Ctrl+C ile durdurun)")
        
        # Ana döngü
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\nProgram sonlandırılıyor...")
        
    finally:
        if 'pi' in locals():
            try:
                pi.bb_serial_read_close(RX_PIN)
                print("Bit-bang UART kapatıldı.")
            except pigpio.error:
                print("Bit-bang UART zaten kapalı.")
            pi.stop()

if __name__ == '__main__':
    print("Serial Reader başlatılıyor...")
    main()