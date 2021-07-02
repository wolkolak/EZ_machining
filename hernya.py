def add_ark_points(self, v, np_num, n_h, n_v, n_p):
    np_line = v[np_num]
    # предыдущие данные
    ph = v[np_num - 1, n_h]  # previous horizontal
    pv = v[np_num - 1, n_v]  # previous vertical
    pp = v[np_num - 1, n_p]  # previous perpendicular
    ch = n_h + 6
    cv = n_v + 6
    cp = n_p + 6
    R = np_line[11]

    # 1 vectors
    OAx = ph - np_line[ch]
    OAy = ph - np_line[cv]

    ABx = np_line[n_h] - ph
    ABy = np_line[n_v] - pv

    # OA = [OAx, OAy]
    # AB = [ABx, ABy]

    # 2 g2 g3
    if np_line[1] == 2:
        AAx = OAy
        AAy = - OAx
    elif np_line[1] == 3:
        AAx = - OAy
        AAy = OAx
    else:
        print('redactor add_ark_points fail')
    # 3 cor gamma
    print('AAx = {}, ABx = {}, AAy = {}, ABy = {}'.format(AAx, ABx, AAy, ABy))
    cos_gamma = (AAx * ABx + AAy * ABy) / (math.sqrt((AAx ** 2 + AAy ** 2) * (ABx ** 2 + ABy ** 2)))
    # 3
    alpha = 2 * math.acos(cos_gamma)
    cos_alpha_segmenta = 1 - 0.5 * ((min_ark_step ** 2) / (R ** 2))
    sin_alpha_segmenta = math.sqrt(1 - cos_alpha_segmenta ** 2)
    alpha_segmenta = math.acos(cos_alpha_segmenta)
    # ищем сколько строк и синусы
    var1 = alpha / alpha_segmenta
    n = math.floor(var1)
    if n < 0:
        print('ТРЕВОООГАА!!! Дальше остаток тоже переделывать')
    # создаем массив
    ark_np_array = np.full((n, 15), np_line)  # axises
    # perpendicular
    print('alpha = ', alpha)
    # L = math.pi * R / 180 * alpha
    # L = min_ark_step * n
    # tg_feta = (np_line[perp] - cp)/L
    # perp_step = min_ark_step * tg_feta
    Lperp = v[np_num, n_p] - v[np_num - 1, n_p]
    perp_step = Lperp / var1  # divide by zero?

    # ark_np_array[: 0] = 22
    # ark_np_array[: 1] = 22
    # заполняем массив
    # print('v.shape = ', v.shape)
    print('ark_np_array.shape = ', ark_np_array.shape)
    ph = ph - ch
    pv = pv - cv

    if np_line[1] == 2:
        for k in range(n - 1):
            new_hor_0 = ph * cos_alpha_segmenta + pv * sin_alpha_segmenta
            ark_np_array[k, n_h] = new_hor_0 + ch
            new_vert_0 = - ph * sin_alpha_segmenta + pv * cos_alpha_segmenta
            ark_np_array[k, n_v] = new_vert_0 + cv
            ph = new_hor_0
            pv = new_vert_0
            ark_np_array[k, n_p] = pp + (k - 1) * perp_step
    elif np_line[1] == 3:
        for k in range(n - 1):
            new_hor_0 = ph * cos_alpha_segmenta - pv * sin_alpha_segmenta
            ark_np_array[k, n_h] = new_hor_0 + ch
            new_vert_0 = ph * sin_alpha_segmenta + pv * cos_alpha_segmenta
            ark_np_array[k, n_v] = new_vert_0 + cv
            ph = new_hor_0
            pv = new_vert_0
            ark_np_array[k, n_p] = pp + (k - 1) * perp_step
    else:
        print('redactor add_ark_points failed')
        # прибавляе
    return np.insert(v, np_num, ark_np_array, axis=0), n
