import copy

class DICT_with_papa(dict):#dict of lists of lists.
    def __init__(self, np_box):
        super().__init__()
        #print('G_MODAL_DICT')
        #todo Тут нужно поменять на Integer
        self.np_box = np_box
        #self['plane'] = 18    #todo всё это отсюда нужно убрать
        #self['absolute_or_incremental'] = 90
        #self['polar_coord'] = 113
        #self['SC'] = 54       #todo встретив G549 я буду просто зажигать флаг
                              #todo соответствующего G549 в special_options_applying

    def PAPAcopy(self):
        np_ = self.np_box
        self.np_box = None
        new1 = copy.deepcopy(self)
        new1.np_box = np_
        print('PAPAcopy: ', new1)
        return new1

if __name__ == "__main__":
    pass
    #a = DICT_with_papa()

