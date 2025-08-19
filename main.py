import subprocess, numpy as np, cv2, time, sys

SERIAL = sys.argv[1] if len(sys.argv) > 1 else "127.0.0.1:5555"

def grab(serial=SERIAL):
    png = subprocess.check_output(["adb", "-s", serial, "exec-out", "screencap", "-p"])
    arr = np.frombuffer(png, np.uint8)
    frame = cv2.imdecode(arr, cv2.IMREAD_COLOR)
    return frame

if __name__ == "__main__":
    frame = grab()
    if frame is None:
        print("Failed to grab frame. Is ADB connected and Clash Royale visible?")
        sys.exit(1)
    cv2.imwrite("test.png", frame)
    print("Saved test.png", frame.shape)
