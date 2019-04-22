

# Calculate line slope given two points
def slope(point_1, point_2):
    return (point_2[1] - point_1[1]) / (point_2[0] - point_1[0])


# Calculate y intersection of a line
def y_intersection(point, m):
    return point[1] - m * point[0]


# Compute intersection point between two lines given slope and y intersection
def line_intersect(m1, q1, m2, q2):

    # Check if the lines are parallel
    if m1 == m2:
        print("These lines are parallel!!!")
        return None

    x = (q2 - q1) / (m1 - m2)
    y = m1 * x + q1

    return int(x), int(y)


# Compute intersection point between two lines
def intersection_point(line_1, line_2):

    m_1 = slope(line_1[0], line_1[1])
    m_2 = slope(line_2[0], line_2[1])

    y_int_1 = y_intersection(line_1[0], m_1)
    y_int_2 = y_intersection(line_2[0], m_2)

    return line_intersect(m_1, y_int_1, m_2, y_int_2)


# print the equation of a line
def find_equation(point_1, point_2):
    m = slope(point_1, point_2)
    c = y_intersection(point_1, m)
    return 'y = ' + str(m) + '*x + ' + str(c)




