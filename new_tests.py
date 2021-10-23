from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import sys
import time

WINDOW_NAME = "Test"
WINDOW_WIDTH = 300
WINDOW_HEIGHT = 300

# Границы области
Y_MIN, Y_MAX = 0, 300
X_MIN, X_MAX = 0, 300

# цвета в формате RGBA
BACKGROUND_COLOR = (0, 0, 0, 1)
FOREGROUND_COLOR = (0, 1, 0, 1)

POLYGON = [
    (60, 80), (100, 100), (20, 120),
    (40, 200), (60, 20)
]


# получить координаты точек пересечения строк пикселей с ребрами многогранника
def get_cross_row_polygon_coords():
    rows = {}
    # Для каждой строчки пикселей...
    for row_y in range(Y_MIN, Y_MAX):
        rows[row_y] = []

        # ... проверяем каждое ребро полигона на пересечение
        x_prev, y_prev = POLYGON[-1]
        x, y = POLYGON[0]
        for x_next, y_next in POLYGON[1:] + [POLYGON[0]]:
            # Если точки ребра находятся по разные стороны от
            # строки пикселей...
            if (row_y - y) * (row_y - y_next) < 0:
                # И если ребро стоит вертикально
                if x == x_next:
                    # запоминаем координату Х для строчки row_y
                    rows[row_y].append(x)
                else:
                    # Иначе находим точку пересечения, и запоминаем её
                    cross_x = x + (x_next - x) * (row_y - y) / (y_next - y)
                    rows[row_y].append(cross_x)

            # Здесь проверка на локальные макс/мин
            elif row_y == y and (row_y - y_prev) * (row_y - y_next) < 0:
                rows[row_y].append(x)

            # переходим к новому ребру
            x_prev, y_prev = x, y
            x, y = x_next, y_next

    return rows


# Процедура инициализации
def init():
    # Здесь начинается выполнение программы
    # Использовать двойную буферизацию и цвета в формате RGB (Красный, Зеленый, Синий)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
    # Указываем начальный размер окна (ширина, высота)
    glutInitWindowSize(WINDOW_WIDTH, WINDOW_HEIGHT)
    # Указываем начальное положение окна относительно левого верхнего угла экрана
    glutInitWindowPosition(50, 50)
    # Инициализация OpenGl
    glutInit(sys.argv)
    # Создаем окно с заголовком
    glutCreateWindow(WINDOW_NAME)
    # Определяем процедуру, отвечающую за перерисовку
    glutDisplayFunc(draw)

    glClearColor(0.5, 0.5, 0.5, 1)  # Серый цвет для первоначальной закраски
    gluOrtho2D(X_MIN, X_MAX, Y_MIN, Y_MAX)  # Определяем границы рисования по горизонтали и вертикали

    # Запускаем основной цикл
    glutMainLoop()


# устанавливаем цвет по умолчанию
def reset_color():
    global current_color
    current_color = BACKGROUND_COLOR
    glColor3f(*current_color)


# меняем текущий цвет на другой
def switch_color():
    global current_color
    if current_color == BACKGROUND_COLOR:
        current_color = FOREGROUND_COLOR
    else:
        current_color = BACKGROUND_COLOR
    glColor3f(*current_color)


# отрисовка путем построчного разкрашивания
def fill_full():
    glBegin(GL_POINTS)
    # Для каждого пересечения строки с ребром
    for y in POLYGON_PIXELS:
        reset_color()
        polygon_cross_x = iter(sorted(POLYGON_PIXELS[y]))
        next_cross = next(polygon_cross_x, None)
        # закрашиваем все пиксели в строке...
        for x in range(Y_MIN, Y_MAX):
            # ...выбранным для них цветом
            if next_cross is None:
                reset_color()
            elif x >= next_cross:
                next_cross = next(polygon_cross_x, None)
                switch_color()
            glVertex2d(x, y)
            # time.sleep(1)
    reset_color()
    glEnd()


# отрисовка многогранника через инвертирование
def fill_right_inverse():
    glBegin(GL_POINTS)
    for y in POLYGON_PIXELS:
        reset_color()
        for cross_x in sorted(POLYGON_PIXELS[y]):
            switch_color()
            # перекрашиваем пиксели с права налево
            for x in range(Y_MIN, Y_MAX)[::-1]:
                if x <= cross_x:
                    break
                glVertex2d(x, y)
        time.sleep(0.001)
    reset_color()
    glEnd()


# Процедура перерисовки
def draw():
    glClear(GL_COLOR_BUFFER_BIT)  # Очищаем экран и заливаем серым цветом

    glColor3f(*FOREGROUND_COLOR)  # Устанавливаем цвет
    glBegin(GL_LINE_STRIP)  # Начинаем отрисовку последовательными линиями

    # Последовательно от точки к точке отрисовываем контуры полигона
    for x, y in POLYGON + [POLYGON[0]]:
        glVertex2d(x, y)
    glEnd()  # Заканчиваем отрисовку

    ### Выбери функцию
    fill_right_inverse()
    ## или
    # fill_full()

    glutSwapBuffers()  # Выводим все нарисованное в памяти на экран
    glutPostRedisplay()


def input_poly():
    poly = []
    x0, y0 = map(int, input('Введите первую вершину: ').split())
    poly.append((x0, y0))
    x, y = map(int, input('Введите вторую вершину: ').split())
    poly.append((x, y))
    while x != x0 or y != y0:
        print(f'Вводите вершины, закончив начальной вершиной ({x0} {y0}): ')
        x, y = map(int, input().split())
        poly.append((x, y))
    return poly


# Вызываем нашу функцию инициализации
if __name__ == "__main__":
    # Раскомментировать для ввода полигона вручную
    # POLYGON = input_poly()
    # находим пересечения строк с ребрами
    POLYGON_PIXELS = get_cross_row_polygon_coords()
    # задаем начальный цвет
    current_color = BACKGROUND_COLOR
    init()