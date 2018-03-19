import math
import time
import numpy as np
import cv2

ORANGE_MIN = np.array([0, 50, 50],np.uint8)
ORANGE_MAX = np.array([8, 255, 255],np.uint8)
RED_MIN = np.array([172, 50, 50],np.uint8)
RED_MAX = np.array([180, 255, 210],np.uint8)
GREEN_MIN = np.array([50, 50, 50],np.uint8)
GREEN_MAX = np.array([70, 255, 255],np.uint8)
PINK_MIN = np.array([160, 50, 50],np.uint8)
PINK_MAX = np.array([170, 255, 255],np.uint8)


def main(rpiCam=True):
    if rpiCam: # Special init for RPi camera.
        from picamera.array import PiRGBArray
        from picamera import PiCamera
        camera = PiCamera()
        camera.resolution = (800, 600)
        camera.framerate = 32
        camera.exposure_mode = 'off'
        camera.iso = 500
        rawCapture = PiRGBArray(camera, size=(800, 600))
        time.sleep(0.1)
        for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=False):
            track_cars(frame.array)
            rawCapture.truncate(0)
    else:
        cap = cv2.VideoCapture(0)
        while True:
            _, frame = cap.read()
            if frame is None:
                continue
            if not track_cars(frame):
                break
        cap.release()
        cv2.destroyAllWindows()

def track_cars(image):
    hsv_img = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    orange = cv2.inRange(hsv_img, ORANGE_MIN, ORANGE_MAX)
    red = cv2.inRange(hsv_img, RED_MIN, RED_MAX)
    green = cv2.inRange(hsv_img, GREEN_MIN, GREEN_MAX)
    pink = cv2.inRange(hsv_img, PINK_MIN, PINK_MAX)

    kernel = np.ones((5, 5), np.uint8)
    orange_closed = cv2.morphologyEx(orange, cv2.MORPH_CLOSE, kernel)
    red_closed = cv2.morphologyEx(red, cv2.MORPH_CLOSE, kernel)
    green_closed = cv2.morphologyEx(green, cv2.MORPH_CLOSE, kernel)
    pink_closed = cv2.morphologyEx(pink, cv2.MORPH_CLOSE, kernel)

    _, orange_contours, _ = cv2.findContours(orange_closed, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
    _, red_contours, _ = cv2.findContours(red_closed, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
    _, green_contours, _ = cv2.findContours(green_closed, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
    _, pink_contours, _ = cv2.findContours(pink_closed, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)


    infoList = [(orange_closed, orange_contours, (0, 136, 255)),
                (red_closed, red_contours, (0, 0, 255)),
                (green_closed, green_contours, (0, 255, 0)),
                (pink_closed, pink_contours, (144, 0, 255))]
    for closed, contours, colour in infoList:
        if len(contours) > 0:
            # TODO: We know how big the cars should be - use this knowledge to filter bad boxes.
            c = max(contours, key=cv2.contourArea)

            boundingBox = cv2.boundingRect(c)
            x, y, w, h = boundingBox
            if w*h < 50: # Contour too small to be significant.
                continue
            #cv2.rectangle(frame, (x, y), (x + w, y + h), colour, 4)
            center = (int(x + w/2), int(y + h/2))
            cv2.circle(image, center, 5, colour, -1)

            orientedRect = cv2.minAreaRect(c)
            box = np.int0(cv2.boxPoints(orientedRect))
            #cv2.drawContours(frame, [box], 0, colour, 2)

            angle = math.radians(orientedRect[2])

            x = orientedRect[0][0]
            y = orientedRect[0][1]
            w = orientedRect[1][0]
            h = orientedRect[1][1]
            a = orientedRect[2]

            if w > h:
                half1 = ( (x - w/8 + (w/8)*math.sin(-angle), y + (h/4)*math.sin(-angle)), (w/4, h), a )
                half2 = ( (x + w/8 + (w/8)*math.sin(angle), y + (h/4)*math.sin(angle)), (w/4, h), a)
            else:
                half1 = ((x - (w/4)*math.sin(-angle), y - h/8 + (h/8)*math.sin(-angle)), (w, h/4), a)
                half2 = ((x - (w/4)*math.sin(angle), y + h/8 + (h/8)*math.sin(angle)), (w, h/4), a)

            box1 = np.int0(cv2.boxPoints(half1))
            box2 = np.int0(cv2.boxPoints(half2))
            cv2.drawContours(image, [box1], 0, colour, 2)
            cv2.drawContours(image, [box2], 0, colour, 2)

            height, width, _ = image.shape
            mask1 = np.zeros((height, width, 1), np.uint8)
            mask2 = np.zeros((height, width, 1), np.uint8)
            cv2.fillConvexPoly(mask1, box1, 255)
            cv2.fillConvexPoly(mask2, box2, 255)
            first = cv2.bitwise_and(closed, closed, mask=mask1)
            second = cv2.bitwise_and(closed, closed, mask=mask2)

            firstCount = cv2.countNonZero(first)
            secondCount = cv2.countNonZero(second)

            if firstCount < secondCount:
                car_front = (int(half1[0][0]),int(half1[0][1]))
                car_back = (int(half2[0][0]),int(half2[0][1]))
            else:
                car_front = (int(half2[0][0]),int(half2[0][1]))
                car_back = (int(half1[0][0]),int(half1[0][1]))

            fx = car_front[1]
            fy = car_front[0]
            bx = car_back[1]
            by = car_back[0]

            if fx>bx and fy==by:
                car_angle = 0
            elif fx>bx and fy>by:
                car_angle = -a
            elif fx==bx and fy>by:
                car_angle = 90
            elif fx<bx and fy>by:
                car_angle = 90 + -a
            elif fx<bx and fy==by:
                car_angle = 180
            elif fx<bx and fy<by:
                car_angle = 180 + -a
            elif fx==bx and fy<by:
                car_angle = 270
            elif fx>bx and fy<by:
                car_angle = 270 + -a

            cv2.circle(image, car_front, 5, (255, 255, 255), -1)
            linePoint = (int(car_front[0] + 80*math.sin(math.radians(car_angle))), int(car_front[1] + 80*math.cos(math.radians(car_angle))))
            cv2.line(image, car_front, linePoint, colour, 3)

    cv2.imshow("", image)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        return False
    return True


if __name__ == "__main__":
    main()