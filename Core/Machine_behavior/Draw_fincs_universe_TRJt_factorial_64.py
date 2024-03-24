from OpenGL.GL import *
import math
import numpy as np
#param_list = []

#from Core.Machine_behavior.machine_transmigrations import return_TR, return_TR_inverse, return_RT, return_RT_inverse, return_R, return_R_inverse, return_T, returnPass
from Core.Machine_behavior.return_func_choser import return_TR, return_TR_inverse, return_RT, return_RT_inverse, return_R, return_R_inverse, return_T, returnPass


def direct_rotate_TransRot(param_list):
    a = param_list[6]
    b = param_list[7]
    c = param_list[8]
    glRotate(c, 0, 0, 1)
    glRotate(b, 0, 1, 0)
    glRotate(a, 1, 0, 0)


def direct_rotate_inverse_TransRot(param_list):
    #print('direct_rotate_inverse')
    a = param_list[6]
    b = param_list[7]
    c = param_list[8]
    glRotate(-c, 0, 0, 1)
    glRotate(b, 0, 1, 0)
    glRotate(a, 1, 0, 0)



def returnPass_TransRot(param_list):#, X, Y, Z
    pass


def return_TR_TransRot(param_list):# ВСЁ это работает верно
    param_list = [-ff for ff in param_list]
    glTranslatef(param_list[0], param_list[1], param_list[2])
    direct_rotate_TransRot(param_list)



def return_TR_inverse_TransRot(param_list):
    param_list = [-ff for ff in param_list]
    glTranslatef(param_list[0], param_list[1], param_list[2])
    direct_rotate_inverse_TransRot(param_list)




def return_RT_TransRot(param_list):
    param_list = [-ff for ff in param_list]
    direct_rotate_TransRot(param_list)
    glTranslatef(param_list[0], param_list[1], param_list[2])



def return_RT_inverse_TransRot(param_list):
    param_list = [-ff for ff in param_list]
    direct_rotate_inverse_TransRot(param_list)
    glTranslatef(param_list[0], param_list[1], param_list[2])



def return_R_TransRot(param_list):
    param_list = [-ff for ff in param_list]
    direct_rotate_TransRot(param_list)



def return_R_inverse_TransRot(param_list):
    param_list = [-ff for ff in param_list]
    direct_rotate_inverse_TransRot(param_list)


def return_T_TransRot(param_list):
    param_list = [-ff for ff in param_list]
    glTranslatef(param_list[0], param_list[1], param_list[2])

    #__________________________________________________________



def direct_rotate(param_list):
    a = param_list[6]
    b = param_list[7]
    c = param_list[8]
    glRotate(a, 1, 0, 0)
    glRotate(b, 0, 1, 0)
    glRotate(c, 0, 0, 1)


def direct_rotate_inverse(param_list):
    #print('direct_rotate_inverse')
    a = param_list[6]
    b = param_list[7]
    c = param_list[8]
    glRotate(a, 1, 0, 0)
    glRotate(b, 0, 1, 0)
    glRotate(-c, 0, 0, 1)#-



def callJaw(jaw_abc, jaw):
    a, b, c = jaw_abc
    glRotate(a, 1, 0, 0)
    glRotate(b, 0, 1, 0)
    glRotate(c, 0, 0, 1)
    glCallList(jaw)
    glRotate(-c, 0, 0, 1)
    glRotate(-b, 0, 1, 0)
    glRotate(-a, 1, 0, 0)


def TRjt(jaw, tier, tier1, tier2, param_list):
    #param_list = [-ff for ff in param_list]
    jaw_abc = param_list[3:6]
    glTranslatef(param_list[0], param_list[1], param_list[2])
    direct_rotate(param_list)
    callJaw(jaw_abc, jaw)
    glCallList(tier)


def inverseTRjt(jaw, tier, tier1, tier2, param_list):

    #param_list = [-ff for ff in param_list]
    jaw_abc = param_list[3:6]
    glTranslatef(param_list[0], param_list[1], param_list[2])
    direct_rotate_inverse(param_list)
    callJaw(jaw_abc, jaw)
    glCallList(tier)


def TRtj(jaw, tier, tier1, tier2, param_list):
    #param_list = [-ff for ff in param_list]
    jaw_abc = param_list[3:6]
    glTranslatef(param_list[0], param_list[1], param_list[2])
    direct_rotate(param_list)
    glCallList(tier)
    callJaw(jaw_abc, jaw)

def inverseTRtj(jaw, tier, tier1, tier2, param_list):
    #param_list = [-ff for ff in param_list]
    jaw_abc = param_list[3:6]
    glTranslatef(param_list[0], param_list[1], param_list[2])
    direct_rotate_inverse(param_list)
    glCallList(tier)
    callJaw(jaw_abc, jaw)

def TjRt(jaw, tier, tier1, tier2, param_list):
    #param_list = [-ff for ff in param_list]
    jaw_abc = param_list[3:6]
    glTranslatef(param_list[0], param_list[1], param_list[2])
    callJaw(jaw_abc, jaw)
    direct_rotate(param_list)
    glCallList(tier)

def inverseTjRt(jaw, tier, tier1, tier2, param_list):
    #param_list = [-ff for ff in param_list]
    jaw_abc = param_list[3:6]
    glTranslatef(param_list[0], param_list[1], param_list[2])
    callJaw(jaw_abc, jaw)
    direct_rotate_inverse(param_list)
    glCallList(tier)

def TjtR(jaw, tier, tier1, tier2, param_list):
    #param_list = [-ff for ff in param_list]
    jaw_abc = param_list[3:6]
    glTranslatef(param_list[0], param_list[1], param_list[2])
    callJaw(jaw_abc, jaw)
    glCallList(tier)
    direct_rotate(param_list)

def inverseTjtR(jaw, tier, tier1, tier2, param_list):
    #param_list = [-ff for ff in param_list]
    jaw_abc = param_list[3:6]
    glTranslatef(param_list[0], param_list[1], param_list[2])
    callJaw(jaw_abc, jaw)
    glCallList(tier)
    direct_rotate_inverse(param_list)


