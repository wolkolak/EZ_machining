import math, copy
import numpy as np
from mathematic.arithmetic import equation_root, between
from left_zone.ARK_solving import centre_R_ARK
#from mathematic.tragectory import Tragectory_3D_one_direction


def find_center(dot_in1, dot_in2, r):
    #print('rrr = ', r)
    #print('find center, dot1 = {}, dot2 = {}'.format(dot_in1, dot_in2))
    dX = dot_in2[0] - dot_in1[0]
    dY = dot_in2[1] - dot_in1[1]
    C1 = dot_in2[1]**2 - dX**2 - dot_in1[1]**2
    a = -4 * dX**2 - 4 * dY**2
    b = 8 * dX**2 * dot_in2[1] + 4 * C1 * dY
    c = 4 * dX**2 * r**2 - 4 * dX**2 * dot_in2[1]**2 - C1**2
    #print('In find a = {}, b = {}, c = {}'.format(a, b, c))
    #что то здесь не так
    if a == 0:
        return dot_in1, dot_in2
    z1, z2 = equation_root(a, b, c)
    C1 = dot_in2[0] ** 2 - dY ** 2 - dot_in1[0] ** 2
    a = -4 * dY ** 2 - 4 * dX ** 2
    b = 8 * dY ** 2 * dot_in2[0] + 4 * C1 * dX
    c = 4 * dY ** 2 * r ** 2 - 4 * dY ** 2 * dot_in2[0] ** 2 - C1 ** 2
    x1, x2 = equation_root(a, b, c)
    if round((x1 - dot_in1[0])**2 + (z1 - dot_in1[1])**2, 6) == round(r**2, 6):
        #print('equal')
        dot1 = [x1, z1]
        dot2 = [x2, z2]
    else:
        #print('not equal')
        dot1 = [x1, z2]
        dot2 = [x2, z1]
    #print('Center1 = {}, Center2 = {}'.format(dot1, dot2))
    return dot1, dot2


def which_closer(a, b, c, distance:str):
    ka_qwa = (c[1] - a[1])**2 + (c[0] - a[0])**2
    ka_qwb = (c[1] - b[1]) ** 2 + (c[0] - b[0]) ** 2
    if distance == 'close':
        result = a if ka_qwa < ka_qwb else b
    else:
        result = a if ka_qwa > ka_qwb else b
    return result



def line_cirle_itersection(center, radius, K, B):
    # y=Kx+B
    a = 1 + K**2
    b = -2*center[0] + 2*K*B -2*K*center[1]
    c = -radius**2 + (B-center[1])**2 + center[0]**2
    D = b**2 - 4*a*c
    if D < 0:
        print('line_cirle_itersection, D < 0!!!!')
        return None, None
    x1 = (-b-math.sqrt(D))/(2*a)
    x2 = (-b+math.sqrt(D))/(2*a)
    dot1 = [x1, K*x1 + B]
    dot2 = [x2, K*x2 + B]
    return dot1, dot2

def make_Kx_plus_B(dot1, dot2):
    if dot1[1] > dot2[1]:
        dotBig = dot1
        dotSmall = dot2
    else:
        dotBig = dot2
        dotSmall = dot1

    k = (dotBig[1] - dotSmall[1]) / (dotBig[0] - dotSmall[0])
    b = dotSmall[1] - k*dotSmall[0]
    print('make_Kx_plus_B K = {}, b = {}'.format(k, b))
    return k, b

def make_closer_to_center(dot, dotC, R, deltaR):
    dot_ = copy.deepcopy(dot)
    k = deltaR/R
    print('||| dotC = ', dotC)
    print("dot before = {}".format(dot))
    for d in dot_:
        dot_delta0 = (d[0] - dotC[0]) * k
        dot_delta1 = (d[1] - dotC[1]) * k
        d[0] = d[0] - dot_delta0
        d[1] = d[1] - dot_delta1
    print('dot after = {} '.format(dot))
    return dot_

def move_the_dot_V_H(dot, angle, distance):
    #dot: V, H
    print('dot = ', dot)
    angle = math.radians(angle)
    print('angle in rad = ', angle)
    d_V = distance * math.sin(angle)
    d_H = distance * math.cos(angle)
    print('d_V = {}, d_H = {}'.format(d_V, d_H))
    new_dot = [dot[0] + d_V, dot[1] + d_H]
    print('new_dot = ', new_dot)
    return new_dot

