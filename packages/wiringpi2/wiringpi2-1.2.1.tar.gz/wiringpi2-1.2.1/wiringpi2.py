# This file was automatically generated by SWIG (http://www.swig.org).
# Version 3.0.2
#
# Do not make changes to this file unless you know what you are doing--modify
# the SWIG interface file instead.





from sys import version_info
if version_info >= (2,6,0):
    def swig_import_helper():
        from os.path import dirname
        import imp
        fp = None
        try:
            fp, pathname, description = imp.find_module('_wiringpi2', [dirname(__file__)])
        except ImportError:
            import _wiringpi2
            return _wiringpi2
        if fp is not None:
            try:
                _mod = imp.load_module('_wiringpi2', fp, pathname, description)
            finally:
                fp.close()
            return _mod
    _wiringpi2 = swig_import_helper()
    del swig_import_helper
else:
    import _wiringpi2
del version_info
try:
    _swig_property = property
except NameError:
    pass # Python < 2.2 doesn't have 'property'.
def _swig_setattr_nondynamic(self,class_type,name,value,static=1):
    if (name == "thisown"): return self.this.own(value)
    if (name == "this"):
        if type(value).__name__ == 'SwigPyObject':
            self.__dict__[name] = value
            return
    method = class_type.__swig_setmethods__.get(name,None)
    if method: return method(self,value)
    if (not static):
        self.__dict__[name] = value
    else:
        raise AttributeError("You cannot add attributes to %s" % self)

def _swig_setattr(self,class_type,name,value):
    return _swig_setattr_nondynamic(self,class_type,name,value,0)

def _swig_getattr(self,class_type,name):
    if (name == "thisown"): return self.this.own()
    method = class_type.__swig_getmethods__.get(name,None)
    if method: return method(self)
    raise AttributeError(name)

def _swig_repr(self):
    try: strthis = "proxy of " + self.this.__repr__()
    except: strthis = ""
    return "<%s.%s; %s >" % (self.__class__.__module__, self.__class__.__name__, strthis,)

try:
    _object = object
    _newclass = 1
except AttributeError:
    class _object : pass
    _newclass = 0



def wiringPiFailure(*args):
  return _wiringpi2.wiringPiFailure(*args)
wiringPiFailure = _wiringpi2.wiringPiFailure

def wiringPiFindNode(*args):
  return _wiringpi2.wiringPiFindNode(*args)
wiringPiFindNode = _wiringpi2.wiringPiFindNode

def wiringPiNewNode(*args):
  return _wiringpi2.wiringPiNewNode(*args)
wiringPiNewNode = _wiringpi2.wiringPiNewNode

def wiringPiSetup():
  return _wiringpi2.wiringPiSetup()
wiringPiSetup = _wiringpi2.wiringPiSetup

def wiringPiSetupSys():
  return _wiringpi2.wiringPiSetupSys()
wiringPiSetupSys = _wiringpi2.wiringPiSetupSys

def wiringPiSetupGpio():
  return _wiringpi2.wiringPiSetupGpio()
wiringPiSetupGpio = _wiringpi2.wiringPiSetupGpio

def wiringPiSetupPhys():
  return _wiringpi2.wiringPiSetupPhys()
wiringPiSetupPhys = _wiringpi2.wiringPiSetupPhys

def pinModeAlt(*args):
  return _wiringpi2.pinModeAlt(*args)
pinModeAlt = _wiringpi2.pinModeAlt

def pinMode(*args):
  return _wiringpi2.pinMode(*args)
pinMode = _wiringpi2.pinMode

def pullUpDnControl(*args):
  return _wiringpi2.pullUpDnControl(*args)
pullUpDnControl = _wiringpi2.pullUpDnControl

def digitalRead(*args):
  return _wiringpi2.digitalRead(*args)
digitalRead = _wiringpi2.digitalRead

def digitalWrite(*args):
  return _wiringpi2.digitalWrite(*args)
digitalWrite = _wiringpi2.digitalWrite

