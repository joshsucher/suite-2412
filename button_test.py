import digitalio
import board
import subprocess
import time
import os
from adafruit_debouncer import Debouncer

# Setup code for your buttons
pinA = digitalio.DigitalInOut(board.D23)
pinB = digitalio.DigitalInOut(board.D24)
lightPin = digitalio.DigitalInOut(board.D12)
pinA.switch_to_input()
pinB.switch_to_input()
lightPin.switch_to_output()

buttonA = Debouncer(pinA)
buttonB = Debouncer(pinB)

current_video_process = None
current_eink_process = None
video_index = -1
sound_on = False
videos = ["cassette-centralq-louder.mp4", "cassette-blumberg-louder.mp4", "cassette-real-estate-louder.mp4", "cassette-lien-louder.mp4"]
    
def start_video_process(command):
    global current_video_process
    if current_video_process:
        os.system("sudo pkill -f mplayer")
        time.sleep(0.5)
    current_video_process = subprocess.Popen(command, shell=True)

def start_eink_process(command):
    global current_eink_process
    if current_eink_process:
        os.system("sudo pkill -f einktest102.py")
        time.sleep(0.5)
    current_eink_process = subprocess.Popen(command, shell=True)

def play_toasters():
    global current_eink_process
    global sound_on

    lightPin.value = True

    if sound_on:
        start_video_process(f"sudo SDL_VIDEODRIVER=fbcon SDL_FBDEV=/dev/fb0 mplayer -vo sdl -framedrop -volume 30 toasters-asmr.mp4 -loop 0")
    else:  
        start_video_process(f"sudo SDL_VIDEODRIVER=fbcon SDL_FBDEV=/dev/fb0 mplayer -vo sdl -framedrop toasters240.mp4 -loop 0")
    
    if current_eink_process is not None:
        time.sleep(5)
        os.system("sudo pkill -f einktest102.py")
        time.sleep(0.5)
        start_eink_process(f"sudo python ~/e-Paper/RaspberryPi_JetsonNano/python/examples/eink102sleepytime.py")
        current_eink_process.wait()
        current_eink_process = None

def play_dictation():
    global video_index
    global current_video_process
    global current_eink_process
    
    if current_video_process:
        os.system("sudo pkill -f mplayer")
        time.sleep(0.5)
        #current_video_process.wait()
        current_video_process = None
    
    if current_eink_process:
        os.system("sudo pkill -f einktest102.py")
        time.sleep(0.5)
    
    video_file = videos[video_index]
    start_video_process(f"sudo SDL_VIDEODRIVER=fbcon SDL_FBDEV=/dev/fb0 mplayer -vo sdl -framedrop -volume 70 {video_file}")
    time.sleep(8)  # Optional: add delay if needed between video and e-ink command
    
    start_eink_process(f"sudo python ~/e-Paper/RaspberryPi_JetsonNano/python/examples/einktest102.py {video_index}")

#     # Wait for the video to finish        
#     if current_video_process is not None:
#         current_video_process.wait()
#         current_video_process = None  # Reset the current_video_process to None
#         
#     play_toasters()
# 
#     if current_eink_process is not None:
#         current_eink_process.wait()
#         current_eink_process = None  # Reset the current_video_process to None

def play_vhs():
    global current_video_process
    global current_eink_process
    
    if current_video_process:
        os.system("sudo pkill -f mplayer")
        time.sleep(0.5)
        #current_video_process.wait()
        current_video_process = None

    if current_eink_process:
        os.system("sudo pkill -f einktest102.py")
        time.sleep(0.5)

    start_video_process(f"sudo SDL_VIDEODRIVER=fbcon SDL_FBDEV=/dev/fb0 mplayer -vo sdl -framedrop -volume 60 1990_mts_240_2.mp4")    
    
    start_eink_process(f"sudo python ~/e-Paper/RaspberryPi_JetsonNano/python/examples/eink102sleepytime.py")

#     # Wait for the video to finish        
#     if current_video_process is not None:
#         current_video_process.wait()
#         current_video_process = None  # Reset the current_video_process to None    

play_toasters()

# Main loop:
try:

    while True:
    
        buttonA.update()
        buttonB.update()

        if not pinA.value and not pinB.value:  # both pressed
            play_vhs()
        elif buttonB.fell:  # Button B pressed
            video_index = (video_index + 1) % len(videos)  # Cycle to the next video
            play_dictation()
        elif buttonA.fell:  # Button A pressed
            sound_on = not sound_on
            play_toasters()
            
        # Check if the current video process has ended
        if current_video_process is not None and current_video_process.poll() is not None:
            # The process has ended
            current_video_process = None
            play_toasters()

        # Check if the current video process has ended
        if current_eink_process is not None and current_eink_process.poll() is not None:
            # The process has ended
            current_eink_process = None
            
except KeyboardInterrupt:
    print("Script terminated by user")
    # Clean up any resources or subprocesses here before exiting
    #os.system("sudo pkill -f mplayer")
    current_video_process.terminate()
    start_eink_process(f"sudo python ~/e-Paper/RaspberryPi_JetsonNano/python/examples/eink102sleepytime.py")
    lightPin.value = False
    # Optional: Additional cleanup actions
finally:
    # This block will always be executed, even if an exception occurs
    print("Exiting script...")
