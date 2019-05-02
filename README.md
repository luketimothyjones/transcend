# Transcend
#### Make communicating between Unity and IoT devices easy and extensible for both you and your players

&nbsp;

### Preface

This repository contains what could be considered two different projects, as it was part of my (in retrospect) rather ambitious senior project.

The first part is server software and flashing utilities for an [ESP8266 microcontroller](https://en.wikipedia.org/wiki/ESP8266) running [MicroPython firmware](https://micropython.org/), which corresponded with a real-world device that I made (converted an IR-controlled lightbulb into an IoT lightbulb by controlling the transistors directly using the aforementioned server software and an ESP-12E). This can be found in [/Hardware/](/Hardware/).

The second part consists of two things:

1) Python middleware (hereafter referred to as the "broker") that uses a standardized module format to handle communicating between Unity and arbitrary IoT devices. Provided the Unity developer provides a consistent and well-documented API, custom modules for linking physical IoT devices with the in-game objects that the Unity developer exposes should be very easy to develop. This can be found in [/Unity/Source/transcend-broker/](/Unity/Source/transcend-broker/).

2) Unity scripts that communicate with the broker and control the in-game side of things. The scripts are a little hobbled together, as they were the last part of the project that I tackled and I was running out of time, but they serve as a decent functional reference. This can be found in [/Unity/Source/Senior-Project/Assets/Scripts/](/Unity/Source/Senior-Project/Assets/Scripts/), namely [TranscendObject.cs](/Unity/Source/Senior-Project/Assets/Scripts/TranscendObject.cs) and [TranscendTrigger.cs](/Unity/Source/Senior-Project/Assets/Scripts/TranscendTrigger.cs).

&nbsp;

It is worth noting that this project was developed on Windows and, as such, the scripts that are provided to automate ESP8266-related tasks (such as flashing code, firmware, and doing automated bug-fixing/quirkiness workarounds) are batch files, and the provided copy of [Adafruit's Ampy](https://github.com/pycampers/ampy) is a Windows executable. With that said, it would be quite trivial to convert the batch files to shell scripts, and Ampy is available for all platforms via `pip`.

&nbsp;

### Building and running the demo game

1) Install Unity 5.5.2f1 [(Windows 64-bit installer download)](https://unity3d.com/get-unity/download?thank-you=update&download_nid=45968&os=Win). If you already have a newer version of Unity installed, you can try and open the project, but the project importer may break things when it tries to upgrade the project.

2) Clone this repository and open `/Unity/Source/Senior-Project/` as the project folder

3) Set the build destination to `/Unity/Build/`

4) Set the platform to `Windows` (x86\_64, because who runs 32-bit anymore?)

5) Set the output file to `transcend_demo` and press Build

6) Run `/Unity/Source/finalize-build.bat`

7) Run `/Unity/Build/open-config.bat` and configure your networked devices

8) Run `/Unity/Build/run-broker.bat`

9) Run `/Unity/Build/transcend_demo.exe`

&nbsp;

### Getting started with the ESP8266

I highly recommend grabbing a copy of [Kolban's ESP8266 guide](http://neilkolban.com/tech/esp8266/). It's available for free, but hopefully you'll be persuaded to buy Kolban a well-deserved coffee once you have seen how incredible it is.

&nbsp;

### Adding new device modules

1) Refer to [basedevice.py](/Unity/Source/transcend-broker/user_modules/basedevice.py) and [BasicRGBLight.py](/Unity/Source/transcend-broker/user_modules/BasicRGBLight.py) for implementing the Python module

2) Add your new device module to `/Unity/Build/transcend_demo_Data/transcend-broker/user_modules/`

3) Add your device configuration to `/Unity/Build/transcend_demo_Data/transcend-broker/config/devices.cfg` by following the documentation at the top of said file

The broker will automatically import your module when it is first run. If you update the module while the broker is running, you will need to restart the broker. The game does not need to be restarted, as it exists independently from the broker.

&nbsp;

### Files and descriptions

