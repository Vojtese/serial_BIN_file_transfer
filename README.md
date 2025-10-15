# serial_BIN_file_transfer

This Python GUI application uploads `.bin` firmware files to the STM32F446 bootloader via UART. It is used for in-field firmware updates of the rainwater signal acquisition unit.

## 🚀 Features

- PyQt5 GUI for user interaction
- Packetization with CRC and headers
- UART transmission with retry logic
- Progress bar and feedback window
- Compatible with bootloader and RS485 test firmware

## 📁 Project Structure

- `guiAPP.py`: GUI logic and packet handling
- `main.py`: Entry point
- `README.md`: Documentation

## 🔗 Related Projects

- [STM32F446-Bootloader](https://github.com/Vojtese/STM32F446-Bootloader)
- [STM32F446-uploadRS485Test](https://github.com/Vojtese/STM32F446-uploadRS485Test)

## 📜 License

This project is licensed under the GNU General Public License v3.0.
