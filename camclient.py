# https://www.youtube.com/watch?v=bJOvYgSqrOs

from vidstream import *
import socket
import threading

ip_address = socket.gethostbyname(socket.gethostname())

camera_client = CameraClient(ip_address, 9999)
#camera_client = CameraClient('192.168.0.203', 9999)
t1 = threading.Thread(target=camera_client.start_stream)
#t1.start() # on macOS, this causes the server to crash with:
# cv2.error: Unknown C++ exception from OpenCV code
# Assertion failed:
# (NSViewIsCurrentlyBuildingLayerTreeForDisplay() != currentlyBuildingLayerTree),
# function NSViewSetCurrentlyBuildingLayerTreeForDisplay,
# file /System/Volumes/Data/SWE/macOS/BuildRoots/38cf1d983f/Library/Caches/
# com.apple.xbs/Sources/AppKit/AppKit-2022.60.128/AppKit.subproj/NSView.m, line 13412.

audio_sender = AudioSender(ip_address, 8888)
t2 = threading.Thread(target=audio_sender.start_stream)
t2.start()

screen_client = ScreenShareClient(ip_address, 9999)
t3 = threading.Thread(target=screen_client.start_stream)
#t3.start() # on macOS, this just takes a screenshot
