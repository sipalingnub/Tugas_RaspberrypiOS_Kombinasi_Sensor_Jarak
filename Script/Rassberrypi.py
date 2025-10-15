import RPi.GPIO as GPIO
import time

# Gunakan mode penomoran BCM (sesuai nomor GPIO)
GPIO.setmode(GPIO.BCM)

# Tentukan pin
TRIG = 23
ECHO = 24

# Set pin
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

print("Mengukur jarak menggunakan HC-SR04...")
time.sleep(2)

try:
    while True:
        # Pastikan TRIG LOW
        GPIO.output(TRIG, False)
        time.sleep(0.000002)

        # Kirim sinyal 10 mikrodetik
        GPIO.output(TRIG, True)
        time.sleep(0.00001)
        GPIO.output(TRIG, False)

        # Tunggu ECHO HIGH
        while GPIO.input(ECHO) == 0:
            pulse_start = time.time()

        # Tunggu ECHO LOW
        while GPIO.input(ECHO) == 1:
            pulse_end = time.time()

        # Hitung durasi
        pulse_duration = pulse_end - pulse_start

        # Hitung jarak (cm)
        distance = (pulse_duration * 34300) / 2

        print(f"Jarak: {distance:.2f} cm")
        time.sleep(1)

except KeyboardInterrupt:
    print("\nProgram dihentikan oleh pengguna.")
    GPIO.cleanup()
