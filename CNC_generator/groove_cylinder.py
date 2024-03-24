import math
from CNC_generator.usefull_funcs import transfer, k_multiplayer, move_ax_along, DrawGrooveGcodeFinish
from CNC_generator.usefull_classes import RTurnTool, CutTurnTool, SharpTurnTool, Turn45Tool, ToolFinishPanel, ToolRoughPanel2
from PyQt5.QtWidgets import QDialog, QCheckBox, QGridLayout, QComboBox, QFrame, QLabel, QTabWidget, QWidget, QLineEdit, QPushButton, QPlainTextEdit
from PyQt5 import QtGui, QtCore
from Gui.little_gui_classes import simple_warning
from CNC_generator.usefull_funcs import move_ax_along
from CNC_generator.proceed import finish_part, semifinish_part, rough_part
from Gui.little_gui_classes import validate_text_digit


class TurnGroove(QFrame):
    def __init__(self, father, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.hide()
        grid = QGridLayout()
        self.setLayout(grid)
        self.father = father
        self.pic_brief = QLabel()
        self.pic_brief.setFixedSize(350, 300)
        self.set_icon('icons/groove0_z1.png')
        grid.addWidget(self.pic_brief, 0, 0, alignment=QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.groove_note = GrooveNote(self)
        grid.addWidget(self.groove_note, 0, 1, alignment=QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)

    def set_icon(self, icon_address):
        ang_im = QtGui.QImage(icon_address)
        ang_im = ang_im.scaled(350, 300, QtCore.Qt.KeepAspectRatio)
        self.pic_brief.setScaledContents(True)
        self.pic_brief.setPixmap(QtGui.QPixmap.fromImage(ang_im))

class GrooveNote(QTabWidget):
    def __init__(self, father, *args, **kwargs):
        super().__init__(*args, **kwargs)
        validate_text_digit(self)
        self.father = father
        self.groove_geometry_item = Groove_Geometry(self)
        self.addTab(self.groove_geometry_item, "Geometry")

        self.groove_strategy_item = Groove_Strategy(self)
        self.addTab(self.groove_strategy_item, 'Strategy')

        self.groove_tool_item = GrooveTool(self)
        self.addTab(self.groove_tool_item, 'Tool')

        self.result = QPlainTextEdit(self)
        self.addTab(self.result, 'Result')
        self.setTabEnabled(3, False)





class ToolRoughPanel(ToolFinishPanel):
    def __init__(self, father, *args, **kwargs):
        super().__init__(father, *args, **kwargs)
        self.tool_chooser.addItem(QtGui.QIcon('icons/turn_passing'), '')
        self.name_lbl.setText('Rough')
        self.tools_list[0].hide()
        self.tools_list = [CutTurnTool(self, 'rough'), RTurnTool(self, 'rough'), SharpTurnTool(self, 'rough'), Turn45Tool(self, 'rough')]
        self.tools_list[0].show()
        for el in self.tools_list:
            self.grid.addWidget(el, 1, 1)



class GrooveTool(QWidget):
    def __init__(self, father, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.father = father
        grid = QGridLayout()
        self.setLayout(grid)
        self.setStyleSheet(' padding-left: 0px; padding-right: 0px')
        self.geometry = self.father.groove_geometry_item
        self.rough = self.father.groove_strategy_item.rough_groove
        self.semifinish = self.father.groove_strategy_item.semi_finish_groove
        self.finish = self.father.groove_strategy_item.finish_groove
        validate_text_digit(self)
        self.rough_groove_panel = ToolRoughPanel(self)
        grid.addWidget(self.rough_groove_panel, 0, 0)



        self.semifinish_groove_panel = ToolFinishPanel(self)
        self.semifinish_groove_panel.name_lbl.setText('Semifinish')
        grid.addWidget(self.semifinish_groove_panel, 1, 0)


        self.finish_groove_panel = ToolFinishPanel(self)
        grid.addWidget(self.finish_groove_panel, 2, 0)

        self.groove_okay = QPushButton('Go')
        self.groove_okay.clicked.connect(self.proceed)
        self.groove_okay.setFixedSize(100, 40)
        grid.addWidget(self.groove_okay, 4, 0, alignment=QtCore.Qt.AlignHCenter)

    def proceed(self):
        if self.geometry.symmetry_check.checkState():
            s_list = self.geometry.symmetry_options.symmetry_list
            for el in s_list:
                if el[2].text_.text() == '':
                    simple_warning('Missing params', 'Geometry need \nmore parameters')
                    return
            if float(s_list[3][2].text_.text()) == float(s_list[4][2].text_.text()):
                simple_warning('Impossible parameters', 'D == d')
                return

        else:  ##############################
            l_list = self.geometry.non_symmetry_options.L_list
            for el in l_list:
                if el[2].text_.text() == '':
                    simple_warning('Missing params', 'Geometry need \nmore parameters')
                    return
            r_list = self.geometry.non_symmetry_options.R_list
            for el in r_list:
                if el[2].text_.text() == '':
                    simple_warning('Missing params', 'Geometry need \nmore parameters')
                    return
            if float(l_list[2][2].text_.text()) == float(r_list[2][2].text_.text()) or float(l_list[2][2].text_.text()) == float(r_list[3][2].text_.text()):
                simple_warning('Impossible parameters', 'D == d')
                return
        result_str = ''

        print('+++ ну +++')
        if self.father.groove_strategy_item.rough_groove.strategy_box.isChecked():
            result_str1 = rough_part(self)
            if result_str1 is not None:
                result_str = result_str + result_str1
        if self.father.groove_strategy_item.semi_finish_groove.strategy_box.isChecked():
            result_str2, r_list, l_list = semifinish_part(self)
            if result_str2 is not None:
                result_str = result_str + result_str2
        if self.father.groove_strategy_item.finish_groove.strategy_box.isChecked():
            result_str3, r_list, l_list = finish_part(self)
            if result_str3 is not None:
                result_str = result_str + result_str3

        if result_str != '':
            self.father.setCurrentIndex(3)
            self.father.setTabEnabled(3, True)
            self.father.result.setPlainText(result_str)
        else:
            simple_warning('Missing operations', 'Zero operations \nchoosed')



class Groove_Geometry(QWidget):
    def __init__(self, father, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.father = father
        self.setFixedWidth(380)
        grid = QGridLayout()
        self.setLayout(grid)
        validate_text_digit(self)
        self.symmetry_options = GeometryProperty(self)
        grid.addWidget(self.symmetry_options, 1, 0)
        self.non_symmetry_options = GeometryPropertyNonSym(self)
        grid.addWidget(self.non_symmetry_options, 1, 0)
        self.symmetry_check = QCheckBox('Symmetry')
        grid.addWidget(self.symmetry_check, 0, 0)
        self.symmetry_check.stateChanged.connect(self.show_time)
        self.symmetry_check.setChecked(True)

    def show_time(self):
        if self.symmetry_check.checkState():
            self.symmetry_options.show()
            self.symmetry_options.Z.changePicture()
            self.non_symmetry_options.hide()

        else:
            self.symmetry_options.hide()
            self.non_symmetry_options.Z.changePicture()
            self.non_symmetry_options.show()

class StrategyShelf(QFrame):
    def __init__(self, father, name, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.father = father
        self.setStyleSheet(' font-size: 15px;')
        self.setFixedSize(350, 150)
        grid = QGridLayout()
        self.setLayout(grid)
        self.strategy_box = QCheckBox(name)
        self.strategy_box.setChecked(True)
        self.strategy_box.stateChanged.connect(self.blinking)
        grid.addWidget(self.strategy_box, 0, 0)

        if name == 'Rough':
            self.accurate = QCheckBox('Accurate')
            grid.addWidget(self.accurate, 0, 1)
            self.el_ = self.accurate
            self.accurate.setChecked(True)
        else:
            self.corrector = QCheckBox('Corrector')
            grid.addWidget(self.corrector, 0, 1)
            self.el_ = self.corrector

        self.X_allowance_lbl = QLabel('R allowance')
        self.X_allowance = QLineEdit('0')
        grid.addWidget(self.X_allowance_lbl, 1, 0)
        grid.addWidget(self.X_allowance, 1, 1)
        self.Z_allowance_lbl = QLabel('Z allowance')
        self.Z_allowance = QLineEdit('0')
        grid.addWidget(self.Z_allowance_lbl, 2, 0)
        grid.addWidget(self.Z_allowance, 2, 1)
        self.thickness_ch = QCheckBox('Thickness')
        self.thickness_ch.stateChanged.connect(self.blinking)
        grid.addWidget(self.thickness_ch, 3, 0)
        self.thickness = QLineEdit('0')
        grid.addWidget(self.thickness, 3, 1)
        self.first = True
        self.blinking()

        self.D_stock = AddStockDiameter(self)
        grid.addWidget(self.D_stock, 0, 2)



    def blinking(self):
        strategy = self.strategy_box.checkState()
        thick = self.thickness_ch.checkState()
        if strategy and thick:
            self.X_allowance.setEnabled(False); self.X_allowance_lbl.setEnabled(False)
            self.Z_allowance.setEnabled(False); self.Z_allowance_lbl.setEnabled(False)
            self.thickness_ch.setEnabled(True); self.thickness.setEnabled(True)
            self.el_.setEnabled(True)
        elif strategy and not thick:
            self.X_allowance.setEnabled(True); self.X_allowance_lbl.setEnabled(True)
            self.Z_allowance.setEnabled(True); self.Z_allowance_lbl.setEnabled(True)
            self.thickness_ch.setEnabled(True); self.thickness.setEnabled(False)
            self.el_.setEnabled(True)
        else:
            self.X_allowance.setEnabled(False); self.X_allowance_lbl.setEnabled(False)
            self.Z_allowance.setEnabled(False); self.Z_allowance_lbl.setEnabled(False)
            self.thickness_ch.setEnabled(False); self.thickness.setEnabled(False)
            self.el_.setEnabled(False)

        if self.first is False:
            name = self.strategy_box.text()
            if strategy:
                letter = True
            else:
                letter = False
            if name == 'Rough':
                self.father.father.groove_tool_item.rough_groove_panel.setEnabled(letter)
            elif name == 'Semi-finish':
                self.father.father.groove_tool_item.semifinish_groove_panel.setEnabled(letter)
            else:
                self.father.father.groove_tool_item.finish_groove_panel.setEnabled(letter)
        self.first = False


class Groove_Strategy(QWidget):
    def __init__(self, father, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.father = father
        grid = QGridLayout()
        validate_text_digit(self)
        self.setLayout(grid)
        self.rough_groove = StrategyShelf(self, 'Rough')
        grid.addWidget(self.rough_groove, 0, 0)
        self.semi_finish_groove = StrategyShelf(self, 'Semi-finish')
        grid.addWidget(self.semi_finish_groove, 1, 0)
        self.finish_groove = StrategyShelf(self, 'Finish')
        self.finish_groove.corrector.clicked.connect(lambda: self.corrector_use_finish(panel=self.father.groove_tool_item.finish_groove_panel))
        grid.addWidget(self.finish_groove, 2, 0)
        self.setStyleSheet(' padding-left: 0px; padding-right: 0px')
        self.rough_groove.X_allowance.setText('1')
        self.rough_groove.Z_allowance.setText('1')
        self.semi_finish_groove.X_allowance.setText('0.5')
        self.semi_finish_groove.Z_allowance.setText('0.5')

    def corrector_use_finish(self, panel):
        tool_panel_B = panel.tools_list[0]
        tool_panel_R = panel.tools_list[1]
        tool_panel_A = panel.tools_list[2]
        if self.finish_groove.corrector.isChecked():
            if tool_panel_B.Bind.currentIndex() != 3:
                tool_panel_B.Bind.setCurrentIndex(2)   #self.Bind.model().item(0).setEnabled(False)
            tool_panel_B.Bind.model().item(0).setEnabled(False)
            tool_panel_B.Bind.model().item(1).setEnabled(False)
            tool_panel_B.Bind.model().item(4).setEnabled(False)
            tool_panel_R.Bind.setCurrentIndex(2)
            tool_panel_R.Bind.setEnabled(False)
            tool_panel_A.Bind.setCurrentIndex(1)
            tool_panel_A.Bind.setEnabled(False)
        else:
            tool_panel_A.Bind.setEnabled(True)
            tool_panel_R.Bind.setEnabled(True)
            tool_panel_B.Bind.model().item(0).setEnabled(True)
            tool_panel_B.Bind.model().item(1).setEnabled(True)
            tool_panel_B.Bind.model().item(4).setEnabled(True)

class GeometryProperty(QFrame):
    def __init__(self, father, *args, **kwargs):
        super().__init__(*args, **kwargs)
        grid = QGridLayout()
        self.setLayout(grid)
        self.father = father
        self.Z = ZClass(self, 'sym')
        grid.addWidget(self.Z, 0, 0)
        self.symmetry_list = [['B', ''], ['b', ''], ['Alpha', ''], ['D', ''], ['d', '']]
        n = 1
        for el in self.symmetry_list:
            el.append(SmallEl(self, el[0], el[1]))
            grid.addWidget(el[2], n, 0)
            n = n + 1
        self.symmetry_list_R_Ch = [['Top', 0, RadiusChamfer(self, 'Top', 0, r'icons\R4.png', r'icons\R_Faska.png')], ['Bot', 0,  RadiusChamfer(self, 'Bot', 0, r'icons\R3.png', r'icons\R_Faska.png')]]#R4.png
        for el in self.symmetry_list_R_Ch:
            grid.addWidget(el[2], n, 0)
            n = n + 1

class GeometryPropertyNonSym(QFrame):
    def __init__(self, father, *args, **kwargs):
        super().__init__(*args, **kwargs)
        grid = QGridLayout()
        self.setLayout(grid)
        self.father = father
        self.Z = ZClass(self, 'nonsym')
        grid.addWidget(self.Z, 0, 0)
        self.setStyleSheet('font-size: 12px;')
        self.left_list_R_Ch = [['Top', 0, RadiusChamfer(self, 'Top L', 0, r'icons\R4.png', r'icons\R_Faska.png')],
                                   ['Bot', 0, RadiusChamfer(self, 'Bot L', 0, r'icons\R3.png', r'icons\R_Faska.png')]]
        self.right_list_R_Ch = [['Top', 0, RadiusChamfer(self, 'Top R', 0, r'icons\R4.png', r'icons\R_Faska.png')],
                                   ['Bot', 0, RadiusChamfer(self, 'Bot R', 0, r'icons\R3.png', r'icons\R_Faska.png')]]
        self.L_list = [['B', ''], ['b', ''], ['d', '']]
        self.R_list = [['Alpha_l', ''], ['Alpha_r', ''], ['D_l', ''], ['D_r', '']]
        n = 1
        for el in self.L_list:
            el.append(SmallElnonSym(self, el[0], el[1]))
            grid.addWidget(el[2], n, 0)
            n = n + 1
        n = 0
        for el in self.R_list:
            el.append(SmallElnonSym(self, el[0], el[1]))
            grid.addWidget(el[2], n, 1)
            n = n + 1
        for el in self.left_list_R_Ch:
            grid.addWidget(el[2], n, 0)
            n = n + 1
        n_= n
        for el in self.left_list_R_Ch:
            el.append(SmallElnonSym(self, el[0], el[1]))
            grid.addWidget(el[2], n, 0)
            n = n + 1
        n = n_
        for el in self.right_list_R_Ch:
            el.append(SmallElnonSym(self, el[0], el[1]))
            grid.addWidget(el[2], n, 1)
            n = n + 1

class ZClass(QFrame):
    def __init__(self, father, typeSym):
        super().__init__()
        self.father = father
        self.type_sym = typeSym
        grid = QGridLayout()
        self.setLayout(grid)
        self.Z_n = QComboBox()
        self.Z_n.currentTextChanged.connect(self.changePicture)
        self.Z_n.addItem('Z1'); self.Z_n.addItem('Z2'); self.Z_n.addItem('Z3')
        self.Z_n.setCurrentIndex(1)
        grid.addWidget(self.Z_n, 0, 0)
        self.Z_value = QLineEdit('0')
        grid.addWidget(self.Z_value, 0, 1)

        validate_text_digit(self)
        self.Z_value.setValidator(self.onlyInt)

    def changePicture(self):
        Z = self.Z_n.currentText()
        if self.type_sym == 'sym':
            if Z == 'Z1':
                self.father.father.father.father.set_icon('icons/groove0_z1.png')
            elif Z == 'Z2':
                self.father.father.father.father.set_icon('icons/groove0_z2.png')
            else:
                self.father.father.father.father.set_icon('icons/groove0_z3.png')
        else:
            if Z == 'Z1':
                self.father.father.father.father.set_icon('icons/groove1_z1.png')
            elif Z == 'Z2':
                self.father.father.father.father.set_icon('icons/groove1_z2.png')
            else:
                self.father.father.father.father.set_icon('icons/groove1_z3.png')


class AddStockDiameter(QFrame):
    def __init__(self, father):
        super().__init__()
        grid = QGridLayout()
        self.setLayout(grid)
        self.father = father

        self.lbl_ch = QCheckBox('Stock D')
        self.lbl_ch.setToolTip('If you need to smooth groove\n to stock D - use it')
        grid.addWidget(self.lbl_ch, 0, 0)

        self.d_stock_value = QLineEdit()
        self.d_stock_value.setEnabled(False)
        grid.addWidget(self.d_stock_value, 0, 1)
        self.lbl_ch.stateChanged.connect(self.upd_d_stock_value)

    def give_new_D(self):
        if self.father.thickness_ch.checkState():
            Xallowance = float(self.father.thickness.text())
        else:
            Xallowance = float(self.father.X_allowance.text())
        Dnew = float(self.d_stock_value.text()) - 2 * Xallowance
        return Dnew


    def upd_d_stock_value(self):
        if self.lbl_ch.checkState():
            self.d_stock_value.setEnabled(True)
        else:
            self.d_stock_value.setEnabled(False)

class RadiusChamfer(QFrame):
    def __init__(self, father, name, value, address_pic1, address_pic2):
        super().__init__()
        self.father = father
        self.lbl = QLabel(name)

        self.text_ = QLineEdit(str(value))
        self.text_.setEnabled(False)

        grid = QGridLayout()
        self.setLayout(grid)
        pic1 = QtGui.QIcon(address_pic1)

        pic2 = QtGui.QIcon(address_pic2)
        self.chooser_r_ch = RChampferChooser(self, pic1, pic2)
        grid.addWidget(self.lbl, 0, 0)
        grid.addWidget(self.chooser_r_ch, 0, 1)
        grid.addWidget(self.text_, 0, 2)

        validate_text_digit(self)
        self.text_.setValidator(self.onlyInt)


class RChampferChooser(QComboBox):
    def __init__(self, father, pic1, pic2, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.father = father
        self.current_text = 'R'
        self.addItem('-')
        self.addItem(pic1, 'R')
        self.addItem(pic2, 'Chamfer Z x45')
        self.update_R_Ch()
        self.currentIndexChanged.connect(self.update_R_Ch)


    def update_R_Ch(self):
        if self.currentIndex() == 0:
            self.current_text = '-'
            self.father.text_.setEnabled(False)
        elif self.currentIndex() == 1:
            self.current_text = 'R'
            self.father.text_.setEnabled(True)
        else:
            self.current_text = 'Chamfer'
            self.father.text_.setEnabled(True)



class SmallEl(QFrame):
    def __init__(self, father, name, d_value):
        super().__init__()
        self.grid = QGridLayout()
        self.setLayout(self.grid)
        self.father = father
        self.lbl = QLabel(name)
        self.text_ = QLineEdit(str(d_value))
        self.text_.textEdited.connect(self.gray_white)
        self.grid.addWidget(self.lbl, 0, 0)
        self.grid.addWidget(self.text_, 0, 1)

        validate_text_digit(self)
        self.text_.setValidator(self.onlyInt)

    def gray_white(self):
        nya = 0
        B = self.father.symmetry_list[nya][2]
        b = self.father.symmetry_list[nya+1][2]
        Alpha = self.father.symmetry_list[nya+2][2]
        D = self.father.symmetry_list[nya+3][2]
        d = self.father.symmetry_list[nya+4][2]

        B_full = True if B.text_.text() != '' and B.text_.isEnabled() else False
        b_full = True if b.text_.text() != '' and b.text_.isEnabled() else False
        Alpha_full = True if Alpha.text_.text() != '' and Alpha.text_.isEnabled() else False
        D_full = True if D.text_.text() != '' and D.text_.isEnabled() else False
        d_full = True if d.text_.text() != '' and d.text_.isEnabled() else False

        if B_full and b_full and Alpha_full and D_full:
            yorick = False
            last_param = d
        elif B_full and b_full and Alpha_full and d_full:
            yorick = False
            last_param = D
        elif B_full and b_full and d_full and D_full:
            yorick = False
            last_param = Alpha
        elif B_full and d_full and Alpha_full and D_full:
            yorick = False
            last_param = b
        elif d_full and b_full and Alpha_full and D_full:
            yorick = False
            last_param = B
        else:
            B.new_state(True, B, b, Alpha, D, d)
            b.new_state(True, B, b, Alpha, D, d)
            Alpha.new_state(True, B, b, Alpha, D, d)
            D.new_state(True, B, b, Alpha, D, d)
            d.new_state(True, B, b, Alpha, D, d)
            #print('4444')
            return
        print('yorick = ', yorick)
        last_param.new_state(yorick, B, b, Alpha, D, d)

    def new_state(self, yorick: bool, B, b, Alpha, D, d):
        self.text_.setEnabled(yorick)
        if yorick is False:
            if self.lbl.text() != 'Alpha':
                my_tg = math.tan(math.radians(float(Alpha.text_.text()) / 2))
            else:
                my_tg = (float(B.text_.text()) - float(b.text_.text())) / (float(D.text_.text()) - float(d.text_.text()))

            if self.lbl.text() == 'B':
                print('D-d = ', float(D.text_.text()) - float(d.text_.text()))
                print('tg = ', my_tg)
                answer = (float(D.text_.text()) - float(d.text_.text())) * my_tg + float(b.text_.text())
            elif self.lbl.text() == 'b':
                answer = float(B.text_.text()) - my_tg * (float(D.text_.text()) - float(d.text_.text()))
            elif self.lbl.text() == 'Alpha':
                answer = math.degrees(float(math.atan(my_tg))) * 2
            elif self.lbl.text() == 'D':
                answer = float(d.text_.text()) + (float(B.text_.text()) - float(b.text_.text())) / my_tg
            elif self.lbl.text() == 'd':
                answer = float(D.text_.text()) - (float(B.text_.text()) - float(b.text_.text())) / my_tg
            else:
                print('AAAAAAA warning. main generator/new state has an error')
            answer = round(answer, 4)
            self.text_.setText(str(answer))

class SmallElnonSym(SmallEl):
    def __init__(self, father, name, d_value):
        super().__init__(father, name, d_value)
        self.grid = QGridLayout()
        self.setLayout(self.grid)

    def gray_white(self):
        nya = 0
        B = self.father.L_list[nya][2]
        b = self.father.L_list[nya+1][2]
        d = self.father.L_list[nya + 2][2]
        Alpha_L = self.father.R_list[nya][2]
        Alpha_R = self.father.R_list[nya+1][2]
        D_l = self.father.R_list[nya+2][2]
        D_r = self.father.R_list[nya+3][2]
        B_full = True if B.text_.text() != '' and B.text_.isEnabled() else False
        b_full = True if b.text_.text() != '' and b.text_.isEnabled() else False
        Alpha_L_full = True if Alpha_L.text_.text() != '' and Alpha_L.text_.isEnabled() else False
        D_l_full = True if D_l.text_.text() != '' and D_l.text_.isEnabled() else False
        d_full = True if d.text_.text() != '' and d.text_.isEnabled() else False
        Alpha_R_full = True if Alpha_R.text_.text() != '' and Alpha_R.text_.isEnabled() else False
        D_r_full = True if D_r.text_.text() != '' and D_r.text_.isEnabled() else False


        if B_full and b_full and Alpha_L_full and Alpha_R_full and D_l_full and D_r_full and d_full:
            yorick = False
            last_param = d
        elif B_full and b_full and Alpha_L_full and Alpha_R_full and D_l_full and d_full:
            yorick = False
            last_param = D_r
        elif B_full and b_full and Alpha_L_full and Alpha_R_full and D_r_full and d_full:
            yorick = False
            last_param = D_l
        elif B_full and b_full and Alpha_L_full and D_l_full and D_r_full and d_full:
            yorick = False
            last_param = Alpha_R
        elif B_full and b_full and Alpha_R_full and D_l_full and D_r_full and d_full:
            yorick = False
            last_param = Alpha_L
        elif B_full and Alpha_L_full and Alpha_R_full and D_l_full and D_r_full and d_full:
            yorick = False
            last_param = b
        elif b_full and Alpha_L_full and Alpha_R_full and D_l_full and D_r_full and d_full:
            yorick = False
            last_param = B
        elif B_full and b_full and Alpha_L_full and Alpha_R_full and D_l_full and D_r_full:
            yorick = False
            last_param = d

        else:
            B.new_state(True, B, b, Alpha_L, Alpha_R, D_l, D_r, d)
            b.new_state(True, B, b, Alpha_L, Alpha_R, D_l, D_r, d)
            Alpha_L.new_state(True, B, b, Alpha_L, Alpha_R, D_l, D_r, d)
            Alpha_R.new_state(True, B, b, Alpha_L, Alpha_R, D_l, D_r, d)
            D_l.new_state(True, B, b, Alpha_L, Alpha_R, D_l, D_r, d)
            D_r.new_state(True, B, b, Alpha_L, Alpha_R, D_l, D_r, d)
            d.new_state(True, B, b, Alpha_L, Alpha_R, D_l, D_r, d)
            print('4444')
            return
        print('yorick = ', yorick)
        last_param.new_state(yorick, B, b, Alpha_L, Alpha_R, D_l, D_r, d)

    def new_state(self, yorick: bool, B, b, Alpha_L, Alpha_R, D_l, D_r, d):
        self.text_.setEnabled(yorick)
        if yorick is False:
            print('self.lbl.text() = ', self.lbl.text())
            if self.lbl.text() == 'Alpha_l':
                my_tg_R = math.tan(math.radians(float(Alpha_R.text_.text())))
                print("B = {}, delta R = {}, my_tg_R = {}, b/2 = {}".format(float(B.text_.text()), (float(D_r.text_.text()) - float(d.text_.text())) / 2, my_tg_R, float(b.text_.text())/2))
                Z_L = float(B.text_.text()) - (float(D_r.text_.text()) - float(d.text_.text())) / 2 * my_tg_R - float(b.text_.text())/2
                my_tg_L = (Z_L - float(b.text_.text()) / 2) / ((float(D_l.text_.text()) - float(d.text_.text())) / 2)
                print('Z_L = ', Z_L)
            else:
                my_tg_L = math.tan(math.radians(float(Alpha_L.text_.text())))
            if self.lbl.text() == 'Alpha_r':
                my_tg_L = math.tan(math.radians(float(Alpha_L.text_.text())))
                Z_R = float(B.text_.text()) - (float(D_l.text_.text()) - float(d.text_.text())) / 2 * my_tg_L - float(b.text_.text()) / 2
                print('Z_R = ', Z_R)
                my_tg_R = (Z_R - float(b.text_.text()) / 2) / ((float(D_r.text_.text()) - float(d.text_.text()))/2)
            else:
                my_tg_R = math.tan(math.radians(float(Alpha_R.text_.text())))
            print('my_tg_R  = {}'.format(my_tg_R))
            print('my_tg_L  = {}'.format(my_tg_L))
            if self.lbl.text() == 'B':
                answer = float(b.text_.text()) + (float(D_l.text_.text()) - float(d.text_.text())) * my_tg_L / 2 + (float(D_r.text_.text()) - float(d.text_.text())) * my_tg_R / 2
            elif self.lbl.text() == 'b':
                answer = float(B.text_.text()) - (float(D_l.text_.text()) - float(d.text_.text())) * my_tg_L / 2 - (float(D_r.text_.text()) - float(d.text_.text())) * my_tg_R / 2
            elif self.lbl.text() == 'Alpha_l':
                answer = math.degrees(math.atan(my_tg_L)) #* 2
            elif self.lbl.text() == 'Alpha_r':
                answer = math.degrees(math.atan(my_tg_R)) #* 2
            elif self.lbl.text() == 'D_l':
                Z_R = my_tg_R * (float(D_r.text_.text()) - float(d.text_.text()))/2 + float(b.text_.text())/2
                Z_L = float(B.text_.text()) - Z_R
                answer = float(d.text_.text()) + 2 * (Z_L - float(b.text_.text()) / 2) / my_tg_L
            elif self.lbl.text() == 'D_r':
                Z_L = my_tg_L * (float(D_l.text_.text()) - float(d.text_.text()))/2 + float(b.text_.text())/2
                Z_R = float(B.text_.text()) - Z_L
                answer = float(d.text_.text()) + 2 * (Z_R - float(b.text_.text()) / 2) / my_tg_R
            elif self.lbl.text() == 'd':
                horizn = float(B.text_.text()) - float(b.text_.text())
                k_l = 1 / my_tg_L;
                k_r = 1 / my_tg_R
                L = (float(D_r.text_.text()) - float(D_l.text_.text())) / 2
                const = L - k_r * horizn
                print('const = ', const)
                print('kr = {}, kl = {}'.format(k_r, k_l))
                x = const / (k_l + k_r)
                print('X = ', x)
                d = float(D_l.text_.text()) + k_l * x * 2
                answer = d
            else:
                print('AAAAAAA warning. main generator/new state has an error')

            answer = round(answer, 4)
            self.text_.setText(str(answer))







