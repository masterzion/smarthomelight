import time
import Adafruit_DHT

dhtpin=18


while True:
    sensor2_value_h, sensor2_value_t = Adafruit_DHT.read_retry(Adafruit_DHT.DHT22, dhtpin)
    print sensor2_value_h, sensor2_value_t
    time.sleep(5)