def pwmWrite(*args):
  return _wiringpi2.pwmWrite(*args)
pwmWrite = _wiringpi2.pwmWrite

def analogRead(*args):
  return _wiringpi2.analogRead(*args)
analogRead = _wiringpi2.analogRead

def analogWrite(*args):
  return _wiringpi2.analogWrite(*args)
analogWrite = _wiringpi2.analogWrite

def piBoardRev():
  return _wiringpi2.piBoardRev()
piBoardRev = _wiringpi2.piBoardRev

def piBoardId(*args):
  return _wiringpi2.piBoardId(*args)
piBoardId = _wiringpi2.piBoardId

def wpiPinToGpio(*args):
  return _wiringpi2.wpiPinToGpio(*args)
wpiPinToGpio = _wiringpi2.wpiPinToGpio

def physPinToGpio(*args):
  return _wiringpi2.physPinToGpio(*args)
physPinToGpio = _wiringpi2.physPinToGpio

def setPadDrive(*args):
  return _wiringpi2.setPadDrive(*args)
setPadDrive = _wiringpi2.setPadDrive

def getAlt(*args):
  return _wiringpi2.getAlt(*args)
getAlt = _wiringpi2.getAlt

def pwmToneWrite(*args):
  return _wiringpi2.pwmToneWrite(*args)
pwmToneWrite = _wiringpi2.pwmToneWrite

def digitalWriteByte(*args):
  return _wiringpi2.digitalWriteByte(*args)
digitalWriteByte = _wiringpi2.digitalWriteByte

def pwmSetMode(*args):
  return _wiringpi2.pwmSetMode(*args)
pwmSetMode = _wiringpi2.pwmSetMode

def pwmSetRange(*args):
  return _wiringpi2.pwmSetRange(*args)
pwmSetRange = _wiringpi2.pwmSetRange

def pwmSetClock(*args):
  return _wiringpi2.pwmSetClock(*args)
pwmSetClock = _wiringpi2.pwmSetClock

def gpioClockSet(*args):
  return _wiringpi2.gpioClockSet(*args)
gpioClockSet = _wiringpi2.gpioClockSet

def waitForInterrupt(*args):
  return _wiringpi2.waitForInterrupt(*args)
waitForInterrupt = _wiringpi2.waitForInterrupt

def wiringPiISR(*args):
  return _wiringpi2.wiringPiISR(*args)
wiringPiISR = _wiringpi2.wiringPiISR

def piThreadCreate(*args):
  return _wiringpi2.piThreadCreate(*args)
piThreadCreate = _wiringpi2.piThreadCreate

def piLock(*args):
  return _wiringpi2.piLock(*args)
piLock = _wiringpi2.piLock

def piUnlock(*args):
  return _wiringpi2.piUnlock(*args)
piUnlock = _wiringpi2.piUnlock

def piHiPri(*args):
  return _wiringpi2.piHiPri(*args)
piHiPri = _wiringpi2.piHiPri

def delay(*args):
  return _wiringpi2.delay(*args)
delay = _wiringpi2.delay

def delayMicroseconds(*args):
  return _wiringpi2.delayMicroseconds(*args)
delayMicroseconds = _wiringpi2.delayMicroseconds

def millis():
  return _wiringpi2.millis()
millis = _wiringpi2.millis

def micros():
  return _wiringpi2.micros()
micros = _wiringpi2.micros

def ds1302rtcRead(*args):
  return _wiringpi2.ds1302rtcRead(*args)
ds1302rtcRead = _wiringpi2.ds1302rtcRead

def ds1302rtcWrite(*args):
  return _wiringpi2.ds1302rtcWrite(*args)
ds1302rtcWrite = _wiringpi2.ds1302rtcWrite

def ds1302ramRead(*args):
  return _wiringpi2.ds1302ramRead(*args)
ds1302ramRead = _wiringpi2.ds1302ramRead

def ds1302ramWrite(*args):
  return _wiringpi2.ds1302ramWrite(*args)
