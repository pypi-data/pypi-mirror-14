from PIL import Image
import cv2

# initialize SURF object
# surf = cv2.SURF(500)
#
# # do not find orientation(better performance)
# # ???????!!!!!!!!!!! need to check it ????????!!!!!!!!!!!!!!!!!!!
# if surf.upright == False:
#     surf.upright = True

import os


def loadClassifier(objectType):
    # os.chdir("..")
    print "running from: " + os.getcwd()
    classifier = None

    if objectType == 'face':
        classifier = cv2.CascadeClassifier('classifiers\haarcascade_frontalface_default.xml')
    elif objectType == 'sign':
        classifier = cv2.CascadeClassifier('classifiers\haarCascadeRoad.xml')
    elif objectType == 'eye':
        classifier = cv2.CascadeClassifier('classifiers\haarcascade_eye.xml')
    else:
        print ('no such object type')
        exit(0)

    # TODO CascadeClassifier returns some value in any case,
    # TODO need more accurate check
    if classifier is None:
        print "fuck off, no classifier"
        exit(0)

    return classifier


def detectObjects(data, classifier):
    gray = cv2.cvtColor(data, cv2.COLOR_BGR2GRAY)

    # Detect objects in the image, rectangles returned
    detections = classifier.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30),
                                             flags=cv2.cv.CV_HAAR_SCALE_IMAGE)

    return detections


def drawDetections(detections, colorIm):
    # Draw a rectangle over detection
    for detection in detections:
        x = detection[0]
        y = detection[1]
        w = detection[2]
        h = detection[3]

        cv2.rectangle(colorIm, (x, y), (x + w, y + h), (0, 255, 240), 2)

    return colorIm


def cropObjects(rects, data):
    objectArr = []

    for rect in rects:
        x = rect[0]
        y = rect[1]
        w = rect[2]
        h = rect[3]

        # Crop from x, y, w, h
        # data[y: y + h, x: x + w]
        crop_img = data[y:y + h, x:x + w]
        objectArr.append(crop_img)

    return objectArr


def detectAndDrawObjectByType(data, classifier, objectType):
    # detect objects by given type
    detections = detectObjects(data, classifier)

    if len(detections) == 0:
        print 'NO ' + str.upper(objectType)
        cv2.destroyWindow("cropped")
    else:
        croppedObjects = cropObjects(detections, data)
        # checkSign(data,detections)
        for object in croppedObjects:
            sizedObject = cv2.resize(object, (128, 128))

            # comp, amnt  = flanndetector.run_flann(sizedObject)
            cv2.imshow("cropped", sizedObject)

        detectedObjects = drawDetections(detections, data)
        return detectedObjects

    return data


def resizeImage(data, scaleFactor):
    resized = cv2.resize(data, None, fx=scaleFactor, fy=scaleFactor)
    return resized


# usage like this: createImageFile('PIC'+time.strftime("%d%m%Y"),dummyShit)
def createImageFile(fileName, data):
    # create a new image
    img = Image.new('RGB', (255, 255), "white")
    pixels = img.load()  # create the pixel map

    # put your data here
    for i in range(img.size[0]):  # for every pixel:
        for j in range(img.size[1]):
            pixels[i, j] = (i, j, 100)  # set the colour accordingly

    img.show()
    img.save(fileName + ".png", "PNG")