def TtRj(jaw, tier, tier1, tier2, param_list):
    #param_list = [-ff for ff in param_list]
    jaw_abc = param_list[3:6]
    glTranslatef(param_list[0], param_list[1], param_list[2])
    glCallList(tier)
    direct_rotate(param_list)
    callJaw(jaw_abc, jaw)

def inverseTtRj(jaw, tier, tier1, tier2, param_list):
    #param_list = [-ff for ff in param_list]
    jaw_abc = param_list[3:6]
    glTranslatef(param_list[0], param_list[1], param_list[2])
    glCallList(tier)
    direct_rotate_inverse(param_list)
    callJaw(jaw_abc, jaw)

def TtjR(jaw, tier, tier1, tier2, param_list):
    #param_list = [-ff for ff in param_list]
    jaw_abc = param_list[3:6]
    glTranslatef(param_list[0], param_list[1], param_list[2])
    glCallList(tier)
    callJaw(jaw_abc, jaw)
    direct_rotate(param_list)

def inverseTtjR(jaw, tier, tier1, tier2, param_list):
    #param_list = [-ff for ff in param_list]
    jaw_abc = param_list[3:6]
    glTranslatef(param_list[0], param_list[1], param_list[2])
    glCallList(tier)
    callJaw(jaw_abc, jaw)
    direct_rotate_inverse(param_list)


def RTjt(jaw, tier, tier1, tier2, param_list):
    #param_list = [-ff for ff in param_list]
    jaw_abc = param_list[3:6]
    direct_rotate(param_list)
    glTranslatef(param_list[0], param_list[1], param_list[2])
    callJaw(jaw_abc, jaw)
    glCallList(tier)

def inverseRTjt(jaw, tier, tier1, tier2, param_list):
    #param_list = [-ff for ff in param_list]
    jaw_abc = param_list[3:6]
    direct_rotate_inverse(param_list)
    glTranslatef(param_list[0], param_list[1], param_list[2])
    callJaw(jaw_abc, jaw)
    glCallList(tier)


def RTtj(jaw, tier, tier1, tier2, param_list):
    #param_list = [-ff for ff in param_list]
    jaw_abc = param_list[3:6]
    direct_rotate(param_list)
    glTranslatef(param_list[0], param_list[1], param_list[2])
    glCallList(tier)
    callJaw(jaw_abc, jaw)

def inverseRTtj(jaw, tier, tier1, tier2, param_list):
    #param_list = [-ff for ff in param_list]
    jaw_abc = param_list[3:6]
    direct_rotate_inverse(param_list)
    glTranslatef(param_list[0], param_list[1], param_list[2])
    glCallList(tier)
    callJaw(jaw_abc, jaw)

def RjTt(jaw, tier, tier1, tier2, param_list):
    #param_list = [-ff for ff in param_list]
    jaw_abc = param_list[3:6]
    direct_rotate(param_list)
    callJaw(jaw_abc, jaw)
    glTranslatef(param_list[0], param_list[1], param_list[2])
    glCallList(tier)


def inverseRjTt(jaw, tier, tier1, tier2, param_list):
    #param_list = [-ff for ff in param_list]
    jaw_abc = param_list[3:6]
    direct_rotate_inverse(param_list)
    callJaw(jaw_abc, jaw)
    glTranslatef(param_list[0], param_list[1], param_list[2])
    glCallList(tier)


def RjtT(jaw, tier, tier1, tier2, param_list):
    #param_list = [-ff for ff in param_list]
    jaw_abc = param_list[3:6]
    direct_rotate(param_list)
    callJaw(jaw_abc, jaw)
    glCallList(tier)
    glTranslatef(param_list[0], param_list[1], param_list[2])


def inverseRjtT(jaw, tier, tier1, tier2, param_list):
    #param_list = [-ff for ff in param_list]
    jaw_abc = param_list[3:6]
    direct_rotate_inverse(param_list)
    callJaw(jaw_abc, jaw)
    glCallList(tier)
    glTranslatef(param_list[0], param_list[1], param_list[2])


def RtTj(jaw, tier, tier1, tier2, param_list):
    #param_list = [-ff for ff in param_list]
    jaw_abc = param_list[3:6]
    direct_rotate(param_list)
    glCallList(tier)
    glTranslatef(param_list[0], param_list[1], param_list[2])
    callJaw(jaw_abc, jaw)

def inverseRtTj(jaw, tier, tier1, tier2, param_list):
    print('inverseRtTj')
    #param_list = [-ff for ff in param_list]
    jaw_abc = param_list[3:6]
    direct_rotate_inverse(param_list)
    glCallList(tier)
    glTranslatef(param_list[0], param_list[1], param_list[2])
    callJaw(jaw_abc, jaw)


def RtjT(jaw, tier, tier1, tier2, param_list):
    #param_list = [-ff for ff in param_list]
    jaw_abc = param_list[3:6]
    direct_rotate(param_list)
    glCallList(tier)
    callJaw(jaw_abc, jaw)
    glTranslatef(param_list[0], param_list[1], param_list[2])

def inverseRtjT(jaw, tier, tier1, tier2, param_list):
    #param_list = [-ff for ff in param_list]
    jaw_abc = param_list[3:6]
    direct_rotate_inverse(param_list)
    glCallList(tier)
    callJaw(jaw_abc, jaw)
    glTranslatef(param_list[0], param_list[1], param_list[2])


def jTRt(jaw, tier, tier1, tier2, param_list):
    #param_list = [-ff for ff in param_list]
    jaw_abc = param_list[3:6]
    callJaw(jaw_abc, jaw)
    glTranslatef(param_list[0], param_list[1], param_list[2])
    direct_rotate(param_list)
    glCallList(tier)


def inversejTRt(jaw, tier, tier1, tier2, param_list):
    #param_list = [-ff for ff in param_list]
    jaw_abc = param_list[3:6]
    callJaw(jaw_abc, jaw)
    glTranslatef(param_list[0], param_list[1], param_list[2])
    direct_rotate_inverse(param_list)
    glCallList(tier)

def jTtR(jaw, tier, tier1, tier2, param_list):
    #param_list = [-ff for ff in param_list]
    jaw_abc = param_list[3:6]
    callJaw(jaw_abc, jaw)
    glTranslatef(param_list[0], param_list[1], param_list[2])
    glCallList(tier)
    direct_rotate(param_list)

