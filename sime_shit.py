import freetype

import pathlib
# определение пути
#currentDirectory = pathlib.Path('.')
#for currentFile in currentDirectory.iterdir():
#    print(currentFile)

face = freetype.Face("Brave New Era G98.ttf")
face.set_char_size( 0*64 )
face.load_char('S')
bitmap = face.glyph.bitmap
print (bitmap.buffer)