import numpy as np
import cv2
import time

LINE = False
MESSAGE = False
N = 0
COLOUR_RED = (100, 100, 255)
COLOUR_GREEN = (100, 255, 100)
COLOUR_BLUE = (255, 100, 100)
THICKNESS = 1


def get_lines(im, number_of_lines, message):

    global MESSAGE, N, THICKNESS

    # Set up data to send to mouse handler
    data = {'image': im.copy(), 'message': message, 'number_of_lines': number_of_lines, 'lines': []}

    THICKNESS = max(THICKNESS, int(0.005 * min(data['image'].shape[0], data['image'].shape[1])))

    # Set the callback function for any mouse event
    cv2.namedWindow("Image", cv2.WINDOW_GUI_NORMAL)
    cv2.imshow("Image", im)
    cv2.setMouseCallback("Image", mouse_handler, data)

    # Wait
    while N < number_of_lines:
        cv2.waitKey(1)
    time.sleep(0.00000000000000000000001)

    N = 0
    MESSAGE = False
    cv2.setMouseCallback("Image", lambda *args: None)

    points = np.array(data['lines'], dtype=int)

    if number_of_lines == 1:
        return points[0]

    else:
        return points


def mouse_handler(event, x, y, flags, data):

    global LINE, MESSAGE, N

    # Write message on image
    if event == cv2.EVENT_MOUSEMOVE and not MESSAGE:
        write_message(data['image'].copy(), data['message'])
        MESSAGE = True

    if event == cv2.EVENT_LBUTTONDOWN and LINE:
        LINE = False
        data['lines'][-1].append((x, y))  # append the second point
        cv2.circle(data['image'], (x, y), 2, COLOUR_RED, 3 * THICKNESS)
        cv2.line(data['image'], data['lines'][-1][0], data['lines'][-1][1], COLOUR_RED, 2 * THICKNESS)
        cv2.imshow("Image", data['image'])
        N += 1

    elif event == cv2.EVENT_MOUSEMOVE and LINE:
        # thi is just for a ine visualization
        image = data['image'].copy()
        cv2.line(image, data['lines'][-1][0], (x, y), COLOUR_RED, 1 * THICKNESS)
        cv2.imshow("Image", image)

    elif event == cv2.EVENT_LBUTTONDOWN and len(data['lines']) <= data['number_of_lines']:
        # Draw the first Point
        LINE = True
        data['lines'].append([(x, y)])  # add the point
        cv2.circle(data['image'], (x, y), 2, COLOUR_RED, 3 * THICKNESS, 16)
        cv2.imshow("Image", data['image'])


def write_message(image, message):

    cv2.namedWindow("Image", cv2.WINDOW_GUI_NORMAL)
    cv2.putText(image, message, (int(image.shape[0] / 5), int(image.shape[1] / 2)),
                fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.5*THICKNESS, color=(255, 255, 255), thickness=THICKNESS)
    cv2.imshow("Image", image)


def draw_point(image, point):

    cv2.namedWindow("Image", cv2.WINDOW_GUI_NORMAL)
    cv2.circle(image, tuple(point), 2, COLOUR_GREEN, 30, 16)
    cv2.imshow("Image", image)


def draw_line(image, line, colour=COLOUR_GREEN):

    cv2.namedWindow("Image", cv2.WINDOW_GUI_NORMAL)
    cv2.line(image, tuple(line[0]), tuple(line[1]), colour, 2 * THICKNESS)
    cv2.imshow("Image", image)

