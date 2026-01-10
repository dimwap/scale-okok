import asyncio
import sys
from datetime import datetime
from bumble.transport import open_transport
"""
 ## КЛАСС ## PacketPrinter:
 Пакет данных полученный через БТ обрабатывается тут.
 в классе хранятся последние полученные значения
 Вес, Температура, заряд батареи, rssi сигнала (бесполезен)
 и полностью сырые данные пакета raw.
 def update_last_values(self, ...) обновляет значения
 def has_changed(...) ->bool проверяет, изменились ли значения.
"""
class PacketPrinter:
    def __init__(self):
        self.log_file = 'scale_log.txt'     # файл для записи данных
        self.last_values = {
            'weight': None,
            'temp': None,
            'battery': None,
            'rssi': None,
            'raw': None
        }
        
    def update_last_values(self, weight, temp, battery, rssi, raw):
        """Обновляет последние сохраненные значения"""
        self.last_values['weight'] = weight
        self.last_values['temp'] = temp
        self.last_values['battery'] = battery
        self.last_values['rssi'] = rssi
        self.last_values['raw'] = raw
        
    def has_changed(self, weight, temp, battery, rssi, raw):
        """Проверяет, изменились ли данные по сравнению с предыдущими"""
        return (
            weight != self.last_values['weight'] or
            temp != self.last_values['temp'] or
            battery != self.last_values['battery'] 
            #rssi != self.last_values['rssi'] or
            #raw != self.last_values['raw']
        )
        
    def on_packet(self, packet):
        try:
            raw = packet.hex()
            if "b4565d7dc2b4" not in raw:     # mac-addres в конце пакета, потом RSSI
                return
                
            bytes_list = [raw[i:i+2] for i in range(0, len(raw), 2)]
            
            # Парсинг данных
            weight = int(bytes_list[18] + bytes_list[19], 16) / 100.0
            temp = packet[20]
            battery = int(bytes_list[16], 16)/2 
            rssi = int(bytes_list[-1], 16) - 256 if int(bytes_list[-1], 16) > 127 else int(bytes_list[-1], 16)
            
            # Проверяем изменения
            if not self.has_changed(weight, temp, battery, rssi, raw):
                return
                
            # Обновляем последние значения
            self.update_last_values(weight, temp, battery, rssi, raw)
            
            # Формируем строку для вывода
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            message = (
                f"[{timestamp}] ВЕС: {weight:05.2f} кг | "
                f"ТЕМП: {temp}°C | "
                f"БАТ: {battery}% | "
                f"RSSI: {rssi} dBm\n"
                f"Сырые данные: {raw}"
            )
            
            print(message)
            
            # Запись в лог
            if (weight>0 and temp>0):
                with open(self.log_file, 'a', encoding='utf-8') as f:
                    f.write(message + '\n\n')
                
        except Exception as e:
            print(f"Ошибка обработки пакета: {e}")


async def main():
    transport_spec = 'usb:0a12:0001'
    printer = PacketPrinter()           #class
    
    async with await open_transport(transport_spec) as (hci_source, hci_sink):
        hci_source.set_packet_sink(printer)
        
        # Инициализация весов
        hci_sink.on_packet(b'\x01\x03\x0c\x00')
        await asyncio.sleep(1)
        
        hci_sink.on_packet(b'\x01\x0b\x20\x07\x01\x10\x00\x10\x00\x00\x00')
        await asyncio.sleep(1)
        
        print("Сканер инициализирован. Ctrl+C для остановки. Вставайте на весы и ожидайте стабилизации значений.")
        hci_sink.on_packet(b'\x01\x0c\x20\x02\x01\x00')

        # Бесконечное ожидание
        while True:
            await asyncio.sleep(3)
     
if __name__ == '__main__':
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        # При нажатии Ctrl+C ловим исключение здесь
        print("Программа прервана пользователем (Ctrl+C)!")
        sys.exit(0) # Завершаем чисто без трассировки
