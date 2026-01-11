#OKOK International - android application for Chinese scale
https://play.google.com/store/apps/details?id=com.chipsea.btcontrol.en  
Приложение размером 150мб читает с весов только вес в килограммах, за 30 секунд. Остальные величины: BMI, жир, и т.д. оно сочиняет само. Весы не измеряют сопротивление босых ног, таких данных в пакете нет. Блестящие контакты это имитация приклеенная к стеклянной основе.

# Инструкция по настройке системы чтения BLE-весов на Python (Windows 10/11)
Данное руководство описывает процесс подготовки компьютера для прямой работы с Bluetooth-донглом на чипе **CSR8510 A10**, 
минуя стандартные ограничения стека Windows. Это позволяет стабильно читать данные с весов и других BLE-устройств.

## 1. Требования к оборудованию и ПО
* **Bluetooth-адаптер:** USB-донгл на чипе (b15148) CSR8510 A10 (VID: `0A12`, PID: `0001`). На OZon = 250руб.  
  Это не самый лучший вариант, ну уж что есть под рукой. Питон лучше работает с чипами RTL, с RTL8761B было бы проще.  
* **ОС:** Windows 10/11 (64-бит).
* **Python:** Версия 3.10 или выше (рекомендуется 3.13 x64).

## 2. Подготовка системных драйверов (Zadig)
Стандартные драйверы "CSR Harmony" или "Generic Bluetooth Radio" блокируют доступ Python к устройству. Необходимо заменить их на универсальный драйвер **WinUSB**.

