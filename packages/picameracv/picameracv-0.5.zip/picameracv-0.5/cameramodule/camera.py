import cv2

import camerautils as camutils
import imageutils as imgutils


class CameraClass:
    shared_var = 0
    cameraType = ['camera', 'web_camera', 'pi_camera']

    def getNextFrame(self):
        if (self.sourceType is self.cameraType[0]) | (self.sourceType is self.cameraType[1]):
            try:
                ret, rawimage = self.stream.read()
            except Exception as e:
                print e.message
        elif self.sourceType is self.cameraType[2]:
            rawimage = self.stream.PiRGBArray(self.stream, size=(640, 480))
        return rawimage

    def launchCameraDetection(self):

        import time
        time.sleep(2)
        while True:
            rawimage = self.getNextFrame()

            imagewithdetections = imgutils.detectAndDrawObjectByType(rawimage, self.classifier, self.objectType)
            # resize if needed and display colour image with detected objects
            # resized = imgutils.resizeImage(imagewithdetections, 0.8)
            cv2.imshow(self.objectType, imagewithdetections)
            # sleep, exit if presses Esc, terminate processes
            if cv2.waitKey(self.delayTime) == 27:
                break

    def __init__(self, sourceType=cameraType[0], objectType='face', delayTime=50):
        self.sourceType = sourceType
        self.objectType = objectType

        if delayTime > 0:
            self.delayTime = delayTime
        else:
            raise Exception("Delay time is incorrect!!!")
            exit(0)

        self.classifier = imgutils.loadClassifier(self.objectType)
        self.stream = camutils.connectCamera(self.sourceType)