def lines_intersection_angles(dot1, angle1, dot2, angle2):
    '''
    :param dot1: [vert, hor]
    :param angle1: from hor
    :param dot2:
    :param angle2:
    :return:
    '''
    print('dot1 = {}, angle1 = {}'.format(dot1, angle1))
    print('dot2 = {}, angle2 = {}'.format(dot2, angle2))
    k1 = math.tan(math.radians(angle1))
    k2 = math.tan(math.radians(angle2))
    b1 = dot1[0] - k1 * dot1[1]
    b2 = dot2[0] - k2 * dot2[1]
    print('first: {} * {} + {} = {}'.format(k1, dot1[0], b1, dot1[1]))
    print('second: {} * {} + {} = {}'.format(k2, dot2[0], b2, dot2[1]))
    cross_1 = (b1 - b2) / (k2 - k1)
    print('cross_0 = ', cross_1)
    cross_0 = k1 * cross_1 + b1
    dot = [cross_0, cross_1]
    print('dot = ', dot)

    return dot



def angle_from_dot_2d(dot1, dot2):#SIC!!!!!!!!!
    # #it has actually some problems and should used for grooves trajectory only. look for angle_from_dot_2d_new instead
    dx = dot2[0] - dot1[0]
    dz = dot2[1] - dot1[1]
    angle = math.atan(dx/dz)
    angle= math.degrees(angle)
    if dx < 0:
        angle = angle + 180
    if dz > 0:
        angle = angle + 180
    return angle


def angle_from_dot_2d_new(dot1, dot2):
    #print('angle_from_dot_2d')
    #print('dot1 = {}, dot2 = {}'.format(dot1, dot2))
    dx = dot2[0] - dot1[0]
    dz = dot2[1] - dot1[1]
    angle = math.atan(dx/dz)
    angle= math.degrees(angle)
    if dx < 0:
        angle = angle + 180
    if dz > 0:
        angle = angle + 180
    return angle

def make_2dot_from_angle(dot1, angle):
    ad = 100
    angle = math.radians(angle)
    tan = math.tan(angle)
    dot2 = [dot1[0] + ad, dot1[1] + tan * ad]
    return dot2

def choose_center(dot1, dot2, g23, r):
    v_iA_ = [np.NAN, np.NAN, 0., 0., 0., 0., 0., 0., 0., 0., np.NAN, np.NAN, np.NAN, np.NAN, np.NAN, np.NAN, np.NAN]
    v_iC_ = [np.NAN, np.NAN, 0., 0., 0., 0., 0., 0., 0., 0., np.NAN, np.NAN, np.NAN, np.NAN, np.NAN, np.NAN, np.NAN]
    v_iA_[4] = dot1[0]; v_iA_[6] = dot1[1]
    v_iC_[4] = dot2[0]; v_iC_[6] = dot2[1]
    v_iC_[13] = r
    if g23 == 'G2' or g23 == '2' or g23 == 2:
        turn_direction = 2.
        print('dot1 = {}, turn_direction = {}'.format(dot1, turn_direction))
    elif g23 == 'G3' or g23 == '3' or g23 == 3:
        turn_direction = 3.
        print('dot2 = {}, turn_direction = {}'.format(dot1, turn_direction))
    else:
        turn_direction = None
    print('v_iA_ = ', v_iA_)
    print('v_iC_ = ', v_iC_)
    print('r = ', r)
    c = centre_R_ARK(turn_direction=turn_direction, plane='18', v_iA=v_iA_, v_iC=v_iC_, n_h=6, n_v=4, n_p=5)
    print('c === ', c)
    c = [c[0], c[2]]
    return c



def line_intersection_segments_by_dots(dot11, dot12, dot21, dot22):#2d dots
    print('line_intersection_segments_by_dots')
    print('444 dot11 = {}, dot12 = {}, dot21 = {}, dot22 = {}'.format(dot11, dot12, dot21, dot22))
    result = None; angl1 = None; angl2 = None
    if not(dot11[0] == dot12[0] and dot11[1] == dot12[1] and dot11[2] == dot12[2]):
        print('ccase1')
        angl1 = angle_from_dot_2d(dot11, dot12)
    if not(dot21[0] == dot12[0] and dot21[1] == dot22[1] and dot21[2] == dot22[2]):
        print('ccase2')
        angl2 = angle_from_dot_2d(dot21, dot22)


    if angl1 is not None and angl2 is not None:
        print('ccase3')
        print('dot11 = {}, angl1 = {}, dot21 = {}, angl2 = {}'.format(dot11, angl1, dot21, angl2))
        intersection = lines_intersection_angles(dot11, angl1, dot21, angl2)
        print('intersection = ', intersection)
        min_dot__1 = min(dot11[0], dot12[0]); max_dot__1 = max(dot11[0], dot12[0])
        min_dot__2 = min(dot21[1], dot22[1]); max_dot__2 = max(dot21[1], dot22[1])
        if min_dot__1 <= intersection[0] <= max_dot__1 and min_dot__2 <= intersection[1] <= max_dot__2:
            result = intersection
    elif angl1 is None and angl2 is not None:
        print('ccase4')
        if check_dot_on_line_2d([dot21, dot22], dot11):
            result = dot11
    elif angl1 is not None and angl2 is None:
        print('ccase5')
        if check_dot_on_line_2d([dot11, dot12], dot21):
            result = dot21
    else:#2 dots is None
        print('ccase6')
        if dot11[0] == dot21 and dot11[1] == dot21[1]:
            result = dot11
    return result

