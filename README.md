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

git clone https://github.com/YOUR_USERNAME/ShadowHunter.git

cd ShadowHunter

Install dependencies:

Bashpip install -r requirements.txt

Open  and update these values:

PythonEMAIL_ADDRESS = "your_email@gmail.com"

EMAIL_PASSWORD = "your_16_char_app_password"

RECIPIENT_EMAIL = "your_email@gmail.com"


Run the tool:

Bashpython shadowhunter.py

Creating Executable (.exe)

Bash

pip install pyinstaller

pyinstaller --onefile --noconsole --name "WindowsHostService" shadowhunter.py

The .exe will be generated in the dist folder.

How to Stop the Tool

Open Task Manager → Details tab → End WindowsHostService.exe

Or restart the computer


Disclaimer

This project is created only for educational and demonstration purposes as part of academic learning.
The developer is not responsible for any misuse of this tool.
Always obtain proper authorization before testing monitoring tools.