def inversejTtR(jaw, tier, tier1, tier2, param_list):
    #param_list = [-ff for ff in param_list]
    jaw_abc = param_list[3:6]
    callJaw(jaw_abc, jaw)
    glTranslatef(param_list[0], param_list[1], param_list[2])
    glCallList(tier)
    direct_rotate_inverse(param_list)


def jRTt(jaw, tier, tier1, tier2, param_list):
    #param_list = [-ff for ff in param_list]
    jaw_abc = param_list[3:6]
    callJaw(jaw_abc, jaw)
    direct_rotate(param_list)
    glTranslatef(param_list[0], param_list[1], param_list[2])
    glCallList(tier)

def inversejRTt(jaw, tier, tier1, tier2, param_list):
    #param_list = [-ff for ff in param_list]
    jaw_abc = param_list[3:6]
    callJaw(jaw_abc, jaw)
    direct_rotate_inverse(param_list)
    glTranslatef(param_list[0], param_list[1], param_list[2])
    glCallList(tier)



def jRtT(jaw, tier, tier1, tier2, param_list):
    #print('jRtT')
    #param_list = [-ff for ff in param_list]
    jaw_abc = param_list[3:6]
    callJaw(jaw_abc, jaw)
    direct_rotate(param_list)
    glCallList(tier)
    glTranslatef(param_list[0], param_list[1], param_list[2])


def inversejRtT(jaw, tier, tier1, tier2, param_list):
    #print('jRtT')
    #param_list = [-ff for ff in param_list]
    jaw_abc = param_list[3:6]
    callJaw(jaw_abc, jaw)
    direct_rotate_inverse(param_list)
    glCallList(tier)
    glTranslatef(param_list[0], param_list[1], param_list[2])


def jtTR(jaw, tier, tier1, tier2, param_list):
    #param_list = [-ff for ff in param_list]
    jaw_abc = param_list[3:6]
    callJaw(jaw_abc, jaw)
    glCallList(tier)
    glTranslatef(param_list[0], param_list[1], param_list[2])
    direct_rotate(param_list)


def inversejtTR(jaw, tier, tier1, tier2, param_list):
    #param_list = [-ff for ff in param_list]
    jaw_abc = param_list[3:6]
    callJaw(jaw_abc, jaw)
    glCallList(tier)
    glTranslatef(param_list[0], param_list[1], param_list[2])
    direct_rotate_inverse(param_list)

def jtRT(jaw, tier, tier1, tier2, param_list):
    #param_list = [-ff for ff in param_list]
    jaw_abc = param_list[3:6]
    callJaw(jaw_abc, jaw)
    glCallList(tier)
    direct_rotate(param_list)
    glTranslatef(param_list[0], param_list[1], param_list[2])


def inversejtRT(jaw, tier, tier1, tier2, param_list):
    #param_list = [-ff for ff in param_list]
    jaw_abc = param_list[3:6]
    callJaw(jaw_abc, jaw)
    glCallList(tier)
    direct_rotate_inverse(param_list)
    glTranslatef(param_list[0], param_list[1], param_list[2])


def tTRj(jaw, tier, tier1, tier2, param_list):
    #param_list = [-ff for ff in param_list]
    jaw_abc = param_list[3:6]
    glCallList(tier)
    glTranslatef(param_list[0], param_list[1], param_list[2])
    direct_rotate(param_list)
    callJaw(jaw_abc, jaw)


def inversetTRj(jaw, tier, tier1, tier2, param_list):
    #param_list = [-ff for ff in param_list]
    jaw_abc = param_list[3:6]
    glCallList(tier)
    glTranslatef(param_list[0], param_list[1], param_list[2])
    direct_rotate_inverse(param_list)
    callJaw(jaw_abc, jaw)

def tTjR(jaw, tier, tier1, tier2, param_list):
    #param_list = [-ff for ff in param_list]
    jaw_abc = param_list[3:6]
    glCallList(tier)
    glTranslatef(param_list[0], param_list[1], param_list[2])
    callJaw(jaw_abc, jaw)
    direct_rotate(param_list)

def inversetTjR(jaw, tier, tier1, tier2, param_list):
    #param_list = [-ff for ff in param_list]
    jaw_abc = param_list[3:6]
    glCallList(tier)
    glTranslatef(param_list[0], param_list[1], param_list[2])
    callJaw(jaw_abc, jaw)
    direct_rotate_inverse(param_list)

def tRTj(jaw, tier, tier1, tier2, param_list):
    #param_list = [-ff for ff in param_list]
    jaw_abc = param_list[3:6]
    glCallList(tier)
    direct_rotate(param_list)
    glTranslatef(param_list[0], param_list[1], param_list[2])
    callJaw(jaw_abc, jaw)

def inversetRTj(jaw, tier, tier1, tier2, param_list):
    #param_list = [-ff for ff in param_list]
    jaw_abc = param_list[3:6]
    glCallList(tier)
    direct_rotate_inverse(param_list)
    glTranslatef(param_list[0], param_list[1], param_list[2])
    callJaw(jaw_abc, jaw)


def tRjT(jaw, tier, tier1, tier2, param_list):
    #param_list = [-ff for ff in param_list]
    jaw_abc = param_list[3:6]
    glCallList(tier)
    direct_rotate(param_list)
    callJaw(jaw_abc, jaw)
    glTranslatef(param_list[0], param_list[1], param_list[2])

def inversetRjT(jaw, tier, tier1, tier2, param_list):
    #param_list = [-ff for ff in param_list]
    jaw_abc = param_list[3:6]
    glCallList(tier)
    direct_rotate_inverse(param_list)
    callJaw(jaw_abc, jaw)
    glTranslatef(param_list[0], param_list[1], param_list[2])

def tjTR(jaw, tier, tier1, tier2, param_list):
    #param_list = [-ff for ff in param_list]
    jaw_abc = param_list[3:6]
    glCallList(tier)
    callJaw(jaw_abc, jaw)
    glTranslatef(param_list[0], param_list[1], param_list[2])
    direct_rotate(param_list)

