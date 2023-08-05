import cv2
import argparse
import os
import re
import sys


def checkSign(frame, signs):
    lastlimit = "00"
    lastdetect = "00"

    matches = 0
    possiblematch = "00"
    origframe = frame
    for sign in signs:
        xpos, ypos, width, height = [ i*1 for i in sign ]

        crop_img = frame[ypos:ypos+height, xpos:xpos+width]
        sized = cv2.resize(crop_img, (128, 128))
        comp = "Unknown"
        comp, amnt  = run_flann(sized)
        if comp != "Unknown":
            if comp != lastlimit:
                # Require two consecutive hits for new limit.
                if comp == lastdetect:
                    possiblematch = comp
                    matches = matches + 1
                    if matches >= 2:
                        print "New speed limit: "+possiblematch
                        lastlimit = possiblematch
                        matches = 0
                else:
                    possiblematch = "00"
                    matches = 0
            cv2.rectangle(
                origframe,
                (xpos, ypos),
                (xpos+width, ypos+height),
                (0, 0, 255))
            cv2.putText(
                origframe,
                "Speed limit: "+comp+" KP: "+str(amnt),
                (xpos,ypos-5),
                cv2.FONT_HERSHEY_SIMPLEX,
                 0.4,
                (0,0,255),
                1,)
        else:
            cv2.rectangle(
                origframe,
                (xpos,ypos),
                (xpos+width,ypos+height),
                (255,0,0))
            cv2.putText(
                origframe,
                "UNKNOWN SPEED LIMIT",
                (xpos,ypos-5),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.4,
                (255,0,0),
                1,)
            comp = lastdetect
        lastdetect = comp

    cv2.putText(
    origframe,
    "Current speed limit: "+str(lastlimit)+" km/h.",
    (5,50),
    cv2.FONT_HERSHEY_SIMPLEX,
    1,
    (0,0,0),
    2
    )

def read_paths(path):
    # Returns a list of files in given path
    images = [[] for _ in range(2)]
    for dirname, dirnames, _ in os.walk(path):
        for subdirname in dirnames:
            filepath = os.path.join(dirname, subdirname)
            for filename in os.listdir(filepath):
                print filepath
                try:
                    imgpath = str(os.path.join(filepath, filename))
                    images[0].append(imgpath)
                    limit = re.findall('[0-9]+', filename)
                    images[1].append(limit[0])
                except IOError, (errno, strerror):
                    print "I/O error({0}): {1}".format(errno, strerror)
                except:
                    print "Unexpected error:", sys.exc_info()[0]
                    raise
    return images

def load_images(imgpath):
    # Loads images in given path and returns a list containing image and keypoints
    images = read_paths(imgpath)
    imglist = [[], [], [], []]
    cur_img = 0
    sift = cv2.SIFT()
    for i in images[0]:
        img = cv2.imread(i, 0)
        imglist[0].append(img)
        imglist[1].append(images[1][cur_img])
        cur_img += 1
        keypoints, des = sift.detectAndCompute(img, None)
        imglist[2].append(keypoints)
        imglist[3].append(des)
    return imglist


def run_flann(img):
    """Run FLANN-detector for given image with given image list"""
# Find the keypoint descriptors with SIFT
    _, des = SIFT.detectAndCompute(img, None)
    if des is None:
        return "Unknown", 0
    if len(des) < ARGS.MINKP:
        return "Unknown", 0

    biggest_amnt = 0
    biggest_speed = 0
    cur_img = 0
    try:
        for _ in IMAGES[0]:
            des2 = IMAGES[3][cur_img]
            matches = FLANN.knnMatch(des2, des, k=2)
            matchamnt = 0
    # Find matches with Lowe's ratio test
            for _, (moo, noo) in enumerate(matches):
                if moo.distance < ARGS.FLANNTHRESHOLD*noo.distance:
                    matchamnt += 1
            if matchamnt > biggest_amnt:
                biggest_amnt = matchamnt
                biggest_speed = IMAGES[1][cur_img]
            cur_img += 1
        if biggest_amnt > ARGS.MINKP:
            return biggest_speed, biggest_amnt
        else:
            return "Unknown", 0
    except Exception, exept:
        print exept
        return "Unknown", 0


ARGS = None
FLANN = None
surf = cv2.SURF(500)
SIFT = surf

PARSER = argparse.ArgumentParser(
      description="Traffic sign recognition and intelligent speed assist.",
      )

PARSER.add_argument("-k", "--keypoints",
        dest="MINKP", default=5,
      help="Min amount of keypoints required in" \
      " limit recognition. Default: 5.")

ARGS = PARSER.parse_args()

print "before load_images:"+os.getcwd()
os.chdir("..")
# print os.getcwd()
IMAGES = load_images("signstext")
os.chdir("cameramodule")
print "after load_images:"+os.getcwd()