1. Скачайте утилиту **Zadig** с официального сайта: [https://zadig.akeo.ie] (zadig.akeo.ie).
2. Запустите Zadig.
3. Перейдите в меню `Options` -> `List All Devices`.
4. В выпадающем списке выберите **CSR8510 A10** (или устройство с ID `0A12 0001`).
5. В поле выбора драйвера (справа от зеленой стрелки) выберите **WinUSB**.
6. Нажмите **Replace Driver**. Дождитесь завершения (устройство пропадет из раздела Bluetooth и появится в разделе "Устройства USB").

## 3. Установка библиотеки libusb-1.0.dll
Библиотека `PyUSB` является лишь оболочкой, для её работы в системе должен быть физический файл бэкенда.

1. Скачайте архив **libusb** с GitHub: [https://github.com/libusb/libusb/releases] 
2. Распакуйте файл `libusb-1.0.dll` из папки `VS2019/MS64/dll/` (для 64-битного Python).
3. **Важно:** Поместите этот файл в папку `C:\Windows\System32` или в корневую папку вашего Python-скрипта.
но тогда, возможно, придется явно указывать путь к DLL (замените на ваш путь)
backend = usb.backend.libusb1.get_backend(find_library=lambda x: r"G:\libusb-1.0.dll")
dev = usb.core.find(idVendor=0x0a12, idProduct=0x0001, backend=backend)
Впрочем,это актуально не для всех донглов и библиотек.

## 4. Установка зависимостей Python
Откройте терминал и выполните установку необходимых библиотек:

**Установка зависимостей**
```bash
pip install pyusb bumble 
```
You do not need to run "pip install asyncio". The asyncio library has been part of the Python standard library since version 3.4.
Attempting to install it via pip install asyncio will only download an obsolete backport package that contains 
no code and exists solely to prevent accidental installation of outdated versions for very old Python environments (prior to Python 3.4)

## 5. Настройка окружения и запуск
Для корректной работы скрипта в Windows 10/11 необходимо учитывать политику циклов событий (asyncio) и права доступа.
Права доступа: Запускайте терминал (CMD или PowerShell) от имени Администратора. Но может работать и без.

**Запуск скрипта:**
```bash
python scale.py
```

## 6. Технические параметры парсинга (для данных весов)
На основе реверс-инжиниринга пакетов от **09.01.2026**:
Адрес устройства: [B4:56:5D:7D:C2:B4] (или текущий рандомный адрес). Находится в конце пакета данных, перед rssi. И внутри пакета с обратный порядком байт.
Вес: Находится в байтах 18 и 19 рекламного пакета (формат не Big Endian ).
Пример: Hex 2021 = Dec 8225 , 8225/100 = 82.25 кг.
Температура: Находится в байте 20. 
Пример: Hex 19 = Dec 25°C. (17h=23°C)
Батарея/Состояние: Байт 21. или 16. делённое на 2. Требуется дополнительная проверка.
RSSI: последний байт пакета, в соответствии со спецификациеё HCI. Значение меняется от расстояния, но ведёт себя непонятно.

## 7. Возможные проблемы
No Backend Available: Проверьте, что **libusb-1.0.dll** соответствует битности вашего Python (x64) и лежит в доступном месте.
Access Denied: Убедитесь, что ни одна другая программа (или старый драйвер) не использует донгл. Переткните донгл в USB-порт.
Тишина в эфире: Весы транслируют данные только в активном состоянии (когда горит экран). Встаньте на весы перед запуском сканирования.

## 8. Теоретические основы содержимого пакета данных BLE
https://www.cs.bilkent.edu.tr/~korpe/lab/resources/Bluetooth_1_1_vol1.pdf
https://software-dl.ti.com/lprf/simplelink_cc2640r2_latest/docs/blestack/ble_user_guide/html/ble-stack-3.x/hci.html
https://stackoverflow.com/questions/26275679/ble-hci-le-advertising-report-event-data-format

```
raw_data = "04 3e 1d 02 01 03 00 b4 c2 7d 5d 56 b4 11 10 ff c0 75 20 17 17 70 0a 01 25 b4 56 5d 7d c2 b4 a8"
```
В структуре HCI_LE_Advertising_Report параметры идут в следующем порядке:  
Event_Type[i] (1 байт)  
Address_Type[i] (1 байт)  
Address[i] (6 байт) -- с обратным порядком пар байт mac-адреса, для систем с обратным порядком.  
Length_Data[i] (1 байт)  
Data[i] (N байт, где N = Length_Data)  
02 01 03 00 - неизвестно, что - может имеет какой-то смысл  
b4 c2 7d 5d 56 b4 - перевернутый мак-адрес (MAC with xch'd bytes' pairs)  
11 10 ff c0 - что-то. 0x11 - длина остальных данных. ff c0 - сигнатура начала блока Данных.  
75 -?  battary  ?  
20 17 - вес (0x2017 == 8215. weight 82.15kg  в режиме килограммы. кнопка режимов на дне весов)    
17 - температура в градусах. 0x17 == 23 градуса. Комнатная t.  
17 70 0a 01 25 - что-то...  
b4 56 5d 7d c2 b4 - MAC-address. Есть в пакете всегда. По нему проверяется, то ли устройство прочитано.  
RSSI[i] (1 байт) — знаковое целое число от -127 до +20 дБм. 0xA8 == -88 dB  

#Конец пакета данных

Length_Data (байт №14 в строке параметров) равен 11 (hex) = 17 (dec).
Таким образом, после поля данных (17 байт) идет финальный байт a8, 

BLE HCI Advertising Reports are structured data packets sent from the Bluetooth Controller to the Host, detailing discovered Bluetooth Low Energy (BLE) 
advertising devices, containing information like device address, RSSI, and advertising data, using the LE Advertising Report event (Event Code 0x3E, Subevent Code 0x02) 
for monitoring and debugging, crucial for scanner roles to identify peripherals. Key HCI commands like HCI_LE_Set_Scan_Parameters and HCI_LE_Set_Scan_Enable initiate scanning, 
while the controller then reports findings via these events, often batched for efficiency. 

Key Aspects of BLE HCI Advertising Reports:
Purpose: To inform the Host (application/OS) about nearby BLE advertising devices, enabling discovery and connection.
Event Structure: A single LE Advertising Report event can contain multiple reports (if Num_Reports > 1), each with details like:
Event_Type: Connectable, scannable, etc..
Address_Type & Address: Device's Bluetooth address.
RSSI: Received Signal Strength Indicator.
Length & Data: The actual advertising payload.
HCI Commands (Initiating Scan):
hci_le_set_scan_param(): Configures scan window, interval, and type.
hci_le_set_scan_enable(): Starts or stops scanning.
