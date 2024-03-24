import math

R1=100. #(X)
R2=0. #(Y)
R3=-1. #(Z0)
R4=-5 #(Z1)
#;
R5= 15.    #(R1 geometry)
R6= 12.    #(R2 geometry)
R7= 10.    #(R tool)
R8 = 0.4   #(RendTool)
#;
R9 = 20. #(dots per ring)
R10 = 0.1   #(Z step)
#;
R11 = 1 #(0 - DNO, 1 - otverstie)


R12 = 360./R9#(step angle)
R13 = math.atan(( R5 - R6) / (R3 - R4)) #(ANGLE FASK)
#R13= math.radians(63.13)
print('R13 = ', math.degrees(R13))
R14 = math.sin(math.pi-R13)*R8 #(Z from C_R to contact dot)
R15 = math.cos(math.pi-R13)*R8 #(X from C_R to contact dot)
print('R14 = ', R14)
print('R15 = ', R15)
R16 = 1 / math.tan(R13) * (R8 - R14) - R8 #(Xdelta )

R5 = R5 + R16 #(increace R1 geometry for RendTool)

if (R11 == 1):# GOTO 100
    print('here1')
    R4 = R4 - R8 + R14
    R6 = R6 + R15 + R8
    print('newR4 = ', R4)
else:
    print('here2')
    R6 = R6 + R16


R5 = (R5 - R7)
R6 = (R6 - R7)


#G0 X(R1) Y(R2)
#Z (R3+10.)
#G1 Z (R3)
#X (R5*2)
R17 = (R3)
R18 = 0
R19 = ((R5-R6)/(R17-R4)*R10/R9)#(Rdecrement)
print('R19 = ', R19)
#WHILE (R17-0.5*R10 GE R4) DO1
#R20 = 0. #(LE 360)
#WHILE (R20 LE 360.01-R12) DO2
#
#G1 X(math.cos(R20)*R5*2) Y(math.SIN(R20)*R5) Z(R17)
#R17=(R17-(R10/R9))
#R5=R5-R19
#R20=R20+R12
#END2
#R18=R18+1
#R17=R3-R18*R10
#
#END1
#R20 = 0. #(LE 360)
#R10=R17-R4
#R19 = ((R5-R6)/(R17-R4)*R10/R9)#(Rdecrement)
#WHILE (R20 LE 360.001) DO1
#
#G1 X(math.cos(R20)*R5*2) Y(math.SIN(R20)*R5) Z(R17)
#R17=(R17-(R10/R9))
#R5=R5-R19
#R20=R20+R12
#END1
#