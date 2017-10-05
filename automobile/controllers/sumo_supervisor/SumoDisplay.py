# Description: SumoDisplay class (used to take picture of SUMO-GUI
#              and display them in a Webots Display)

pilFound = True

from controller import Display
try:
    from PIL import Image
except ImportError as e:
    import sys
    pilFound = False
    if sys.platform == 'linux2':
        sys.stderr.write("PIL module not found, please install it with:\n")
        sys.stderr.write("apt-get install python-pip\n")
        sys.stderr.write("pip install pillow\n")
    else:
        sys.stderr.write("PIL module not found, please install it with:\n")
        sys.stderr.write("pip install pillow\n")


class SumoDisplay:
    def __init__(self, displayDevice, zoom, view, directory, refreshRate, resize, traci):
        self.displayDevice = displayDevice
        self.view          = view
        self.directory     = directory
        self.refreshRate   = refreshRate
        self.resize        = resize
        self.traci         = traci
        self.screeshotID   = 0
        self.timeCounter   = 0
        self.width         = displayDevice.getWidth()
        self.height        = displayDevice.getHeight()
        self.traci.gui.setZoom(view, 100 * zoom)

    def step(self, step):
        if not pilFound:
            return
        self.timeCounter += step
        if self.timeCounter >= self.refreshRate:
            imageFilename = self.directory + '/screeshot_' + str(self.screeshotID) + '.jpg'
            self.traci.gui.screenshot(self.view, imageFilename)
            if self.resize:
                im = Image.open(imageFilename)
                im = im.resize(size=(self.width, self.height))
                im.save(imageFilename)
                im.close()
                image = self.displayDevice.imageLoad(imageFilename)
                self.displayDevice.imagePaste(image, 0, 0)
            else:
                image = self.displayDevice.imageLoad(imageFilename)
                im = Image.open(imageFilename)
                imageWidth, imageHeight = im.size
                im.close()
                widthOffset = imageWidth / 2 - self.width / 2
                if widthOffset < 0:
                    widthOffset = 0
                heightOffset = imageHeight / 2 - self.height / 2
                if heightOffset < 0:
                    heightOffset = 0
                self.displayDevice.imagePaste(image, -widthOffset, -heightOffset)
            self.screeshotID += 1
            self.timeCounter = 0
