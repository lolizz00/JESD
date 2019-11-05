# JESD_8SYNCV01


### Запуск: start.py


> Версия Python: 3.7

##### Список необходимых пакетов:
- libusb1
- cp2130
- PyQt5

#### Исправление !!

##### Скопировать содержимое папки `patch` в корневую папку Python (например, `C:\Python37\`)


##### Возможные ошибки

- ...Не является приложение Win32....  ---> заменить файл `libusb-1.0.dll` в корневой папке на нужную разрядность из папки `dll` 

- ... Не найден файл, системе не удается найти путь, Не найден указанный модуль ... ----> Добавьте в PATH папку с файлом `libusb-1.0.dll` (https://www.java.com/ru/download/help/path.xml)

- Проверьте, установлен ли драйвер для CP2130 (https://www.silabs.com/products/interface/usb-bridges/classic-usb-bridges/device.cp2130?q=cp2130)