ds1302ramWrite = _wiringpi2.ds1302ramWrite

def ds1302clockRead(*args):
  return _wiringpi2.ds1302clockRead(*args)
ds1302clockRead = _wiringpi2.ds1302clockRead

def ds1302clockWrite(*args):
  return _wiringpi2.ds1302clockWrite(*args)
ds1302clockWrite = _wiringpi2.ds1302clockWrite

def ds1302trickleCharge(*args):
  return _wiringpi2.ds1302trickleCharge(*args)
ds1302trickleCharge = _wiringpi2.ds1302trickleCharge

def ds1302setup(*args):
  return _wiringpi2.ds1302setup(*args)
ds1302setup = _wiringpi2.ds1302setup

def gertboardAnalogWrite(*args):
  return _wiringpi2.gertboardAnalogWrite(*args)
gertboardAnalogWrite = _wiringpi2.gertboardAnalogWrite

def gertboardAnalogRead(*args):
  return _wiringpi2.gertboardAnalogRead(*args)
gertboardAnalogRead = _wiringpi2.gertboardAnalogRead

def gertboardSPISetup():
  return _wiringpi2.gertboardSPISetup()
gertboardSPISetup = _wiringpi2.gertboardSPISetup

def gertboardAnalogSetup(*args):
  return _wiringpi2.gertboardAnalogSetup(*args)
gertboardAnalogSetup = _wiringpi2.gertboardAnalogSetup

def lcd128x64setOrigin(*args):
  return _wiringpi2.lcd128x64setOrigin(*args)
lcd128x64setOrigin = _wiringpi2.lcd128x64setOrigin

def lcd128x64setOrientation(*args):
  return _wiringpi2.lcd128x64setOrientation(*args)
lcd128x64setOrientation = _wiringpi2.lcd128x64setOrientation

def lcd128x64orientCoordinates(*args):
  return _wiringpi2.lcd128x64orientCoordinates(*args)
lcd128x64orientCoordinates = _wiringpi2.lcd128x64orientCoordinates

def lcd128x64getScreenSize(*args):
  return _wiringpi2.lcd128x64getScreenSize(*args)
lcd128x64getScreenSize = _wiringpi2.lcd128x64getScreenSize

def lcd128x64point(*args):
  return _wiringpi2.lcd128x64point(*args)
lcd128x64point = _wiringpi2.lcd128x64point

def lcd128x64line(*args):
  return _wiringpi2.lcd128x64line(*args)
lcd128x64line = _wiringpi2.lcd128x64line

def lcd128x64lineTo(*args):
  return _wiringpi2.lcd128x64lineTo(*args)
lcd128x64lineTo = _wiringpi2.lcd128x64lineTo

def lcd128x64rectangle(*args):
  return _wiringpi2.lcd128x64rectangle(*args)
lcd128x64rectangle = _wiringpi2.lcd128x64rectangle

def lcd128x64circle(*args):
  return _wiringpi2.lcd128x64circle(*args)
lcd128x64circle = _wiringpi2.lcd128x64circle

def lcd128x64ellipse(*args):
  return _wiringpi2.lcd128x64ellipse(*args)
lcd128x64ellipse = _wiringpi2.lcd128x64ellipse

def lcd128x64putchar(*args):
  return _wiringpi2.lcd128x64putchar(*args)
lcd128x64putchar = _wiringpi2.lcd128x64putchar

def lcd128x64puts(*args):
  return _wiringpi2.lcd128x64puts(*args)
lcd128x64puts = _wiringpi2.lcd128x64puts

def lcd128x64update():
  return _wiringpi2.lcd128x64update()
lcd128x64update = _wiringpi2.lcd128x64update

def lcd128x64clear(*args):
  return _wiringpi2.lcd128x64clear(*args)
lcd128x64clear = _wiringpi2.lcd128x64clear

def lcd128x64setup():
  return _wiringpi2.lcd128x64setup()
lcd128x64setup = _wiringpi2.lcd128x64setup

