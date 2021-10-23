import

# draft1
def draft(self):
    if self.flag_draft is False:
        return
    a = 'white'
    a = 'nope'
    if a == 'white':
        glColor3f(1,1,1)
    else:
        glColor4f(*OpenGL_color_map_RGBA)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)  # Clear The Screen And The Depth Buffer
    #glLoadIdentity() # Reset The View
    glBindTexture(GL_TEXTURE_2D, self.tex)# this is the texture we will manipulate
    glEnable(GL_TEXTURE_2D)
    glRotate(self.alpha, 0., 0., 1.)
    dz = -1427
    r = self.ratio / self.picratio# screen h/w  // picture h/w
    #print('self.draft_scale ==== ', self.draft_scale)
    k = self.draft_scale#*2
    hor = self.draft_zero_horiz
    vert = self.draft_zero_vert
    if (r < 1):   # screen wider than image
        dy = 1
        dx = r
    elif (r > 1): # screen taller than image
        dx = 1
        dy = 1 / r
    else:
        dx = 1
        dy = 1
    glBegin(GL_QUADS)
    glTexCoord2f(0.0, 0.0); glVertex3f(-k*dx+hor, k*dy+vert, dz)
    glTexCoord2f(1.0, 0.0); glVertex3f(k*dx+hor, k*dy+vert, dz)
    glTexCoord2f(1.0, 1.0); glVertex3f(k*dx+hor, -k*dy+vert, dz)
    glTexCoord2f(0.0, 1.0); glVertex3f(-k*dx+hor, -k*dy+vert, dz)
    glEnd()
    glPointSize(30)
    glBegin(GL_POINTS)
    glColor3f(0.5, 0.5, 0.5)
    glVertex3f(hor, vert, 0.0)
    glColor3f(0.2, 0.5, 0.5)
    glEnd()
    glRotate(-self.alpha, 0., 0., 1.)
    glDisable(GL_TEXTURE_2D)