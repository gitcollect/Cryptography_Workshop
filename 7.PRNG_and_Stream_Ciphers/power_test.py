import subprocess

volth=subprocess.check_output(['i2cget','-y','-f','0','0x34','0x56'])
voltl=subprocess.check_output(['i2cget','-y','-f','0','0x34','0x57'])
volts=(int(volth,16)<<4)+(int(voltl,16))
ampsh=subprocess.check_output(['i2cget','-y','-f','0','0x34','0x58'])
ampsl=subprocess.check_output(['i2cget','-y','-f','0','0x34','0x59'])
amps=(int(ampsh,16)<<4)+(int(ampsl,16))
volts=volts*0.0017
amps=amps*0.000625
print 'Volts =',volts
print 'Amps =',amps
