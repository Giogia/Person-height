import numpy as np
import cv2
import glob


def remove_radial_distortion(image):

    # termination criteria
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

    # prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
    object_p = np.zeros((6 * 7, 3), np.float32)
    object_p[:, :2] = np.mgrid[0:7, 0:6].T.reshape(-1, 2)

    # Arrays to store object points and image points from all the images.
    object_points = []  # 3d point in real world space
    image_points = []  # 2d points in image plane.

    calibration_images = glob.glob('calibration/*.jpg')

    for calibration_image in calibration_images:

        img = cv2.imread(calibration_image)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Find the chess board corners
        ret, corners = cv2.findChessboardCorners(gray, (7, 6), None)

        # If found, add object points, image points (after refining them)
        if ret:
            object_points.append(object_p)

            corners2 = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
            image_points.append(corners2)

            # Draw and display the corners
            # img = cv2.drawChessboardCorners(img, (7, 6), corners2, ret)
            # cv2.imshow('img', img)
            # cv2.waitKey(500)

    cv2.destroyAllWindows()

    ret, mtx, dist, r_vectors, t_vectors = cv2.calibrateCamera(object_points, image_points, gray.shape[::-1], None, None)

    height, width = image.shape[:2]

    new_camera_matrix, roi = cv2.getOptimalNewCameraMatrix(mtx, dist, (width, height), 1, (width, height))

    undistorted_image = cv2.undistort(image, mtx, dist, None, new_camera_matrix)

    # crop the image
    # x, y, width, height = roi
    # undistorted_image = undistorted_image[y:y + height, x:x + width]
    # cv2.imwrite('calibration_result.jpg', undistorted_image)

    return undistorted_image