from OpenGL.GLU import *
from OpenGL.GL import *
import freetype
import numpy as np

#сейчас не исполььзуется

class CharacterSlot:
    def __init__(self, texture, glyph):
        self.texture = texture
        self.textureSize = (glyph.bitmap.width, glyph.bitmap.rows)

        if isinstance(glyph, freetype.GlyphSlot):
            self.bearing = (glyph.bitmap_left, glyph.bitmap_top)
            self.advance = glyph.advance.x
        elif isinstance(glyph, freetype.BitmapGlyph):
            self.bearing = (glyph.left, glyph.top)
            self.advance = None
        else:
            raise RuntimeError('unknown glyph type')

def _get_rendering_buffer(xpos, ypos, w, h, zfix=0.0):
    return np.asarray([
        xpos,     ypos - h, 0, 0,
        xpos,     ypos,     0, 1,
        xpos + w, ypos,     1, 1,
        xpos,     ypos - h, 0, 0,
        xpos + w, ypos,     1, 1,
        xpos + w, ypos - h, 1, 0
    ], np.float32)



def render_text_exact(window, text, x, y, scale, color):
        global shaderProgram
        global Characters
        global VBO
        global VAO

        face = freetype.Face(fontfile)
        face.set_char_size(48 * 64)
        glUniform3f(glGetUniformLocation(shaderProgram, "textColor"),
                    color[0] / 255, color[1] / 255, color[2] / 255)

        glActiveTexture(GL_TEXTURE0)

        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        glBindVertexArray(VAO)
        for c in text:
            ch = Characters[c]
            w, h = ch.textureSize
            w = w * scale
            h = h * scale
            vertices = _get_rendering_buffer(x, y, w, h)

            # render glyph texture over quad
            glBindTexture(GL_TEXTURE_2D, ch.texture)
            # update content of VBO memory
            glBindBuffer(GL_ARRAY_BUFFER, VBO)
            glBufferSubData(GL_ARRAY_BUFFER, 0, vertices.nbytes, vertices)

            glBindBuffer(GL_ARRAY_BUFFER, 0)
            # render quad
            glDrawArrays(GL_TRIANGLES, 0, 6)
            # now advance cursors for next glyph (note that advance is number of 1/64 pixels)
            x += (ch.advance >> 6) * scale

        glBindVertexArray(0)
        glBindTexture(GL_TEXTURE_2D, 0)

        glfw.swap_buffers(window)
        glfw.poll_events()