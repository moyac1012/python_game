import pyxel

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
        blocks = [
            Block(-1, 0),
            Block(0, 0),
            Block(0, -1),
            Block(1, 0),
        ]

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
    
    def putBlock(self, x, y):
        self.tiles[y][x] = 1

    def draw(self):
        for y in range(FIELD_HEIGHT):
            for x in range(FIELD_WIDTH):
                if self.tileAt(x, y) == 0:
                    continue
                Block(x, y).draw()

class App:
    def __init__(self):
        pyxel.init(WIDTH, HEIGHT, title="TETRIS")
        self.mino = Mino(5, 10, 0, 0)
        self.minoVx = 0
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


    def input(self):
        if pyxel.btnp(pyxel.KEY_RIGHT):
            self.minoVx += 1
        if pyxel.btnp(pyxel.KEY_LEFT):
            self.minoVx -= 1
        if pyxel.btnp(pyxel.KEY_UP):
            self.minoVr += 1
        if pyxel.btnp(pyxel.KEY_DOWN):
            self.minoVr -= 1

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
                    self.mino = Mino(5, 10, 0, 0)


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
