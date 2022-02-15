import os
import sys

import pygame

from MainWindow import Ui_MainWindow
from PyQt5.QtWidgets import *
from main import get_map, load_image

pygame.init()


class Data(Ui_MainWindow, QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.initUi()

    def initUi(self):
        self.d, self.sh, self.sc = None, None, None
        self.is_do = False
        self.pushButton.clicked.connect(self.do)

    def do(self):
        self.d, self.sh = float(self.input_d.text()), float(self.input_sh.text())
        self.old_d, self.old_sh = float(self.input_d.text()), float(self.input_sh.text())
        self.sc = float(self.scale.currentText())

        self.spn_x, self.spn_y = self.sc, self.sc
        self.spn = f'{self.spn_x},{self.spn_y}'
        self.ll = f'{self.d},{self.sh}'

        response = get_map(self.ll, add_params={'spn': f'{self.spn}'})
        map_file = "map.png"
        with open(map_file, "wb") as file:
            file.write(response.content)

        size = height, width = 650, 500
        screen = pygame.display.set_mode(size)
        self.image = pygame.transform.scale(load_image('лупа.png'), (40, 40))
        image = load_image('map.png')
        screen.blit(image, (10, 10))
        pygame.display.flip()
        running = True
        map_type = 'map'
        while running:
            screen.fill('white')
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.KEYDOWN:

                    """if event.key == pygame.K_PAGEDOWN:
                        self.sc += 1
                        if self.sc > 17:
                            self.sc = 17

                    elif event.key == pygame.K_PAGEUP:
                        self.sc -= 1
                        if self.sc < 0:
                            self.sc = 0

                    elif event.key == pygame.K_DOWN:
                        self.sh -= 0.02 * ((17 - self.sc) / 2) ** 2
                        if -85.5 <= self.sh <= 85.5:
                            self.old_sh = self.sh
                        self.sh = self.old_sh

                    elif event.key == pygame.K_UP:
                        self.sh += 0.02 * ((17 - self.sc) / 2) ** 2
                        if -85.5 <= self.sh <= 85.5:
                            self.old_sh = self.sh
                        self.sh = self.old_sh

                    elif event.key == pygame.K_LEFT:
                        self.d -= 0.02 * (17 - self.sc) ** 2
                        if 0 <= self.d <= 180:
                            self.old_d = self.d
                        self.d = self.old_d

                    elif event.key == pygame.K_RIGHT:
                        self.d += 0.02 * (17 - self.sc) ** 2
                        if 0 <= self.d <= 180:
                            self.old_d = self.d
                        self.d = self.old_d"""

                    if event.key == pygame.K_q:
                        map_type = 'map'

                    elif event.key == pygame.K_w:
                        map_type = 'sat'

                    elif event.key == pygame.K_e:
                        map_type = 'sat,skl'

                    if event.key == pygame.K_PAGEUP:
                        self.spn_x *= 2
                        self.spn_y *= 2
                    elif event.key == pygame.K_PAGEDOWN:
                        self.spn_x /= 2
                        self.spn_y /= 2
                    elif event.key == pygame.K_UP:
                        self.sh = (self.sh + 0.1 * self.spn_y) if (self.sh + 0.1 * self.spn_y) < 85 else 85
                    elif event.key == pygame.K_DOWN:
                        self.sh = (self.sh - 0.1 * self.spn_y) if (self.sh - 0.1 * self.spn_y) > -85 else -85
                    elif event.key == pygame.K_RIGHT:
                        self.d = (self.d + 0.1 * self.spn_x) if (self.d + 0.1 * self.spn_x) < 180 else 180
                    elif event.key == pygame.K_LEFT:
                        self.d = (self.d - 0.1 * self.spn_x) if (self.d - 0.1 * self.spn_x) > -180 else -180

                    self.ll = f'{self.d},{self.sh}'
                    self.spn = f'{self.spn_x},{self.spn_y}'
                    print(self.spn)
                    try:
                        response = get_map(self.ll, add_params={'spn': f'{self.spn}'}, map_type=map_type)
                        map_file = "map.png"
                        with open(map_file, "wb") as file:
                            file.write(response.content)
                        image = load_image('map.png')
                    except Exception:
                        print('(((((')

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if 610 <= event.pos[0] <= 650 and 10 <= event.pos[1] <= 50:
                        name, ok_pressed = QInputDialog.getText(self, "Введите адрес", "Адрес:")
                        if ok_pressed:
                            print(name)
                            pass



            screen.blit(image, (10, 10))
            self.print_text(screen)
            screen.blit(self.image, (610, 10))
            pygame.display.flip()

        pygame.quit()
        os.remove(map_file)
        sys.exit(app.exec())

    def print_text(self, surface):
        text = ['Q/W/E - схема/спутник/гибрид']
        font = pygame.font.SysFont('arial', 20)
        text = font.render(text[0], True, 'black')
        x, y = 10, 460
        surface.blit(text, (x, y))

    def ret(self):
        return self.d, self.sh, self.sc, self.is_do


sys._excepthook = sys.excepthook


def exception_hook(exctype, value, traceback):
    sys._excepthook(exctype, value, traceback)
    sys.exit(1)


sys.excepthook = exception_hook

app = QApplication(sys.argv)
win = Data()
win.show()
sys.exit(app.exec())