def lcdHome(*args):
  return _wiringpi2.lcdHome(*args)
lcdHome = _wiringpi2.lcdHome

def lcdClear(*args):
  return _wiringpi2.lcdClear(*args)
lcdClear = _wiringpi2.lcdClear

def lcdDisplay(*args):
  return _wiringpi2.lcdDisplay(*args)
lcdDisplay = _wiringpi2.lcdDisplay

def lcdCursor(*args):
  return _wiringpi2.lcdCursor(*args)
lcdCursor = _wiringpi2.lcdCursor

def lcdCursorBlink(*args):
  return _wiringpi2.lcdCursorBlink(*args)
lcdCursorBlink = _wiringpi2.lcdCursorBlink

def lcdSendCommand(*args):
  return _wiringpi2.lcdSendCommand(*args)
lcdSendCommand = _wiringpi2.lcdSendCommand

def lcdPosition(*args):
  return _wiringpi2.lcdPosition(*args)
lcdPosition = _wiringpi2.lcdPosition

def lcdCharDef(*args):
  return _wiringpi2.lcdCharDef(*args)
lcdCharDef = _wiringpi2.lcdCharDef

def lcdPutchar(*args):
  return _wiringpi2.lcdPutchar(*args)
lcdPutchar = _wiringpi2.lcdPutchar

def lcdPuts(*args):
  return _wiringpi2.lcdPuts(*args)
lcdPuts = _wiringpi2.lcdPuts

def lcdPrintf(*args):
  return _wiringpi2.lcdPrintf(*args)
lcdPrintf = _wiringpi2.lcdPrintf

def lcdInit(*args):
  return _wiringpi2.lcdInit(*args)
lcdInit = _wiringpi2.lcdInit

def piFaceSetup(*args):
  return _wiringpi2.piFaceSetup(*args)
piFaceSetup = _wiringpi2.piFaceSetup

def piGlow1(*args):
  return _wiringpi2.piGlow1(*args)
piGlow1 = _wiringpi2.piGlow1

def piGlowLeg(*args):
  return _wiringpi2.piGlowLeg(*args)
piGlowLeg = _wiringpi2.piGlowLeg

def piGlowRing(*args):
  return _wiringpi2.piGlowRing(*args)
piGlowRing = _wiringpi2.piGlowRing

def piGlowSetup(*args):
  return _wiringpi2.piGlowSetup(*args)
piGlowSetup = _wiringpi2.piGlowSetup

def setupNesJoystick(*args):
  return _wiringpi2.setupNesJoystick(*args)
setupNesJoystick = _wiringpi2.setupNesJoystick

def readNesJoystick(*args):
  return _wiringpi2.readNesJoystick(*args)
readNesJoystick = _wiringpi2.readNesJoystick

def sr595Setup(*args):
  return _wiringpi2.sr595Setup(*args)
sr595Setup = _wiringpi2.sr595Setup

def drcSetupSerial(*args):
  return _wiringpi2.drcSetupSerial(*args)
drcSetupSerial = _wiringpi2.drcSetupSerial

def max31855Setup(*args):
  return _wiringpi2.max31855Setup(*args)
max31855Setup = _wiringpi2.max31855Setup

def max5322Setup(*args):
  return _wiringpi2.max5322Setup(*args)
max5322Setup = _wiringpi2.max5322Setup

def mcp23008Setup(*args):
  return _wiringpi2.mcp23008Setup(*args)
mcp23008Setup = _wiringpi2.mcp23008Setup

def mcp23016Setup(*args):
  return _wiringpi2.mcp23016Setup(*args)
mcp23016Setup = _wiringpi2.mcp23016Setup

def mcp23017Setup(*args):
  return _wiringpi2.mcp23017Setup(*args)
mcp23017Setup = _wiringpi2.mcp23017Setup

def mcp23s08Setup(*args):
  return _wiringpi2.mcp23s08Setup(*args)
mcp23s08Setup = _wiringpi2.mcp23s08Setup

