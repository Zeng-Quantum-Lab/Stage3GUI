# How to setup
To install the scripts, go to the release section of this repo. </br>
It is recommended to choose the newest release. </br>
<img src="images\image1.png" alt="release" width="300"/> </br>
##
Install the zip file in the release. It should include all the necessary dependency to control KIM101 and Prior ProScan Stage controller. </br>
<img src="images\image2.png" alt="install" width="600"/> </br>
##
After unzip in prefer directory, run [setup.bat](setup.bat). </br>
This installation will bring up a terminal. Wait until the terminal is gone and .venv folder appears in your directory. This means that dependencies has sucessfully been installed. </br>
<img src="images\image3.png" alt="setup" width="600"/> </br>
<img src="images\image4.png" alt="setup1" width="600"/> </br>
##
After successfully install dependencies, the script can be launch correctly via [launch.bat](launch.bat). </br>
<img src="images\image5.png" alt="setup1" width="600"/> </br>

# Potential Issues
1. When running [setup.bat](setup.bat), there are chances that instrumentkit, a dependency to control TC200 heat controller, will failed. </br>
If this happen, ensure that you have Python 3.13.7 installed (tested Python Version), remove .venv folder and rerun [setup.bat](setup.bat) again.
2. After running [launch.bat](launch.bat), if you cannot connect to any of the devices, make sure that you have had the correct virtual port entered in the setup phase of the scripts. You can find them in Window Device Manager, under Ports. </br>
<img src="images\image6.png" alt="setup1" width="300"/> </br>
In addition, make sure that there is no other running instances of the script as the older script would have already occupied the ports connected to the devices, causing said issues.
3. Feel free to report new issues or suggestion under Issues Tab on Github as I am not personally using the devices.