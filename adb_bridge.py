import subprocess

DEFAULT_PORTS = [
    "127.0.0.1:5555",  # BlueStacks default
    "127.0.0.1:5556",  
]

class EmulatorController:
    """
    """
    def __init__(self,adb_path = 'adb',device_ip):
        self.adb_path = adb_path
        self.device_ip = device_ip
        self.device_serial = None

    def connect_device(self):
        result = subprocess.run()