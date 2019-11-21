from .scpisender import SCPI 

def make_data_from_PNAX(data_y, freq_out, band):
    
    data_y = data_y.split(',')
    all_data = ""
    step = (band/(len(data_y)-1))
    start_freq_out = freq_out - (band / 2)
    for idx, data_item in enumerate(data_y):
        x = start_freq_out + step * idx
        y = float(data_item)
        all_data = all_data + f"{x}:{y};"
    return all_data

def create_meas(freqin, freqout, band, meas_type,numpoint):

    device = SCPI()
    device.reset()
    device.__send__("SENS:SWE:MODE HOLD")#Устанавливает количество принимаемых сигналов

    device.__send__("CALC:CUST:DEF 'My SC21', 'Scalar Mixer/Converter', 'SC21'")#Создать измерение SC21 c именем "My SC21"
    device.__send__("DISP:WIND:TRAC2:FEED 'My SC21'")#Поместить измерение 'My SC21' в окно <1> на график <2>
    device.__send__(f"SENS:SWE:POIN {numpoint}")#Выставляет количество точек для измерения
    start_freq = freqin - band/2
    stop_freq = freqin + band/2
    device.__send__(f"SENS:MIX:INP:FREQ:START {start_freq}")#Выставляет начальную частоту
    device.__send__(f"SENS:MIX:INP:FREQ:STOP {stop_freq}")#Выставляет конечную частоту
    device.__send__(f"SENS:MIX:LO:FREQ:FIXED {freqout-freqin}")#Частота гетеродина
    device.__send__("SENS:MIX:OUTput:FREQuency:MODE swept")	#Метод свипирования по частоте
    device.__send__("SENS:MIX:OUTP:FREQ:SID HIGH")#Сумманый сигнал с выхода гетеродина?
    device.__send__("SENS:MIX:INP:POW -60")
    device.__send__("SENS:MIX:LO:POW -30")
    device.__send__("SENS:MIX:PHAS 1") # set phase measurement

    device.__send__("SENS:MIX:CALC OUTPut")#Пересчет частоты и мощности к выходу
    opc = device.__send__("*OPC?")
    print(opc)
    result=""
    device.__send__("CALC:PAR:SEL 'My SC21'")#Выбрать измерение " 'My SC21'
    device.__send__("INITiate:CONTinuous OFF")#Отключить режим бесконечного свипирования
    device.__send__("INITiate:IMMediate;*wai")#Моментальный запуск
    
    if meas_type=="afc":
        device.__send__("CALC:FORM MLOG")#Устанавливает формат отображения для измерения лог?
        device.__send__("DISP:WIND:Y:AUTO")#Autoscale All
        print(device.__send__("*OPC?"))
        result = device.__send__("CALC:DATA? FDATA")#Получение данныx для НАЧХ

    if meas_type=="gd":
        device.__send__("CALC:FORM GDEL")
        device.__send__("DISP:WIND:Y:AUTO")
        print(device.__send__("*OPC?"))
        result = device.__send__("CALC:DATA? FDATA")
        print(result)
    result2 = make_data_from_PNAX(result,freqout,band)
    return result2
    # device.__send__("SOUR:POW:MODE OFF")