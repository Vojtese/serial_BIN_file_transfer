
import sys
from PyQt5.QtWidgets import (QWidget, QGridLayout,QPushButton, QApplication, QFileDialog, QProgressBar, QLineEdit)
import numpy as np
import serial.tools.list_ports
import serial
import time
from crc import CrcCalculator, Crc8

class guiApp(QWidget):
    def __init__(self):
        super().__init__()
        grid_layout = QGridLayout()
        self.setLayout(grid_layout)

        self.button1 = QPushButton("Read .bin app file", self)
        self.button1.clicked.connect(self.open)
        self.button2 = QPushButton("Send file", self)
        self.button2.clicked.connect(self.send)
        self.connectionBTN = QPushButton("Connect",self)
        self.connectionBTN.clicked.connect(self.connection)
        self.pbar = QProgressBar(self)
        self.tbox = QLineEdit(self)
        grid_layout.addWidget(self.button1, 0, 0, 1, 3)
        grid_layout.addWidget(self.button2, 2, 0, 1, 3)
        grid_layout.addWidget(self.tbox, 0, 4, 1, 2)
        grid_layout.addWidget(self.pbar, 2, 4, 1, 2)
        grid_layout.addWidget(self.connectionBTN, 1, 0, 1, 6)

        self.setGeometry(100, 100, 300, 200)

        self.byteArray = []
        self.setWindowTitle('Basic Grid Layout')
        self.ports = serial.tools.list_ports.comports()
        self.comOpen = serial.Serial()
        self.packetArray = bytearray()
    def open(self):
        path = QFileDialog.getOpenFileName(self, "Open a .bin file", "", "bin (*.bin)")
        cnt = 0
        i = 0
        with open(path[0], 'rb') as f:
            b = f.read(1).hex()
            while b != b'':
                b = f.read(1)
                cnt += 1
        num_lines = sum(1 for line in open(path[0],'rb'))
        cnt2 = 0
        cnt3 = 0
        cnt4 = int(np.round(cnt/240))
        self.pbar.maximum = cnt4
        k = []
        calcCRC = CrcCalculator(Crc8.MAXIM_DOW)
        with open(path[0], 'rb') as file:
            for byte in file.read():
                if cnt2 == 0:
                    k.append(0)     # Header
                    k.append(0)     # Data length
                    k.append(cnt3)  # packet number
                    k.append(cnt4)  # last packet number
                    k.append(byte)
                    cnt2 += 1
                    cnt3 += 1
                else:
                    k.append(byte)
                    cnt2 += 1
                if cnt2 == 240:
                    k[1] = 240     # Data length
                    crc = calcCRC.calculate_checksum(k[4:len(k)])
                    k.append(crc)
                    #k.append(1)
                    self.byteArray.append(k)
                    print(''.join('{:02x}'.format(x) for x in k))
                    print('\n')
                    k = []
                    cnt2 = 0
                if cnt3 >= cnt4:
                    if cnt2 == (cnt - len(self.byteArray)*240):
                        if cnt3 > cnt4:
                            k[3] = cnt3 - 1
                        else:
                            k[3] -= 1
                        k[1] = (cnt - len(self.byteArray)*240)     # Data length
                        crc = calcCRC.calculate_checksum(k[4:len(k)])
                        crc = self.crc8(k[4:len(k)])
                        k.append(crc)
                        #k.append(1)
                        self.byteArray.append(k)
                        print(''.join('{:02x}'.format(x) for x in k))
                        print('\n')
                        k = []
                        #self.byteArray = []
                        cnt2 = 0
                    if cnt2 == (cnt - 14*210-20):
                        print("sds")      
        #for i in range(len(self.byteArray)):
            
        self.tbox.setText("Acquired")
    def send(self):
        if self.comOpen.is_open:
            print("sending ....")
            s = self.byteArray[0]
            c = 0
            pbarCNT = 0
            print(s)
            for k in range(len(self.byteArray)):
                pbarCNT += 1
                for i in range(len(self.byteArray[k])):
                    self.comOpen.write(self.byteArray[k][i].to_bytes(1, byteorder='big'))
                    time.sleep(0.005)
                    self.pbar.setValue(pbarCNT)
                    while True:
                        response = 1#self.comOpen.read()
                        #time.sleep(0.0001)
                        #print(response)
                        if response:
                            c += 1
                        #    #print(c)
                            break
                        else:
                            self.comOpen.write(self.byteArray[k][i].to_bytes(1, byteorder='big'))
                    # a = self.comOpen.read_all().decode("ascii")
                print(''.join('{:02x}'.format(x) for x in self.byteArray[k]))
                print(k)
                if k ==0:
                    time.sleep(5)
                
                #time.sleep(0.5)
                c = 0
            #print("a")           
        else:
            print("Not connected")
    def connection(self):
        self.ports = serial.tools.list_ports.comports()
        if not self.comOpen.is_open:
            if self.ports[0].name:
                self.comOpen.baudrate=38400
                self.comOpen.port=self.ports[0].name
                self.comOpen.bytesize=8
                self.comOpen.parity='N'
                self.comOpen.stopbits=1
                self.comOpen.timeout=None
                self.comOpen.open()
        else:
            pass
    def crc8(self, data):
        crc = 0
        for b in data:
            crc ^= b
            for i in range(8):
                if crc & 0x1:
                    crc = (crc >> 1) ^ 0x8C
                else:
                    crc >>= 1
        return crc


if __name__ == '__main__':
    app = QApplication(sys.argv)
    windowExample = guiApp()
    windowExample.show()
    sys.exit(app.exec_())

