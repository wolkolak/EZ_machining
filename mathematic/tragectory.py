from mathematic.geometry import find_center, lines_intersection_angles, sectors_intersection_in_plane
from mathematic.arithmetic import equation_root, min_None, max_None
import math

class Tragectory_3D_one_direction(list):
    """Universal tagectory:
    coord_list = [[x1, y1, z1, R, 'G2'], [x2', y2', z2', -R', 'G3'], ...]
    """
    def __init__(self,  iterable, plane, *args, **kwargs):#coord_list,

        super().__init__(item for item in iterable)

        self.plane = plane
        #self.coord3D = coord_list
        self.amount = len(self)
        #R = param['TopFRl'][1] + Radd
        print('Create tragectory: ', self)


    def __setitem__(self, index, item):
        super().__setitem__(index, str(item))

    def insert(self, index, item):
        super().insert(index, str(item))

    def append(self, item):
        super().append(str(item))

    def extend(self, other):
        if isinstance(other, type(self)):
            super().extend(other)
        else:
            super().extend(str(item) for item in other)

    def return_axes(self, x, y, z, ax):
        print('return_axes in: x = {}, y = {}, z = {}, ax = {}'.format(x, y, z, ax))
        """Need ax which normal to plane G17-G19
           Only one place for given ax.
           Take one ax == None. Solve and return it"""
        #G17 - XY, G18 - XZ, G19 - YZ
        dot_first = self[0]; dot_second = self[1]
        if ax == 'x':
            k = 0
        elif ax == 'y':
            k = 1
        else:
            k = 2
        if ax == 'x':
            aax = x
        elif ax == 'y':
            aax = y
        else:
            aax = z
        print('SELF = ', self)
        print("X = {}, dot_first = {}, dot_second = {}".format(x, dot_first, dot_second))
        #print("type(dot_second[k]) = ", type(dot_second[k]))
        #direction = 1 if dot_second[k] - dot_first[k] >= 0 else -1
        direction = 1 if self[-1][k] - self[0][k] >= 0 else -1
        print('self.amount = ', self.amount)
        print('direction is ', direction)
        print('aax = ', aax)
        for n in range(self.amount):
            print('self[n][k] = {}, n = {}'.format(self[n][k], n))
            if self[n][k] * direction >= aax * direction:
                print('here might be a problem. I asked if {} > {}'.format(self[n][k] * direction, aax * direction))
                dot_first = self[n-1]; dot_second = self[n]
                break

        print("AFTER dot_first = {}, dot_second = {} ".format(dot_first, dot_second))
        print('dot_second[4] = ', dot_second[4])
        if dot_second[4] == 'G2' or dot_second[4] == 'G3':
            print('mygodness')
            side = 'right' if dot_second[3] > 0 and dot_second[4] == 'G2' or dot_second[3] < 0 and dot_second[4] == 'G3' else 'left'#todo по R и G2
            #side = 'small' if dot_second[3] > 0 and dot_second[4] == 'G2' or dot_second[3] < 0 and dot_second[4] == 'G3' else 'big'
            if self.plane == 'G17':#XY
                dotC1, dotC2 = find_center([dot_first[0], dot_first[1]], [dot_second[0], dot_second[1]], r=abs(dot_second[3]))
                multy = check_is_center_at_right(dotC1, [dot_first[0], dot_first[1]], [dot_second[0], dot_second[1]])
                dotC1 = [dotC1[0], dotC1[1], None]; dotC2 = [dotC2[0], dotC2[1], None]
                dotC_finish = dotC1 if multy < 0 and side == 'left' or multy > 0 and side == 'right' else dotC2
                # https://habr.com/ru/post/148325/
                #    dotC_finish = dotC1 if D < 0 and side == 'right' else dotC2
                if ax == 'x':
                    AX_1, AX_2 = equation_root(a=1, b=-2 * dotC_finish[1], c=dotC_finish[0] ** 2 + dotC_finish[1] ** 2 + x ** 2 - dotC_finish[0] * x * 2 - dot_second[3] ** 2)
                    y = AX_1; y2 = AX_2; x2 = None; z2 = None
                else:
                    AX_1, AX_2 = equation_root(a=1, b=-2 * dotC_finish[0], c=dotC_finish[1] ** 2 + dotC_finish[0] ** 2 + y ** 2 - dotC_finish[1] * y * 2 - dot_second[3] ** 2)
                    x = AX_1; x2 = AX_2; y2 = None; z2 = None
            elif self.plane == 'G18':#XZ
                print('G18 here')
                print('dot_first = {}, dot_second = {}'.format(dot_first, dot_second))
                dotC1, dotC2 = find_center([dot_first[0], dot_first[2]], [dot_second[0], dot_second[2]], r=abs(dot_second[3]))
                print('dotC1 = {}, dotC2 = {}'.format(dotC1, dotC2))
                multy = check_is_center_at_right(dotC1, [dot_first[0], dot_first[2]], [dot_second[0], dot_second[2]])
                dotC1 = [dotC1[0], 0, dotC1[1]]; dotC2 = [dotC2[0], 0, dotC2[1]]
                dotC_finish = dotC1 if multy < 0 and side == 'left' or multy > 0 and side == 'right' else dotC2
                if ax == 'x':
                    print('ggggggggg')
                    print('dotC_finish = ', dotC_finish)
                    print('dotC_finish[0] = {}, dotC_finish[2] = {}, dot_second[3] = {}'.format(dotC_finish[0], dotC_finish[2], dot_second[3]))
                    AX_1, AX_2 = equation_root(a=1, b=-2 * dotC_finish[2], c=dotC_finish[0] ** 2 + dotC_finish[2] ** 2 + x ** 2 - dotC_finish[0] * x * 2 - dot_second[3] ** 2)
                    z = AX_1; z2 = AX_2; x2 = None; y2 = None
                else:
                    AX_1, AX_2 = equation_root(a=1, b=-2 * dotC_finish[0], c=dotC_finish[2] ** 2 + dotC_finish[0] ** 2 + z ** 2 - dotC_finish[2] * z * 2 - dot_second[3] ** 2)
                    x = AX_1; x2 = AX_2; z2 = None; y2 = None

            else:#G19 YZ
                print('Вычисляем G19')
                dotC1, dotC2 = find_center([dot_first[1], dot_first[2]], [dot_second[1], dot_second[2]], r=abs(dot_second[3]))
                multy = check_is_center_at_right(dotC1, [dot_first[1], dot_first[2]], [dot_second[1], dot_second[2]])
                dotC1 = [None, dotC1[0], dotC1[1]]; dotC2 = [None, dotC2[0], dotC2[1]]
                dotC_finish = dotC1 if multy < 0 and side == 'left' or multy > 0 and side == 'right' else dotC2
                if ax == 'y':
                    AX_1, AX_2 = equation_root(a=1, b=-2 * dotC_finish[2], c=dotC_finish[1] ** 2 + dotC_finish[2] ** 2 + y ** 2 - dotC_finish[1] * y * 2 - dot_second[3] ** 2)
                    z = AX_1; z2 = AX_2; y2 = None; x2 = None
                else:
                    AX_1, AX_2 = equation_root(a=1, b=-2 * dotC_finish[1], c=dotC_finish[2] ** 2 + dotC_finish[1] ** 2 + z ** 2 - dotC_finish[2] * z * 2 - dot_second[3] ** 2)
                    y = AX_1; y2 = AX_2; z2 = None; x2 = None
        else:
            delta = dot_second[k] - dot_first[k]
            #print('X in return axes: ', x)
            print('WTF dot_second[k] = ', dot_second[k])
            print('delta = ', delta)
            if delta == 0.:
                x2 = None; y2 = None; z2 = None
                return dot_second[0], dot_second[1], dot_second[2], x2, y2, z2

            k_delta = (aax - dot_first[k]) / delta
            print('chamfer in tragectory: ', ax)
            if ax == 'x':
                print('xX')
                print('dot_first = ', dot_first)
                print('dot_second = ', dot_second)
                y = dot_first[1] + k_delta * (dot_second[1] - dot_first[1])
                z = dot_first[2] + k_delta * (dot_second[2] - dot_first[2])
                print('ZzZ = ', z)
            elif ax == 'y':
                x = dot_first[0] + k_delta * (dot_second[0] - dot_first[0])
                z = dot_first[2] + k_delta * (dot_second[2] - dot_first[2])
            else:
                x = dot_first[0] + k_delta * (dot_second[0] - dot_first[0])
                y = dot_first[1] + k_delta * (dot_second[1] - dot_first[1])
            x2 = None; y2 = None; z2 = None
            print('all in ', self)
            print('dot_first = {}, dot_second = {}'.format(dot_first, dot_second))
            print('k_delta = {}, x = {}, z = {}'.format(k_delta, x, z))
        return x, y, z, x2, y2, z2

    def line_cross_tragectory_(self, dot1, dot2, plane):
        print('line_cross_tragectory_   dot1 = ', dot1)
        intersection1, intersection2 = None, None
        temporary_tragectory = [[*dot1, None, None], [*dot2, None, None]]
        ##track = [[x1, y1, z1], [x2, y2, z2], -R, 'G3']
        print('temporary_tragectory: ', temporary_tragectory)
        print('self = ', self)
        for nya in range(1, len(self)):
            track2 = [self[nya-1], self[nya]]
            print('||=||track2 = ', track2)
            if track2[0][0] == track2[1][0] and track2[0][1] == track2[1][1] and track2[0][2] == track2[1][2]:
                print('continue 2')
                continue
            print('line_cross_tragectory_22')
            print('temporary_tragectory: ', temporary_tragectory)
            print('track2 = ', track2)
            intersection1, intersection2 = sectors_intersection_in_plane(temporary_tragectory, track2, plane)
            print('line_cross_tragectory_: intersection1 = {}, intersection2 = {}'.format(intersection1, intersection2))
            if intersection1 is not None or intersection2 is not None:
                break
        #какую взять
        print('__________________________________')
        return intersection1, intersection2










def check_is_center_at_right(center, dot1, dot2):
    #   dot1=[hh, vv] dot2=[hh, vv] center=[hh, vv]
    print('                         check_is_center_at_right:')
    print('center = {}, dot1 = {}, dot2 = {}'.format(center, dot1, dot2))
    dx = dot2[0] - dot1[0]; dy = dot2[1] - dot1[1]
    dcx = center[0] - dot1[0]; dcy = center[1] - dot1[1]
    #косое произведение векторов если +, то left
    multy = dx*dcy - dcx*dy

    #if multy > 0:
    #    result = False
    #else:
    #    result = True
    return multy
