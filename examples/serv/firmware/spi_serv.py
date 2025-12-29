from machine import Pin, SPI
import time

PIN_MISO = 0
PIN_CS   = 1
PIN_SCK  = 2
PIN_MOSI = 3

PIN_FPGA_EN  = 13
PIN_FPGA_PWR = 12

SPI_BAUD = 1_000_000  # 1 MHz
spi = SPI(
    0,
    baudrate=SPI_BAUD,
    polarity=0,
    phase=0,
    bits=8,
    firstbit=SPI.MSB,
    sck=Pin(PIN_SCK),
    mosi=Pin(PIN_MOSI),
    miso=Pin(PIN_MISO),
)

cs = Pin(PIN_CS, Pin.OUT, value=1)
en = Pin(PIN_FPGA_EN, Pin.OUT, value=0)
pwr = Pin(PIN_FPGA_PWR, Pin.OUT, value=1)

def cs_low():
    cs.value(0)

def cs_high():
    cs.value(1)

def send_u32_be(w):
    # 32-bit word
    spi.write(bytes([
        (w >> 24) & 0xFF,
        (w >> 16) & 0xFF,
        (w >>  8) & 0xFF,
        (w >>  0) & 0xFF,
    ]))

def fpga_load(words):
    # Hold FPGA/SERV in reset/disabled while loading
    en.value(0)
    time.sleep_ms(5)

    cs_low()
    time.sleep_us(5)

    for w in words:
        send_u32_be(w)

    cs_high()           # CS rising edge = done 
    time.sleep_ms(1)
    en.value(1)         # release reset

prog = [0x0000006F]

print("Loading...")
fpga_load(prog)
print("Done. SERV should be running now.")

