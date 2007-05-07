from VideoCapture import Device
import ImageDraw
import Image
import sys
import pygame


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

# init pygame
pygame.init()

# setup screen size
size = width, height = 320,240


# get cam device
cam = Device()


screen = pygame.display.set_mode(size)
left_button = None
right_button = None

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

    camshot = cam.getImage()

    # process left button
    new_left_button = camshot.crop((20,20,70,70))
    draw = ImageDraw.Draw(camshot)
    if diff_image(left_button, new_left_button):
        draw.rectangle((20,20,70,70), fill=128)
    else:
        draw.rectangle((20,20,70,70), outline=128)
    left_button = new_left_button

    # process right button
    new_right_button = camshot.crop((250,20,300,70))
    draw = ImageDraw.Draw(camshot)
    if diff_image(right_button, new_right_button):
        draw.rectangle((250,20,300,70), fill=128)
    else:
        draw.rectangle((250,20,300,70), outline=128)
    right_button = new_right_button


    camshot = camshot.transpose(0)
    camshot = pygame.image.fromstring(camshot.tostring(), (320,240), "RGB")

    screen.blit(camshot, (0,0))
    pygame.display.flip()