def inversetjTR(jaw, tier, tier1, tier2, param_list):
    #param_list = [-ff for ff in param_list]
    jaw_abc = param_list[3:6]
    glCallList(tier)
    callJaw(jaw_abc, jaw)
    glTranslatef(param_list[0], param_list[1], param_list[2])
    direct_rotate_inverse(param_list)

def tjRT(jaw, tier, tier1, tier2, param_list):
    #param_list = [-ff for ff in param_list]
    jaw_abc = param_list[3:6]
    glCallList(tier)
    callJaw(jaw_abc, jaw)
    direct_rotate(param_list)
    glTranslatef(param_list[0], param_list[1], param_list[2])

def inversetjRT(jaw, tier, tier1, tier2, param_list):
    #param_list = [-ff for ff in param_list]
    jaw_abc = param_list[3:6]
    glCallList(tier)
    callJaw(jaw_abc, jaw)
    direct_rotate_inverse(param_list)
    glTranslatef(param_list[0], param_list[1], param_list[2])


def TRj(jaw, tier, tier1, tier2, param_list):
    #param_list = [-ff for ff in param_list]
    jaw_abc = param_list[3:6]
    glTranslatef(param_list[0], param_list[1], param_list[2])
    direct_rotate(param_list)
    callJaw(jaw_abc, jaw)

def inverseTRj(jaw, tier, tier1, tier2, param_list):
    #param_list = [-ff for ff in param_list]
    jaw_abc = param_list[3:6]
    glTranslatef(param_list[0], param_list[1], param_list[2])
    direct_rotate_inverse(param_list)
    callJaw(jaw_abc, jaw)

def TjR(jaw, tier, tier1, tier2, param_list):
    #param_list = [-ff for ff in param_list]
    jaw_abc = param_list[3:6]
    glTranslatef(param_list[0], param_list[1], param_list[2])
    callJaw(jaw_abc, jaw)
    direct_rotate(param_list)

def inverseTjR(jaw, tier, tier1, tier2, param_list):
    #param_list = [-ff for ff in param_list]
    jaw_abc = param_list[3:6]
    glTranslatef(param_list[0], param_list[1], param_list[2])
    callJaw(jaw_abc, jaw)
    direct_rotate_inverse(param_list)


def RTj(jaw, tier, tier1, tier2, param_list):
    #param_list = [-ff for ff in param_list]
    jaw_abc = param_list[3:6]
    direct_rotate(param_list)
    glTranslatef(param_list[0], param_list[1], param_list[2])
    callJaw(jaw_abc, jaw)

def inverseRTj(jaw, tier, tier1, tier2, param_list):
    #param_list = [-ff for ff in param_list]
    jaw_abc = param_list[3:6]
    direct_rotate_inverse(param_list)
    glTranslatef(param_list[0], param_list[1], param_list[2])
    callJaw(jaw_abc, jaw)


def RjT(jaw, tier, tier1, tier2, param_list):
    #param_list = [-ff for ff in param_list]
    jaw_abc = param_list[3:6]
    direct_rotate(param_list)
    callJaw(jaw_abc, jaw)
    glTranslatef(param_list[0], param_list[1], param_list[2])

def inverseRjT(jaw, tier, tier1, tier2, param_list):
    #param_list = [-ff for ff in param_list]
    jaw_abc = param_list[3:6]
    direct_rotate_inverse(param_list)
    callJaw(jaw_abc, jaw)
    glTranslatef(param_list[0], param_list[1], param_list[2])


def jTR(jaw, tier, tier1, tier2, param_list):
    #param_list = [-ff for ff in param_list]
    jaw_abc = param_list[3:6]
    callJaw(jaw_abc, jaw)
    glTranslatef(param_list[0], param_list[1], param_list[2])
    direct_rotate(param_list)

def inversejTR(jaw, tier, tier1, tier2, param_list):
    #param_list = [-ff for ff in param_list]
    jaw_abc = param_list[3:6]
    callJaw(jaw_abc, jaw)
    glTranslatef(param_list[0], param_list[1], param_list[2])
    direct_rotate_inverse(param_list)


def jRT(jaw, tier, tier1, tier2, param_list):
    #param_list = [-ff for ff in param_list]
    jaw_abc = param_list[3:6]
    callJaw(jaw_abc, jaw)
    direct_rotate(param_list)
    glTranslatef(param_list[0], param_list[1], param_list[2])

def inversejRT(jaw, tier, tier1, tier2, param_list):
    #param_list = [-ff for ff in param_list]
    jaw_abc = param_list[3:6]
    callJaw(jaw_abc, jaw)
    direct_rotate_inverse(param_list)
    glTranslatef(param_list[0], param_list[1], param_list[2])


def TRt(jaw, tier, tier1, tier2, param_list):
    #param_list = [-ff for ff in param_list]
    jaw_abc = param_list[3:6]
    glTranslatef(param_list[0], param_list[1], param_list[2])
    direct_rotate(param_list)
    glCallList(tier)


def inverseTRt(jaw, tier, tier1, tier2, param_list):
    #param_list = [-ff for ff in param_list]
    jaw_abc = param_list[3:6]
    glTranslatef(param_list[0], param_list[1], param_list[2])
    direct_rotate_inverse(param_list)
    glCallList(tier)


def TtR(jaw, tier, tier1, tier2, param_list):
    #param_list = [-ff for ff in param_list]
    jaw_abc = param_list[3:6]
    glTranslatef(param_list[0], param_list[1], param_list[2])
    glCallList(tier)
    direct_rotate(param_list)

def inverseTtR(jaw, tier, tier1, tier2, param_list):
    #param_list = [-ff for ff in param_list]
    jaw_abc = param_list[3:6]
    glTranslatef(param_list[0], param_list[1], param_list[2])
    glCallList(tier)
    direct_rotate_inverse(param_list)


def RTt(jaw, tier, tier1, tier2, param_list):
    #param_list = [-ff for ff in param_list]
    jaw_abc = param_list[3:6]
    direct_rotate(param_list)
    glTranslatef(param_list[0], param_list[1], param_list[2])
    glCallList(tier)

def inverseRTt(jaw, tier, tier1, tier2, param_list):
    #param_list = [-ff for ff in param_list]
    jaw_abc = param_list[3:6]
    direct_rotate_inverse(param_list)
    glTranslatef(param_list[0], param_list[1], param_list[2])
    glCallList(tier)



