import random
import sys
import time
import pygame as pg
import sounds


class Button:
    def __init__(self, surface, colour, rgb, tone, x, y, w, h):
        self.surface = surface
        self.colour = colour
        self.rgb = rgb
        self.tone = tone
        self.rect = pg.Rect(x, y, w, h)
        self.draw()
        pg.display.update(self.rect)

    def draw(self, on=False):
        if on:
            pg.draw.rect(self.surface, self.rgb[1], self.rect)
        else:
            pg.draw.rect(self.surface, self.rgb[0], self.rect)

    def flash(self, on=0.35, off=0.15):
        beep_length = int(on * 1000)
        self.draw(on=True)
        sounds.Tone(self.tone, 'b', 0.1).play(-1, maxtime=beep_length)
        pg.display.update(self.rect)
        time.sleep(on)
        self.draw(on=False)
        pg.display.update(self.rect)
        time.sleep(off)

    def rapid_flash(self):
        sounds.Tone(49, 'b', 0.1).play(-1, maxtime=1000)
        flashes = 10
        while flashes > 0:
            self.draw(on=True)
            pg.display.update(self.rect)
            time.sleep(0.1)
            self.draw(on=False)
            pg.display.update(self.rect)
            time.sleep(0.1)
            flashes -= 1

    def mouseover(self, event):
        pos = pg.mouse.get_pos()
        if self.rect.collidepoint(pos) and event.type == pg.MOUSEBUTTONDOWN:
            self.flash()
            return True
        return False


class RedButton(Button):
    def __init__(self, surface, x, y, w, h):
        self.rgb = ((105, 0, 0), (255, 0, 0))
        self.tone = 440
        super().__init__(surface, "RED", self.rgb, self.tone, x, y, w, h)


class GreenButton(Button):
    def __init__(self, surface, x, y, w, h):
        self.rgb = ((0, 105, 0), (0, 255, 0))
        self.tone = 164.81
        super().__init__(surface, "GREEN", self.rgb, self.tone, x, y, w, h)


class BlueButton(Button):
    def __init__(self, surface, x, y, w, h):
        self.rgb = ((0, 0, 105), (0, 0, 255))
        self.tone = 329.63
        super().__init__(surface, "BLUE", self.rgb, self.tone, x, y, w, h)


class YellowButton(Button):
    def __init__(self, surface, x, y, w, h):
        self.rgb = ((105, 105, 0), (255, 255, 0))
        self.tone = 277.18
        super().__init__(surface, "YELLOW", self.rgb, self.tone, x, y, w, h)