def mcp23s17Setup(*args):
  return _wiringpi2.mcp23s17Setup(*args)
mcp23s17Setup = _wiringpi2.mcp23s17Setup

def mcp3002Setup(*args):
  return _wiringpi2.mcp3002Setup(*args)
mcp3002Setup = _wiringpi2.mcp3002Setup

def mcp3004Setup(*args):
  return _wiringpi2.mcp3004Setup(*args)
mcp3004Setup = _wiringpi2.mcp3004Setup

def mcp3422Setup(*args):
  return _wiringpi2.mcp3422Setup(*args)
mcp3422Setup = _wiringpi2.mcp3422Setup

def mcp4802Setup(*args):
  return _wiringpi2.mcp4802Setup(*args)
mcp4802Setup = _wiringpi2.mcp4802Setup

def pcf8574Setup(*args):
  return _wiringpi2.pcf8574Setup(*args)
pcf8574Setup = _wiringpi2.pcf8574Setup

def pcf8591Setup(*args):
  return _wiringpi2.pcf8591Setup(*args)
pcf8591Setup = _wiringpi2.pcf8591Setup

def sn3218Setup(*args):
  return _wiringpi2.sn3218Setup(*args)
sn3218Setup = _wiringpi2.sn3218Setup

def softPwmCreate(*args):
  return _wiringpi2.softPwmCreate(*args)
softPwmCreate = _wiringpi2.softPwmCreate

def softPwmWrite(*args):
  return _wiringpi2.softPwmWrite(*args)
softPwmWrite = _wiringpi2.softPwmWrite

def softPwmStop(*args):
  return _wiringpi2.softPwmStop(*args)
softPwmStop = _wiringpi2.softPwmStop

def softServoWrite(*args):
  return _wiringpi2.softServoWrite(*args)
softServoWrite = _wiringpi2.softServoWrite

def softServoSetup(*args):
  return _wiringpi2.softServoSetup(*args)
softServoSetup = _wiringpi2.softServoSetup

def softToneCreate(*args):
  return _wiringpi2.softToneCreate(*args)
softToneCreate = _wiringpi2.softToneCreate

def softToneStop(*args):
  return _wiringpi2.softToneStop(*args)
softToneStop = _wiringpi2.softToneStop

def softToneWrite(*args):
  return _wiringpi2.softToneWrite(*args)
softToneWrite = _wiringpi2.softToneWrite

def wiringPiSPIGetFd(*args):
  return _wiringpi2.wiringPiSPIGetFd(*args)
wiringPiSPIGetFd = _wiringpi2.wiringPiSPIGetFd

def wiringPiSPIDataRW(*args):
  return _wiringpi2.wiringPiSPIDataRW(*args)
wiringPiSPIDataRW = _wiringpi2.wiringPiSPIDataRW

def wiringPiSPISetup(*args):
  return _wiringpi2.wiringPiSPISetup(*args)
wiringPiSPISetup = _wiringpi2.wiringPiSPISetup

def wiringPiI2CRead(*args):
  return _wiringpi2.wiringPiI2CRead(*args)
wiringPiI2CRead = _wiringpi2.wiringPiI2CRead

def wiringPiI2CReadReg8(*args):
  return _wiringpi2.wiringPiI2CReadReg8(*args)
wiringPiI2CReadReg8 = _wiringpi2.wiringPiI2CReadReg8

def wiringPiI2CReadReg16(*args):
  return _wiringpi2.wiringPiI2CReadReg16(*args)
wiringPiI2CReadReg16 = _wiringpi2.wiringPiI2CReadReg16

def wiringPiI2CWrite(*args):
  return _wiringpi2.wiringPiI2CWrite(*args)
wiringPiI2CWrite = _wiringpi2.wiringPiI2CWrite

def wiringPiI2CWriteReg8(*args):
  return _wiringpi2.wiringPiI2CWriteReg8(*args)
wiringPiI2CWriteReg8 = _wiringpi2.wiringPiI2CWriteReg8