def RtT(jaw, tier, tier1, tier2, param_list):
    #param_list = [-ff for ff in param_list]
    jaw_abc = param_list[3:6]
    direct_rotate(param_list)
    glCallList(tier)
    glTranslatef(param_list[0], param_list[1], param_list[2])

def inverseRtT(jaw, tier, tier1, tier2, param_list):
    #param_list = [-ff for ff in param_list]
    #print('inverseRtT')
    jaw_abc = param_list[3:6]
    direct_rotate_inverse(param_list)
    glCallList(tier)
    glTranslatef(param_list[0], param_list[1], param_list[2])


def tTR(jaw, tier, tier1, tier2, param_list):
    #param_list = [-ff for ff in param_list]
    jaw_abc = param_list[3:6]
    glCallList(tier)
    glTranslatef(param_list[0], param_list[1], param_list[2])
    direct_rotate(param_list)


def inversetTR(jaw, tier, tier1, tier2, param_list):
    #param_list = [-ff for ff in param_list]
    jaw_abc = param_list[3:6]
    glCallList(tier)
    glTranslatef(param_list[0], param_list[1], param_list[2])
    direct_rotate_inverse(param_list)

def tRT(jaw, tier, tier1, tier2, param_list):
    #param_list = [-ff for ff in param_list]
    jaw_abc = param_list[3:6]
    glCallList(tier)
    direct_rotate(param_list)
    glTranslatef(param_list[0], param_list[1], param_list[2])

def inversetRT(jaw, tier, tier1, tier2, param_list):
    #param_list = [-ff for ff in param_list]
    jaw_abc = param_list[3:6]
    glCallList(tier)
    direct_rotate_inverse(param_list)
    glTranslatef(param_list[0], param_list[1], param_list[2])

def tRj(jaw, tier, tier1, tier2, param_list):
    #param_list = [-ff for ff in param_list]
    jaw_abc = param_list[3:6]
    glCallList(tier)
    direct_rotate(param_list)
    callJaw(jaw_abc, jaw)

def inversetRj(jaw, tier, tier1, tier2, param_list):
    #param_list = [-ff for ff in param_list]
    jaw_abc = param_list[3:6]
    glCallList(tier)
    direct_rotate_inverse(param_list)
    callJaw(jaw_abc, jaw)


def tjR(jaw, tier, tier1, tier2, param_list):
    #param_list = [-ff for ff in param_list]
    jaw_abc = param_list[3:6]
    glCallList(tier)
    callJaw(jaw_abc, jaw)
    direct_rotate(param_list)

def inversetjR(jaw, tier, tier1, tier2, param_list):
    #param_list = [-ff for ff in param_list]
    jaw_abc = param_list[3:6]
    glCallList(tier)
    callJaw(jaw_abc, jaw)
    direct_rotate_inverse(param_list)


def Rtj(jaw, tier, tier1, tier2, param_list):
    #param_list = [-ff for ff in param_list]
    jaw_abc = param_list[3:6]
    direct_rotate(param_list)
    glCallList(tier)
    callJaw(jaw_abc, jaw)

def inverseRtj(jaw, tier, tier1, tier2, param_list):
    #param_list = [-ff for ff in param_list]
    jaw_abc = param_list[3:6]
    direct_rotate_inverse(param_list)
    glCallList(tier)
    callJaw(jaw_abc, jaw)


def Rjt(jaw, tier, tier1, tier2, param_list):
    #param_list = [-ff for ff in param_list]
    jaw_abc = param_list[3:6]
    direct_rotate(param_list)
    callJaw(jaw_abc, jaw)
    glCallList(tier)

def inverseRjt(jaw, tier, tier1, tier2, param_list):
    #param_list = [-ff for ff in param_list]
    jaw_abc = param_list[3:6]
    direct_rotate_inverse(param_list)
    callJaw(jaw_abc, jaw)
    glCallList(tier)



def jtR(jaw, tier, tier1, tier2, param_list):
    #param_list = [-ff for ff in param_list]
    jaw_abc = param_list[3:6]
    callJaw(jaw_abc, jaw)
    glCallList(tier)
    direct_rotate(param_list)

def inversejtR(jaw, tier, tier1, tier2, param_list):
    #param_list = [-ff for ff in param_list]
    jaw_abc = param_list[3:6]
    callJaw(jaw_abc, jaw)
    glCallList(tier)
    direct_rotate_inverse(param_list)

def jRt(jaw, tier, tier1, tier2, param_list):
    #param_list = [-ff for ff in param_list]
    jaw_abc = param_list[3:6]
    callJaw(jaw_abc, jaw)
    direct_rotate(param_list)
    glCallList(tier)

def inversejRt(jaw, tier, tier1, tier2, param_list):
    #param_list = [-ff for ff in param_list]
    jaw_abc = param_list[3:6]
    callJaw(jaw_abc, jaw)
    direct_rotate_inverse(param_list)
    glCallList(tier)

def Ttj(jaw, tier, tier1, tier2, param_list):
    #param_list = [-ff for ff in param_list]
    jaw_abc = param_list[3:6]
    glTranslatef(param_list[0], param_list[1], param_list[2])
    glCallList(tier)
    callJaw(jaw_abc, jaw)


def Tjt(jaw, tier, tier1, tier2, param_list):
    #param_list = [-ff for ff in param_list]
    jaw_abc = param_list[3:6]
    glTranslatef(param_list[0], param_list[1], param_list[2])
    callJaw(jaw_abc, jaw)
    glCallList(tier)


def tTj(jaw, tier, tier1, tier2, param_list):
    #param_list = [-ff for ff in param_list]
    jaw_abc = param_list[3:6]
    glCallList(tier)
    glTranslatef(param_list[0], param_list[1], param_list[2])
    callJaw(jaw_abc, jaw)


def tjT(jaw, tier, tier1, tier2, param_list):
    #param_list = [-ff for ff in param_list]
    jaw_abc = param_list[3:6]
    glCallList(tier)
    callJaw(jaw_abc, jaw)
    glTranslatef(param_list[0], param_list[1], param_list[2])


