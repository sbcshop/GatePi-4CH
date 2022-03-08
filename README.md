# GatePi
<img src= "https://github.com/sbcshop/GatePi/blob/main/images/img4.png" />

## GatePi is a low-power consumption data transmission board, that comes with an onboard CH340 USB TO UART converter, Voltage Level Translator(74HC125V), E22-400T22S/E22-900T22S SMA antenna connector that covers 433/868/915 MHz frequency band, 4-Ch Relays, IPEX antenna connector, LoRa™ Spread Spectrum Modulation technology with auto multi-level repeating. GatePi is developed to enable data transmission up to 5 KM through the serial port.

## Pin Mapping
<img src= "https://github.com/sbcshop/GatePi/blob/main/images/img1.png" />

## You can control GatePi with the help of raspberry pi GUI, or you can also control through pc via GUI
<img src="https://github.com/sbcshop/GatePi/blob/main/images/img7.JPG" />

## How to start And Setup Lora Home Automation Application
### In Windows
  * Download GatePi directory from Github, and open window application folder, inside this folder you see one application name "Lora Home Automation"
     <img src="https://github.com/sbcshop/GatePi/blob/main/images/imgs7.JPG" />
     <img src="https://github.com/sbcshop/GatePi/blob/main/images/imgs13.JPG" />
     <img src="https://github.com/sbcshop/GatePi/blob/main/images/imgs1.JPG" />
  
  * Run the application, when you run the application you see one folder named "imp" which is automatically generated. this contains your id and password
     <img src="https://github.com/sbcshop/GatePi/blob/main/images/imgs2.JPG" />
  
  * Change the jumperwire to USB-Lora(1),and do not remove jumper wires from M0, M1, then connect device to laptop via USB cable
     <img src="https://github.com/sbcshop/GatePi/blob/main/images/imgs15.JPG" />
     <img src="https://github.com/sbcshop/GatePi/blob/main/images/imgs14.JPG" />
   
  * After USB plugin, open device manager, go to Ports, then see the port number, then port number write in the application
     <img src="https://github.com/sbcshop/GatePi/blob/main/images/imgs3.JPG" />

  * Select the baudrate, and click on connect button
     <img src="https://github.com/sbcshop/GatePi/blob/main/images/imgs4.JPG" />
     <img src="https://github.com/sbcshop/GatePi/blob/main/images/imgs5.JPG" />
   
  * Now you can able to control the GatePi, by pressing the buttons, The configuration of the button is a single button ON/OFF switch. for example when you press button one then relay 1 
    turns on, if you press button 1 again relay 1 turns off. 
     <img src="https://github.com/sbcshop/GatePi/blob/main/images/imgs6.JPG" />
   
  * When you press the "status of relay" button, the button color changes to red, which means these relays are on
     <img src="https://github.com/sbcshop/GatePi/blob/main/images/imgs12.JPG" />
   
  * You can also change the Relay transmission code, which means when you press the button in GUI, then one encoded code or encoded string is sent to the receiver(GatePi). for this, you need to enter the user name and password, at the same time you also need to write the transmission code in the relay 1,2,3,4 entry box. then click on the "Login/Update Relay Code" button.after pressing the button you see that all the entry box is empty or blank , this means encode code is sucessfully change. this is not necessary, the default encode code is there, but you can also change it if you change this, you also need to change in the PICO code   "main.py"
     <img src="https://github.com/sbcshop/GatePi/blob/main/images/imgs8.JPG" />
     <img src="https://github.com/sbcshop/GatePi/blob/main/images/imgs16.JPG" />

  * If you forgot the password, then write user id in user id entry, and write a new password in password entry then click to the "Forgot Password" button.after pressing the button you see that all the entry box is empty or blank , this means password is sucessfully change.
     <img src="https://github.com/sbcshop/GatePi/blob/main/images/imgs8.JPG" />
  
   
## Working
  <img src="https://github.com/sbcshop/GatePi/blob/main/images/giff.gif" />


