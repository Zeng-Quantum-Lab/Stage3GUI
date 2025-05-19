from ctypes import WinDLL, create_string_buffer
import os
import sys
import time


class prior():
    def __init__(self, port_num, sdk_path):
        self.port_num = port_num
        self.path = sdk_path
        self.velocity = 0
        if os.path.exists(self.path):
            global SDKPrior
            SDKPrior = WinDLL(self.path, winmode=0)
        else:
            raise RuntimeError("DLL could not be loaded.")
        global rx
        rx = create_string_buffer(1000)

        ret = SDKPrior.PriorScientificSDK_Initialise()
        if ret:
            print(f"Error initialising {ret}")
            sys.exit()
        else:
            print(f"Ok initialising {ret}")

        ret = SDKPrior.PriorScientificSDK_Version(rx)
        print(f"dll version api ret={ret}, version={rx.value.decode()}")

        global sessionID
        sessionID = SDKPrior.PriorScientificSDK_OpenNewSession()
        if sessionID < 0:
            print(f"Error getting sessionID {ret}")
        else:
            print(f"SessionID = {sessionID}")

        ret = SDKPrior.PriorScientificSDK_cmd(
            sessionID, create_string_buffer(b"dll.apitest 33 goodresponse"), rx
        )
        print(f"api response {ret}, rx = {rx.value.decode()}")

        ret = SDKPrior.PriorScientificSDK_cmd(
            sessionID, create_string_buffer(b"dll.apitest -300 stillgoodresponse"), rx
        )
        print(f"api response {ret}, rx = {rx.value.decode()}")

        print("controller.connect ", self.port_num)
        self.cmd("controller.connect ", self.port_num)

        self.check_busy()
        position = self.cmd("controller.stage.position.get")
        position.split(" ")
        
        self.x = int(position[0])
        self.y = int(position[1])


    def cmd(msg):
        print(msg)
        ret = SDKPrior.PriorScientificSDK_cmd(
            sessionID, create_string_buffer(msg.encode()), rx
        )
        if ret:
            print(f"Api error {ret}")
        else:
            print(f"OK {rx.value.decode()}")
        return ret, rx.value.decode()
    
    def check_busy(self):
        while self.cmd("controller.stage.busy.get") == 1 :
            print("Controller is Busy\n")
            time.sleep(1)

    def set_velocity(self, velocity):
        self.check_busy()
        self.velocity = velocity
        self.cmd(f"controller.stage.velocity.set {velocity} {velocity}")

    def set_acceleration(self, acceleration):
        self.check_busy()
        self.cmd(f"controller.stage.acc.set {acceleration}")

    def go_to_pos(self, new_x, new_y):
        self.x = new_x
        self.y = new_y
        self.check_busy()
        self.cmd(f"controller.stage.goto-position {self.x} {self.y}")
        self.cmd(f"controller.stage.move-at-velocity {self.velocity} {self.velocity}")

    def get_curr_pos(self):
        self.check_busy()
        position = self.cmd("controller.stage.position.get")
        position.split(" ")
        self.x = position[0]
        self.y = position[1]

    def disconnect(self):
        self.check_busy()
        self.cmd("controller.disconnect")

