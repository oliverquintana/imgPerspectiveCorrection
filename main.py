import numpy as np
import pygame
import cv2
import tkinter as tk
from tkinter import filedialog

def loadImage(fname = 'img.jpg'):
    img = cv2.imread(fname)
    img = np.rot90(cv2.flip(img, 1))
    w, h = 512, 512
    img = cv2.resize(img, (w, h))

    return img

def drawCircle(pos):
    c = (255,0,0)
    pygame.draw.circle(display_surface, c, pos, 5, 5)

def perspective(img, points):
    pts = np.array([points], np.float32)
    print(points)
    a = abs(min(points[0][0], points[1][0]) - max(points[2][0], points[3][0]))
    b = abs(min(points[0][1], points[2][1]) - max(points[1][1], points[3][1]))
    dst = np.array([[0, 0], [0, b], [a, 0], [a, b]], np.float32)
    retval = cv2.getPerspectiveTransform(pts, dst)
    warp = cv2.warpPerspective(img, retval, (a, b))

    return warp

def drawButton(pos, size, color = [128, 128, 128]):

    pygame.draw.rect(display_surface, color, pygame.Rect(pos[0], pos[1], size[0], size[1]))

def sortPoints(points):

    points = np.array(points)
    x = points[points[:,0].argsort()]
    left = x[:2]
    right = x[2:]
    left = left[left[:,1].argsort()]
    right = right[right[:,1].argsort()]
    points = np.concatenate((left, right))

    return points.tolist()

pygame.init()
pygame.display.set_caption('Ajuste de Perspectiva')

c = 60
white = (c, c, c)
X = 630
Y = 512

display_surface = pygame.display.set_mode((X, Y))
img = loadImage()
frame = pygame.surfarray.make_surface(img)
points = []

btn_pos = [520, 20]
btn_size = [100, 30]
font = pygame.font.Font('freesansbold.ttf', 15)
btn_txt = font.render('Abrir Imagen', True, [255, 255, 255], [128, 128, 128])
textRect = btn_txt.get_rect()
textRect.center = ((btn_pos[0] + btn_size[0] // 2), (btn_pos[1] + btn_size[1] // 2))

while True:

    display_surface.fill(white)

    mouse = pygame.mouse.get_pos()
    display_surface.blit(frame, (0, 0))

    drawButton(btn_pos, btn_size)
    display_surface.blit(btn_txt, textRect)

    for event in pygame.event.get():

        if event.type == pygame.MOUSEBUTTONUP:

            pos = pygame.mouse.get_pos()
            if pos[0] > btn_pos[0] and pos[1] > btn_pos[1] and pos[1] < btn_pos[1] + btn_size[1]:
                root = tk.Tk()
                root.withdraw()
                file_path = filedialog.askopenfilename()

                if not(file_path):
                    continue

                img = loadImage(file_path)
                frame = pygame.surfarray.make_surface(img)
                points = []

            else:
                drawCircle(pos)
                points.append(pos)

            if len(points) > 3:
                points = sortPoints(points)
                out_img = perspective(img, points)
                #out_img = cv2.resize(out_img, (w, h))
                frame = pygame.surfarray.make_surface(out_img)
                points = []

        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

        pygame.display.update()
