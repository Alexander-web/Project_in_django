import socket
import time

class DeviceNotConnected(Exception):
    def __init__(self, *args, **kwargs):
        self.message = 'Устройство не подключено'

def loging(func):
    def wrapper(self, *args, **kwargs):   
        print('Вызываем функцию {} с параметрами {}'.format(func.__name__, args.__str__()))
        func(self, *args, **kwargs)
    return wrapper

class SCPI():
    sock = socket.socket()
    isConnected = False
    IP = '192.168.230.115'
    port = 5025
    window_num = '1'
    trace_num = '1'
    calc_num = '1'
    def __new__(cls):#Синглтон проверка на то существует объект или нет
        if not hasattr(cls, 'instance'):
            cls.instance = super().__new__(cls)
        return cls.instance    #Возвращает один единственный экземпляр класса

    def __end_session__(self):
        self.isConnected = False
        self.sock.close()

    def __start_session__(self):
        try:
            self.sock.connect((self.IP, self.port))
            print('Успешное соединение с устройством {}'.format(self.IP))
            self.isConnected = True
        except Exception:
            print('Соединение не успешное {}'.format(self.IP))
    
    def __send__(self, data_to_send='*IDN?'):#Автоматически отправляет на первый порт
        if self.isConnected:
            data_to_send+='\n'
            self.sock.send(bytes(data_to_send,'utf-8'))
            data = b''
            if '?' in data_to_send:#В случае, когда в команде имеется вопрос ВАЦ передаст ответ, который надо обработать
                while True:   
                    tmp = self.sock.recv(1024)
                    data += tmp
                    if '\n' in tmp.decode('utf-8'):
                        break
                return data.decode('utf-8')
            else:
                return 'OK'
        else:
            try:#Если что-то пошло не так на этапе создания соиденения и передачи команды выдает Нет соединения с устройством
                self.__start_session__()
                self.__send__(data_to_send)
            except Exception:     
                print('Нет соединения с устройством')
                raise DeviceNotConnected

    def reset(self):
        self.__send__('*SYSTEM:FPRESET')#Команда скидывает все настройки, закрывает окна
        self.__send__('*RST')#Выполняет сброс устройства и отменяет любую ожидающую команду или запрос
        self.__send__('CALCulate{}:PAR:DEL:ALL'.format(self.calc_num))#Удалить все измерения

    # def reset_status_registers_and_clear_error_queue(self):
    #     self.__send__('*CLS')

    # def define_custom_measure(self, Mname = 'MyMeas', type = 'SC21'):
    #     self.__send__('CALCulate{}:CUSTom:DEFine \'{Mname}\', \'Scalar Mixer/Converter\' ,\'{type}\''.format(self.calc_num, Mname = Mname, type=type))
    
    # def set_window_state_and_feed_measure(self, Mname='MyMeas', on_of = 'ON',  ):
    #     self.__send__('DISP:WIND{}:STATe {}'.format(self.window_num, on_of))
    #     self.__send__('DISP:WIND{}:TRACe{}:FEED \'{Mname}\''.format(self.window_num, self.trace_num, Mname=Mname))
    
    # def select_measure(self, Mname='MyMeas'):
    #     self.__send__('CALCulate{}:PAR:SEL \'{Mname}\''.format(self.calc_num, Mname=Mname))

    # def set_num_sweep_point(self, num_sweep_point): #FIXME добавить логику работы функции
    #     self.__send__()

    # def select_mixer_file(self, path_to_mixer_file):
    #     self.__send__('SENSE:MIXer:Load \"\"{}\"\"'.format(path_to_mixer_file))

    # def SETUP_MEASURE(self):
    #     self.reset()
    #     self.define_custom_measure('SomeMeasure')
    #     self.set_window_state_and_feed_measure('SomeMeasure','ON')
    #     self.select_measure('SomeMeasure')
    #     self.select_mixer_file('C:\M\Mixer.mxr')

def create_meas(numpoint, freqin, freqout, band):
    device = SCPI()#device = SCPI(auto_connect=True)#Создает экземпляр класса SCPI
    device.reset()#Производит сброс настроек, отправляя команды ВАЦ используя мнтод класса reset() и sent(вызывается внутри функции reset())
    device.__send__("SENS:SWE:MODE HOLD")#Устанавливает количество принимаемых сигналов

    device.__send__("CALC:CUST:DEF 'My SC21', 'Scalar Mixer/Converter', 'SC21'")#Создать измерение SC21 c именем "My SC21"
    device.__send__("DISP:WIND:TRAC2:FEED 'My SC21'")#Поместить измерение 'My SC21' в окно <1> на график <2>
    # device.__send__("CALC:PAR:SEL 'My SC21'")

    # device.__send__("SENS:CORR:COLL:SESS6:SMC:TWOPort:OPTion \"ECAL\"")
