from scpisender import SCPI

#make gca_meas
CompLevel         = 1      # 1 dB compression level
Tolerance         = 0.05   # SMART Sweep tolerance
StartFreq         = 2.244E9
StopFreq          = 2.246E9
NumFreqs          = 201
Scale             = 0.1
LinearPower       = -20
BackOff           = 10     # Not used for Deviation from linear gain
StartPower        = -70
StopPower         = -50
NumPowers         = 60     # Not used for SMART Sweep
DwellTime         = 0.0005 # Allow some time for DUT bias/thermal effects
IFBandwidth       = 1000   # Reasonable trace noise at -20 dBm


gca_meas = SCPI()

gca_meas.reset()

gca_meas.__send__("CALC:CUST:DEF 'Gain Comp', 'Gain Compression Converters', 'CompOut21'")
gca_meas.__send__("DISP:WIND:TRAC1:FEED 'Gain Comp'")
gca_meas.__send__("CALC:PAR:SEL 'Gain Comp'")
gca_meas.__send__("SENS:SWE:MODE HOLD")

gca_meas.__send__("DISP:WIND:TRAC:Y:SCAL:PDIV " + str(Scale))
gca_meas.__send__("DISP:WIND:TRAC:Y:RLEV -" + str(CompLevel))

gca_meas.__send__("SENS:MIX:LO:POW 0")
gca_meas.__send__("SENS:MIX:INP:FREQ:FIXED 2.245e9") # 2345-2145
gca_meas.__send__("SENS:MIX:LO:FREQ:FIXED 8.705e9") 
gca_meas.__send__("SENS:MIX:OUTP:FREQ:SID HIGH")
gca_meas.__send__("SENS:MIX:CALC OUTPut")

gca_meas.__send__("SENS:GCS:AMOD SMAR")

gca_meas.__send__("SENS:GCS:COMP:ALG CFLG")
gca_meas.__send__("SENS:GCS:COMP:INT OFF")
gca_meas.__send__("SENS:GCS:SMAR:SIT OFF")

gca_meas.__send__("SENS:GCS:COMP:LEV " +str(CompLevel))
gca_meas.__send__("SENS:GCS:COMP:BACK:LEV " +str(BackOff))
gca_meas.__send__("SENS:GCS:COMP:DELT:X " +str(BackOff))
gca_meas.__send__("SENS:GCS:COMP:DELT:Y " +str(BackOff))
gca_meas.__send__("SENS:GCS:SWE:FREQ:POIN " +str(NumPowers))
gca_meas.__send__("SENS:GCS:SMAR:STIM " +str(DwellTime))
gca_meas.__send__("SENS:BAND " +str(IFBandwidth))
gca_meas.__send__("SENS:SWE:DWEL " +str(DwellTime))
gca_meas.__send__("SOUR:POW:STAR " +str(StartPower))
gca_meas.__send__("SOUR:POW:STOP " +str(StopPower))
gca_meas.__send__("SENS:FREQ:STAR " +str(StartFreq))
gca_meas.__send__("SENS:FREQ:STOP " +str(StopFreq))
gca_meas.__send__("SENS:SWE:POIN " +str(NumFreqs))
gca_meas.__send__("SENS:SWE:MODE SING")

gca_meas.__send__("*OPC?")

gca_meas.__send__("CALC:PAR:MNUM 1")
gca_meas.__send__("CALC:GCM:ANAL:ENABLE 1") 
gca_meas.__send__("CALC:GCM:ANAL:CWFR 1e9")
