import pykka

from mopidy import core
import time 
import RPi.GPIO as GPIO
LCD_RS = 7 
LCD_E = 8 
LCD_D4 = 17 
LCD_D5 = 18 #GPIO18 = Pi pin 12
LCD_D6 = 27 #GPIO21 = Pi pin 13 (Use 21 on Rev.1 
LCD_D7 = 22 #GPIO22 = Pi pin 15
OUTPUTS = [LCD_RS,LCD_E,LCD_D4,LCD_D5,LCD_D6,LCD_D7]
SW1 = 4 #GPIO4 = Pi pin 7
SW2 = 23 #GPIO16 = Pi pin 16
SW3 = 10 #GPIO10 = Pi pin 19
SW4 = 9 #GPIO9 = Pi pin 21
INPUTS = [SW1,SW2,SW3,SW4]
CLEARDISPLAY = 0x01
SETCURSOR = 0x80
LINE = [0x00,0x40] #for 16x2 display

class switch(object):
		    def __init__(self, value):
		        self.value = value
		        self.fall = False

		    def __iter__(self):
		        """Return the match method once, then stop"""
		        yield self.match
		        raise StopIteration
		    
		    def match(self, *args):
		        """Indicate whether or not to enter a case suite"""
		        if self.fall or not args:
		            return True
		        elif self.value in args: # changed for v1.5, see below
		            self.fall = True
		            return True
			        else:
            return False
class GPIO420Frontend(pykka.ThreadingActor, core.CoreListener):
	def CheckSwitches():		
	 val1 = not GPIO.input(SW1)
	 val2 = not GPIO.input(SW2)
	 val3 = not GPIO.input(SW3)
	 val4 = not GPIO.input(SW4)
	 return (val4,val1,val2,val3)
	def PulseEnableLine():
	 mSec = 0.0005 #use half-millisecond delay
	 time.sleep(mSec) #give time for inputs to settle
	 GPIO.output(LCD_E, GPIO.HIGH) #pulse E high
	 time.sleep(mSec)
	 GPIO.output(LCD_E, GPIO.LOW) #return E low
	 time.sleep(mSec) #wait before doing anything else
	def SendNibble(data):
	 GPIO.output(LCD_D4, bool(data & 0x10))
	 GPIO.output(LCD_D5, bool(data & 0x20))
	 GPIO.output(LCD_D6, bool(data & 0x40))
	 GPIO.output(LCD_D7, bool(data & 0x80))
	def SendByte(data,charMode=False):
	 GPIO.output(LCD_RS,charMode) #set mode: command vs. char
	 SendNibble(data) #send upper bits first
	 PulseEnableLine() #pulse the enable line
	 data = (data & 0x0F)<< 4 #shift 4 bits to left
	 SendNibble(data) #send lower bits now
	 PulseEnableLine() #pulse the enable lin
	def SendChar(ch):
	 SendByte(ord(ch),True)
	def ShowMessage(string, line): for character in string:
	 	GotoLine(line)
	 	SendChar(character)
	def GotoLine(row):
	 addr = LINE[row]
	 SendByte(SETCURSOR+addr)
	def print420(headline,text, repeats):
     zeit=0.3
	 ShowMessage(headline,0)
	 while(len(text)<=16):
	 	text = text + "***"+ text
	 temptext = text+"***"
	 repeats = (len(text)+3) * repeats
	 while(repeats > 0):
	    firsttext=""
	    lasttext=""
	    counter = 0
	    while(counter < len(temptext)):
	     if(counter>16):
	      lasttext+=temptext[counter]
	     else:
	      firsttext+=temptext[counter]
	     counter = counter +1
	     ShowMessage(firsttext,1)
   	 newtext = ""
     for x in range(1, len(firsttext)):
         newtext += firsttext[x]
     lasttext +=firsttext[0]
     newtext += lasttext[0]
     firsttext = newtext
     newtext = ""
     for x in range (1, len(lasttext)):
      newtext += lasttext[x]
     lasttext= newtext
     repeats = repeats -1
     temptext = firsttext+lasttext
     time.sleep(zeit)

    def __init__(self, config, core):
        super(GPIO420Frontend, self).__init__()
        self.core = core
        GPIO.setmode(GPIO.BCM)
	 	GPIO.setwarnings(False)
	 	for lcdLine in OUTPUTS:
	 		GPIO.setup(lcdLine, GPIO.OUT)
	 	for switch in INPUTS:
	 		GPIO.setup(switch, GPIO.IN, pull_up_down=GPIO.PUD_UP)
	 	SendByte(0x33) #initialize
	 	SendByte(0x32) #set to 4-bit mode
	 	SendByte(0x28) #2 line, 5x7 matrix
	 	SendByte(0x0C) #turn cursor off (0x0E to enable)
	 	SendByte(0x06) #shift cursor right
	 	SendByte(CLEARDISPLAY) #remove any stray characters on display
	 	print420("Hallo :)","Du kannst jetzt die Keys benutzen",10)
	

	


    def on_start(self):
    	ShowMessage("MUSIK                      ")
		while (True):
		 time.sleep(0.2)
		 lt = localtime()
		 stunde = strftime("%H", lt)
		 minute = strftime("%M", lt)
		 if(((stunde=="4")or(stunde=="16"))and(minute=="20")):
		 	print420("420 Blaze it","Lodere es, es ist 420!!",1)
		 if(((stunde=="4")or(stunde=="16"))and((minute>10)and(minute>20))):
		 	print420("420","Get ready for takeoff",1)
		 switchValues = CheckSwitches()
		 decimalResult = "%d %d %d %d" % switchValues
		 for case in switch(decimalResult):
		    if case("1 0 0 0"):#Knopf 1 
		        sound = mopidy.core.MixerController.get_volume()
		        soundString = "Volume: "
		        if (sound > 5):
					sound = sound - 5
					mopidy.core.MixerController.set_volume(sound)
					soundString += 'sound'
					print420("Sound",soundString,1)
				else:
					mopidy.core.MixerController.set_volume(0)
					print420("Sound","MUTE", 1)
		        break
		    if case("0 1 0 0"):#Knopf 2
				state = mopidy.core.PlaybackController.get_state()
				if (state == "PLAYING"):
					mopidy.core.PlaybackController.stop()
				else:
					mopidy.core.PlaybackController.resume()
		    if case("0 0 1 0"):#Knopf 3
		        sound = mopidy.core.MixerController.get_volume()
		        soundString = "Volume: "
		        if (sound < 95): 
		        	sound = sound + 5
		        	soundString += 'sound'
					mopidy.core.MixerController.set_volume(sound)
					print420("Sound",soundString,1)
				else:
					mopidy.core.MixerController.set_volume(100)
					print420("Sound","Volume: 100",1)
		        break
		    if case("0 0 0 1"):#Knopf4
		        mopidy.core.PlaybackController.next()
    		    break