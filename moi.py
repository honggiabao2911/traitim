import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import math, random, time

# ======================
# Trái tim lấp lánh
# ======================
def heart_points(n=5000):
    points = []
    for _ in range(n):
        t = random.uniform(0, math.pi)
        x = 16 * math.sin(t)**3
        y = 13*math.cos(t) - 5*math.cos(2*t) - 2*math.cos(3*t) - math.cos(4*t)
        points.append((x/20, y/20))
    return points

# ======================
# Render text
# ======================
def draw_text(text, x, y, z=0, scale=0.002):
    glPushMatrix()
    glTranslatef(x, y, z)
    glScalef(scale, scale, scale)
    for ch in text:
        glutStrokeCharacter(GLUT_STROKE_ROMAN, ord(ch))
    glPopMatrix()

# ======================
# Main
# ======================
def main():
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.load("nhac.mp3")
    pygame.mixer.music.play(-1)

    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

    gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)
    glTranslatef(0.0, 0.0, -5)

    heart = heart_points()
    particles = [[random.uniform(-1,1), -1.5, random.uniform(-1,1)] for _ in range(200)]
    angle = 0
    start_time = time.time()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Hiệu ứng tim đập
        scale = 1 + 0.05*math.sin((time.time()-start_time)*5)
        glColor3f(0.7, 0.9, 1.0)
        glBegin(GL_POINTS)
        for x, y in heart:
            glVertex3f(x*scale, y*scale, 0)
        glEnd()

        # Lời chúc quay vòng
        angle += 0.5
        glColor3f(1,1,1)
        for i, msg in enumerate(["Chúc Trung Thu ấm áp", "Vui vẻ", "Đoàn viên", "Hạnh phúc"]):
            theta = math.radians(angle + i*90)
            x = math.cos(theta)*2
            z = math.sin(theta)*2
            draw_text(msg, x, -1.5, z)

        # Hạt bay lên
        glPointSize(2)
        glColor3f(1,0.2,0.3)
        glBegin(GL_POINTS)
        for p in particles:
            glVertex3f(p[0], p[1], p[2])
            p[1] += 0.01
            if p[1] > 1.2:
                p[1] = -1.5
                p[0] = random.uniform(-1,1)
                p[2] = random.uniform(-1,1)
        glEnd()

        pygame.display.flip()
        pygame.time.wait(10)

if __name__ == "__main__":
    from OpenGL.GLUT import glutInit, glutStrokeCharacter, GLUT_STROKE_ROMAN
    glutInit()
    main()
