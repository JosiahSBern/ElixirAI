import subprocess

DEFAULT_PORTS = [
    "127.0.0.1:5555",  # BlueStacks default
    "127.0.0.1:5556",  
]

class EmulatorController:
    """
    Helper class to control Android emulator via ADB commands.It can connect to an emulator instance, launch apps,
    change resolution, send taps/clicks, and type text.

    adb_path : str
        Path to the adb binary 
    device_ip : str
        The IP: port of the emulator device 
    device_serial : str or None
        The device identifier once connected (None until `connect_device` is called).
    """
    def __init__(self, device_ip, adb_path="adb"):
        self.adb_path = adb_path
        self.device_ip = device_ip
        self.device_serial = None
    
    def adb_run(self,timeout):
        cmd = [self.adb_path]
        if self.device_serial:
            cmd += ["-s",self.device_serial]
        return subprocess.run(
            cmd + args,
            capture_output= True,
            text = True,
            timeout= timeout,
            check = False
        )

    def connect_device(self):
        """
        Connects to emulator using adb connect 
        Returns:
            device_serial message
        Raises:
            RuntimeError: If connection fails.
        """
        result = subprocess.run(
            [self.adb_path,"connect",self.device_ip],
            capture_output= True, 
            text = True
        )
        if "connected" in result.stdout:
            print("Connected")
            return result.stdout.strip()
        raise RuntimeError(f"Failed to connect: {result.stderr.split()}")

    def find_package_name(self,package_name):
        """
        Checks if application/package exits on device 
        Args:
            Package name
        Returns:
           The matched package string if found, else None.
        """
        if not self.device_serial:
            raise RuntimeError("Device not connected")
        result = self.adb_run(
            ["shell", 
             "pm", 
             "list", 
             "packages", 
             package_name])
        for line in (result.stdout or "").splitlines():
            line = line.strip()
            if line.startswith("package:"):
                found = line.split("package:", 1)[1].strip()
                if found == package_name:
                    return found
        return None
            
    

    def run_app(self,package_name):
        """
        Launches app by package name

        Return:
        True on success, False otherwise
        """
        result = self.adb_run([
            "shell", "monkey",
            "-p", package_name,
            "-c", "android.intent.category.LAUNCHER",
            "1"
        ], timeout=15)
        return result.returncode == 0

    
    def set_res(self,width,height):
        """
        Sets the emulator screen resolution
        """
        if not self.device_serial:
            raise RuntimeError("Device not connected")
        result = self.adb_run(["shell", "wm", "size", f"{width}x{height}"])
        return result.returncode == 0


    
    def click_button(self,x,y):
        """
        Simulates a tap at (x, y).
        """
        if not self.device_serial:
            raise RuntimeError("Device not connected.")
        result = self.adb_run(["shell", "input", "tap", str(x), str(y)])
        return result.returncode == 0


    
    def type_text(self, text):
        """
        Types text into the emulator.
        """
        if not self.device_serial:
            raise RuntimeError("Device not connected.")
        escaped = text.replace(" ", "%s")
        result = self._adb_run(["shell", "input", "text", escaped])
        return result.returncode == 0
