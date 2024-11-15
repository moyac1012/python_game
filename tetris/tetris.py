import pyxel
import random
WIDTH = 200
HEIGHT = 200
DOT_SIZE = 8
FIELD_WIDTH = 12
FIELD_HEIGHT = 21

class Block:
    def __init__(self, x , y):
        self.x = x
        self.y = y

    def draw(self):
        pyxel.rect(self.x * DOT_SIZE, self.y * DOT_SIZE, DOT_SIZE, DOT_SIZE, 7)


class Mino:
    def __init__(self, x, y, rot, shape):
        self.x = x
        self.y = y
        self.rot = rot
        self.shape = shape

    def calcBlocks(self):
        blocks = []
        if self.shape == 0:
            blocks = [Block(-1, 0),Block(0, 0),Block(0, -1),Block(1, 0)]
        elif self.shape == 1:
            blocks = [Block(0, -1),Block(0, 0),Block(1, 0),Block(1, -1)]
        elif self.shape == 2:
            blocks = [Block(-1, 0),Block(0, 0),Block(0, -1),Block(-1, 1)]
        elif self.shape == 3:
            blocks = [Block(0, 1),Block(0, 0),Block(0, -1),Block(0, -2)]
        elif self.shape == 4:
            blocks = [Block(0, 0),Block(0, 1),Block(1, 0),Block(1, 1)]
        elif self.shape == 5:
            blocks = [Block(0, 1),Block(0, 0),Block(0, -1),Block(1, -1)]
        elif self.shape == 6:
            blocks = [Block(0, 1),Block(0, 0),Block(0, -1),Block(-1, -1)]

        rot = self.rot % 4
        for _ in range(rot):
            blocks = [Block(-b.y, b.x) for b in blocks]

        blocks = list(map(lambda b: Block(b.x+self.x, b.y+self.y), blocks))

        return blocks
    
    def copy(self):
        return Mino(self.x, self.y, self.rot, self.shape)

    def draw(self):
        blocks = self.calcBlocks()

        for b in blocks:
            b.draw()


class Field:
    def __init__(self):
        self.tiles = [
            [1,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,0,0,0,0,0,0,0,0,0,1],
            [1,1,1,1,1,1,1,1,1,1,1,1],
        ]

    def tileAt(self, x, y):
        return self.tiles[y][x]

    def isLineFilled(self, line):
        for x in range(1, FIELD_WIDTH-1):
            if line[x] != 2:
                return False
        return True

    def deleteLine(self, y):
        for yi in range(y, 0, -1):
            self.tiles[yi] = self.tiles[yi-1].copy()
        # トップ行をリセット
        self.tiles[0] = [1] + [0]*(FIELD_WIDTH-2) + [1]

    def clearLines(self):
        lines_cleared = 0
        for y in range(FIELD_HEIGHT):
            if self.isLineFilled(self.tiles[y]):
                self.deleteLine(y)
                lines_cleared += 1
        return lines_cleared

    def putBlock(self, x, y):
        self.tiles[y][x] = 2

    def draw(self):
        for y in range(FIELD_HEIGHT):
            for x in range(FIELD_WIDTH):
                if self.tileAt(x, y) == 0:
                    continue
                Block(x, y).draw()
class App:
    def __init__(self):
        pyxel.init(WIDTH, HEIGHT, title="TETRIS")
        self.mino = self.makeMino()
        self.minoVx = 0
        self.minoVy = 0
        self.minoVr = 0
        self.field = Field()
        self.fc = 0

        pyxel.run(self.update, self.draw)

    def isMinoMovable(self, mino: Mino, field: Field):
        blocks = mino.calcBlocks()
        for b in blocks:
            if field.tileAt(b.x, b.y) != 0:
                # print(f"Collision at: ({b.x}, {b.y})")
                return False
        return True

    def makeMino(self):
        return Mino(5, 1, 0, random.randrange(0, 7))

    def input(self):
        if pyxel.btnp(pyxel.KEY_RIGHT):
            self.minoVx += 1
        if pyxel.btnp(pyxel.KEY_LEFT):
            self.minoVx -= 1
        if pyxel.btnp(pyxel.KEY_A):
            self.minoVr -= 1
        if pyxel.btnp(pyxel.KEY_D):
            self.minoVr += 1

        if pyxel.btn(pyxel.KEY_DOWN):
            self.minoVy += 1

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

        self.input()

        # 落下処理
        if self.fc % 20 == 19:
            futureMino = self.mino.copy()
            futureMino.y += 1

            if self.isMinoMovable(futureMino, self.field):
                self.mino.y += 1
            else:
                for b in self.mino.calcBlocks():
                    self.field.putBlock(b.x, b.y)
                # ミノを配置した後にラインクリアを行う
                self.field.clearLines()
                # ミノをリセット
                self.mino = self.makeMino()

        # 下移動
        if self.minoVy != 0:
            futureMino = self.mino.copy()
            futureMino.y += self.minoVy

            if self.isMinoMovable(futureMino, self.field):
                self.mino.y += self.minoVy

            self.minoVy = 0

        # 左右移動
        if self.minoVx != 0:
            futureMino = self.mino.copy()
            futureMino.x += self.minoVx

            if self.isMinoMovable(futureMino, self.field):
                self.mino.x += self.minoVx

            self.minoVx = 0

        # 回転
        if self.minoVr != 0:
            futureMino = self.mino.copy()
            futureMino.rot += self.minoVr

            if self.isMinoMovable(futureMino, self.field):
                self.mino.rot += self.minoVr

            self.minoVr = 0

        self.fc += 1

    def draw(self):
        pyxel.cls(0)
        self.field.draw()
        self.mino.draw()

App()