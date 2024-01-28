# Suite 2412
 Mini TFT & e-ink code to drive a book nook miniature of my dad's office

 Components used:

 - Raspberry Pi Zero W 2
 - Adafruit 4393 1.14" 135x240 Mini PiTFT Display
 - Waveshare 17575 128x80 1.02" E-ink Display
 - Adafruit 3885 STEMMA Speaker & Amplifier

 This code turns on the LEDs, plays a looping video file, and then swaps videos when certain buttons are pressed on the PiTFT. It also prints lines of text on the e-ink screen (set up in the miniature to resemble a sheet of paper in an old typewriter).

 SPI1 must be enabled to drive the e-ink display. Some buttons have been remapped in the Waveshare e-ink library's config file.

 Full blog post here: https://thingswemake.com/suite-2412/

 Video demo: https://youtube.com/shorts/BGXuU4g5b6Y