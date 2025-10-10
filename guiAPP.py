import sys
import time
import numpy as np
import serial
import serial.tools.list_ports
from PyQt5.QtWidgets import (
    QWidget, QGridLayout, QPushButton, QApplication,
    QFileDialog, QProgressBar, QLineEdit
)
from crc import CrcCalculator, Crc8

class guiApp(QWidget):
    def __init__(self):
        super().__init__()

        # GUI layout setup
        grid_layout = QGridLayout()
        self.setLayout(grid_layout)

        # UI elements
        self.button1 = QPushButton("Read .bin app file", self)
        self.button1.clicked.connect(self.open)

        self.button2 = QPushButton("Send file", self)
        self.button2.clicked.connect(self.send)

        self.connectionBTN = QPushButton("Connect", self)
        self.connectionBTN.clicked.connect(self.connection)

        self.pbar = QProgressBar(self)
        self.tbox = QLineEdit(self)

        # Add widgets to layout
        grid_layout.addWidget(self.button1, 0, 0, 1, 3)
        grid_layout.addWidget(self.button2, 2, 0, 1, 3)
        grid_layout.addWidget(self.tbox, 0, 4, 1, 2)
        grid_layout.addWidget(self.pbar, 2, 4, 1, 2)
        grid_layout.addWidget(self.connectionBTN, 1, 0, 1, 6)

        # Window setup
        self.setGeometry(100, 100, 300, 200)
        self.setWindowTitle('Serial BIN Transfer')

        # Serial and data buffers
        self.byteArray = []  # List of packets to send
        self.ports = serial.tools.list_ports.comports()
        self.comOpen = serial.Serial()
        self.packetArray = bytearray()

    def open(self):
        # Open .bin file and prepare packets with CRC
        path = QFileDialog.getOpenFileName(self, "Open a .bin file", "", "bin (*.bin)")
        if not path[0]:
            return

        # Count total bytes
        cnt = sum(1 for _ in open(path[0], 'rb'))
        cnt2 = 0
        cnt3 = 0
        cnt4 = int(np.round(cnt / 240))  # Total number of packets
        self.pbar.setMaximum(cnt4)

        k = []
        calcCRC = CrcCalculator(Crc8.MAXIM_DOW)

        with open(path[0], 'rb') as file:
            for byte in file.read():
                if cnt2 == 0:
                    # Packet header
                    k = [0, 0, cnt3, cnt4, byte]
                    cnt2 += 1
                    cnt3 += 1
                else:
                    k.append(byte)
                    cnt2 += 1

                if cnt2 == 240:
                    # Finalize packet
                    k[1] = 240
                    crc = calcCRC.calculate_checksum(k[4:])
                    k.append(crc)
                    self.byteArray.append(k)
                    print(''.join('{:02x}'.format(x) for x in k), '\n')
                    cnt2 = 0

                # Handle last partial packet
                if cnt3 >= cnt4 and cnt2 == (cnt - len(self.byteArray) * 240):
                    k[3] = cnt3 - 1 if cnt3 > cnt4 else k[3] - 1
                    k[1] = cnt - len(self.byteArray) * 240
                    crc = self.crc8(k[4:])
                    k.append(crc)
                    self.byteArray.append(k)
                    print(''.join('{:02x}'.format(x) for x in k), '\n')
                    cnt2 = 0

        self.tbox.setText("Acquired")

    def send(self):
        if not self.comOpen.is_open:
            print("Not connected")
            return

        print("Sending...")
        pbarCNT = 0

        for k, packet in enumerate(self.byteArray):
            pbarCNT += 1
            for byte in packet:
                self.comOpen.write(byte.to_bytes(1, byteorder='big'))
                time.sleep(0.005)
                self.pbar.setValue(pbarCNT)

                # Simulated response check (placeholder)
                while True:
                    response = 1  # Replace with actual: self.comOpen.read()
                    if response:
                        break
                    else:
                        self.comOpen.write(byte.to_bytes(1, byteorder='big'))

            print(''.join('{:02x}'.format(x) for x in packet))
            print(f"Packet {k}")
            if k == 0:
                time.sleep(5)

    def connection(self):
        # Connect to first available COM port
        self.ports = serial.tools.list_ports.comports()
        if not self.comOpen.is_open and self.ports:
            port_name = self.ports[0].name
            self.comOpen.baudrate = 38400
            self.comOpen.port = port_name
            self.comOpen.bytesize = 8
            self.comOpen.parity = 'N'
            self.comOpen.stopbits = 1
            self.comOpen.timeout = None
            self.comOpen.open()
            print(f"Connected to {port_name}")

    def crc8(self, data):
        # Manual CRC8 calculation (fallback or alternative)
        crc = 0
        for b in data:
            crc ^= b
            for _ in range(8):
                crc = (crc >> 1) ^ 0x8C if crc & 0x1 else crc >> 1
        return crc

if __name__ == '__main__':
    app = QApplication(sys.argv)
    windowExample = guiApp()
    windowExample.show()
    sys.exit(app.exec_())