class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.screen = pg.display.set_mode((self.width, self.height))
        self.screen.fill((155, 155, 155))
        pg.display.update()
        self.border = 10
        self.banner_h = 50
        self.banner_rgb = (0, 0, 0)
        self.banner_rect = pg.Rect(0 + self.border,
                                   0 + self.border,
                                   self.width - self.border * 2,
                                   self.banner_h - self.border * 2)
        self.draw_banner(0, 0)
        self.button_h = (self.height - self.banner_h - self.border * 2) / 2
        self.button_w = (self.width - self.border * 3) / 2
        self.buttons = {"YELLOW": YellowButton(self.screen,
                                               self.border,
                                               self.banner_h,
                                               self.button_w,
                                               self.button_h),
                        "BLUE": BlueButton(self.screen,
                                           self.button_w + self.border * 2,
                                           self.banner_h,
                                           self.button_w,
                                           self.button_h),
                        "RED": RedButton(self.screen,
                                         self.border,
                                         self.banner_h + self.border + self.button_h,
                                         self.button_w,
                                         self.button_h),
                        "GREEN": GreenButton(self.screen,
                                             self.button_w + self.border * 2,
                                             self.banner_h + self.border + self.button_h,
                                             self.button_w,
                                             self.button_h)}

    def draw_banner(self, score, hiscore, msg=None):
        pg.draw.rect(self.screen, self.banner_rgb, self.banner_rect)
        # setup text objects
        if not msg:
            msg = "CLICK MOUSE TO START!"
        font1 = pg.font.SysFont('Courier', 14)
        font2 = pg.font.SysFont('Courier', 16)
        score_txt = font1.render(f"SCORE: {score}", True, (205, 175, 0))
        hiscore_txt = font1.render(f"HI-SCORE: {hiscore}", True, (205, 175, 0))
        msg_txt = font2.render(msg, True, (205, 175, 0))
        # centre the messages
        score_txt_rect = score_txt.get_rect(center=(45, self.banner_h / 2))
        hiscore_txt_rect = hiscore_txt.get_rect(center=(self.width - 65, self.banner_h / 2))
        msg_txt_rect = msg_txt.get_rect(center=(self.width / 2, self.banner_h / 2))
        # display
        self.screen.blit(score_txt, score_txt_rect)
        self.screen.blit(hiscore_txt, hiscore_txt_rect)
        self.screen.blit(msg_txt, msg_txt_rect)
        pg.display.update(self.banner_rect)

    def demo(self):
        notes = ["GREEN", "YELLOW", "BLUE", "RED", "BLUE", "YELLOW"]
        for n in notes:
            self.buttons[n].flash(on=0.2, off=0.05)

    def fanfare(self):
        notes = ["GREEN", "YELLOW", "BLUE", "RED"]
        length = [0.25, 0.25, 0.25, 0.5]
        for i in range(len(notes)):
            self.buttons[notes[i]].flash(on=length[i], off=0.05)


class Game:
    def __init__(self):
        self.colours = ['RED', 'GREEN', 'BLUE', 'YELLOW']
        self.seq = []
        self.current_seq = []
        self.score = 0
        self.next_colour = None

    def extend_seq(self):
        self.seq.append(random.randrange(4))
        self.current_seq = self.seq[:]
        self.score = len(self.seq) - 1

    def check_input(self, pressed):
        self.next_colour = self.colours[self.current_seq.pop(0)]
        if self.next_colour == pressed:
            return True
        return False

    def reset_seq(self):
        if not self.current_seq:
            self.extend_seq()
            return True
        return False

    def seq_to_text(self):
        return [self.colours[i] for i in self.current_seq]

    def check_score(self):
        if self.score == 5:
            text = "NICE!"
        elif self.score == 10:
            text = "AWESOME!"
        elif self.score == 15:
            text = "EPIC!!!"
        else:
            text = None
        return text


def main():
    hiscore = 0
    pg.mixer.pre_init(44100, -16, 1, 1024)
    pg.init()
    pg.display.set_caption('Simon')
    board = Board(700, 550)
    # board.fanfare()
    mode = "DEMO"
    while True:
        if mode == "DEMO":
            board.draw_banner(0, hiscore)
            board.demo()
            for event in pg.event.get():
                if event.type == pg.MOUSEBUTTONDOWN:
                    mode = "GAME"
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
        if mode == "GAME":
            game = Game()
            time.sleep(0.4)
            match = True
            msg = "LET'S GO!"
            board.draw_banner(game.score, hiscore, msg)
            while match:
                game.extend_seq()
                new_msg = game.check_score()
                if new_msg:
                    board.draw_banner(game.score, hiscore, new_msg)
                    board.fanfare()
                else:
                    board.draw_banner(game.score, hiscore, msg)
                time.sleep(0.5)
                for clr in game.seq_to_text():
                    board.buttons[clr].flash()
                pg.event.clear()
                while len(game.current_seq) > 0:
                    event = pg.event.wait()
                    if event.type == pg.MOUSEBUTTONDOWN:
                        for clr, btn in board.buttons.items():
                            if btn.mouseover(event):
                                # pressed = clr
                                match = game.check_input(clr)
                                break
                    if not match:
                        break
                msg = " "
            board.buttons[game.next_colour].rapid_flash()
            if game.score > hiscore:
                hiscore = game.score
                board.draw_banner(game.score, hiscore)
            mode = "DEMO"
            pg.event.clear()


if __name__ == '__main__':
    main()
