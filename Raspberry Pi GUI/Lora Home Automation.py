
#! /usr/bin/python3

"""
This file contains GUI code for Configuring of lora home automation
Developed by - SB Components
http://sb-components.co.uk
"""
import logging
import os
from tkinter import font
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import time
import webbrowser
os_name = os.name

if os.name == "posix":
    COMPORT_BASE = "/dev/"
else:
    COMPORT_BASE = ""

#from serial_comm import SerialComm
from time import sleep
import ctypes
import serial

import logging
import threading

from cryptography.fernet import Fernet
key = "Be1PA8snHgb1DS6oaWek62WLE9nxipFw3o3vB4uJ8ZI="  # "secret key" This must be kept secret
cipher_suite = Fernet(key)  # This class provides both encryption and decryption facilities.

ctypes.windll.shcore.SetProcessDpiAwareness(1) # it increase the window clearity
dirName = 'imp'
if not os.path.exists(dirName):
        os.mkdir(dirName)
class SerialComm(object):
    """
    Low level serial operations
    """
    log = logging.getLogger("serial")
    log.addHandler(logging.StreamHandler())
    logging.basicConfig(filename='imp/.log.log', level=logging.DEBUG)

    def __init__(self, handlerNotification=None, *args, **kwargs):
        self.__ser = None

        self.alive = False
        self.timeout = 0.01
        self.rxThread = None
        self.rxData = []
        self._txLock = threading.Lock()
        self.handlerNotification = handlerNotification

    def connect_port(self, port='/dev/ttyS0', baud_rate=115200, timeout=0.5):
        """
        Connects to the Comm Port
        """
        try:
            # open serial port
            self.__ser = serial.Serial(port=port, baudrate=baud_rate,
                                       timeout=timeout)
            self.alive = True
            self.rxThread = threading.Thread(target=self._readLoop)
            self.rxThread.daemon = True
            self.rxThread.start()
            self.log.info("Connected with {} at {} "
                          "baudrate.".format(port, baud_rate))
            return True
        except serial.serialutil.SerialException:
            self.alive = False
            self.log.error("Couldn't connect with {}.".format(port))
            return False

    def disconnect(self):
        """
        Stops read thread, waits for it to exit cleanly and close serial port
        """
        self.alive = False
        if self.rxThread:
            self.rxThread.join()
        self.close_port()
        self.log.info("Serial Port Disconnected")

    def read_port(self, n=1):
        """
        Read n number of bytes from serial port
        :param n: Number of bytes to read
        :return: read bytes
        """
        return self.__ser.read(n)

    def read_line(self):
        return self.__ser.readline()
        # return self.__ser.readall()

    def write_port(self, data):
        """
        :param data: data to send to servo, type: bytearray
        :return: Number of bits sent
        """
        return self.__ser.write(data)

    def close_port(self):
        """
        Check if the port is open.
        Close the Port if open
        """
        if self.__ser and self._connected:
            self.__ser.close()
        self.alive = False

    def flush_input(self):
        self.__ser.reset_input_buffer()

    def flush_output(self):
        self.__ser.reset_output_buffer()

    @property
    def _connected(self):
        if self.__ser:
            return self.__ser.is_open

    @property
    def _waiting(self):
        if self.__ser:
            return self.__ser.inWaiting()

    def _readLoop(self):
        """
        Read thread main loop
        """
        try:
            while self.alive:
                data = self.read_line()
                if data != b'':
                    self.log.info("Serial Response: %s", data)
                    self.rxData.append(data)
                    self.update_rx_data(data)
                    #self.rxData = []

        except serial.SerialException as SE:
            self.log.error("Serial Exception: {}.".format(SE))
            self.close_port()

    def write(self, data):
        """
        Write data to serial port
        """
        with self._txLock:
            self.log.info("Serial Write: {}".format(data))
            self.write_port(data)
            self.flush_input()
            return True

    def update_rx_data(self, data):
        pass