def wiringPiI2CWriteReg16(*args):
  return _wiringpi2.wiringPiI2CWriteReg16(*args)
wiringPiI2CWriteReg16 = _wiringpi2.wiringPiI2CWriteReg16

def wiringPiI2CSetupInterface(*args):
  return _wiringpi2.wiringPiI2CSetupInterface(*args)
wiringPiI2CSetupInterface = _wiringpi2.wiringPiI2CSetupInterface

def wiringPiI2CSetup(*args):
  return _wiringpi2.wiringPiI2CSetup(*args)
wiringPiI2CSetup = _wiringpi2.wiringPiI2CSetup

def serialOpen(*args):
  return _wiringpi2.serialOpen(*args)
serialOpen = _wiringpi2.serialOpen

def serialClose(*args):
  return _wiringpi2.serialClose(*args)
serialClose = _wiringpi2.serialClose

def serialFlush(*args):
  return _wiringpi2.serialFlush(*args)
serialFlush = _wiringpi2.serialFlush

def serialPutchar(*args):
  return _wiringpi2.serialPutchar(*args)
serialPutchar = _wiringpi2.serialPutchar

def serialPuts(*args):
  return _wiringpi2.serialPuts(*args)
serialPuts = _wiringpi2.serialPuts

def serialPrintf(*args):
  return _wiringpi2.serialPrintf(*args)
serialPrintf = _wiringpi2.serialPrintf

def serialDataAvail(*args):
  return _wiringpi2.serialDataAvail(*args)
serialDataAvail = _wiringpi2.serialDataAvail

def serialGetchar(*args):
  return _wiringpi2.serialGetchar(*args)
serialGetchar = _wiringpi2.serialGetchar

def shiftIn(*args):
  return _wiringpi2.shiftIn(*args)
shiftIn = _wiringpi2.shiftIn

def shiftOut(*args):
  return _wiringpi2.shiftOut(*args)
shiftOut = _wiringpi2.shiftOut
class nes(object):
  def setupNesJoystick(self,*args):
    return setupNesJoystick(*args)
  def readNesJoystick(self,*args):
    return readNesJoystick(*args)

class Serial(object):
  device = '/dev/ttyAMA0'
  baud = 9600
  serial_id = 0
  def printf(self,*args):
    return serialPrintf(self.serial_id,*args)
  def dataAvail(self,*args):
    return serialDataAvail(self.serial_id,*args)
  def getchar(self,*args):
    return serialGetchar(self.serial_id,*args)
  def putchar(self,*args):
    return serialPutchar(self.serial_id,*args)
  def puts(self,*args):
    return serialPuts(self.serial_id,*args)
  def __init__(self,device,baud):
    self.device = device
    self.baud = baud
    self.serial_id = serialOpen(self.device,self.baud)
  def __del__(self):
    serialClose(self.serial_id)

class I2C(object):
  def setupInterface(self,*args):
  	return wiringPiI2CSetupInterface(*args)
  def setup(self,*args):
    return wiringPiI2CSetup(*args)
  def read(self,*args):
    return wiringPiI2CRead(*args)
  def readReg8(self,*args):
    return wiringPiI2CReadReg8(*args)
  def readReg16(self,*args):
    return wiringPiI2CReadReg16(*args)
  def write(self,*args):
    return wiringPiI2CWrite(*args)
  def writeReg8(self,*args):
    return wiringPiI2CWriteReg8(*args)
  def writeReg16(self,*args):
    return wiringPiI2CWriteReg16(*args)

