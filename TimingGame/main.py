import pyxel

WINDOW_WIDTH = 128
WINDOW_HEIGHT = 128

GAUGE_WIDTH = 100
GAUGE_HEIGHT = 15

BAR_HEIGHT = GAUGE_HEIGHT + 2
BAR_WIDTH = 3

class Bar:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.dx = 1
        self.speed = 1

    def move(self, speed=1):
        self.speed = speed
        center = WINDOW_WIDTH // 2
        if self.x < center - GAUGE_WIDTH // 2 or center - 2 + (GAUGE_WIDTH // 2) < self.x:
            self.dx *= -1
        self.x += self.dx
        self.draw()

    def movex_dev(self, dx):
        self.x += dx

    def draw(self):
        pyxel.rect(self.x, self.y, BAR_WIDTH, BAR_HEIGHT, 7)

    def get_position_in_gauge(self, gauge):
        center = WINDOW_WIDTH // 2
        distance_from_center = self.x - center

        if -gauge.redWidth // 2 <= distance_from_center <= gauge.redWidth // 2 - 1:
            return "red"
        elif -gauge.yellowWidth // 2 <= distance_from_center <= gauge.yellowWidth // 2 - 1:
            return "yellow"
        elif -gauge.greenWidth // 2 <= distance_from_center <= gauge.greenWidth // 2 - 1:
            return "green"
        else:
            return "out"


class Gauge:
    def __init__(self):
        redWidthRatio = 0.1
        yellowWidthRatio = 0.3
        greenWidthRatio = 1.0

        self.y = 10
        self.redWidth = GAUGE_WIDTH * redWidthRatio
        self.yellowWidth = GAUGE_WIDTH * yellowWidthRatio
        self.greenWidth = GAUGE_WIDTH * greenWidthRatio

    def draw(self):
        center = WINDOW_WIDTH // 2

        pyxel.rect(center - (self.greenWidth // 2), self.y, self.greenWidth, GAUGE_HEIGHT, 11)
        pyxel.rect(center - (self.yellowWidth // 2), self.y, self.yellowWidth, GAUGE_HEIGHT, 10)
        pyxel.rect(center - (self.redWidth // 2), self.y, self.redWidth, GAUGE_HEIGHT, 8)


class Effect:
    def __init__(self, max_frames, update_delay):
        self.x = 0
        self.y = 0
        self.frame = 0
        self.active = False
        self.direction = "right"
        self.max_frames = max_frames
        self.delay_counter = 0
        self.update_delay = update_delay

    def activate(self, x, y, direction):
        self.x = x
        self.y = y
        self.frame = 0
        self.active = True
        self.direction = direction
        self.delay_counter = 0

    def update(self):
        if self.active:
            self.delay_counter += 1
            if self.delay_counter >= self.update_delay:
                self.delay_counter = 0
                self.frame += 1
                if self.frame >= self.max_frames:
                    self.active = False

    def draw(self):
        if self.active:
            u = (self.frame % self.max_frames) * 16  # スプライトの U 座標

            # 向きに応じて幅と高さを設定
            if self.direction == "right":
                pyxel.blt(self.x, self.y, 0, u, 16, -16, 16, pyxel.COLOR_RED)
            elif self.direction == "left":
                pyxel.blt(self.x, self.y, 0, u, 16, 16, 16, pyxel.COLOR_RED)  # 横反転
            elif self.direction == "up":
                pyxel.blt(self.x, self.y, 0, u, 16, 16, -16, pyxel.COLOR_RED, 90)  # 縦反転
            elif self.direction == "down":
                pyxel.blt(self.x, self.y, 0, u, 16, 16, 16, pyxel.COLOR_RED, 90)


class SlashEffect(Effect):
    def __init__(self):
        super().__init__(max_frames=4, update_delay=3)  # フレーム数4、遅延3フレーム



class Player:
    def __init__(self, x, y, effect_type):
        self.x = x
        self.y = y
        self.direction = "right"  # 初期方向
        self.effect = effect_type  # エフェクトをオブジェクトとして保持

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

        # 向きの更新
        if dx > 0:
            self.direction = "right"
        elif dx < 0:
            self.direction = "left"
        elif dy > 0:
            self.direction = "down"
        elif dy < 0:
            self.direction = "up"

    def attack(self):
        """攻撃時にエフェクトを発動"""
        if self.direction == "right":
            self.effect.activate(self.x + 16, self.y, "right")
        elif self.direction == "left":
            self.effect.activate(self.x - 16, self.y, "left")
        elif self.direction == "up":
            self.effect.activate(self.x, self.y - 16, "up")
        elif self.direction == "down":
            self.effect.activate(self.x, self.y + 16, "down")

    def update(self):
        self.effect.update()

    def draw(self):
        pyxel.blt(self.x, self.y, 0, 0, 0, 16, 16, 8)
        self.effect.draw()


class Text:
    def __init__(self, x, y, message="", cls=7):
        self.x = x
        self.y = y
        self.message = message
        self.cls = cls

    def update_message(self, new_message):
        self.message = new_message

    def draw(self):
        if self.message:
            pyxel.text(self.x, self.y, self.message, self.cls)


class App:
    def __init__(self):
        pyxel.init(WINDOW_WIDTH, WINDOW_HEIGHT, title="タイミングゲーム")
        pyxel.load("material.pyxres")
        self.gauge = Gauge()
        self.bar = Bar(WINDOW_WIDTH // 2, 9)
        self.player = Player((WINDOW_WIDTH - 16) // 2, (WINDOW_HEIGHT - 16) // 2, SlashEffect())
        self.message = Text(10, 100)

        pyxel.run(self.update, self.draw)

    def update(self):
        self.bar.move()

        if pyxel.btn(pyxel.KEY_RIGHT):
            self.player.move(1, 0)
        if pyxel.btn(pyxel.KEY_LEFT):
            self.player.move(-1, 0)
        if pyxel.btn(pyxel.KEY_UP):
            self.player.move(0, -1)
        if pyxel.btn(pyxel.KEY_DOWN):
            self.player.move(0, 1)

        # スペースキーでアタック
        if pyxel.btnp(pyxel.KEY_SPACE):
            self.player.attack()

            # ゲージの判定
            position = self.bar.get_position_in_gauge(self.gauge)
            if position == "red":
                self.message.update_message("Perfect!")
            elif position == "yellow":
                self.message.update_message("Good!")
            elif position == "green":
                self.message.update_message("Miss!")

        # エフェクトの更新
        self.player.update()

    def draw(self):
        pyxel.cls(0)
        self.player.draw()
        self.gauge.draw()
        self.bar.draw()
        self.message.draw()


App()