def jTt(jaw, tier, tier1, tier2, param_list):
    #param_list = [-ff for ff in param_list]
    jaw_abc = param_list[3:6]
    callJaw(jaw_abc, jaw)
    glTranslatef(param_list[0], param_list[1], param_list[2])
    glCallList(tier)

def jtT(jaw, tier, tier1, tier2, param_list):
    #param_list = [-ff for ff in param_list]
    jaw_abc = param_list[3:6]
    callJaw(jaw_abc, jaw)
    glCallList(tier)
    glTranslatef(param_list[0], param_list[1], param_list[2])

def TR(jaw, tier, tier1, tier2, param_list):
    #param_list = [-ff for ff in param_list]
    jaw_abc = param_list[3:6]
    glTranslatef(param_list[0], param_list[1], param_list[2])
    direct_rotate(param_list)

def inverseTR(jaw, tier, tier1, tier2, param_list):
    #param_list = [-ff for ff in param_list]
    jaw_abc = param_list[3:6]
    glTranslatef(param_list[0], param_list[1], param_list[2])
    direct_rotate_inverse(param_list)


def RT(jaw, tier, tier1, tier2, param_list):
    #param_list = [-ff for ff in param_list]
    jaw_abc = param_list[3:6]
    direct_rotate(param_list)
    glTranslatef(param_list[0], param_list[1], param_list[2])

def inverseRT(jaw, tier, tier1, tier2, param_list):
    #param_list = [-ff for ff in param_list]
    jaw_abc = param_list[3:6]
    direct_rotate_inverse(param_list)
    glTranslatef(param_list[0], param_list[1], param_list[2])

def Tj(jaw, tier, tier1, tier2, param_list):
    #param_list = [-ff for ff in param_list]
    jaw_abc = param_list[3:6]
    glTranslatef(param_list[0], param_list[1], param_list[2])
    callJaw(jaw_abc, jaw)

def jT(jaw, tier, tier1, tier2, param_list):
    #param_list = [-ff for ff in param_list]
    jaw_abc = param_list[3:6]
    callJaw(jaw_abc, jaw)
    glTranslatef(param_list[0], param_list[1], param_list[2])


def Tt(jaw, tier, tier1, tier2, param_list):
    #param_list = [-ff for ff in param_list]
    jaw_abc = param_list[3:6]
    glTranslatef(param_list[0], param_list[1], param_list[2])
    glCallList(tier)


def tT(jaw, tier, tier1, tier2, param_list):
    #param_list = [-ff for ff in param_list]
    jaw_abc = param_list[3:6]
    glCallList(tier)
    glTranslatef(param_list[0], param_list[1], param_list[2])


def Rj(jaw, tier, tier1, tier2, param_list):
    #param_list = [-ff for ff in param_list]
    #return
    jaw_abc = param_list[3:6]
    direct_rotate(param_list)
    callJaw(jaw_abc, jaw)

def inverseRj(jaw, tier, tier1, tier2, param_list):
    #param_list = [-ff for ff in param_list]
    jaw_abc = param_list[3:6]
    direct_rotate_inverse(param_list)
    callJaw(jaw_abc, jaw)

def jR(jaw, tier, tier1, tier2, param_list):
    #param_list = [-ff for ff in param_list]
    jaw_abc = param_list[3:6]
    callJaw(jaw_abc, jaw)
    direct_rotate(param_list)

def inversejR(jaw, tier, tier1, tier2, param_list):
    #param_list = [-ff for ff in param_list]
    jaw_abc = param_list[3:6]
    callJaw(jaw_abc, jaw)
    direct_rotate_inverse(param_list)

def Rt(jaw, tier, tier1, tier2, param_list):
    #param_list = [-ff for ff in param_list]
    jaw_abc = param_list[3:6]
    direct_rotate(param_list)
    glCallList(tier)

def inverseRt(jaw, tier, tier1, tier2, param_list):
    #param_list = [-ff for ff in param_list]
    jaw_abc = param_list[3:6]
    direct_rotate_inverse(param_list)
    glCallList(tier)

def tR(jaw, tier, tier1, tier2, param_list):
    #param_list = [-ff for ff in param_list]
    jaw_abc = param_list[3:6]
    glCallList(tier)
    direct_rotate(param_list)

def inversetR(jaw, tier, tier1, tier2, param_list):
    #param_list = [-ff for ff in param_list]
    jaw_abc = param_list[3:6]
    glCallList(tier)
    direct_rotate(param_list)

def jt(jaw, tier, tier1, tier2, param_list):
    #param_list = [-ff for ff in param_list]
    jaw_abc = param_list[3:6]
    callJaw(jaw_abc, jaw)
    glCallList(tier)


def tj(jaw, tier, tier1, tier2, param_list):
    #param_list = [-ff for ff in param_list]
    jaw_abc = param_list[3:6]
    glCallList(tier)
    callJaw(jaw_abc, jaw)


def T(jaw, tier, tier1, tier2, param_list):
    #param_list = [-ff for ff in param_list]
    jaw_abc = param_list[3:6]
    glTranslatef(param_list[0], param_list[1], param_list[2])


def R(jaw, tier, tier1, tier2, param_list):
    #param_list = [-ff for ff in param_list]
    jaw_abc = param_list[3:6]
    direct_rotate(param_list)

def inverseR(jaw, tier, tier1, tier2, param_list):
    #param_list = [-ff for ff in param_list]
    jaw_abc = param_list[3:6]
    direct_rotate_inverse(param_list)

def j(jaw, tier, tier1, tier2, param_list):
    #param_list = [-ff for ff in param_list]
    jaw_abc = param_list[3:6]
    callJaw(jaw_abc, jaw)

def t(jaw, tier, tier1, tier2, param_list):
    #param_list = [-ff for ff in param_list]
    jaw_abc = param_list[3:6]
    glCallList(tier)



def HeadTable(jaw, tier, tier1, tier2, param_list):
    #print('HeadTable')
    tier_list = [tier, tier1, tier2]
    jaw_abc = param_list[3:6]

    p_list = [[param_list[0], 0, 0], [0, param_list[1], 0], [0, 0, param_list[2]]]

    #direct_rotate(jaw_abc)
    for n in range(0, 3):
        num = jaw_abc[n]
        glCallList(tier_list[num])
        glTranslatef(*p_list[num])
    glCallList(jaw)


