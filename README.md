# serial_BIN_file_transfer

This Python GUI application uploads `.bin` firmware files to the STM32F446 bootloader via UART. It is used for in-field firmware updates of the rainwater signal acquisition unit and supports both App1 and App2 flashing.

## 🚀 Features

- PyQt5 GUI with progress bar and status feedback
- Packetization of `.bin` files into 240-byte blocks
- CRC calculation and header insertion
- UART transmission with retry logic
- Compatible with bootloader and RS485 upload test firmware

## 🧠 Technical Highlights

- Uses `serial` module for UART communication
- GUI built with `PyQt5`
- CRC implemented using Maxim-DOW standard
- Packet structure: `[Header][Length][Packet ID][Last Packet ID][Data][CRC]`

## 📁 Project Structure

- `guiAPP.py`: GUI logic and packet handling, Entry point and CRC calculator
- `README.md`: Documentation

## 🔗 Related Projects

- [STM32F446-Bootloader](https://github.com/Vojtese/STM32F446-Bootloader)
- [STM32F446-uploadRS485Test](https://github.com/Vojtese/STM32F446-uploadRS485Test)

## 📜 License

This project is licensed under the GNU General Public License v3.0.