class GPIO(object):
  WPI_MODE_PINS = 0
  WPI_MODE_GPIO = 1
  WPI_MODE_GPIO_SYS = 2
  WPI_MODE_PHYS = 3
  WPI_MODE_PIFACE = 4
  WPI_MODE_UNINITIALISED = -1

  INPUT = 0
  OUTPUT = 1
  PWM_OUTPUT = 2
  GPIO_CLOCK = 3

  LOW = 0
  HIGH = 1

  PUD_OFF = 0
  PUD_DOWN = 1
  PUD_UP = 2

  PWM_MODE_MS = 0
  PWM_MODE_BAL = 1

  INT_EDGE_SETUP = 0
  INT_EDGE_FALLING = 1
  INT_EDGE_RISING = 2
  INT_EDGE_BOTH = 3

  LSBFIRST = 0
  MSBFIRST = 1

  MODE = 0
  def __init__(self,pinmode=0):
    self.MODE=pinmode
    if pinmode==self.WPI_MODE_PINS:
      wiringPiSetup()
    if pinmode==self.WPI_MODE_GPIO:
      wiringPiSetupGpio()
    if pinmode==self.WPI_MODE_GPIO_SYS:
      wiringPiSetupSys()
    if pinmode==self.WPI_MODE_PHYS:
      wiringPiSetupPhys()
    if pinmode==self.WPI_MODE_PIFACE:
      wiringPiSetupPiFace()

  def delay(self,*args):
    delay(*args)
  def delayMicroseconds(self,*args):
    delayMicroseconds(*args)
  def millis(self):
    return millis()
  def micros(self):
    return micros()

  def piHiPri(self,*args):
    return piHiPri(*args)

  def piBoardRev(self):
    return piBoardRev()
  def wpiPinToGpio(self,*args):
    return wpiPinToGpio(*args)
  def setPadDrive(self,*args):
    return setPadDrive(*args)
  def getAlt(self,*args):
    return getAlt(*args)
  def digitalWriteByte(self,*args):
    return digitalWriteByte(*args)

  def pwmSetMode(self,*args):
    pwmSetMode(*args)
  def pwmSetRange(self,*args):
    pwmSetRange(*args)
  def pwmSetClock(self,*args):
    pwmSetClock(*args)
  def gpioClockSet(self,*args):
    gpioClockSet(*args)
  def pwmWrite(self,*args):
    pwmWrite(*args)

  def pinMode(self,*args):
    pinMode(*args)

  def digitalWrite(self,*args):
    digitalWrite(*args)
  def digitalRead(self,*args):
    return digitalRead(*args)
  def digitalWriteByte(self,*args):
    digitalWriteByte(*args)

  def analogWrite(self,*args):
    analogWrite(*args)
  def analogRead(self,*args):
    return analogRead(*args)

  def shiftOut(self,*args):
    shiftOut(*args)
  def shiftIn(self,*args):
    return shiftIn(*args)

  def pullUpDnControl(self,*args):
    return pullUpDnControl(*args)

  def waitForInterrupt(self,*args):
    return waitForInterrupt(*args)
  def wiringPiISR(self,*args):
    return wiringPiISR(*args)

  def softPwmCreate(self,*args):
    return softPwmCreate(*args)
  def softPwmWrite(self,*args):
    return sofPwmWrite(*args)

  def softToneCreate(self,*args):
    return softToneCreate(*args)
  def softToneWrite(self,*args):
    return softToneWrite(*args)

  def lcdHome(self,*args):
    return lcdHome(self,*args)
  def lcdCLear(self,*args):
    return lcdClear(self,*args)
  def lcdSendCommand(self,*args):
    return lcdSendCommand(self,*args)
  def lcdPosition(self,*args):
    return lcdPosition(self,*args)
  def lcdPutchar(self,*args):
    return lcdPutchar(self,*args)
  def lcdPuts(self,*args):
    return lcdPuts(self,*args)
  def lcdPrintf(self,*args):
    return lcdPrintf(self,*args)
  def lcdInit(self,*args):
    return lcdInit(self,*args)
  def piGlowSetup(self,*args):
    return piGlowSetup(self,*args)
  def piGlow1(self,*args):
    return piGlow1(self,*args)
  def piGlowLeg(self,*args):
    return piGlowLeg(self,*args)
  def piGlowRing(self,*args):
    return piGlowRing(self,*args)

# This file is compatible with both classic and new-style classes.