class LoraHat(SerialComm):
    def __init__(self):
        SerialComm.__init__(self)
    def connect_hat(self, port, baud_rate):
        self.connect_port(port=port, baud_rate=baud_rate, timeout=0.5)

    def disconnect_hat(self):
        self.disconnect()

    def transmit_message(self, data):
        self.write(data)

    def set_variables(self):
        pass
    
class MainApp(tk.Tk, LoraHat):
    """
    This is a class for Creating Frames and Buttons for left and top frame
    """
    port = "COM19"
    current_baud = 9600

    def __init__(self, *args, **kwargs):
        global logo, img, xy_pos
        

        tk.Tk.__init__(self, *args, **kwargs)
        LoraHat.__init__(self)

        self.screen_width = tk.Tk.winfo_screenwidth(self)
        self.screen_height = tk.Tk.winfo_screenheight(self)
        self.app_width = 1100
        self.app_height = 650
        self.xpos = (self.screen_width / 2) - (self.app_width / 2)
        self.ypos = (self.screen_height / 2) - (self.app_height / 2)
        xy_pos = self.xpos, self.ypos
        self.relay_text = tk.StringVar()
            
        self.label_font = font.Font(family="Helvetica", size=20)
        self.heading_font = font.Font(family="Helvetica", size=12)

        self.geometry(
            "%dx%d+%d+%d" % (self.app_width, self.app_height, self.xpos,
                             self.ypos))
        if not self.screen_width > self.app_width:
            self.attributes('-fullscreen', True)

        self.title("Lora Home Automation")

        self.config(bg="gray85")

        self.label_font = font.Font(family="Helvetica", size=16)
        self.heading_font = font.Font(family="Helvetica", size=18)
        self.LARGE_FONT = ("Verdana", 14)

        img = tk.PhotoImage(file=path + '/images/smart-home.png')
        logo = tk.PhotoImage(file=path + '/images/sblogo.png')

        self.top_frame_color = "dimgray"
        self.left_frame_color = "gray21"
        self.left_frame_color_1 = "gray30"
        self.middle_frame_color = "gray30"####
        self.middle_frame_color1 = "gray35"####
        self.right_frame_color = "gray24"

        self.top_frame = tk.Frame(self, height=int(self.app_height / 9), bd=2,
                                  width=self.app_width,
                                  bg=self.top_frame_color)
        self.top_frame.pack(side="top", fill="both")

        self.left_frame = tk.Frame(self, width=int(self.app_width / 2.7),
                                   bg=self.left_frame_color)
        self.left_frame.pack(side="left", fill="both", expand="True")
        self.left_frame.pack_propagate()
        
        self.middle_frame1=tk.Frame(self.left_frame,width=400,height=340,bg=self.middle_frame_color1)
        self.middle_frame1.pack(pady=10,padx=10)
        self.middle_frame1.place(x=0,y=0)       
        
        self.middle_frame=tk.Frame(self.left_frame,width=352,height=340,bg=self.middle_frame_color)
        self.middle_frame.pack(pady=10,padx=10)
        self.middle_frame.place(x=400,y=0)
       
        
        self.right_frame = tk.Frame(self, bg=self.right_frame_color)
        self.right_frame.pack(side="right", fill="both", expand=True)
        self.right_frame.propagate(0)

        self.rtx_frame = TransceiverFrame(parent=self.right_frame,controller=self)
        self.rtx_frame.tkraise()
        
        
        #  Top Bar
        tk.Label(self.top_frame, bg="dimgray", fg="ghostwhite",text="LORA HOME AUTOMATION SYSTEM",font=font.Font(family="times new roman", size=35)).place(x=60,y=5)
        tk.Label(self.middle_frame, bg="gray30", fg="ghostwhite",text="Port Configuration",font=font.Font(family="times new roman", size=25)).place(x=20,y=20)
        tk.Label(self.middle_frame1, bg="gray35", fg="ghostwhite",text="Relay",font=font.Font(family="times new roman", size=25)).place(x=130,y=20)
        
        def relay1():
            self.btn1.configure(bg="yellow")
            #lora.write(b'1relay1')#send "1relay1" to other lora
            if self.rtx_frame.controller.alive:
                with open('imp/relay1.txt','rb') as f:
                    new_1 = f.readlines()
                    rel1 = cipher_suite.decrypt(new_1[0])
                    rel1 = rel1.decode("utf-8")
                    rel_1 = rel1.rstrip()
                self.rtx_frame.controller.transmit_message(rel_1.encode("utf-8")+b'\n\r')#rel_1.encode("utf-8")
            else:
                messagebox.showerror("Port Error","Serial port not connected!")
            
            

        def relay2():
            self.btn2.configure(bg="yellow")
            #lora.write(b'2relay2')#send "2relay2" to other lora
            if self.rtx_frame.controller.alive:
                with open('imp/relay2.txt','rb') as f:
                    new_2 = f.readlines()
                    rel2 = cipher_suite.decrypt(new_2[0])
                    rel2 = rel2.decode("utf-8")
                    rel_2 = rel2.rstrip()
                self.rtx_frame.controller.transmit_message(rel_2.encode("utf-8")+b'\n\r')
            else:
                messagebox.showerror("Port Error","Serial port not connected!")
               

        def relay3():
            self.btn3.configure(bg="yellow")
            #lora.write(b'3relay3')#send "3relay3" to other lora
            if self.rtx_frame.controller.alive:
                with open('imp/relay3.txt','rb') as f:
                    new_3 = f.readlines()
                    rel3 = cipher_suite.decrypt(new_3[0])
                    rel3 = rel3.decode("utf-8")
                    rel_3 = rel3.rstrip()
                self.rtx_frame.controller.transmit_message(rel_3.encode("utf-8")+b'\n\r')
            else:
                messagebox.showerror("Port Error","Serial port not connected!")
                
            
        def relay4():
            self.btn4.configure(bg="yellow")
            #lora.write(b'4relay4')#send "4relay4" to other lora
            if self.rtx_frame.controller.alive:
                with open('imp/relay4.txt','rb') as f:
                    new_4 = f.readlines()
                    rel4 = cipher_suite.decrypt(new_4[0])
                    rel4 = rel4.decode("utf-8")
                    rel_4 = rel4.rstrip()
                self.rtx_frame.controller.transmit_message(rel_4.encode("utf-8")+b'\n\r')
            else:
                messagebox.showerror("Port Error","Serial port not connected!")
            

        
        def allRelayON_OFF():
            self.btn5.configure(bg="yellow")
            if self.rtx_frame.controller.alive:
                lst = ['imp/relay1.txt','imp/relay2.txt','imp/relay3.txt','imp/relay4.txt']
                
                for  i in range(len(lst)):
                    with open(lst[i],'rb') as f:
                        new1_1 = f.readlines()
                        rel11 = cipher_suite.decrypt(new1_1[0])
                        rel11 = rel11.decode("utf-8")
                        rel_11 = rel11.rstrip()
                    self.rtx_frame.controller.transmit_message(rel_11.encode("utf-8")+b'\n\r')
                    time.sleep(0.2)
            else:
                messagebox.showerror("Port Error","Serial port not connected!")

        def statusRelay():
            self.btn5.configure(bg="yellow")
            if self.rtx_frame.controller.alive:
                    msg = '12status12' 
                    self.rtx_frame.controller.transmit_message(msg.encode("utf-8")+b'\n\r')
                    time.sleep(0.2)
            else:
                messagebox.showerror("Port Error","Serial port not connected!")
            
        self.btn1=tk.Button(self, text = 'Relay 1',bg='yellow', bd = '10',command = relay1,activebackground='white')
        self.btn1.place(x=50,y=150)

        self.btn2 = tk.Button(self, text = 'Relay 2',bg='yellow', bd = '10',command = relay2,activebackground='white')
        self.btn2.place(x=230,y=150)

        self.btn3 = tk.Button(self, text = 'Relay 3',bg='yellow', bd = '10',command = relay3,activebackground='white') 
        self.btn3.place(x=50,y=250)

        self.btn4 = tk.Button(self, text = 'Relay 4',bg='yellow', bd = '10',command = relay4,activebackground='white') 
        self.btn4.place(x=230,y=250)

        self.btn5 = tk.Button(self, text = 'All Relay ON/OFF',bg='yellow', bd = '10',command = allRelayON_OFF,activebackground='white') 
        self.btn5.place(x=20,y=350)

        self.btn6 = tk.Button(self, text = 'Status Of Relay',bg='yellow', bd = '10',command = statusRelay,activebackground='white') 
        self.btn6.place(x=210,y=350)



        if not os.path.isfile("imp/passd.txt"):
            now = open("imp/passd.txt", "wb")
            user = "admin@123"
            password = "sbcomponents"
            user = cipher_suite.encrypt(bytes(user, encoding='utf-8'))
            password = cipher_suite.encrypt(bytes(password, encoding='utf-8'))  
            
            now.write(user)
            now.write(b'\n')
            now.write(password)
            now.close()
            
        if not os.path.isfile("imp/relay1.txt"):
            now = open("imp/relay1.txt", "wb")
            r1 = "1relay1"
            r1 = cipher_suite.encrypt(bytes(r1, encoding='utf-8'))  
            now.write(r1)
            now.close()
            
        if not os.path.isfile("imp/relay2.txt"):
            now = open("imp/relay2.txt", "wb")
            r2 = "2relay2"
            r2 = cipher_suite.encrypt(bytes(r2, encoding='utf-8'))  
            now.write(r2)
            now.close()

        if not os.path.isfile("imp/relay3.txt"):
            now = open("imp/relay3.txt", "wb")
            r3 = "3relay3"
            r3 = cipher_suite.encrypt(bytes(r3, encoding='utf-8'))  
            now.write(r3)
            now.close()

        if not os.path.isfile("imp/relay4.txt"):
            now = open("imp/relay4.txt", "wb")
            r4 = "4relay4"
            r4= cipher_suite.encrypt(bytes(r4, encoding='utf-8'))  
            now.write(r4)
            now.close()
            
            
        def forgotPassword():
            with open('imp/passd.txt','rb') as f:
                new = f.readlines()
                user_ = cipher_suite.decrypt(new[0])
                user_ = user_.decode("utf-8")
                user_1 = user_.rstrip()

                
            if self.user_entry.get() == user_1:  
                        now = open("imp/passd.txt", "wb")                        
                        pass_1 = self.pass_entry.get()
                        user = cipher_suite.encrypt(bytes(user_1, encoding='utf-8'))
                        password = cipher_suite.encrypt(bytes(pass_1, encoding='utf-8'))
                        
                        now.write(user)
                        now.write(b'\n')
                        now.write(password)
                        now.close()
                        self.user_entry.delete(0, 'end')
                        self.pass_entry.delete(0, 'end')
            else:
                messagebox.showerror("error", "wrong user name")
                self.user_entry.delete(0, 'end')
                self.pass_entry.delete(0, 'end')
            
        def changRelay_code(self):
                self.relay1_var = tk.StringVar()
                self.relay2_var = tk.StringVar()
                self.relay3_var = tk.StringVar()
                self.relay4_var = tk.StringVar()
                
                tk.Label(self, bg="gray21", fg="ghostwhite",text="Relay 1",
                        font=font.Font(family="times new roman", size=20)).place(x=425,y=470)

                tk.Label(self, bg="gray21", fg="ghostwhite",text="Relay 2",
                        font=font.Font(family="times new roman", size=20)).place(x=425,y=510)

                tk.Label(self, bg="gray21", fg="ghostwhite",text="Relay 3",
                        font=font.Font(family="times new roman", size=20)).place(x=425,y=550)

                tk.Label(self, bg="gray21", fg="ghostwhite",text="Relay 4",
                        font=font.Font(family="times new roman", size=20)).place(x=425,y=590)
                

                self.relay1_entry = tk.Entry(self,textvariable = self.relay1_var, font=('calibre',16,'normal'),width=12)
                self.relay1_entry.place(x=550,y=470)

                self.relay2_entry = tk.Entry(self,textvariable = self.relay2_var, font=('calibre',16,'normal'),width=12)
                self.relay2_entry.place(x=550,y=508)

                self.relay3_entry = tk.Entry(self,textvariable = self.relay3_var, font=('calibre',16,'normal'),width=12)
                self.relay3_entry.place(x=550,y=547)

                self.relay4_entry = tk.Entry(self,textvariable = self.relay4_var, font=('calibre',16,'normal'),width=12)
                self.relay4_entry.place(x=550,y=585)

                
        changRelay_code(self)



        def login_in():
            with open('imp/passd.txt','rb') as f:
                new = f.readlines()
                user_ = cipher_suite.decrypt(new[0])
                user_ = user_.decode("utf-8")
                user_1 = user_.rstrip()

                pass_ = cipher_suite.decrypt(new[1])
                pass_ = pass_.decode("utf-8")
                pass_1 = pass_.rstrip()
                
            if self.user_entry.get() == user_1 and self.pass_entry.get() == pass_1:
                def save_relay_code(): 
                            d1 = self.relay1_entry.get()
                            d2 = self.relay2_entry.get()
                            d3 = self.relay3_entry.get()
                            d4 = self.relay4_entry.get()
        
                            if len(d1)>0:
                                now1 = open("imp/relay1.txt", "wb")
                                data1 = self.relay1_entry.get()
                                data1 = cipher_suite.encrypt(bytes(data1, encoding='utf-8'))
                                now1.write(data1)
                                now1.close()
                            
                                                      
                            if len(d2)>0:
                                now2 = open("imp/relay2.txt", "wb")
                                data2 = self.relay2_entry.get()
                                data2 = cipher_suite.encrypt(bytes(data2, encoding='utf-8'))
                                now2.write(data2)
                                now2.close()

                                                      
                            if len(d3)>0:
                                now3 = open("imp/relay3.txt", "wb")
                                data3 = self.relay3_entry.get()
                                data3 = cipher_suite.encrypt(bytes(data3, encoding='utf-8'))
                                now3.write(data3)
                                now3.close()

                                                       
                            if len(d4)>0:
                                now4 = open("imp/relay4.txt", "wb")
                                data4 = self.relay4_entry.get()
                                data4 = cipher_suite.encrypt(bytes(data4, encoding='utf-8'))
                                now4.write(data4)
                                now4.close()

                            self.relay1_entry.delete(0, 'end')
                            self.relay2_entry.delete(0, 'end')
                            self.relay3_entry.delete(0, 'end')
                            self.relay4_entry.delete(0, 'end')
                save_relay_code()
                self.user_entry.delete(0, 'end')
                self.pass_entry.delete(0, 'end')
            else:
                messagebox.showerror("error", "login Failed")
                self.relay1_entry.delete(0, 'end')
                self.relay2_entry.delete(0, 'end')
                self.relay3_entry.delete(0, 'end')
                self.relay4_entry.delete(0, 'end')



        self.large_font = ('times new roman', 22)
        self.small_font = ('times new roman', 10)
        self.user = tk.StringVar()
        self.password = tk.StringVar()

        tk.Label(self, bg="gray21", fg="ghostwhite",text="Relay Code Configuration",
                        font=font.Font(family="times new roman", size=22)).place(x=205,y=415)
        
        tk.Label(self, bg="gray21", fg="ghostwhite",text="User",
                        font=font.Font(family="times new roman", size=20)).place(x=15,y=470)

        tk.Label(self, bg="gray21", fg="ghostwhite",text="Password",
                        font=font.Font(family="times new roman", size=20)).place(x=15,y=510)
                
        self.user_entry = tk.Entry(self,textvariable = self.user, font=('calibre',16,'normal'),width=15)
        self.user_entry.place(x=150,y=470)
        
        self.pass_entry = tk.Entry(self,textvariable = self.password, font=('calibre',16,'normal'),width=15,show='*')
        self.pass_entry.place(x=150,y=510)
        
        self.btn7 = tk.Button(self, text = 'Login / Update Relay Code',bg='yellow', bd = '8',command = login_in,activebackground='white') 
        self.btn7.place(x=150,y=550)

        self.btn8 = tk.Button(self, text = 'Forgot Password',bg='yellow', bd = '6',command = forgotPassword,activebackground='white') 
        self.btn8.place(x=150,y=600)
        
        self.left_frame_contents()

    def left_frame_contents(self):
        """
        This function creates the left frame widgets
        """
        global logo
        x_ref, y_ref = 10, 20
        font_ = font.Font(family="Helvetica", size=11)

        self.baud_var = tk.StringVar()


        self._com_port = tk.StringVar()
        self._set_baud_rate_var = tk.IntVar()

        self.baud_var.set("9600")

        self._com_port.set(self.port)
        self._set_baud_rate_var.set(self.current_baud)



        self.baud_options = ["1200", "2400", "4800", "9600", "19200", "38400",
                             "57600", "115200"]
        self._set_baud_rate_options = [1200, 2400, 4800, 9600, 19200, 38400,
                                       57600, 115200]


        tk.Label(self.left_frame, fg="white", bg=self.left_frame_color_1,font=self.LARGE_FONT, text="Port").place(x=x_ref + 450,y=y_ref + 120)
        self.com_entry = tk.Entry(self.left_frame, fg="black",font=self.label_font, width=8,textvariable=self._com_port)
        self.com_entry.place(x=x_ref + 580, y=y_ref + 120)

        tk.Label(self.left_frame, fg="white", bg=self.left_frame_color_1,font=self.LARGE_FONT, text="Baudrate").place(x=x_ref + 450,y=y_ref + 160)

        tk.OptionMenu(self.left_frame, self._set_baud_rate_var,*self._set_baud_rate_options).place(x=x_ref + 580,y=y_ref + 160,width=105,height=30)
        self.connect_button = tk.Button(self.left_frame, text="Connect",fg="white", bg=self.left_frame_color,font=self.LARGE_FONT, width=9,bd=4,
                                       highlightthickness=0,command=self.connect_lora_hat)
        
                                  
        self.connect_button.place(x=x_ref + 450, y=y_ref + 200)

        self.circle = tk.Canvas(self.left_frame, height=30, width=30,
                                bg=self.left_frame_color_1, bd=0,
                                highlightthickness=0)
        self.indication = self.circle.create_oval(5, 5, 30, 30, fill="red")
        self.circle.place(x=x_ref + 600, y=y_ref + 200)

    def set_variables(self):
        self._baud_rate = self.baud_options.index(self.baud_var.get())


    def get_values(self, data):
        self.baud_var.set(self.baud_options[data[6] >> 5])
        
    def connect_lora_hat(self):
        """
        This function connects the serial port
        """
        if self.connect_button.cget(
                'text') == 'Connect' and self._com_port.get():
            self.connect_hat(port=COMPORT_BASE + self._com_port.get(),
                             baud_rate=self._set_baud_rate_var.get())
            if self.alive:
                self.connect_button.config(relief="sunken", text="Disconnect")
                self.circle.itemconfigure(self.indication, fill="green3")
                self.com_entry.config(state="readonly")
            else:
                messagebox.showerror("Port Error",
                                     "Couldn't Connect with {} ".format(self._com_port.get(), self._set_baud_rate_var.get()))

        elif self.connect_button.cget('text') == 'Disconnect':
            self.connect_button.config(relief="raised", text="Connect")
            self.circle.itemconfigure(self.indication, fill="red")
            self.com_entry.config(state="normal")
            self.disconnect_hat()

    def update_rx_data(self, data):
        try:
                data = data.decode("utf-8")
                self.rtx_frame.rx_text.set(data + "\n")
                relay_1 = data[0]
                relay_2 = data[1]
                relay_3 = data[2]
                relay_4 = data[3]
                
                if relay_1 == '0': 
                    self.btn1.configure(bg="yellow")

                if relay_2 == '0':
                    self.btn2.configure(bg="yellow")

                if relay_3 == '0':
                    self.btn3.configure(bg="yellow")

                if relay_4 == '0':
                    self.btn4.configure(bg="yellow")

                if relay_1 == '1':
                    self.btn1.configure(bg="red")

                if relay_2 == '1':
                    self.btn2.configure(bg="red")

                if relay_3 == '1':
                    self.btn3.configure(bg="red")

                if relay_4 == '1':
                    self.btn4.configure(bg="red")
                       
                self.rxData = []
        except:
            pass
    


class TransceiverFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.LARGE_FONT = self.controller.LARGE_FONT
        self.bg_color = self.controller.right_frame_color
    
        #self.talk_var = tk.IntVar()
        #self.talk_var.set(0)
        self.rx_text = tk.StringVar()

        logo = tk.PhotoImage(file=path + '/images/sblogo.png')
        url = "https://shop.sb-components.co.uk/"
        LabelButton(parent, url=url, image=logo,height=85,width = 300,
                    bg="white", x_pos=20, y_pos=50)

        
        # Receiver Label Box
        self.rx_label = tk.Label(parent, justify="left", anchor="nw",
                                 wraplength=270,
                                 bg="gray80", fg="red",
                                 bd=2, height=4, width=37, padx=10, pady=10,
                                 textvariable=self.rx_text)
        self.rx_label.place(x=10, y=210)

        tk.Label(parent, fg="white", bg=self.bg_color, font=font.Font(
            family="Helvetica", size=15), text="Rx Message").place(x=10, y=175)

        # Transmitter Text Box
        self.tx_text = tk.Text(parent, padx=10, pady=
                               10, bg="gray80",
                               fg="red", height=4, width=30,
                               wrap="word",
                               relief="sunken", state="normal")
        self.tx_text.place(x=10, y=370)
        tk.Label(parent, fg="white", bg=self.bg_color, font=font.Font(family="Helvetica", size=15), text="Tx Message").place(x=10,y=335)

        self.send_button = tk.Button(parent, text='Send',
                                     fg="white", bg="gray30", relief="raised",
                                     font=self.LARGE_FONT, bd=4,
                                     highlightthickness=0, width=10,
                                     command=self.send_msg)
        self.send_button.place(x=10, y=478)
      
    def send_msg(self):
        if self.controller.alive:
            msg = self.tx_text.get("1.0", "end")
            self.controller.transmit_message(msg.encode("utf-8")+b'\n\r')
        else:
            messagebox.showerror("Port Error",
                                 "Serial port not connected!")


class LabelButton(object):
    def __init__(self, master, image=None, height=40, width=250, bg="white",
                 url=None, x_pos=7, y_pos=700):
        global logo
        # if image is None:
        image = logo
        self.url = url
        self.label = tk.Label(master, image=logo, height=height,
                              width=width, bg=bg)
        self.label.place(x=x_pos, y=y_pos)
        self.label.bind("<Button-1>", self.open_url)

    def open_url(self, tmp):
        webbrowser.open(self.url, new=1)


logo = None
img = None
path = os.path.abspath(os.path.dirname(__file__))
logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.DEBUG)

if __name__ == "__main__":
    app = MainApp()
    app.tk.call('wm', 'iconphoto', app._w, img)
    app.resizable(0, 0)
    app.mainloop()
