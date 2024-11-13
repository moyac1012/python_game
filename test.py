import pyxel 

def is_colliding(x, y):
    x1 = pyxel.floor(x) // 8
    y1 = pyxel.floor(y) // 8
    x2 = (pyxel.ceil(x) + 8) // 8
    y2 = (pyxel.ceil(y) + 8) // 8
    for yi in range(y1, y2 + 1):
        for xi in range(x1, x2 + 1):
            if pyxel.tilemaps[0].pget(xi, yi) == (6, 14):
                return True
    return False

class App:
    def __init__(self):
        pyxel.init(128, 128, title="TEST GAME")
        pyxel.load("my_resource.pyxres")

        self.player_x = 0
        self.player_y = 100
        self.player_dy = 0
        self.player_animate_cnt = 0
        self.is_jumping = False
        self.vy = 0 # Y方向の速度
        self.gravity = 0.05 # 重力
        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

        self.update_player()
        
    def draw(self):
        pyxel.cls(0)

        pyxel.bltm(0,0,0,0,0,128,128, 0) 

        pyxel.bltm(0,0,1,0,0,128,128, 0) 
        pyxel.blt(
            self.player_x,
            self.player_y,
            1,
            self.player_animate_cnt*8,
            0,
            8,
            8,
            0,
        )

        
        
        self.player_animate_cnt += 1
        self.player_animate_cnt %= 2

    def input_key(self):
        if pyxel.btnp(pyxel.KEY_SPACE):
            if self.is_jumping == False:
                # ジャンプする
                self.vy = -1.5
                self.is_jumping = True # ジャンプ中
        if pyxel.btn(pyxel.KEY_A):
            if not(is_colliding(self.player_x-1, self.player_y)):
                self.player_x -= 1
        if pyxel.btn(pyxel.KEY_D):
            if not(is_colliding(self.player_x+1, self.player_y)):
                self.player_x += 1

    def update_player(self):
        self.input_key()

        # 加速度更新
        self.vy += self.gravity
        # 速度を更新
        if not(is_colliding(self.player_x, self.player_y+self.vy)):
            self.player_y += self.vy
        else:
            self.is_jumping = False
            self.vy = 0

App()