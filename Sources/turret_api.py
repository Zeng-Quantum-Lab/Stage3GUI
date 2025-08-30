# Usart Library
import serial
import time as t

class TurretController:
    """
    API class for controlling BX-REMCB turret controller
    """
    
    def __init__(self, port: str):
        """
        Initialize the serial port and log in to the controller
        """
        print("Starting BX-REMCB controller")
        
        # Initialize serial connection
        self.Usart = serial.Serial(
            port=port,
            baudrate=19200,                     # BX-REMCB default baudrate
            bytesize=serial.EIGHTBITS,             # 8 data bits
            parity=serial.PARITY_EVEN,             # Even parity
            stopbits=serial.STOPBITS_TWO,          # 2 stop bits
            timeout=1                             # 1 s read timeout
        )
        
        # Check CTS status
        if self.Usart.getCTS():
            print("CTS asserted (ready to receive)")
        else:
            print("CTS de-asserted (not ready)")
        
        t.sleep(1)
        
        # Log in to the controller
        self.Usart.write('1LOG IN\r\n'.encode())
        t.sleep(0.5)
        current_response = self.Usart.readline()
        
        if current_response == b'1LOG +\r\n':
            print("LOG IN successful!")
        else:
            print(f"Login failed. Response: {current_response}")
    
    def check_if_log_in(self):
        """
        Check if the controller is logged in
        
        Returns:
            bool: True if logged in, False otherwise
        """
        self.Usart.write("1LOG?\r\n".encode())
        t.sleep(0.5)
        response = self.Usart.readline()
        print(response)
        
        # Check for valid response indicating logged in status
        if response and b'1LOG IN' in response:
            print("Controller is logged in")
            return True
        else:
            print("Controller is not logged in")
            return False
    
    def turn_to_position(self, value):
        """
        Turn the turret to a specific position
        
        Args:
            value (int): Position number (1-6 for 6-place nosepiece)
        """
        command = f"1OB {value}\r\n"
        self.Usart.write(command.encode())

        t.sleep(0.5)

        # Read acknowledgement
        ack = self.Usart.readline()
        print(f"Position {value} command sent. Response: {ack}")
    
    def check_position(self):
        """
        Check the current position of the turret
        
        Returns:
            int: Current position number, or None if error
        """
        self.Usart.write("1OB?\r\n".encode())

        t.sleep(0.5)

        response = self.Usart.readline()
        
        try:
            # Parse response to extract position number
            # Expected format: b'1OB X\r\n' where X is the position
            if response and b'1OB' in response:
                # Extract the position number from the response
                response_str = response.decode().strip()
                parts = response_str.split()
                if len(parts) >= 2:
                    position = int(parts[1])
                    print(f"Current position: {position}")
                    return position
        except (ValueError, IndexError) as e:
            print(f"Error parsing position response: {e}")
        
        print(f"Could not determine position. Response: {response}")
        return None
    
    def close(self):
        """
        Log out of the device and close the serial port
        """
        try:
            # Log out
            self.Usart.write('1LOG OUT\r\n'.encode())

            t.sleep(0.5)

            logout_response = self.Usart.readline()
            print(f"Logout response: {logout_response}")
            
            # Close serial port
            self.Usart.close()
            print("Serial port closed")
        except Exception as e:
            print(f"Error during close: {e}")


def test_run():
    """
    Test function containing the original code logic
    """
    try:
        controller = TurretController(port='COM5')
        
        # Test check_if_log_in
        print("\n--- Testing check_if_log_in ---")
        controller.check_if_log_in()
        
        # Test check_position
        print("\n--- Testing check_position ---")
        controller.check_position()
        
        t.sleep(3)
        # move the six-place nosepiece to position 1
        controller.turn_to_position(1)

        t.sleep(3)
        # move the six-place nosepiece to position 2
        controller.turn_to_position(2)

        t.sleep(3)
        # move the six-place nosepiece to position 3
        controller.turn_to_position(3)

        t.sleep(3)
        # move the six-place nosepiece to position 3
        controller.turn_to_position(4)

        t.sleep(3)
        # move the six-place nosepiece to position 3
        controller.turn_to_position(5)
        
        t.sleep(3)
        # move the six-place nosepiece to position 3
        controller.turn_to_position(6)

        print("Write done")
        
        controller.close()
        
    except KeyboardInterrupt:
        print("Interrupted by user")
        if 'controller' in locals():
            controller.close()


if __name__ == "__main__":
    test_run()