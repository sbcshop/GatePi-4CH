# GatePi 4Channel
<img src= "https://github.com/sbcshop/GatePi/blob/main/images/img4.png" />

## GatePi is a low-power consumption data transmission board, that comes with an onboard CH340 USB TO UART converter, Voltage Level Translator(74HC125V), E22-400T22S/E22-900T22S SMA antenna connector that covers 433/868/915 MHz frequency band, 4-Ch Relays, IPEX antenna connector, LoRa™ Spread Spectrum Modulation technology with auto multi-level repeating. GatePi is developed to enable data transmission up to 5 KM through the serial port.

## Pin Mapping
<img src= "https://github.com/sbcshop/GatePi/blob/main/images/img1.png" />

## Code
  * You see the "main.py" file. you need to save this file inside GatePi(RP2040)
  * Rest the two folders is of Application(GUI), one is of window other is of raspberry pi
    * Window application->open the app and follow the below instruction, you need to connect one of them Pi Lora Hat or PICO Lora Expansion and RangePi(transmitter)
    * Raspberry pi application->open "raspberry pi GUI" folder.run "Lora Home Automation.py" file, before this, you need to put Pi Lora Hat(transmitter) 
    
## **rangepi__transmitter_app_control.py** - save this code as main in RangePi and connect RangePi to laptop, open application and control GatePi(Only For RangePi)

## You can control GatePi with the help of raspberry pi GUI, or you can also control through pc via GUI
In windows, you can use PICO Lora Expansion, Pi Lora Hat and RangePi
<img src="https://github.com/sbcshop/GatePi/blob/main/images/img7.JPG" />

## GatePi Instruction Manual
   For manual download the GitHub directory GatePi, in this directory you see "GatePi instruction manual.pdf" open that manual
   * In this manual you see:-
      * how to setup GatePi 
      * How to use "LoRa Home Automation Application(App)

     
## Working With GatePi 4Ch

For working with this board you will need two or more than two loara product, it can be same products or may be our other LoRa products to establish the communication between them.

* ***The "main.py" is the reciever example code for controlling 8 relays. This code should be saved in RP2040 of GatePi 8ch so that when it recieve data from transmitter it will operate realys one by one according to data recieved at this end.

* ***The "Transmit.py" file is the code for sending the data for the purpose of controlling relays of GatePi. This code can be saved in any of our LoRa devices(such as RangePi) to send data. It will send "1relay1" at a fix interval of time to operate "relay-1" and so on for other relays, you can replace this by any keywords you want but this should be change in reciever code also.

## Our Other LoRa Products

* GatePi 4Channel*
* GatePi 8channel
* RangePi(USB Dongle)
* LoRA HAT for RPi
* PICO LoRa Expansion

You will simply need to make one device to work as reciever and another one is as a transmitter. So that you can communicate to each other and this can be done with any of our LoRa products mentioned above. For working with our other products please follow the below link:

* GatePi 4Channel* (Itself)
* GatePi 8channel
https://github.com/sbcshop/GatePi-8CH
* RangePi
https://github.com/sbcshop/RangePi
* LoRA HAT for RPi
https://github.com/sbcshop/Lora-HAT-for-Raspberry-Pi
* PICO LoRa Expansion
https://github.com/sbcshop/PICO-LORA-EXPANSION

### Note: Every time you choose the mode of transmit device the transmit code of that device should be run in it and reciever code will always same.Note: Every time you choose the mode of transmit device the transmit code of that device should be run in it and reciever code will always same.

