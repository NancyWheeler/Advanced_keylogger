# Advanced_keylogger
A python keylogger with features like recording audio, taking screenshots, retrieving system information, etc.


## Features

- Keylogging
- Audio Recording
- Screenshots of set number of monitors
- Encryption (& decryption) of log files gathered using Ferenet (symmertic encryption)
- Gethering of system information including:
  - Hostname
  - Internal IP
  - External IP
  - Processor
  - System Version
  - Version Information
  - Machine Information

 
## Libraries Utilized

- pynput - Keyloggin
- scipy - Audio file creation
- sounddevice - Audio recording
- requests - HTTP GET requests
- mss - Screenshots
- cryptography.fernet - Encryption/Decryption
