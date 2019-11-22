from JESDdriver import JESD
import sys

from version import version_logo

class ConsoleApp:

    def __init__(self):
        self.dev = JESD()

    def outError(self):
        sys.stdout.write('Wrong args!')

    def handleArgs(self, argv):
        #  вывод помощи, копипаст из README
        if argv[0] == '-h' or argv[0] == '--help':
            print("'-h' или '--help' --- Вывод помощи.")
            print("'-v' или '--ver' --- Вывод текущей версии. ")
            print("'-l' или '--list' --- Вывод списка доступных устройств")
            print("'-d [номер]' или  '--device [номер]' --- Необязательный аргумент, по умолчанию 0. Выбор устройства для работы.")
            print("'-st' или '--status' --- Вывод статуса устройства. Пример вызова: `start.py -d 1 -st` или `start.py  --status`.")
            print("'-ld [файл]' или '--load [файл]'   --- Загрузка файла в устройство. Пример вызова: `start.py -d 1 -ld text.txt` или `start.py  --load H:\TEST\\test.txt`.")
            print("'-bl' или '--blink' --- Мигнуть светодиодом. Пример вызова: `start.py -d 0 -bl` или `start.py --blink`.")
            print("'-rs' или '--reset' --- Сбросить устройство. Пример вызова: `start.py -d 0 -rs` или `start.py --reset`.")
            print("'-cs' или '--clrstat' --- Сбросить статус PLL. Пример вызова: `start.py -d 0 -cs` или `start.py --clrstat`.")
            print("'-rd [адрес(hex)]' или '--read' --- Считать значение регистра. Пример вызова: `start.py -d 0 -rd 0x03` или `start.py --read 0xAA`.")
            print("'-wr [адрес(hex)] [значение(hex)]' или '--write  [адрес(hex)] [значение(hex)]' --- Запись в регистр. Пример вызова: `start.py -d 0 -wr 0x0 0x0` или `start.py --write 0xA 0xFF`.")

            return 0

        # версия ПО из генератора
        if argv[0] == '-v' or argv[0] == '--ver':
           print('Version: ' + version_logo)
           return 0

        #  вывод списка устройств, OK
        if argv[0] == '-l' or argv[0] == '--list':
            lst = self.dev.getListStr()

            for i in range(len(lst)):
                sys.stdout.write(str(i) + ': ' + lst[i])

            return 0


        # Если нужно, указываем номер устройства

        devFlg = 0
        devn = 0
        if argv[0] == '-d' or argv[0] == '--device':
            try:
                devn = int(argv[1]) # если номер указан, увеличиваем номер аргумента, с которым работаем
                devFlg = 2
            except:
                print('Неверный номер устрйства!')
                return -1


        # проверяем, что устройство живое
        try:
            info = self.dev.connect(devn)
            print('Выбранное устройство: ' +  self.dev.getListStr()[devn])
        except Exception as e:
            print('Ошибка при подключении: ' + str(e))
            return -1


            ##  Работа с устройствами


        # проверяем, есть ли аргументы.
        try:
            tmp =  argv[0 + devFlg]
        except:
            print('Неверные аргументы!')
            return -1

        #  вывод статуса
        if argv[0 + devFlg]  == '-st' or argv[0 + devFlg] == '--status':
            stat1 = self.dev.checkStatus(1)
            stat2 = self.dev.checkStatus(2)
            print('PLL1 Status: ' + stat1)
            print('PLL2 Status: ' + stat2)
            return 0

        # запись в файл, работает так же, как и в оконном
        # если непонятно, смотри MainForm::parseFile
        elif argv[0 + devFlg] == '-ld' or argv[0 + devFlg] == '--load':

            self.dev.reset()
            self.dev.enableWrite()
            self.dev.set4Wire()


            try:

                sch = 0
                fname = argv[1 + devFlg]
                fd = open(fname, 'r')

                flg = True

                for line in fd:
                    sch = sch + 1
                    _line = line
                    line = line.replace('\n', '')
                    line = line.replace('0x', '')

                    if line == '':
                        continue

                    line = line.split('\t')
                    line = line[1]
                    line = int(line, 16)

                    regAddr = line >> 8
                    regVal = line & 0xFF

                    # хз, нв всякий случай
                    if regAddr & 0x8000:
                        print('Пропускаем чтение из регистра ' + hex(regAddr))
                        continue

                    # пропускаем сбросы
                    skip = [0x0, 0x1ffd, 0x1ffe, 0x1fff, 0x006]
                    if regAddr in skip:
                        continue


                    self.dev.write(regAddr, regVal)
                    tmp = self.dev.read(regAddr)

                    if tmp != regVal:
                        print('Предупреждение: Регистр ' + hex(regAddr) + ' после записи значения ' + hex(
                            regVal) + ' равен ' + hex(tmp))
                        flg = False


                fd.close()

                if flg:
                    print('Запись прошла без ошибок!')

                print('Запись завершена.')
                return 0

            except Exception as e:
                if sch:
                    print('Неверный файл! ' + "Ошибка: '" + str(e) + "' на строке " + str(sch))
                else:
                    print('Неверный файл! ' + "Ошибка: '" + str(e))
                return -1

        # мигнуть светодиодом
        elif argv[0 + devFlg] == '-bl' or argv[0 + devFlg] == '--blink':
            self.dev.LEDBlink()
            print('Успешно помигали светодиодом.')
            return 0

        # сбросить
        elif argv[0 + devFlg] == '-rs' or argv[0 + devFlg] == '--reset':
            self.dev.reset()
            print('Устройство успешно сброшено.')
            return 0

        # очистить статус
        elif argv[0 + devFlg] == '-cs' or argv[0 + devFlg] == '--clrstat':
            self.dev.clearStatus()
            print('Статус успешно очищен.')
            return 0

        # чтение регистра
        elif argv[0 + devFlg] == '-rd' or argv[0 + devFlg] == '--read':
            try:
                self.dev.set4Wire()
                self.dev.enableWrite()
                addr = argv[1 + devFlg]
                _addr = addr
                addr = int(addr, 16)
                val = self.dev.read(addr)
                print('Значение регистра ' + hex(addr) + ' : ' + hex(val))
                return 0
            except:
                print('Неверный номер регистра!')
                return -1

        # запись в регистр
        elif argv[0 + devFlg] == '-wr' or argv[0 + devFlg] == '--write':
            try:
                self.dev.set4Wire()
                self.dev.enableWrite()
                addr = argv[1 + devFlg]
                addr = int(addr, 16)

                val = argv[2 + devFlg]
                val = int(val, 16)
                self.dev.write(addr, val)
                print("Успешно записано.")
                return 0
            except:
                print('Неверный номер или значение регистра!')
                return -1

        else:
            print('Неизвестный или отсутсвующий аргумент!')
            return -1
