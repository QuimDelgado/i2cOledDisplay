#!/usr/bin/env python3
"""
Mostra una cara com un banner rotatiu al display i2c
"""

import board
import digitalio
import time  # Importar el módulo time
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306
import os

# Asegurarse de que 'oled' se define en un ámbito donde todas las funciones y bloques pueden accederlo
oled = None

def banner_rotativo(frase, image, draw, font, wait, oled):
    for i in range(len(frase)):
        draw.rectangle((0, 0, oled.width, oled.height), outline=0, fill=0)
        segmento = " " * (len(frase) - i) + frase[:i]
        draw.text((0, 0), segmento, font=font, fill=255)
        oled.image(image)
        oled.show()
        time.sleep(wait)

    for i in range(len(frase)):
        draw.rectangle((0, 0, oled.width, oled.height), outline=0, fill=0)
        segmento = frase[i + 1 : len(frase)]
        draw.text((0, 0), segmento, font=font, fill=255)
        oled.image(image)
        oled.show()
        time.sleep(wait)

    time.sleep(2)

def setup_banner():
    global oled  # Utilizar la variable global 'oled'
    ttf_directorio = '/usr/share/fonts/truetype'
    font_size = 35  # Tamaño de la fuentes
    letter_wait = 0.1  # Tiempo de espera entre letras

    i2c = board.I2C()
    oled = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c, addr=0x3c)

    frase = "      :D"

    image = Image.new("1", (oled.width, oled.height))
    draw = ImageDraw.Draw(image)

    while True:
        for dirpath, dirnames, filenames in os.walk(ttf_directorio):
            for filename in filenames:
                if filename.endswith('.ttf'):
                    font_path = os.path.join(dirpath, filename)
                    font = ImageFont.truetype(font_path, font_size)

                    # Pasar 'oled' como argumento a la función
                    banner_rotativo(frase, image, draw, font, letter_wait, oled)

try:
    setup_banner()

except KeyboardInterrupt:
    if oled:  # Comprobar si 'oled' ha sido definido
        oled.fill(0)
        oled.show()

finally:
    if oled:  # Comprobar si 'oled' ha sido definido
        # Limpiar el display al final.
        oled.fill(0)
        oled.show()
