from .scpisender import SCPI 
from app.models import MeasureType

def data_gca(measure_type,input_frequency,output_frequency):
    measure_parameter=MeasureType.objects.get(name=measure_type)
    in_pow=measure_parameter.key.input_power_first
    out_pow=measure_parameter.key.input_power_last
    num_points=measure_parameter.key.namber_of_points_for_averaging
    linear_power=measure_parameter.key.input_power

    CompLevel         = 1      # 1 dB compression level
    Tolerance         = 0.05   # SMART Sweep tolerance
    NumFreqs          = 21
    Scale             = 0.1
    LinearPower       = linear_power
    BackOff           = 10     # Not used for Deviation from linear gain
    StartPower        = in_pow
    StopPower         = out_pow
    NumPowers         = num_points     # Not used for SMART Sweep
    DwellTime         = 0.0005 # Allow some time for DUT bias/thermal effects
    IFBandwidth       = 1000   # Reasonable trace noise at -20 dBm
    EnableInterp      = False  # Disable interpolation
    AcqMode           = 2      # Smart Sweep
    CompAlg           = 0      # Deviation from linear gain
    ShowIterations  = False  # Configure SMART to not show iteration results

    sender = SCPI()

    sender.__send__("*RST")
    sender.__send__(':MMEM:LOAD "C:\gca_preset.sta"')
    sender.__send__("source:power:att 60")

    if AcqMode==0:
        sender.__send__("SENS:GCS:AMOD SMAR")
    if AcqMode==1:
        sender.__send__("SENS:GCS:AMOD PFREQ")
    if AcqMode==2:
        sender.__send__("SENS:GCS:AMOD FPOW")


    if CompAlg==0:sender.__send__("SENS:GCS:COMP:ALG CFLG")
    if CompAlg==1:sender.__send__("SENS:GCS:COMP:ALG CFMG")
    if CompAlg==2:sender.__send__("SENS:GCS:COMP:ALG BACK")
    if CompAlg==3:sender.__send__("SENS:GCS:COMP:ALG XYCOM")

    if EnableInterp:
        sender.__send__("SENS:GCS:COMP:INT ON")
    else:
        sender.__send__("SENS:GCS:COMP:INT OFF")

    if ShowIterations:
        sender.__send__("SENS:GCS:SMAR:SIT ON")
    else:
        sender.__send__("SENS:GCS:SMAR:SIT OFF")

    sender.__send__("SENS:GCS:COMP:LEV " + str(CompLevel))
    sender.__send__("SENS:GCS:COMP:BACK:LEV " + str(BackOff))
    sender.__send__("SENS:GCS:COMP:DELT:X " + str(BackOff))
    sender.__send__("SENS:GCS:COMP:DELT:Y " + str(BackOff))
    sender.__send__("SENS:GCS:SWE:FREQ:POIN " + str(NumFreqs))
    sender.__send__("SENS:GCS:SMAR:STIM " + str(DwellTime))
    sender.__send__("SENS:GCS:SWE:POW:POIN "+ str(NumPowers))
    sender.__send__("SENS:BAND " + str(IFBandwidth))
    sender.__send__("SENS:SWE:DWEL " + str(DwellTime))
    sender.__send__("SOUR:POW:STAR " + str(StartPower))
    sender.__send__("SOUR:POW:STOP " + str(StopPower))
    sender.__send__("SOUR:POW " + str(LinearPower))
    sender.__send__("SENS:SWE:POIN " + str(NumFreqs))

    sender.__send__("SENS:MIX:INP:FREQ:FIXED "+ str(input_frequency))
    sender.__send__("SENS:MIX:LO:FREQ:FIX " + str(output_frequency))
    sender.__send__("SENS:MIX:LO:POW -30")
    sender.__send__("SENS:MIX:OUTP:FREQ:SID HIGH")
    sender.__send__("SENS:MIX:CALC Output")
    sender.__send__("SENS:MIX:APPLY")

    sender.__send__("SENS:SWE:MODE SING")
    strs = sender.__send__("*OPC?")
    sender.__send__("DISP:WIND:Y:AUTO")
    sender.__send__('MMEMory:STORe:DATA "GCA125.csv","CSV Formatted Data","Displayed","DB",-1')
    r = sender.__send__('MMEMory:TRANsfer? "GCA125.csv"')

    xydata=[]
    parse=r.split('\n')
    data=parse[9:parse.__len__()-4]
    result=''
    for i in data:
        d=i.split(',')
        result+='{}:{};'.format(d[0],d[1])
    return result