[/Hardware/Lightbulb/](/Hardware/Lightbulb/)

  - `boot.py`    -  Empty; silences MicroPython complaint

  - `helpers.py`    -  System helper functions

  - `light.py`    -  LED commands &amp; data processing

  - `main.py`    -  Device boot handler

  - `responder.py`    -  Connection handling

  - `server.py`    -  Server initialization &amp; main loop

   - [/Hardware/Lightbulb/config/](/Hardware/Lightbulb/config/)

     - `hw_config.py`   -  WiFi setup, LED pin assignment

     - `server_config.py`  -  IP and port, HTTP responses

     - `server_debug.py`  -  Serial printing &amp; IP flashing

     - `wifi_config.py`   -  SSID connection info

  - [/Hardware/Lightbulb/send_scripts/](/Hardware/Lightbulb/send_scripts/)

     - `run-script.bat`   -  Script runner (see doc. below)

    - [/Hardware/Lightbulb/send_scripts/scripts/](/Hardware/Lightbulb/send_scripts/scripts)   -  See documentation at bottom of this file

  - [/Hardware/Lightbulb/stubs/](/Hardware/Lightbulb/stubs)     -  Stub modules for PC-side server testing (mocks for ESP8266-specific libraries)

  - [/Hardware/Lightbulb/tests/](/Hardware/Lightbulb/tests)     -  Tests for the lightbulb

&nbsp;

[/Unity/Source/](/Unity/Source)

  - `finalize-build.bat`   -  Copy UX-scripts to game build folder
  
  - [/Unity/Source/UX-scripts/](/Unity/Source/UX-scripts)    -  Scripts to simplify configuration

  - [/Unity/Source/transcend-broker/](/Unity/Source/transcend-broker)

    - `run-broker.bat` -  Run the broker (using a portable Python install [/Unity/Source/transcend-broker/broker/venv/](/Unity/Source/transcend-broker/broker/venv/)

  - [/Unity/Source/transcend-broker/config/](/Unity/Source/transcend-broker/config)

    - `device.cfg` -  Device connection information

    - `transcend.cfg` -  Broker <--> Unity communication settings

  - [/Unity/Source/transcend-broker/broker/](/Unity/Source/transcend-broker/broker)

    - `transcend-broker.py`   -  Broker

  - [user\_modules](/Unity/Source/transcend-broker/user_modules)/

    - `basedevice.py`  -  TranscendDevice superclass

    - `BasicRGBLight.py` -  Subclass for our lightbulb

  - [/Unity/Source/Senior-Project/Assets/Scripts/](/Unity/Source/Senior-Project/Assets/Scripts)

    - `BasicPlayerController.cs` -  Player mouse movement

    - `Crosshair.cs`   -  Crosshair manager

    - `MouseKiller.cs`  -  Mouse hider

    - `TranscendObject.cs`  -  Game object <--> device module (via broker)

    - `TranscendTrigger.cs`  -  Game object input handler

&nbsp;

### Send scripts documentation

**WARNING:** Flashing files without removing `main.py` from the microcontroller first ***MAY RESULT IN THE CURRUPTION OF THE MICROCONTROLLER'S FILESYSTEM.***

**BEFORE FLASHING:** While `run-script.bat` attempts to fix this issue, it is best to connect to the REPL and make sure that the file has been deleted. This can be done in one line: import os; os.remove("main.py")

**IF YOU IGNORE THIS:** Oops. Running `all` as per below; will fix the filesystem and restore the files. Try not to do it again; it's slow, annoying, and it makes the flash memory cry (seriously, flash has a limited lifespan, be courteous)

&nbsp;

These are the available arguments for [/Hardware/Lightbulb/send_scripts/run-script.bat](/Hardware/Lightbulb/send_scripts/run-script.bat), and correspond with batch files in the [scripts]([/Hardware/Lightbulb/send_scripts/scripts) subdirectory. These scripts handle flashing code onto the microcontroller; it is best to flash only what has changed, as it will extend the life of your microcontroller's flash memory significantly. Additionally, flashing one file at a time is far faster.

Most of the scripts are intuitive, as they match the respective filenames, but there are a few scripts that need some explanation:

 - `all`   -  Runs clean\_filesystem and then flashes all files

 - `all_config`  -  Flashes all config files

 - `clean_filesystem` -  Rebuilds the FAT filesystem by running utils/fix\_filesystem on the microcontroller. utils/ampy sometimes destroys the filesystem during `put` commands that freeze – use `all` to fix this instead of a direct call.

 - `flash_firmware` -  Uses utils/esptool to flash utils/micropython-v1.8.7.bin to the microcontroller

 - `set_path` -  Sets environment variables for use with the scripts above. This is called by `run-script.bat`, so don't bother running it manually.


NOTE: The COM port configuration assumes that you only have one serial device (the microcontroller) connected at any given time.
Additionally, this defaults to the range COM0-COM9, so if your system uses a higher COM port number, you'll need to tweak the for-loop.
