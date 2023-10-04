from datetime import datetime
from time import sleep
from pifacecad.tools.scanf import LCDScanf
from pyowm.owm import OWM
import pifacecad
import lirc
import pygame

#비트맵 설정
global _j,_n,_n2,_i,_g,_g2,_y,_y2
_j = pifacecad.LCDBitmap([0x1F,
  0x04,
  0x04,
  0x04,
  0x04,
  0x0A,
  0x11,
  0x00])
_i = pifacecad.LCDBitmap([0x01,
  0x01,
  0x01,
  0x01,
  0x01,
  0x01,
  0x01,
  0x01])
_n = pifacecad.LCDBitmap([0x00,
  0x00,
  0x10,
  0x10,
  0x10,
  0x10,
  0x10,
  0x1F])
_n2 = pifacecad.LCDBitmap([0x00,
  0x00,
  0x00,
  0x00,
  0x00,
  0x00,
  0x00,
  0x1F])
_g = pifacecad.LCDBitmap([0x0F,
  0x00,
  0x00,
  0x00,
  0x00,
  0x00,
  0x00,
  0x1F])
_g2 = pifacecad.LCDBitmap([0x1E,
  0x02,
  0x02,
  0x02,
  0x02,
  0x02,
  0x00,
  0x1F])
_y = pifacecad.LCDBitmap([0x04,
  0x04,
  0x04,
  0x04,
  0x04,
  0x04,
  0x04,
  0x04])
_y2 = pifacecad.LCDBitmap([0x04,
  0x04,
  0x04,
  0x04,
  0x04,
  0x04,
  0x04,
  0x04])
cad = pifacecad.PiFaceCAD()
cad.lcd.backlight_on()
cad.lcd.cursor_off()

#변수 선언 및 초기화
global LED_F
LED_F = 1
global btn
btn = -1
global remote
remote = -1
global Alarm
global mode 
mode = 0
global Time
Time = 0
global flag
flag = 0
global alarm_time
alarm_time = [0,0]
global weather_num
weather_num = 0

def clock():
	global mode
	global Time
	global Alarm
	global flag
	cad.lcd.cursor_on()
	cad.lcd.set_cursor(0,0)
	now = datetime.now()
	cad.lcd.write(now.strftime("%Y-%m-%d"))
	cad.lcd.set_cursor(0,1)
	cad.lcd.write(now.strftime("%A %H:%M"))
	Time = now.strftime('%H:%M')
	if(flag == 1):
		Alarm = '{:02d}'.format(alarm_time[0])+":"+'{:02d}'.format(alarm_time[1])
		if(Time == Alarm):
			mode = 1

def Alarm_run():
	cad.lcd.clear()
	cad.lcd.write("Alarm!!!!")
	if(mode != 0):
		pygame.mixer.music.play()

def check_button(event):
	global btn
	btn = event.pin_num
	print(btn)
	
def check_remote(event):
	global remote
	remote = int(event.ir_code)
	print(remote)

def back_ON_OFF():
	global LED_F
	if(LED_F == 1):
		cad.lcd.backlight_off()
		LED_F = 0
	else:
		cad.lcd.backlight_on()
		LED_F = 1

