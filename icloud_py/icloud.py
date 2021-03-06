# https://pypi.org/project/pyicloud/
# pip install pyicloud

from pyicloud import PyiCloudService
import sys
from datetime import datetime

mypass = input("Password: ")
api = PyiCloudService('agouliel@icloud.com', mypass)

if api.requires_2fa:
    print("Two-factor authentication required.")
    code = input("Enter the code you received of one of your approved devices: ")
    result = api.validate_2fa_code(code)
    print("Code validation result: %s" % result)

    if not result:
        print("Failed to verify security code")
        sys.exit(1)

    if not api.is_trusted_session:
        print("Session is not trusted. Requesting trust...")
        result = api.trust_session()
        print("Session trust result %s" % result)

        if not result:
            print("Failed to request trust. You will likely be prompted for the code again in the coming weeks")
elif api.requires_2sa:
    import click
    print("Two-step authentication required. Your trusted devices are:")

    devices = api.trusted_devices
    for i, device in enumerate(devices):
        print(i, device.get('deviceName',
            "SMS to %s" % device.get('phoneNumber')))

    device = click.prompt('Which device would you like to use?', default=0)
    device = devices[device]
    if not api.send_verification_code(device):
        print("Failed to send verification code")
        sys.exit(1)

    code = click.prompt('Please enter validation code')
    if not api.validate_verification_code(device, code):
        print("Failed to verify verification code")
        sys.exit(1)

#print(api.devices)
print(api.devices[2].location())

# calendar is not working (PyiCloudAPIResponseException: Authentication required for Account. (421))
#print(api.calendar.events())
from_dt = datetime(2021, 1, 1)
to_dt = datetime(2021, 1, 31)
#print(api.calendar.events(from_dt, to_dt))

print(api.contacts.all())
print(api.drive.dir()) #api.files.dir()
print(api.photos.all)
