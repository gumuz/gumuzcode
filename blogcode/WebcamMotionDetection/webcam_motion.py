from VideoCapture import Device

import time
import Image

def diff_image(img1, img2, pix_threshold=50, img_threshold=10):
    """ Compare 2 images to detect possible motion """
    if not img1 or not img2: return False
    img1 = img1.getdata()
    img2 = img2.getdata()
    pixel_count = len(img1)
    pixdiff = 0
    for i in range(pixel_count):
        if abs(sum(img1[i]) - sum(img2[i])) > pix_threshold:
            pixdiff += 1
            diffperc = pixdiff / (pixel_count/100)
            if diffperc > img_threshold:
                # motion detected
                return True


# get cam device
cam = Device()

# interval or framerate
interval = 1

prevImg = None
counter = 0

while True:
    currImg = cam.getImage()
    if diff_image(prevImg, currImg):
        print "motion detected!"
        currImg.save('image_%s.png' % (counter))
        interval = 3
        counter += 1
    else:
        interval = 1

    prevImg = currImg
    time.sleep(interval)