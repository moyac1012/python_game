import pyxel
import random

# 定数定義
WIDTH = 64
HEIGHT = 64
DOT_SIZE = 8

class Button:
    def __init__(self, x, y, width, height, label):
        """ボタンの初期化
        x, y: ボタンの左上座標
        width, height: ボタンのサイズ
        label: ボタンに表示するテキスト
        """
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.label = label

    def draw(self):
        """ボタンを描画する"""
        # ボタンの背景
        pyxel.rect(self.x, self.y, self.width, self.height, 7)
        # ボタンの枠
        pyxel.rectb(self.x, self.y, self.width, self.height, 0)
        # テキストを中央に配置
        text_x = self.x + (self.width - len(self.label) *4) // 2
        text_y = self.y + ((self.height - 4) // 2)  # 7はテキストの高さ
        pyxel.text(text_x, text_y, self.label, 0)

    def is_clicked(self):
        """ボタンがクリックされたかを判定する"""
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            mx, my = pyxel.mouse_x, pyxel.mouse_y
            if (self.x <= mx <= self.x + self.width and
                self.y <= my <= self.y + self.height):
                return True
        return False

class Dice:
    def __init__(self, x, y, size):
        """サイコロの初期化
        x, y: サイコロの左上座標
        size: サイコロのサイズ
        """
        self.x = x
        self.y = y
        self.size = size
        self.face = random.randint(1, 6)

    def roll(self):
        """サイコロを振る"""
        self.face = random.randint(1, 6)

    def draw(self):
        """サイコロの描画
            x: x座標, y: y座標, d: ダイスの目（0~6)
        """
        pyxel.blt(self.x, self.y, 0, 8*(self.face-1), 0, DOT_SIZE, DOT_SIZE)

class App:
    def __init__(self):
        pyxel.init(WIDTH, HEIGHT, title="DICE")
        pyxel.load("material.pyxres")

        pyxel.mouse(True)  # マウスを有効化

        # ボタンの位置とサイズを設定
        button_width = 24
        button_height = 12
        button_x = (WIDTH - button_width) // 2
        button_y = HEIGHT - button_height - 4  # 下部に配置
        self.dice_button = Button(button_x, button_y, button_width, button_height, "ROLL")

        # サイコロの位置を中央に設定
        dice_x = WIDTH // 2 - DOT_SIZE // 2
        dice_y = HEIGHT // 2 - DOT_SIZE // 2
        self.dice = Dice(dice_x, dice_y, DOT_SIZE)  # サイズを16に設定
        pyxel.run(self.update, self.draw)

    def update(self):
        """更新処理"""
        # スペースキーが押されたらサイコロを振る
        if pyxel.btnp(pyxel.KEY_SPACE):
            self.dice.roll()
        # ボタンがクリックされたらサイコロを振る
        if self.dice_button.is_clicked():
            self.dice.roll()

    def draw(self):
        """描画処理"""
        pyxel.cls(5)  # 背景色を設定（5は好みで変更可能）
        self.dice_button.draw()
        self.dice.draw()

App()
