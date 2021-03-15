import pygame
from pygame.locals import *
from random import randint, choice

class Panel:
    def __init__(self, image, number):
        self.image = image
        self.rect = pygame.Rect((0, 0), image.get_rect().size)
        self.number = number
    
    def draw(self, pygame, screen, x, y):
        self.rect = pygame.Rect((x * 100, y * 100), self.image.get_rect().size)
        image = pygame.transform.scale(self.image, (100, 100))
        screen.blit(image, self.rect)

class Field:
    def __init__(self):
        self.width = 3
        self.is_cleared = False

        # パネルを並べる。一つは空き
        empty_image = pygame.image.load("empty.png")
        self.empty = Panel(empty_image, 8)
        self.panels = [Panel(pygame.image.load(f"{i + 1}.png"), i) for i in range(self.width ** 2 - 1)]
        self.panels.append(self.empty)

        # 解けない問題にならないようにシャッフル
        for i in range(randint(20, 30)):
            empty_position = self.get_empty_position()
            movable_positions = self.get_movable_positions(empty_position)
            index = choice(movable_positions)
            self.panels[index], self.panels[empty_position] = self.panels[empty_position], self.panels[index]
    
    # 空いている位置のインデックスを取得する
    def get_empty_position(self):
        return self.panels.index(self.empty)
    
    # 引数の位置から隣（移動できる位置）を取得する
    def get_movable_positions(self, index):
        positions = []
        x = index % self.width
        y = index // self.width

        # 一番左以外であれば、左のマスを追加
        if x > 0:
            positions.append(index - 1)

        # 一番右以外であれば、右のマスを追加
        if x < self.width - 1:
            positions.append(index + 1)

        # 一番上以外であれば、上のマスを追加
        if y > 0:
            positions.append(index - self.width)

        # 一番下以外であれば、下のマスを追加
        if y < self.width - 1:
            positions.append(index + self.width)
        
        return positions
    
    def click(self, pos, pygame, screen):
        for i in range(len(self.panels)):
            # クリックしたパネルに当たるまでループ
            if self.panels[i].rect.collidepoint(pos) == False:
                continue
            
            # クリックしたパネルの隣に空きがあれば、パネルと空きを入れ替える
            empty_position = self.get_empty_position()
            movable_positions = self.get_movable_positions(i)
            if empty_position in movable_positions:
                self.panels[i], self.panels[empty_position] = self.panels[empty_position], self.panels[i]
            break
        
        # クリアチェック
        if self.check_clear() == True:
            self.is_cleared = True
        
        # 画面を更新
        self.draw(pygame, screen)
    
    def check_clear(self):
        for i in range(len(self.panels)):
            # Panel.number が正しく並んでいないところがあれば False
            if self.panels[i].number != i:
                return False
        
        # すべて正しく並んでいれば True
        return True

    # 画面を描画する
    def draw(self, pygame, screen):
        # パネルを表示
        for i in range(len(self.panels)):
            x = i % self.width
            y = i // self.width
            self.panels[i].draw(pygame, screen, x, y)
        
        # クリアしていたら「CLEAR」を表示
        if self.is_cleared:
            font = pygame.font.SysFont(None, 50)
            text = font.render("CLEAR", True, (224, 224, 224))
            screen.blit(text, (0, 300))
        
        # 更新
        pygame.display.update()
