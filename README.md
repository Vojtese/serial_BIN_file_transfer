# serial_BIN_file_transfer

This Python GUI application allows users to upload `.bin` firmware files to STM32 microcontrollers over a serial (UART) connection. It is designed to work seamlessly with the [STM32F446 Bootloader](https://github.com/Vojtese/STM32F446-Bootloader), enabling easy firmware updates using a graphical interface.

## 🖥️ Features

- Upload `.bin` files to STM32 flash memory via UART
- Select COM port and configure serial parameters (baud rate, parity, stop bits, flow control)
- Automatic reception feedback printed in GUI
- Simple and intuitive interface for testing and deployment
- Compatible with STM32 bootloader IAP protocol

## 📁 Project Structure

- `guiAPP.py`: Main GUI application logic
- `main.py`: Entry point for launching the GUI
- `README.md`: Project documentation

## 🧪 How to Use

1. Connect your STM32 device via USB or serial adapter.
2. Launch the GUI by running `main.py`.
3. Select the `.bin` file you want to upload.
4. Choose the correct COM port and configure serial settings.
5. Click **SEND** to transmit the firmware.
6. Monitor the feedback window for transmission status and response.

## 🔗 Related Repositories

- [STM32F446-Bootloader](https://github.com/Vojtese/STM32F446-Bootloader): Bootloader that receives and flashes the `.bin` file
- [STM32F446-APP1](https://github.com/Vojtese/STM32F446-APP1): Primary application slot
- [STM32F446-APP2](https://github.com/Vojtese/STM32F446-APP2): Secondary application slot
- [STM32F446-SensorTestAndHW](https://github.com/Vojtese/STM32F446-SensorTestAndHW): Sensor and hardware interface testing

## 🛠️ Requirements

- Python 3.x
- `pyserial` library (`pip install pyserial`)
- Compatible STM32 device with bootloader flashed

## 📜 License

This project is licensed under the GNU General Public License v3.0.
