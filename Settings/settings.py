from PyQt5.QtGui import QFont

#interface
default_interface_settings = {'main_width': 1450, 'main_height': 900, 'txt_width': 600}
interface_settings = {'main_width': 1387, 'main_height':817 }
axises = 17
font1 = QFont("Helvetica [Cronyx]", 12)
font2 = QFont("Helvetica [Cronyx]", 12)#QFont.Bold
font3 = QFont("Times", 10, QFont.Bold)
#gui_classes
color1 = 'rgb(145,191,204)'
color2 = 'rgb(72,128,143)'
color3 = 'rgb(47, 69, 82)'
color4 = 'rgb(195,221,234)' #бледный
OpenGL_color_map_RGBA = 0.85, 0.85, 0.8, 1.

OpenGL_color_G1_line = 0.4, 0.8, 0
OpenGL_color_G0_line = 0.9, 1, 0.
OpenGL_color_main_point = 'rgb(145,191,204)'
OpenGL_color_extra1_point = 145, 191, 204
OpenGL_color_extra2_point = 'rgb(145,191,204)'

splitter_parameters = {'lefty': 956, 'righty': 333, 'flag': 1 }
#self.splitter_flag
min_ark_step = 0.5
g_programs_folder = 'D:/Users/72014/Desktop/EZ_machining-master'
scaling_draft_prime = 1000

draft_page_format = {'A0': [1189, 841], 'А1': [841, 594], 'А2': [594, 420], 'А3': [420, 297],
                     'А4': [297, 210], 'А5': [210, 148.5]}

default_machine = 'Modelling_clay/machines/Machine_CBA_Head_Example'
default_processor = 'Modelling_clay/Processors/Fanuc_NT.py'


saved_toolbars = b'\x00\x00\x00\xff\x00\x00\x00\x00\xfd\x00\x00\x00\x00\x00\x00\x05\x1f\x00\x00\x03\r\x00\x00\x00\x04\x00\x00\x00\x04\x00\x00\x00\x08\x00\x00\x00\x08\xfc\x00\x00\x00\x03\x00\x00\x00\x00\x00\x00\x00\x01\xff\xff\xff\xff\x03\x00\x00\x00\x00\x00\x00\x02\xde\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x01\xff\xff\xff\xff\x03\x00\x00\x00\x00\xff\xff\xff\xff\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x02\x00\x00\x00\x00'
