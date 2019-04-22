import numpy as np
import cv2
import time

line = False
N = 0
COLOUR = (100, 100, 255)
COLOUR_VANISHING = (100, 255, 100)
THICKNESS = 1


def get_lines(im, number_of_lines):

    global N, THICKNESS

    # Set up data to send to mouse handler
    data = {'image': im.copy(), 'number_of_lines': number_of_lines, 'lines': []}

    THICKNESS = max(THICKNESS, int(0.005 * min(data['image'].shape[0], data['image'].shape[1])))

    # Set the callback function for any mouse event
    cv2.namedWindow("Image", cv2.WINDOW_GUI_NORMAL)
    cv2.imshow("Image", im)
    cv2.setMouseCallback("Image", mouse_handler, data)

    # Wait
    while N < number_of_lines:
        cv2.waitKey(1)
    time.sleep(1)
    N = 0

    points = np.array(data['lines'], dtype=float)

    return points


def mouse_handler(event, x, y, flags, data):
    global line, N

    if event == cv2.EVENT_LBUTTONDOWN and line:
        line = False
        data['lines'][-1].append((x, y))  # append the second point
        cv2.circle(data['image'], (x, y), 2, COLOUR, 3*THICKNESS)
        cv2.line(data['image'], data['lines'][-1][0], data['lines'][-1][1], COLOUR, 2*THICKNESS)
        cv2.imshow("Image", data['image'])
        N += 1

    elif event == cv2.EVENT_MOUSEMOVE and line:
        # thi is just for a ine visualization
        image = data['image'].copy()
        cv2.line(image, data['lines'][-1][0], (x, y), COLOUR, 1*THICKNESS)
        cv2.imshow("Image", image)

    elif event == cv2.EVENT_LBUTTONDOWN and len(data['lines']) <= data['number_of_lines']:
        # Draw the first Point
        line = True
        data['lines'].append([(x, y)])  # add the point
        cv2.circle(data['image'], (x, y), 2, COLOUR, 3*THICKNESS, 16)
        cv2.imshow("Image", data['image'])


def draw_vanishing_point(image, vanishing_point):

    cv2.namedWindow("Image", cv2.WINDOW_GUI_NORMAL)
    cv2.circle(image, vanishing_point, 2, COLOUR_VANISHING, 30, 16)
    cv2.imshow("Image", image)


def draw_vanishing_line(image, vanishing_points):

    cv2.namedWindow("Image", cv2.WINDOW_GUI_NORMAL)
    cv2.line(image, vanishing_points[0], vanishing_points[1], COLOUR_VANISHING, 2*THICKNESS)
    cv2.imshow("Image", image)


