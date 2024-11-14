import pyxel
import random
from abc import ABC, abstractmethod

# 定数定義
WIDTH = 64
HEIGHT = 64
DOT_SIZE = 8

# サイコロの位置を定数化
DICE_POSITIONS = [
    (WIDTH // 2 - DOT_SIZE // 2, HEIGHT // 2 - DOT_SIZE // 2),
    (20, 20), (36, 20), (28, 12), (28, 20),  # 2-5個の配置
    (20, 28), (36, 28), (20, 12), (36, 12), (48, 20)  # 6-10個の配置
]

class Button(ABC):
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

    @abstractmethod
    def draw(self):
        """ボタンを描画する"""
        pass

    @abstractmethod
    def is_clicked(self):
        """ボタンがクリックされたかを判定する"""
        pass

class RectangleButton(Button):
    def draw(self):
        """四角形のボタンを描画する"""
        pyxel.rect(self.x, self.y, self.width, self.height, 7)  # 背景色
        pyxel.rectb(self.x, self.y, self.width, self.height, 0)  # 枠
        # テキストを中央に配置
        text_x = self.x + (self.width - len(self.label) * 4) // 2
        text_y = self.y + (self.height - 7) // 2
        pyxel.text(text_x, text_y, self.label, 0)  # テキスト色

    def is_clicked(self):
        """四角形のボタンがクリックされたかを判定する"""
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            mx, my = pyxel.mouse_x, pyxel.mouse_y
            if (self.x <= mx <= self.x + self.width and
                self.y <= my <= self.y + self.height):
                return True
        return False
    
    def isDrag(self):
        pass



class TriangleButton(Button):
    def draw(self):
        """三角形のボタンを描画する"""
        # 三角形の頂点
        ax, ay = self.x, self.y + self.height
        bx, by = self.x + self.width // 2, self.y
        cx, cy = self.x + self.width, self.y + self.height
        # 塗りつぶし
        pyxel.tri(ax, ay, bx, by, cx, cy, 7)
        # 枠
        pyxel.line(ax, ay, bx, by, 0)
        pyxel.line(bx, by, cx, cy, 0)
        pyxel.line(cx, cy, ax, ay, 0)
        # テキストの配置（頂点に対して適切に調整）
        text_x = self.x + (self.width - len(self.label) * 4) // 2
        text_y = self.y + self.height // 2 - 4
        pyxel.text(text_x, text_y, self.label, 0)

    def is_clicked(self):
        """三角形のボタンがクリックされたかを判定する"""
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            mx, my = pyxel.mouse_x, pyxel.mouse_y
            # 三角形の頂点
            ax, ay = self.x, self.y + self.height
            bx, by = self.x + self.width // 2, self.y
            cx, cy = self.x + self.width, self.y + self.height

            # バリ座標（バリセンター座標）を使用した点の内外判定
            denom = ((by - cy)*(ax - cx) + (cx - bx)*(ay - cy))
            if denom == 0:
                return False  # 三角形が退化している
            a = ((by - cy)*(mx - cx) + (cx - bx)*(my - cy)) / denom
            b = ((cy - ay)*(mx - cx) + (ax - cx)*(my - cy)) / denom
            c = 1 - a - b
            if 0 <= a <= 1 and 0 <= b <= 1 and 0 <= c <= 1:
                return True
        return False

class InvertedTriangleButton(Button):
    def draw(self):
        """逆三角形のボタンを描画する"""
        # 逆三角形の頂点
        ax, ay = self.x, self.y
        bx, by = self.x + self.width // 2, self.y + self.height
        cx, cy = self.x + self.width, self.y
        # 塗りつぶし
        pyxel.tri(ax, ay, bx, by, cx, cy, 7)  # 塗りつぶし色
        # 枠
        pyxel.line(ax, ay, bx, by, 0)
        pyxel.line(bx, by, cx, cy, 0)
        pyxel.line(cx, cy, ax, ay, 0)
        # テキストの配置
        text_width = len(self.label) * 4
        text_x = self.x + (self.width - text_width) // 2
        text_y = self.y + self.height // 2 - 4
        pyxel.text(text_x, text_y, self.label, 0)  # テキスト色

    def is_clicked(self):
        """逆三角形のボタンがクリックされたかを判定する"""
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            mx, my = pyxel.mouse_x, pyxel.mouse_y
            # 逆三角形の頂点
            ax, ay = self.x, self.y
            bx, by = self.x + self.width // 2, self.y + self.height
            cx, cy = self.x + self.width, self.y

            # バリ座標（バリセンター座標）を使用した点の内外判定
            denom = ((by - cy)*(ax - cx) + (cx - bx)*(ay - cy))
            if denom == 0:
                return False  # 三角形が退化している
            a = ((by - cy)*(mx - cx) + (cx - bx)*(my - cy)) / denom
            b = ((cy - ay)*(mx - cx) + (ax - cx)*(my - cy)) / denom
            c = 1 - a - b
            if 0 <= a <= 1 and 0 <= b <= 1 and 0 <= c <= 1:
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

        self.dice_count = 1

        # ボタンの設定
        button_width = 27
        button_height = 16

        # 四角形ボタン
        rect_button_x = 20
        rect_button_y = HEIGHT - button_height - 10
        self.button_rect = RectangleButton(rect_button_x, rect_button_y, button_width, button_height, "ROLL")

        # 三角形ボタン
        tri_button_x = 0
        tri_button_y = 20
        self.button_tri = TriangleButton(tri_button_x, tri_button_y, 10, 5, "△")

        # 逆三角形ボタン
        self.button_tri_inv = InvertedTriangleButton(0, 40, 10, 5, "▽")

        # サイコロの位置を中央に設定
        # dice_x = WIDTH // 2 - DOT_SIZE // 2
        # dice_y = HEIGHT // 2 - DOT_SIZE // 2
        self.dice = [Dice(*DICE_POSITIONS[i], DOT_SIZE) for i in range(self.dice_count)]
        pyxel.run(self.update, self.draw)

    def update(self):
        """更新処理"""
        # スペースキーが押されたらサイコロを振る
        if pyxel.btnp(pyxel.KEY_SPACE):
            for d in self.dice:
                d.roll()

        # ボタンがクリックされたらサイコロを振る
        if self.button_rect.is_clicked():
            pyxel.play(0, pyxel.sounds[0])
            for d in self.dice:
                d.roll()

        if self.button_tri.is_clicked():
            if self.dice_count < 10:
                self.dice_count += 1
                self.update_dice_count()


        if self.button_tri_inv.is_clicked():
            if self.dice_count > 0:
                self.dice_count -= 1
                self.update_dice_count()

    def update_dice_count(self):
        """サイコロの数を更新する"""
        self.dice = [Dice(*DICE_POSITIONS[i], DOT_SIZE) for i in range(self.dice_count)]

    def draw(self):
        """描画処理"""
        pyxel.cls(5)  # 背景色を設定（5は好みで変更可能）
        self.button_tri_inv.draw()
        self.button_rect.draw()
        self.button_tri.draw()
        for d in self.dice:
            d.draw()

        pyxel.text(2, 30, str(self.dice_count), 0)

App()
