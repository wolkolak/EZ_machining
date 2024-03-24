DICTshiftsINT = {
    'WHILE':        0,
    'ENDWHILE':     1,
    'ELSE':         2,
    'IF':           3,
    'ELIF':         4,#todo это вообще не нужно для siemens и fanuc
    'ENDIF':        5,
    'REPEATu':      6,
    'UNTIL':        7,
    'LOOP':         8,
    'END_LOOP':     9,
    'FOR':          10,
    'END_FOR':      11,
    'CASE':         12,
    'OF':           13,
    'DEFAULT':      14,
    'IF_THEN':      15,
    'IF_GOTOF':     50,
    'IF_GOTOB':     51,
    'IF_GOTOC':     52,
    'IF_GOTOS':     53,
    'IF_GOTO':      16,
    'GOTO':         17,
    'GOTOC':        18,  # GOTO without error
    'GOTOS':        19,  # to start of the program
    'GOTOB':        20,  # backward direction
    'GOTOF':        21,  # forward direction
    'REPEAT_LB':    22,
    'R = ':         30,
    'LABEL':        41,
    'SUB_PROGRAM':  33,
    'M30':          34,
    'SUB_PROG_START':       35,
    'POLAR':                36,
    'GOTO_FANUC':           37,
    'IF_GOTO_FANUC':        38,
    'MACRO_PROGRAM_FANUC':    39,
    'CYCLE800':               40

}

DICTconstructionsF = {
DICTshiftsINT['WHILE']:     DICTshiftsINT['ENDWHILE'],
DICTshiftsINT['IF']:        DICTshiftsINT['ENDIF'],
DICTshiftsINT['REPEATu']:    DICTshiftsINT['UNTIL'],
DICTshiftsINT['LOOP']:      DICTshiftsINT['END_LOOP'],
DICTshiftsINT['FOR']:       DICTshiftsINT['END_FOR'],
#DICTshiftsINT['CASE']:      DICTshiftsINT['DEFAULT'],
#DICTshiftsINT['REPEAT_LB']: DICTshiftsINT['REPEAT_LB'],
}

DICTconstructionsB = {
DICTshiftsINT['ENDWHILE']:  DICTshiftsINT['WHILE'],
DICTshiftsINT['ENDIF']:     DICTshiftsINT['IF'],
DICTshiftsINT['UNTIL']:     DICTshiftsINT['REPEATu'],
DICTshiftsINT['END_LOOP']:  DICTshiftsINT['LOOP'],
DICTshiftsINT['END_FOR']:   DICTshiftsINT['FOR'],
#DICTshiftsINT['DEFAULT']:   DICTshiftsINT['CASE']
}

DICTconstrucionINTERIM = {
DICTshiftsINT['ELIF']:  DICTshiftsINT['ENDIF'],
DICTshiftsINT['ELSE']:  DICTshiftsINT['ENDIF'],
#DICTshiftsINT['OF']: DICTshiftsINT['DEFAULT'],
}

#1 - Forward, 2 - Backward, 3 - From the start to the end, 4 - Nothing (next line)

# command: [1/2/3/4, [**words to look for]
# IF:   [1, [key_ELIF, key_ELSE, key_ENDIF]]

DICTshift = {

    DICTshiftsINT['WHILE']:     [1, [DICTshiftsINT['ENDWHILE'],]],
    DICTshiftsINT['ENDWHILE']:  [2, [DICTshiftsINT['WHILE'],]],
    DICTshiftsINT['REPEATu']:    [1, [DICTshiftsINT['UNTIL'],]],
    DICTshiftsINT['REPEAT_LB']:    [1, [DICTshiftsINT['LABEL'],]],
    DICTshiftsINT['UNTIL']:     [2, [DICTshiftsINT['REPEATu'],]],
    DICTshiftsINT['LOOP']:      [1, [DICTshiftsINT['END_LOOP'],]],
    DICTshiftsINT['END_LOOP']:  [2, [DICTshiftsINT['LOOP'],]],
    DICTshiftsINT['FOR']:       [1, [DICTshiftsINT['END_FOR'],]],
    DICTshiftsINT['END_FOR']:   [2, [DICTshiftsINT['FOR'],]],

    DICTshiftsINT['IF']:        [1, [DICTshiftsINT['ELIF'], DICTshiftsINT['ELSE'], DICTshiftsINT['ENDIF']]],
    DICTshiftsINT['ELIF']:      [1, [DICTshiftsINT['ELIF'], DICTshiftsINT['ELSE'], DICTshiftsINT['ENDIF']]],
    DICTshiftsINT['ELSE']:      [1, [DICTshiftsINT['ENDIF'],]],
    DICTshiftsINT['ENDIF']:     [3, [None]],
    DICTshiftsINT['CASE']:      [1, [DICTshiftsINT['OF'], DICTshiftsINT['DEFAULT']]],
    DICTshiftsINT['OF']:        [1, [DICTshiftsINT['DEFAULT'],]],#todo mb DELETE, mb correct it in the future
    #'DEFAULT':  [None],
    DICTshiftsINT['DEFAULT']:   [3, [None]],

    DICTshiftsINT['IF_THEN']:   [3, [DICTshiftsINT['LABEL']]],
    DICTshiftsINT['IF_GOTO']:   [3, [DICTshiftsINT['LABEL']]],
    DICTshiftsINT['IF_GOTOF']:   [3, [DICTshiftsINT['LABEL']]],
    DICTshiftsINT['IF_GOTOB']:   [3, [DICTshiftsINT['LABEL']]],
    DICTshiftsINT['IF_GOTOC']:   [3, [DICTshiftsINT['LABEL']]],
    DICTshiftsINT['IF_GOTOS']:   [3, [DICTshiftsINT['LABEL']]],
    DICTshiftsINT['GOTO']:      [3, [DICTshiftsINT['LABEL']]],
    DICTshiftsINT['GOTOC']:     [3, [DICTshiftsINT['LABEL']]],# GOTO without error
    DICTshiftsINT['GOTOS']:     [3, [DICTshiftsINT['LABEL']]],# to start of the prog
    DICTshiftsINT['GOTOB']:     [2, [DICTshiftsINT['LABEL']]],# backward direction
    DICTshiftsINT['GOTOF']:     [1, [DICTshiftsINT['LABEL']]],# forward direction
    DICTshiftsINT['GOTO_FANUC']:      [3, [DICTshiftsINT['LABEL']]],
    DICTshiftsINT['SUB_PROGRAM']:[1, [DICTshiftsINT['LABEL'],]],
    DICTshiftsINT['SUB_PROG_START']:[1, [DICTshiftsINT['LABEL'],]],
    DICTshiftsINT['IF_GOTO_FANUC']:  [3, [DICTshiftsINT['LABEL']]],
    DICTshiftsINT['MACRO_PROGRAM_FANUC']:        [1, [DICTshiftsINT['LABEL'],]],


    DICTshiftsINT['M30']:       [1, [DICTshiftsINT['LABEL'],]],
    #сюда подпрограмму добавить?
    #DICTshiftsINT['R = ']:    [1, [None]],
    #DICTshiftsINT['LABEL']:    [1, [None]],
}

