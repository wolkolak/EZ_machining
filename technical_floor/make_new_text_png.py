import numpy as np
from PIL import Image
from left_zone.D3_interface import restore_zero_position_shell, make_label
import os

#||||||||:  D:\Users\72014\Desktop\EZ_machining-master\technical_floor
father_fold_list = os.getcwd().split('\\')[0:-1]
father_fold = ''
for p in father_fold_list:
    father_fold = father_fold + '\\' + p
father_fold = father_fold[1:] + '\\'
print('father = ', father_fold)

def text_preparation(text, text_size, name_png, father_fold, k=1., black=False):

    if not os.path.exists(father_fold + r'Settings\textTextures\{}.png'.format(name_png)):
        if not os.path.exists(father_fold + r'Settings\textTextures'):
            os.makedirs(father_fold + r'Settings\textTextures')
        lines_of_text = text.splitlines()
        N_lines = lines_of_text.__len__()
        h_of_one_line = int(text_size / N_lines)
        #self.typing_height = 0.4 * N_lines
        len_l = 0
        for l in lines_of_text:
            a = l.__len__()
            if a > len_l:
                len_l = a

        H, W = text_size, int(len_l * text_size * k)  # * 0.35
        I = np.zeros((H, W, 4), dtype=np.ubyte)
        angle = 0
        #os.path.split(...)[0]

        array_L = [np.flip(make_label(textN, father_fold + 'Brave New Era G98.ttf', h_of_one_line, angle=angle), 0) for textN in
                   lines_of_text]
        x0 = W // 2
        # y0 = H // 2
        x = int(x0)

        # y = int(y0)

        def color_text(a, b, c, d):
            def transparentcy(i, j):
                I[i, j, 3] = 255 if I[i, j, 2] != 0 or I[i, j, 1] != 0 or I[i, j, 0] != 0 else 0#color

            I[a:b, c:d, 0] |= (L).astype('ubyte') #R
            #I[a:b, c:d, 1] |= (L).astype('ubyte') #G
            #I[a:b, c:d, 2] |= (L).astype('ubyte') #B
            [transparentcy(i, j) for i in range(a, b) for j in range(c, d)]

        start = 0
        line_gap = 5
        for L in array_L:
            h, w = L.shape
            # раскрашиваем
            color_text(start,
                       start + h,
                       x - w // 2,
                       x - w // 2 + w)

            start = start + h + line_gap

            if black:
                I[:, :, 0] = 0
                I[:, :, 1] = 0
                I[:, :, 2] = 0
            nya = Image.fromarray(I[::1, ::1, ::1], mode='RGBA')
            nya.save(father_fold + r'Settings\textTextures\{}.png'.format(name_png))


text_preparation(text='G112', text_size=50, name_png='G112', father_fold=father_fold, k=1., black=True)