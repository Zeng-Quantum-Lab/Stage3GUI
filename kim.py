import os
import time
import sys
import clr

clr.AddReference("C:\\Program Files\\Thorlabs\\Kinesis\\Thorlabs.MotionControl.DeviceManagerCLI.dll")
clr.AddReference("C:\\Program Files\\Thorlabs\\Kinesis\\Thorlabs.MotionControl.GenericMotorCLI.dll")
clr.AddReference("C:\\Program Files\\Thorlabs\\Kinesis\\ThorLabs.MotionControl.KCube.InertialMotorCLI.dll")
from Thorlabs.MotionControl.DeviceManagerCLI import *
from Thorlabs.MotionControl.GenericMotorCLI import *
from Thorlabs.MotionControl.KCube.InertialMotorCLI import *
from System import Decimal  # necessary for real world units

class kim:
    def __init__(self, serial_num):
        self.serial_num = serial_num
        try:
            DeviceManagerCLI.BuildDeviceList()

            # create new device
            self.serial_num = "97251106"  # Replace this line with your device's serial number
            
            
            self.device = KCubeInertialMotor.CreateKCubeInertialMotor(self.serial_num)

            # Connect
            self.device.Connect(self.serial_num)
            time.sleep(0.25)


            # Ensure that the self.device settings have been initialized
            if not self.device.IsSettingsInitialized():
                self.device.WaitForSettingsInitialized(10000)  # 10 second timeout
                assert self.device.IsSettingsInitialized() is True

            # Get self.device Information and display description
            device_info = self.device.GetDeviceInfo()
            print(device_info.Description)
            # Start polling and enable channel
            self.device.StartPolling(250)  #250ms polling rate
            time.sleep(0.25)
            self.device.EnableDevice()
            time.sleep(0.25)  # Wait for self.device to enable

            # Load any configuration settings needed by the controller/stage
            inertial_motor_config = self.device.GetInertialMotorConfiguration(self.serial_num)

            # Get parameters related to homing/zeroing/moving
            device_settings = ThorlabsInertialMotorSettings.GetSettings(inertial_motor_config)

            # Step parameters for an intertial motor channel
            self.x_motor = InertialMotorStatus.MotorChannels.Channel1  # enum chan ident
            device_settings.Drive.Channel(self.x_motor).StepRate = 500
            device_settings.Drive.Channel(self.x_motor).StepAcceleration = 100000

            self.y_motor = InertialMotorStatus.MotorChannels.Channel2  # enum chan ident
            device_settings.Drive.Channel(self.y_motor).StepRate = 500
            device_settings.Drive.Channel(self.y_motor).StepAcceleration = 100000

            self.z_motor = InertialMotorStatus.MotorChannels.Channel3  # enum chan ident
            device_settings.Drive.Channel(self.z_motor).StepRate = 500
            device_settings.Drive.Channel(self.z_motor).StepAcceleration = 100000

            self.angle_motor = InertialMotorStatus.MotorChannels.Channel4 # enum chan ident
            device_settings.Drive.Channel(self.angle_motor).StepRate = 500
            device_settings.Drive.Channel(self.angle_motor).StepAcceleration = 100000

            # Send settings to the self.device
            self.device.SetSettings(device_settings, True, True)

            print("Zeroing self.device")
            self.device.SetPositionAs(self.x_motor, 0)
            self.device.SetPositionAs(self.y_motor, 0)
            self.device.SetPositionAs(self.z_motor, 0)
            self.device.SetPositionAs(self.angle_motor, 0)
        except Exception as e:
            print(e)

    def go_to_Xpos(self, new_x):
        self.device.MoveTo(self.x_motor, new_x, 1000)
    
    def go_to_Ypos(self, new_y):
        self.device.MoveTo(self.y_motor, new_y, 1000)
    
    def go_to_Zpos(self, new_z):
        self.device.MoveTo(self.z_motor, new_z, 1000)
    
    def go_to_Angle(self, new_angle):
        self.device.MoveTo(self.angle_motor, new_angle, 1000)

    def disconnect(self):
        self.device.StopPolling()
        self.device.Disconnect()


        