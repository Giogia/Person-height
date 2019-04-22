import cv2


def slope(point_1, point_2):
    return (point_2[1] - point_1[1]) / (point_2[0] - point_1[0])


def y_intersection(point, m):
    return point[1] - m * point[0]


def line_intersect(m1, q1, m2, q2):

    # Check if the lines are parallel
    if m1 == m2:
        print("These lines are parallel!!!")
        return None

    x = (q2 - q1) / (m1 - m2)
    y = m1 * x + q1

    return int(x), int(y)


def intersection_point(line_1, line_2):

    m_1 = slope(line_1[0], line_1[1])
    m_2 = slope(line_2[0], line_2[1])

    y_int_1 = y_intersection(line_1[0], m_1)
    y_int_2 = y_intersection(line_2[0], m_2)

    return line_intersect(m_1, y_int_1, m_2, y_int_2)


def find_equation(a, b):
    m = slope(a, b)
    c = y_intersection(a, m)
    return 'y = ' + str(m) + '*x + ' + str(c)