def check_dot_on_line_2d(line, dot):
    angl1 = angle_from_dot_2d(line[0], line[1])
    angl2 = angle_from_dot_2d(line[0], dot)
    result = False
    if angl1 == angl2:
        if line[0][0] <= dot[0][0] <= line[1][0] or line[0][0] >= dot[0][0] >= line[1][0]:
            result = True


def segments_line_cirle_itersection(dot11, dot12, dot_r21, dot_r22, R, direction):
    #print('')
    k, b = make_Kx_plus_B(dot11, dot12)
    print('R = ', R)
    center = choose_center(dot_r21, dot_r22, direction, R)
    #print('dot11 = {}, dot12 = {}, dot_r21 = {}, dot_r22 = {}'.format(dot11, dot12, dot_r21, dot_r22))
    #print('center = ', center)
    intersection1, intersection2 = line_cirle_itersection(center, radius=R, K=k, B=b)
    print('segments_line_cirle_itersection:\n intersection1 = {}, intersection2 = {}'.format(intersection1, intersection2))
    return intersection1, intersection2



def circles_cross(dot_1_c1, dot_2_c1, dot_1_c2, dot_2_c2, R1, R2, g1_23, g2_23):
    print('dot_1_c1 = ', dot_1_c1)
    c1 = choose_center(dot_1_c1, dot_2_c1, g1_23, R1)
    c2 = choose_center(dot_1_c2, dot_2_c2, g2_23, R2)
    print('c1 = {}, c2 = {}'.format(c1, c2))
    c1_new = [0, 0]
    c2_new = [c2[0] - c1[0], c2[1] - c1[1]]
    #print()
    print('c2_new[1] = ', c2_new[1])
    A = - 2 * c2_new[0]
    B = - 2 * c2_new[1]
    C = c2_new[0]**2 + c2_new[1]**2 + R1**2 - R2**2
    new_k = - A / B
    new_b = - C / B
    print('new_b = {}, new_c = {}'.format(new_k, new_b))
    int1, int2 = line_cirle_itersection(c1_new, radius=abs(R1), K=new_k, B=new_b)
    int1 = [int1[0] + c1[0], int1[1] + c1[1]]
    int2 = [int2[0] + c1[0], int2[1] + c1[1]]
    return int1, int2