def main_fuc():
	global flag
	global btn
	global remote
	global mode
	global weather_num
	global alarm_time
	if(remote == 0):
		back_ON_OFF()
	elif((btn == 1 or remote == 1)and mode == 1):
		pygame.mixer.music.stop()
		alarm_time = [0,0]
		mode = 0
		flag = 0
	elif((btn == 2 or remote == 2)and mode == 0):
		set_alarm()
		mode = 0
	elif((btn == 3 or remote ==3)and mode == 0):
		check_alarm()
		mode = 0
	elif((btn == 4 or remote == 4)and mode == 0):
		listener.deactivate()
		remote_listener.deactivate()
		cad.lcd.clear()
		cad.lcd.write("End")
		exit()
	elif((btn == 5 or remote ==5)and (mode == 0 or mode ==6)):
		if(mode == 6):
			cad.lcd.clear()
			mode = 0
		elif(mode == 0):
			mode = 5
	elif((btn == 6 or remote == 6)and mode == 6):
		if(weather_num >= 1):
			weather_num -= 1
			W_Weather(weather_num)
	elif((btn == 7 or remote == 7)and mode == 6):
		if(weather_num < 4):
			weather_num += 1
			W_Weather(weather_num)
	elif(remote == 8 and mode == 0):
		global _j,_n,_n2,_i
		cad.lcd.clear()
		cad.lcd.set_cursor(0,1)
		cad.lcd.write("Made by")
		cad.lcd.set_cursor(9,0)
		cad.lcd.store_custom_bitmap(0,_j)
		cad.lcd.store_custom_bitmap(1,_i)
		cad.lcd.store_custom_bitmap(2,_n)
		cad.lcd.store_custom_bitmap(3,_n2)
		cad.lcd.store_custom_bitmap(4,_g)
		cad.lcd.store_custom_bitmap(5,_g2)
		cad.lcd.store_custom_bitmap(6,_y)
		cad.lcd.store_custom_bitmap(7,_y2)
		cad.lcd.write_custom_bitmap(0)
		cad.lcd.write_custom_bitmap(1)
		cad.lcd.set_cursor(9,1)
		cad.lcd.write_custom_bitmap(2)
		cad.lcd.write_custom_bitmap(3)
		cad.lcd.set_cursor(13,0)
		cad.lcd.write_custom_bitmap(4)
		cad.lcd.write_custom_bitmap(5)
		cad.lcd.set_cursor(13,1)
		cad.lcd.write_custom_bitmap(6)
		cad.lcd.write_custom_bitmap(7)
		sleep(3)
		cad.lcd.clear()
	btn = -1
	remote = -1		
	
def set_alarm():
	global flag
	global alarm_time
	flag = 1
	scanner = LCDScanf("set_time %2i:%2i %r")
	alarm_time = scanner.scan()
	cad.lcd.clear()
	cad.lcd.write("SetAlarm")
	cad.lcd.set_cursor(0,1)
	cad.lcd.write('{:02d}'.format(alarm_time[0])+":"+'{:02d}'.format(alarm_time[1]))
	cad.lcd.cursor_off()
	sleep(1)

def check_alarm():
	global alarm_time
	cad.lcd.clear()
	cad.lcd.write("Alarm_time")
	cad.lcd.set_cursor(0,1)
	cad.lcd.write('{:02d}'.format(alarm_time[0])+":"+'{:02d}'.format(alarm_time[1]))
	sleep(2)

def W_Weather(num):
	global mode
	mode = 6
	global observation
	weather = observation[num].weather
	location = observation[num].location
	cad.lcd.clear()
	cad.lcd.set_cursor(0,0)
	cad.lcd.write(location.name)
	cad.lcd.set_cursor(0,1)
	cad.lcd.write(weather.detailed_status)

#사운드 설정
pygame.mixer.init()
pygame.mixer.music.set_volume(1)
pygame.mixer.music.load('alarm.mp3')

#리모컨 리스너 설정
socketid = lirc.init("myprogram")
remote_listener = pifacecad.IREventListener(prog='myprogram')
for i in range(10):
	remote_listener.register(str(i), check_remote)
remote_listener.activate()

#버튼 리스너 설정
listener = pifacecad.SwitchEventListener(chip=cad)
for i in range(1,8):
	listener.register(i, pifacecad.IODIR_FALLING_EDGE,check_button)
listener.activate()

#날씨 설정
global observation
mykey = '50295f09ffe55550dad6cd3f2f6c35aa'
owm = OWM(mykey)
mgr = owm.weather_manager()
observation = [0,0,0,0,0]
observation[0] = mgr.weather_at_place('Incheon,KR')
observation[1] = mgr.weather_at_place('Paris,FR')
observation[2] = mgr.weather_at_place('New York,US')
observation[3] = mgr.weather_at_place('Shanghai,CN')
observation[4] = mgr.weather_at_place('London,UK')
	
#mode 
while True:
	main_fuc()
	if(mode == 0):
		clock()
		sleep(2)
	elif(mode == 1 and flag == 1):
		Alarm_run()
		sleep(1)
	elif(mode == 5):
		W_Weather(weather_num)

