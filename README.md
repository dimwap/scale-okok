# Python for OKOK Scales  

[![Python][python-shield]][pyth] [![HACS][hacs-shield]][hacs]   
Analogues: [![Analog][Analogue-shield]][Analogue-on-Github]  

BLE hci script for reading data packet from floor scales OKOK

### Пример вывода в файл:  
[2026-01-10 06:52:01] ВЕС: 82.25 кг | ТЕМП: 23°C | БАТ: 96.0% | RSSI: -88 dBm  
Сырые данные: 043e1d02010300b4c27d5d56b41110ffc048202117700a0125b4565d7dc2b4a8

[2026-01-10 07:51:11] ВЕС: 81.75 кг | ТЕМП: 23°C | БАТ: 96.0% | RSSI: -85 dBm  
Сырые данные: 043e1d02010300b4c27d5d56b41110ffc04a1fef17700a0125b4565d7dc2b4ab  

* цветом отмечены байты которые меняются  
--------------------------------------------26°C---BAT--10%-------------------  
[2026-01-10 23:21:06] ВЕС: 82.95 кг | ТЕМП: 23°C | БАТ: 96.0% | RSSI: -84 dBm  
Сырые данные: 043e1d02010300b4c27d5d56b41110ffc0 $\color{green}{02}\space\color{red}{2067}$ 17700a0125b4565d7dc2b4 $\color{blue}{ac}$  
Сырые данные: 043e1d02010300b4c27d5d56b41110ffc0 $\color{green}{4c}\space\color{red}{2012}$ 17700a0125b4565d7dc2b4 $\color{blue}{a8}$  

***  
> [!IMPORTANT]
> Вдумчивый анализ пакетов показывает, что реально передаётся только вес.  
> Изменения температуры на экране никак не отражаются на данных в пакете.  
> После замены батареек, в пакете меняется и байт перед весом, и картинка на экране весов.  
> Последний байт меняется, но вместо RSSI показывает погоду на Марсе.  
Link: [![INSTR][instruct-shield]][inst]  

[Analogue-on-Github]: https://github.com/rrooggiieerr/homeassistant-okokscale
[Analogue-shield]: https://img.shields.io/badge/github-repo-blue?logo=github
[hacs]: https://hacs.xyz/
[hacs-shield]: https://img.shields.io/badge/HACS-Custom-41BDF5.svg?style=for-the-badge
[python-shield]: https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54
[pyth]: https://www.python.org/downloads/
[instruct-shield]: https://img.shields.io/badge/just%20the%20instruct-8A2BE2
[inst]: https://github.com/dimwap/scale-okok/blob/main/instruct.md
