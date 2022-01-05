# -*- coding: utf-8 -*-
from sys import exit
import math
from random import randint
from itertools import cycle
import pygame
from pygame.locals import *

pygame.init()
screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption("A126871")

# クラス名は大文字で


class Fire(object):
    def __init__(self, x, y):
        super().__init__()
        self.w = 10
        self.h = 10
        self.rect = Rect(x, y, self.w, self.h)
        # x方向の増分は固定値:5
        self.vx = 5
        # 描画色
        self.color = (randint(0, 255), randint(0, 255), randint(0, 255))

    def move(self):
        radians = self.rect.x % 360
        vy = 2 * math.sin(math.radians(radians)) * self.h
        # 移動
        self.rect.move_ip(self.vx, vy)

    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect)

    @property
    def is_destroy(self) -> bool:
        return any([self.rect.x < -self.w, self.rect.y < -self.h, self.rect.x > 640, self.rect.y > 480])
        # 以下の5行と判定は同じです。
        # if self.rect.x < -self.w or self.rect.y < -self.h:
        #    return True
        # if self.rect.x > 640 or self.rect.y > 480:
        #    return True
        # return False

    def __str__(self):
        return ','.join(map(str, [self.rect.x, self.rect.y, self.rect.width, self.rect.height, self.is_destroy]))


def application_exit():
    pygame.quit()
    exit()


def main():
    clock = pygame.time.Clock()
    note_list = []
    # 生成間隔:20、数値が小さいほど生成間隔が短くなります。
    t = cycle(list(range(20)))
    while True:
        clock.tick(30)
        screen.fill((0, 0, 0))
        # 時間経過を元に生成
        i = next(t)
        if i == 0:
            note_list.append(Fire(0, 40))

        # 生成したオブジェクトに対して移動と描画を行う
        for note in note_list:
            note.move()
            note.draw()
        # リストからスクリーン範囲外の物を削除
        note_list = list(filter(lambda x: not x.is_destroy, note_list))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == QUIT:
                application_exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    application_exit()


if __name__ == "__main__":
    main()