#    device.select_mixer_file('C:\M\Mixer.mxr')
    device.__send__(f"SENS:SWE:POIN {numpoint}")#Выставляет количество точек для измерения
    
    #device.__send__("SENS:MIX:INP:FREQ:START 2237e6")
    #device.__send__("SENS:MIX:INP:FREQ:STOP 2253e6")
    # device.__send__("SENS:MIX:INP:FREQ:START 2145e6")
    # device.__send__("SENS:MIX:INP:FREQ:STOP 2345e6")
    """
    Полоса частот, в которой проводятся измерения
    """
    start_freq = freqin - band/2
    stop_freq = freqin + band/2
    device.__send__(f"SENS:MIX:INP:FREQ:START {start_freq}")#Выставляет начальную частоту
    device.__send__(f"SENS:MIX:INP:FREQ:STOP {stop_freq}")#Выставляет конечную частоту
    # device.__send__("SENS:MIX:LO:FREQ:MODE Swept")
    # device.__send__("SENS:MIX:LO:FREQ:MODE FIXED")
    device.__send__(f"SENS:MIX:LO:FREQ:FIXED {freqout-freqin}")#Частота гетеродина
    
    
    #device.__send__("SENS:MIX:OUTPUT:FREQ:FIX 3.4e9")
    device.__send__("SENS:MIX:OUTput:FREQuency:MODE swept")	#Метод свипирования по частоте
    # device.__send__("SENS:MIX:OUTP:FREQ:START 1e9")
    # device.__send__("SENS:MIX:OUTP:FREQ:STOP 1e9")

    device.__send__("SENS:MIX:OUTP:FREQ:SID HIGH")#Сумманый сигнал с выхода гетеродина?
    device.__send__("SENS:MIX:INP:POW -60")#Выставляет входную частоту равной -60dBm
    device.__send__("SENS:MIX:LO:POW -30")#Мощность гетеродина -30dB
    device.__send__("SENS:MIX:PHAS 1") # set phase measurement

    device.__send__("SENS:MIX:CALC OUTPut")#Пересчет частоты и мощности к выходу
    #device.__send__("SENS:MIX:APPL")
    
    # device.__send__("SENS:CORR:COLL:SESS6:SMC:ECAL:CHAR 1,0")
    # device.__send__("SENS:CORR:COLL:SESS6:SMC:TWOP:METH \"DEFAULT\"")
    # device.__send__("SENS:CORR:COLL:SESS6:SMC:TWOP:OMIT 1")
    # device.__send__("SENS:CORR:COLL:SESS6:SMC:TWOP:ECAL:ORI:STATE 1")
    # device.__send__("SENS:CORR:COLL:SESS6:STEP")
    
    # steps = device.__send__("SENS:CORR:COLL:SESS6:STEP?")
    # for i in range(1,steps+1):
    #     desc = device.__send__("SENS:CORR:COLL:SESS6:DESC? " + str(i))
    #     print(desc)
    #     device.__send__("SENS:CORR:COLL:SESS6:ACQ " + str(i))
    # calset = device.__send__("SENS:CORR:COLL:SESS6:SAVE?")
    # print(calset)
    # print("Calibration finished\nConnect DUT")
    # input()
    # device.__send__("SOUR:POW:MODE ON")
    # device.__send__("SENS:SWE:GRO:COUN 1")
    # device.__send__("SENS:SWE:MODE GROUPS")
    opc = device.__send__("*OPC?")#Проверяет прошли ли измерения
    print(opc)#Печатает ответ
    device.__send__("CALC:PAR:SEL 'My SC21'")#Выбрать измерение " 'My SC21'
    device.__send__("INITiate:CONTinuous OFF")#Отключить режим бесконечного свипирования
    device.__send__("INITiate:IMMediate;*wai")#Моментальный запуск

    device.__send__("CALC:FORM MLOG")#Устанавливает формат отображения для измерения лог?
    device.__send__("DISP:WIND:Y:AUTO")#Autoscale All
    time.sleep(3)
    print(device.__send__("*OPC?"))
    result = device.__send__("CALC:DATA? FDATA")#Получение данныx для НАЧХ
    result = result.split(',')
    result2 = []
    step = band/numpoint
    counter = 0
    for i in result:
        result2+=str(start_freq+step*counter)+":"+i+";" #Поскольку ВАЦ выдает только уровень в mdB необходимо востанавливать значения по х
        counter+=1
    device.__send__("CALC:FORM GDEL")#Получение данныx для Нгвз
    device.__send__("DISP:WIND:Y:AUTO")#Autoscale All
    time.sleep(3)
    print(device.__send__("*OPC?"))
    
    result = device.__send__("CALC:DATA? FDATA")
    result = result.split(',')
    device.__end_session__()
    return result2
    # device.__send__("SOUR:POW:MODE OFF")


"""
Выполняется проверка на то запущен файл посредством импорта (Import ...)или вызван на прямую
если вызывается напрямую имеет значение True и код выполняется
"""

if __name__ == '__main__':
    # device = SCPI(auto_connect=False)
    create_meas(201,2245e6,2245e6+8705e6,300e6)
    # device.SETUP_MEASURE()