def sectors_intersection_in_plane(track1, track2, plane):
    """
    Not universal. It will not work here: EZ_machining-master\CNC_generator\icons\sectors_intersection_in_plane_PROBLEM_illustration.png.
    :param track1:
    :param track2:
    :param plane:
    :return:
    """
    print('sectors_intersection_in_plane')
    print('track1 = ', track1)
    print('track2 = ', track2)
    print('plane = ', plane)
    if plane == 'G18':
        plane = 18
    elif plane == 'G17':
        plane = 17
    else:
        plane = 19
    print('track1 = ', track1)
    """Here 2 parts cheeked if crossing"""
    #track = [[x1, y1, z1], [x2, y2, z2], -R, 'G3']
    if plane == 18:
        print('here')
        dot11 = [track1[0][0], track1[0][2]]
        dot12 = [track1[1][0], track1[1][2]]
        dot21 = [track2[0][0], track2[0][2]]
        dot22 = [track2[1][0], track2[1][2]]
        print('|||  dot11 = {}, dot12 = {}, dot21 = {}, dot22 = {}'.format(dot11, dot12, dot21, dot22))
    elif plane == 17:
        print('g17')
        dot11 = [track1[0][0], track1[0][1]]
        dot12 = [track1[1][0], track1[1][1]]
        dot21 = [track2[0][0], track2[0][1]]
        dot22 = [track2[1][0], track2[1][1]]
    else:
        dot11 = [track1[0][1], track1[0][2]]
        dot12 = [track1[1][1], track1[1][2]]
        dot21 = [track2[0][1], track2[0][2]]
        dot22 = [track2[1][1], track2[1][2]]

    print('track1 = ', track1)
    print('track2 = ', track2)
    if track1[1][3] is None and track2[1][3] is None:
        print('case 1')
        print('here dot11 = {}, dot12 = {}, dot21 = {}, dot22 = {}'.format(dot11, dot12, dot21, dot22))
        intersection1, intersection2 = line_intersection_segments_by_dots(dot11, dot12, dot21, dot22), None
        print('case 1 intersection1 = {}, intersection2 = {}'.format(intersection1, intersection2))
    elif track1[1][3] is None and track2[1][3] is not None:
        print('case 2')
        print('here dot11 = {}, dot12 = {}, dot21 = {}, dot22 = {}'.format(dot11, dot12, dot21, dot22))
        print('track2[1][3] = ', track2[1][3])
        print('track2[1][4] = ', track2[1][4])
        intersection1, intersection2 = segments_line_cirle_itersection(dot11=dot11, dot12=dot12, dot_r21=dot21, dot_r22=dot22, R=track2[1][3], direction=track2[1][4])
        print('intersection1 = {}, intersection2 = {}'.format(intersection1, intersection2))
        if not between(intersection1[0], dot21[0], dot22[0]) or not between(intersection1[1], dot21[1], dot22[1]) \
                or not between(intersection1[0], dot11[0], dot12[0]) or not between(intersection1[1], dot11[1], dot12[1]):
            intersection1 = None
        if not between(intersection2[0], dot21[0], dot22[0]) or not between(intersection2[1], dot21[1], dot22[1]) \
                or not between(intersection2[0], dot11[0], dot12[0]) or not between(intersection2[1], dot11[1], dot12[1]):
            intersection2 = None
    elif track1[1][3] is not None and track2[1][3] is None:
        print('case 3')
        #todo between
        intersection1, intersection2 = segments_line_cirle_itersection(dot11=dot21, dot12=dot22, dot_r21=dot11, dot_r22=dot12, R=track1[1][3], direction=track1[1][4])
        if not between(intersection1[0], dot11[0], dot12[0]) or not between(intersection1[1], dot11[1], dot12[1])\
                or not between(intersection1[0], dot21[0], dot22[0]) or not between(intersection1[1], dot21[1], dot22[1]):
            intersection1 = None
        if not between(intersection2[0], dot11[0], dot12[0]) or not between(intersection2[1], dot11[1], dot12[1])\
                or not between(intersection2[0], dot21[0], dot22[0]) or not between(intersection2[1], dot21[1], dot22[1]):
            intersection2 = None
    else:   # here circle intersection
        print('case 4')
        intersection1, intersection2 = circles_cross(dot_1_c1=dot11, dot_2_c1=dot12, dot_1_c2=dot21, dot_2_c2=dot22, R1=track1[1][2], R2=track2[1][2], g1_23=track1[1][3], g2_23=track2[1][3])
        if not between(intersection1[0], dot11[0], dot12[0]) or not between(intersection1[1], dot11[1], dot12[1])\
                or not between(intersection1[0], dot21[0], dot22[0]) or not between(intersection1[1], dot21[1], dot22[1]):
            intersection1 = None
        if not between(intersection2[0], dot11[0], dot12[0]) or not between(intersection2[1], dot11[1], dot12[1])\
                or not between(intersection2[0], dot21[0], dot22[0]) or not between(intersection2[1], dot21[1], dot22[1]):
            intersection2 = None
    #пересечение только
    print('intersection1 = ', intersection1)
    print('intersection2 = ', intersection2)


    return intersection1, intersection2



def GetCirclesIntersect(p1, r1, p2, r2):
    x = p1[0]
    y = p1[1]
    R = r1
    a = p2[0]
    b = p2[1]
    S = r2
    d = math.sqrt((abs(a - x)) ** 2 + (abs(b - y)) ** 2)
    if d > (R + S) or d < (abs(R - S)):
        # print("Two circles have no intersection")
        return None#, None
    elif d == 0:
        # print("Two circles have same center!")
        return None#, None
    else:
        A = (R ** 2 - S ** 2 + d ** 2) / (2 * d)
        h = math.sqrt(R ** 2 - A ** 2)
        x2 = x + A * (a - x) / d
        y2 = y + A * (b - y) / d
        x3 = round(x2 - h * (b - y) / d, 2)
        y3 = round(y2 + h * (a - x) / d, 2)
        x4 = round(x2 + h * (b - y) / d, 2)
        y4 = round(y2 - h * (a - x) / d, 2)
        c1 = [x3, y3]
        c2 = [x4, y4]
        if abs(p1[0] - c1[0]) > abs(p1[0] - c2[0]):
            print('case 1')
            c = c1
        else:
            print('case 2')
            c = c2
        return c