def HeadTableR(jaw, tier, tier1, tier2, param_list):

    tier_list = [tier, tier1, tier2]
    jaw_abc = param_list[3:6]
    tier_abc = param_list[6:9]

    p_list = [[param_list[0], 0, 0], [0, param_list[1], 0], [0, 0, param_list[2]]]

    direct_rotate(param_list)
    for n in range(0, 3):
        num = jaw_abc[n]
        glCallList(tier_list[num])
        glTranslatef(*p_list[num])
    glCallList(jaw)






MACHINE_FUNCTIONS = {
'TRjt': [TRjt, return_RT, return_RT_TransRot],
'TRtj': [TRtj, return_RT, return_RT_TransRot],
'TjRt': [TjRt, return_RT, return_RT_TransRot],
'TjtR': [TjtR, return_RT, return_RT_TransRot],
'TtRj': [TtRj, return_RT, return_RT_TransRot],
'TtjR': [TtjR, return_RT, return_RT_TransRot],
'RTjt': [RTjt, return_TR, return_TR_TransRot],
'RTtj': [RTtj, return_TR, return_TR_TransRot],
'RjTt': [RjTt, return_TR, return_TR_TransRot],
'RjtT': [RjtT, return_TR, return_TR_TransRot],
'RtTj': [RtTj, return_TR, return_TR_TransRot],
'RtjT': [RtjT, return_TR, return_TR_TransRot],
'jTRt': [jTRt, return_RT, return_RT_TransRot],
'jTtR': [jTtR, return_RT, return_RT_TransRot],
'jRTt': [jRTt, return_TR, return_TR_TransRot],
'jRtT': [jRtT, return_TR, return_TR_TransRot],
'jtTR': [jtTR, return_RT, return_RT_TransRot],
'jtRT': [jtRT, return_TR, return_TR_TransRot],
'tTRj': [tTRj, return_RT, return_RT_TransRot],
'tTjR': [tTjR, return_RT, return_RT_TransRot],
'tRTj': [tRTj, return_TR, return_TR_TransRot],
'tRjT': [tRjT, return_TR, return_TR_TransRot],
'tjTR': [tjTR, return_RT, return_RT_TransRot],
'tjRT': [tjRT, return_TR, return_TR_TransRot],
'TRj': [TRj, return_RT, return_RT_TransRot],
'TjR': [TjR, return_RT, return_RT_TransRot],
'RTj': [RTj, return_TR, return_TR_TransRot],
'RjT': [RjT, return_TR, return_TR_TransRot],
'jTR': [jTR, return_RT, return_RT_TransRot],
'jRT': [jRT, return_TR, return_TR_TransRot],
'TRt': [TRt, return_RT, return_RT_TransRot],
'TtR': [TtR, return_RT, return_RT_TransRot],
'RTt': [RTt, return_TR, return_TR_TransRot],
'RtT': [RtT, return_TR, return_TR_TransRot],
'tTR': [tTR, return_RT, return_RT_TransRot],
'tRT': [tRT, return_TR, return_TR_TransRot],
'tRj': [tRj, return_R, return_R_TransRot],
'tjR': [tjR, return_R, return_R_TransRot],
'Rtj': [Rtj, return_R, return_R_TransRot],
'Rjt': [Rjt, return_R, return_R_TransRot],
'jtR': [jtR, return_R, return_R_TransRot],
'jRt': [jRt, return_R, return_R_TransRot],
'Ttj': [Ttj, return_T, return_T_TransRot],
'Tjt': [Tjt, return_T, return_T_TransRot],
'tTj': [tTj, return_T, return_T_TransRot],
'tjT': [tjT, return_T, return_T_TransRot],
'jTt': [jTt, return_T, return_T_TransRot],
'jtT': [jtT, return_T, return_T_TransRot],
'TR': [TR, return_RT, return_RT_TransRot],
'RT': [RT, return_TR, return_TR_TransRot],
'Tj': [Tj, return_T, return_T_TransRot],
'jT': [jT, return_T, return_T_TransRot],
'Tt': [Tt, return_T, return_T_TransRot],
'tT': [tT, return_T, return_T_TransRot],
'Rj': [Rj, return_R, return_R_TransRot],
'jR': [jR, return_R, return_R_TransRot],
'Rt': [Rt, return_R, return_R_TransRot],
'tR': [tR, return_R, return_R_TransRot],
'jt': [jt, returnPass, returnPass_TransRot],
'tj': [tj, returnPass, returnPass_TransRot],
't': [t, returnPass, returnPass_TransRot],
'T': [T, return_T, return_T_TransRot],
'R': [R, return_R, return_R_TransRot],
'j': [j, returnPass, returnPass_TransRot],
'HeadTable': [HeadTable, return_T, return_T_TransRot],
'HeadTableR': [HeadTableR, return_TR, return_TR_TransRot],

'inverse_TRjt': [inverseTRjt, return_RT_inverse, return_RT_inverse_TransRot],
'inverse_TRtj': [inverseTRtj, return_RT_inverse, return_RT_inverse_TransRot],
'inverse_TjRt': [inverseTjRt, return_RT_inverse, return_RT_inverse_TransRot],
'inverse_TjtR': [inverseTjtR, return_RT_inverse, return_RT_inverse_TransRot],
'inverse_TtRj': [inverseTtRj, return_RT_inverse, return_RT_inverse_TransRot],
'inverse_TtjR': [inverseTtjR, return_RT_inverse, return_RT_inverse_TransRot],
'inverse_RTjt': [inverseRTjt, return_TR_inverse, return_TR_inverse_TransRot],
'inverse_RTtj': [inverseRTtj, return_TR_inverse, return_TR_inverse_TransRot],
'inverse_RjTt': [inverseRjTt, return_TR_inverse, return_TR_inverse_TransRot],
'inverse_RjtT': [inverseRjtT, return_TR_inverse, return_TR_inverse_TransRot],
'inverse_RtTj': [inverseRtTj, return_TR_inverse, return_TR_inverse_TransRot],
'inverse_RtjT': [inverseRtjT, return_TR_inverse, return_TR_inverse_TransRot],
'inverse_jTRt': [inversejTRt, return_RT_inverse, return_RT_inverse_TransRot],
'inverse_jTtR': [inversejTtR, return_RT_inverse, return_RT_inverse_TransRot],
'inverse_jRTt': [inversejRTt, return_TR_inverse, return_TR_inverse_TransRot],
'inverse_jRtT': [inversejRtT, return_TR_inverse, return_TR_inverse_TransRot],
'inverse_jtTR': [inversejtTR, return_RT_inverse, return_RT_inverse_TransRot],
'inverse_jtRT': [inversejtRT, return_TR_inverse, return_TR_inverse_TransRot],
'inverse_tTRj': [inversetTRj, return_RT_inverse, return_RT_inverse_TransRot],
'inverse_tTjR': [inversetTjR, return_RT_inverse, return_RT_inverse_TransRot],
'inverse_tRTj': [inversetRTj, return_TR_inverse, return_TR_inverse_TransRot],
'inverse_tRjT': [inversetRjT, return_TR_inverse, return_TR_inverse_TransRot],
'inverse_tjTR': [inversetjTR, return_RT_inverse, return_RT_inverse_TransRot],
'inverse_tjRT': [inversetjRT, return_TR_inverse, return_TR_inverse_TransRot],
'inverse_TRj': [inverseTRj, return_RT_inverse, return_RT_inverse_TransRot],
'inverse_TjR': [inverseTjR, return_RT_inverse, return_RT_inverse_TransRot],
'inverse_RTj': [inverseRTj, return_TR_inverse, return_TR_inverse_TransRot],
'inverse_RjT': [inverseRjT, return_TR_inverse, return_TR_inverse_TransRot],
'inverse_jTR': [inversejTR, return_RT_inverse, return_RT_inverse_TransRot],
'inverse_jRT': [inversejRT, return_TR_inverse, return_TR_inverse_TransRot],
'inverse_TRt': [inverseTRt, return_RT_inverse, return_RT_inverse_TransRot],
'inverse_TtR': [inverseTtR, return_RT_inverse, return_RT_inverse_TransRot],
'inverse_RTt': [inverseRTt, return_TR_inverse, return_TR_inverse_TransRot],
'inverse_RtT': [inverseRtT, return_TR_inverse, return_TR_inverse_TransRot],
'inverse_tTR': [inversetTR, return_RT_inverse, return_RT_inverse_TransRot],
'inverse_tRT': [inversetRT, return_TR_inverse, return_TR_inverse_TransRot],
'inverse_tRj': [inversetRj, return_R_inverse, return_R_inverse_TransRot],
'inverse_tjR': [inversetjR, return_R_inverse, return_R_inverse_TransRot],
'inverse_Rtj': [inverseRtj, return_R_inverse, return_R_inverse_TransRot],
'inverse_Rjt': [inverseRjt, return_R_inverse, return_R_inverse_TransRot],
'inverse_jtR': [inversejtR, return_R_inverse, return_R_inverse_TransRot],
'inverse_jRt': [inversejRt, return_R_inverse, return_R_inverse_TransRot],
'inverse_TR': [inverseTR, return_RT_inverse, return_RT_inverse_TransRot],
'inverse_RT': [inverseRT, return_TR_inverse, return_TR_inverse_TransRot],
'inverse_Rj': [inverseRj, return_R_inverse, return_R_inverse_TransRot],
'inverse_jR': [inversejR, return_R_inverse, return_R_inverse_TransRot],
'inverse_Rt': [inverseRt, return_R_inverse, return_R_inverse_TransRot],
'inverse_tR': [inversetR, return_R_inverse, return_R_inverse_TransRot],
'inverse_R': [inverseR, return_R_inverse, return_R_inverse_TransRot],

}


