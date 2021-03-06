





import time,font
from machine import Pin, I2C
from time import sleep
font=font.font
i2c = I2C(scl=Pin(4), sda=Pin(5))
# LCD Control constants
ADDR = 0x3C
# Holds the segments on in each of the four digits
def command(c):
    i2c.writeto(ADDR, b'\x00' + bytearray(c))

def initialize():

    cmd = [
        [0xAE],                    # DISPLAYOFF
        [0xA4],           #显示恢复
        [0xD5, 0xF0],            # 设置显示时钟SETDISPLAYCLOCKDIV
        [0xA8, 0x3F],                  # 设置多重 SETMULTIPLEX
        [0xD3, 0x00],              # 设置显示偏移SETDISPLAYOFFSET
        [0 | 0x0],                   # 设定起始行 SETSTARTLINE
        [0x8D,  0x14],                    # CHARGEPUMP
        [0x20,  0x00],  #  内存模式水平 MEMORYMODE horizontal
        [0x21,  0, 127],  # 列地址 COLUMNADDR
        [0x22,  0, 63],   # 页面地址 PAGEADDR
        [0xa0 | 0x1],  # SEGREMAP
        [0xc8],   #  通讯扫描COMSCANDEC
        [0xDA,  0x12],                    #设置组合 SETCOMPINS
        [0x81,  0xCF],                   #  SETCONTRAST
        [0xd9,  0xF1],                  # SETPRECHARGE
        [0xDB,  0x40],                 # SETVCOMDETECT
        [0xA6],                 # NORMALDISPLAY
        [0xd6, 0],  # zoom off

    ]
    for c in cmd:
        command(c)
    clear()
    command([0xaf])  # SSD1306_DISPLAYON
def set(rect):
  #设置范围 rect[0],rect[1] 从列到几列最大127
  #         rect[2],rect[3] 从行到几行最大7
    command([0x21, rect[0], rect[1]]) 
    command([0x22, rect[2], rect[3]])

def clear(rect=[0, 127, 0, 7]):
    set(rect)
    screen = bytearray(33)
    screen[0] = 0x40
    print (screen)
    for i in range(0, 32):
        i2c.writeto(ADDR, screen)
    #i2c.writeto(ADDR, b'@0\x00\x00\x00\x000')    

def write(b):
  i2c.writeto(ADDR, b)
  # 一个十六进制 控制每一列向下的8个像素  

  
  
def  fillall(s):
  a=1
  while a<100:
    a+=1
    write(s)

def draw(arr,x,y):
    set([x,127,y,7])
    for i in range(0,len(arr)):
        write(arr[i][0])
        y+=1 
        set([x,127,y,7])
 
def display(s):
    
    s=str(s)
    x=0
    draw(font[int(s[0:1])],x,0)
    x+=20
    draw(font[int(s[1:2])],x,0)
    x+=20
    draw(font[10],x,0)
    x+=2
    draw(font[int(s[2:3])],x,0)
    x+=20
    draw(font[int(s[3:4])],x,0)
    x+=20
    draw(font[10],x,0)
    x+=2
    draw(font[int(s[4:5])],x,0)
    x+=20
    draw(font[int(s[5:6])],x,0)
    
    
#test    
while 1:
  sleep(1)
  t=time.localtime()
  print (t) 
  t=str("%02d" % t[3])+str("%02d" % t[4])+str("%02d" % t[5])
  display(t)
