# DCC Render Status (Application for Host)
[![GLXY](https://github.com/SideswipeeZ/dcc-render-status/blob/master/IMG/banner_ssrs.png)](https://galaxy.store/dcc)

Now available on the Samsung Galaxy Store ***(Search: DCC Render Status)***

DCC Render Status is a concept application that allows you to recieve the status of a local render from a machine that has access to the local files directly to your wrist device. Current features include:

  - On-Demand update from Machine
  - Average time per frame
  - Display ROP used to render
  - Number of frames rendered

![](https://github.com/SideswipeeZ/dcc-render-status/blob/master/IMG/Github_Cap.png)

## Requirements
- Supported OS with Script.
- Python 3.5
- Tornado for Python
- Internet Connection
- Tizen Smart Watch (Galaxy Watch, Gear S3) with tizen 3.0 and up. (As of Version 1.0.0)

## Supported Platforms*
*Tested on the following platforms.
OS:
  - x86/64 Windows (Python 3.5)
  - 32Bit Raspberry Pi OS (a.k.a Rasbian) **(WORK IN PROGRESS)**

Companion App:
  - Tizen Wearable (Tizen 3.0+)

More applications to possibly come.

### Tech

This application requires one or more of the following app to run correctly in addition to the Supported Platform:

- ***[Houdini]***
    - [Arnold]
    - Mantra
    - [Redshift]
- ***[Maya]***
    - [Arnold]
    - [Redshift]
- ***[Python] 3.5+***
    - Tornado Module


## Installation
### Network Settings.
As of version 1.0.0, this application is intended for the target machine which has access to the files being rendered, to be able to communicate over the network to a request from the Tizen app. This is possible from Port Forwarding a free unused port (Ideally a port over 1024) e,g, using port 8989 for communication. This can be done using your router settings. (In testing Port Triggering was also used.)

Please lookup your router settings for more details. This step may change in the future for it to be alot more convenient to setup but as of now this is the current solution.

The following installation is for Windows OS.
### **Houdini/Maya**
To get started download the **DCC** folder from the Repository and save files to a sensible directory that Houdini/Maya can read.

For Houdini open:
Open the **TizenApp_Connect_Hou.py** file and edit the **app_location** variable to the directory you have saved. 
For Maya:
Open the **TizenApp_Connect_Maya.py** file and edit the **app_location** variable to the directory you have saved. 

```sh
app_location = os.path.join("PATH_TO_DIRECTORY")
```
After this save the file and open Houdini/Maya. Next create a new shelf tool and copy the contents of the script to the new shelf tool. After giving the tool a name (icon Optional) hit save and lauching the tool should bring up the GUI for the tool. Simple follow the steps from the help page and you are good to start using the tool.
The GUI is created using Qt. (Which can be found in the Assets folder.)

### **Python Server**
To create the server instance you first need to define the servers options. This requires you to port forward an unused port to allow the tizen app to communicate with the target machine.

In order to get started you must have python 3.5+ installed and the tornado module installed along side.
You can use the **pip** module to install it if you have that functionallity.

**Remember to use Python 3**
```sh
python -m pip install tornado
```
After this step you must edit the python file with the path to the Assoc folder from the Houdini/Maya application installed. You may also change the port you wish to open with the appropriate number.
```sh
echo_file = os.path.join("PATH_HERE")

PORT = 8989 #Change Port to a Integer value
```
After these have been correctly configured, simply run the python script with Python 3 and it should start listening for a connection for as long as it stays open.

### Future Plans

 - Add a image preview system to allow you to view the latest image rendered.
 - Add custom jobs for other applications such as Nuke or After Effects or other file formats.
 - Add more devices to companion app e.g. Android OS, iOS, Wear OS etc.

License
----

MIT


[//]: # (These are reference links used in the body of this note and get stripped out when the markdown processor does its job. There is no need to format nicely because it shouldn't be seen. Thanks SO - http://stackoverflow.com/questions/4823468/store-comments-in-markdown-syntax)


   [Houdini]: <https://www.sidefx.com/products/houdini/>
   [Maya]: <https://www.autodesk.com/products/maya/overview>
   [Python]: <https://www.python.org/downloads/>
   [Arnold]: <https://www.arnoldrenderer.com/>
   [Redshift]: <https://www.redshift3d.com/>
   [GLXY]: <https://galaxy.store/dcc>