def ABC_rot(A, B, C):
    glRotate(A, 1, 0, 0)  # A
    glRotate(B, 0, 1, 0)  # B
    glRotate(C, 0, 0, 1)  # C

# total0 = total.dot(C_rotTabl)
# total0 = total0.dot(B_rotTabl)
# total0 = total0.dot(A_rotTabl)
# return total0

def ACB_rot(A, B, C):
    glRotate(A, 1, 0, 0)  # A
    glRotate(C, 0, 0, 1)  # C
    glRotate(B, 0, 1, 0)  # B


# total0 = total.dot(A_rotTabl)
# total0 = total0.dot(C_rotTabl)
# total0 = total0.dot(B_rotTabl)
# return total0

def BAC_rot(A, B, C):
    glRotate(B, 0, 1, 0)  # B
    glRotate(A, 1, 0, 0)  # A
    glRotate(C, 0, 0, 1)  # C

# total0 = total.dot(B_rotTabl)
# total0 = total0.dot(A_rotTabl)
# total0 = total0.dot(C_rotTabl)
# return total0

def BCA_rot(A, B, C):
    glRotate(B, 0, 1, 0)  # B
    glRotate(C, 0, 0, 1)  # C
    glRotate(A, 1, 0, 0)  # A

# total0 = total.dot(B_rotTabl)
# total0 = total0.dot(C_rotTabl)
# total0 = total0.dot(A_rotTabl)
# return total0

def CAB_rot(A, B, C):
    glRotate(C, 0, 0, 1)  # C
    glRotate(A, 1, 0, 0)  # A
    glRotate(B, 0, 1, 0)  # B


# total0 = total.dot(C_rotTabl)
# total0 = total0.dot(A_rotTabl)
# total0 = total0.dot(B_rotTabl)
# return total0

def CBA_rot(A, B, C):
    glRotate(C, 0, 0, 1)  # C
    glRotate(B, 0, 1, 0)  # B
    glRotate(A, 1, 0, 0)  # A

# total0 = total.dot(C_rotTabl)
# total0 = total0.dot(B_rotTabl)
# total0 = total0.dot(A_rotTabl)
# return total0

rot_order_dict = {'xyz': ABC_rot, 'xzy': ACB_rot, 'yxz': BAC_rot, 'yzx': BCA_rot, 'zxy': CAB_rot, 'zyx': CBA_rot}

def order_rotation(order:str, A, B, C):
    #print('order_rotation')
    rot_order_dict[order](A, B, C)
