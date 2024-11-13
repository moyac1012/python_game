import pyxel
import random

WIDTH = 64
HRIGHT = 64
DOT_SIZE = 8

# class Button:
#     def draw_button():


class Dice:
    def draw_dice(x, y, d):
        """サイコロの描画
            x: x座標, y: y座標, d: ダイスの目（0~6)
        """
        pyxel.blt(x, y, 0, 8*(d-1), 0, DOT_SIZE, DOT_SIZE)


class App:
    def __init__(self):
        pyxel.init(WIDTH, HRIGHT, title="DICE")
        pyxel.load("material.pyxres")
        Dice.draw_dice(WIDTH/2-DOT_SIZE/2, HRIGHT/2-DOT_SIZE/2, random.randint(1, 6))
        pyxel.mouse(True)
        pyxel.run(self.update, self.draw)

    def update(self):
        pass

    def draw(self):
        if pyxel.btn(pyxel.KEY_SPACE):
            Dice.draw_dice(WIDTH/2-DOT_SIZE/2, HRIGHT/2-DOT_SIZE/2, random.randint(1, 6))



App()