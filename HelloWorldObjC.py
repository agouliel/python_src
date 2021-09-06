# https://pyobjc.readthedocs.io/en/latest/examples/core/Scripts/HelloWorld/index.html

from Cocoa import NSObject, NSApplication, NSApp, NSWindow, NSButton, NSSound
from PyObjCTools import AppHelper


class AppDelegate(NSObject):
    def applicationDidFinishLaunching_(self, aNotification):
        print("Hello, World!")

    def sayHello_(self, sender):
        print("Hello again, World!")


def main():
    app = NSApplication.sharedApplication()

    # we must keep a reference to the delegate object ourselves,
    # NSApp.setDelegate_() doesn't retain it. A local variable is
    # enough here.
    delegate = AppDelegate.alloc().init()
    NSApp().setDelegate_(delegate)

    win = NSWindow.alloc()
    frame = ((200.0, 300.0), (250.0, 100.0))
    win.initWithContentRect_styleMask_backing_defer_(frame, 15, 2, 0)
    win.setTitle_("HelloWorld")
    win.setLevel_(3)  # floating window

    hel = NSButton.alloc().initWithFrame_(((10.0, 10.0), (80.0, 80.0)))
    win.contentView().addSubview_(hel)
    hel.setBezelStyle_(4)
    hel.setTitle_("Hello!")
    hel.setTarget_(app.delegate())
    hel.setAction_("sayHello:")

    beep = NSSound.alloc()
    beep.initWithContentsOfFile_byReference_("/System/Library/Sounds/Tink.Aiff", 1)
    hel.setSound_(beep)

    bye = NSButton.alloc().initWithFrame_(((100.0, 10.0), (80.0, 80.0)))
    win.contentView().addSubview_(bye)
    bye.setBezelStyle_(4)
    bye.setTarget_(app)
    bye.setAction_("stop:")
    bye.setEnabled_(1)
    bye.setTitle_("Goodbye!")

    adios = NSSound.alloc()
    adios.initWithContentsOfFile_byReference_("/System/Library/Sounds/Basso.aiff", 1)
    bye.setSound_(adios)

    win.display()
    win.orderFrontRegardless()  # but this one does

    AppHelper.runEventLoop()


if __name__ == "__main__":
    main()

# https://superuser.com/questions/1491509/is-the-format-schema-of-the-apple-music-library-musicdb-used-in-macos-catalina

#import <iTunesLibrary/ITLibrary.h>
#NSError *error = nil;
#ITLibrary *library = [ITLibrary libraryWithAPIVersion:@"1.1" error:&error];
#if (library) {
#        NSArray *playlists = library.allPlaylists; //  <- NSArray of ITLibPlaylist
#        NSArray *tracks = library.allMediaItems; //  <- NSArray of ITLibMediaItem
#}

