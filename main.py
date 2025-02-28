import pygame
import random
import time
import os
import sys
import logging

# 初始化 Pygame
pygame.init()
pygame.font.init()
pygame.mixer.init()  # 初始化混音器模块
font = pygame.font.SysFont('Arial', 32)


# 配置日志记录
logging.basicConfig(filename='game.log', level=logging.DEBUG)

#修改绝对路径到相对路径
def resource_path(relative_path):
    """ Get the absolute path to the resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = getattr(sys, '_MEIPASS', os.path.abspath("."))
    except Exception:
        base_path = os.path.abspath(".")
    full_path = os.path.join(base_path, relative_path)
    print(f"Resource path for {relative_path}: {full_path}")  # 测试添加调试输出
    logging.debug(f"Resource path for {relative_path}: {full_path}")  # 使用日志记录
    return full_path
# 示例使用日志记录
logging.info("程序启动")


# 加载背景音乐
pygame.mixer.music.load(resource_path('music/start_music.mp3'))  # 游戏开始前的音乐
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)  # 循环播放

# 加载音效
jump_sound = pygame.mixer.Sound(resource_path('sound/jump.mp3'))  # 跳跃音效            # 跳跃音效
coin_sound = pygame.mixer.Sound(resource_path('sound/coin.mp3'))  # 吃金币音效
game_over_sound = pygame.mixer.Sound(resource_path('sound/game_over.mp3'))  # 游戏结束音效

# 设置音效音量
jump_sound.set_volume(0.5)
coin_sound.set_volume(0.7)
game_over_sound.set_volume(0.8)

#--------------------------------------------------------------------------------

# 屏幕尺寸
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# 加载并缩放鸟类图像 
bird_image = pygame.image.load(resource_path('pic/bird.png')) 
bird_image = pygame.transform.scale(bird_image, (40, 40))

# 加载管道图像 
pipe_top_image = pygame.image.load(resource_path('pic/tube_up.png'))
pipe_top_image = pygame.transform.scale(pipe_top_image, (80, 400))
pipe_bottom_image = pygame.image.load(resource_path('pic/tube_down.png'))
pipe_bottom_image = pygame.transform.scale(pipe_bottom_image, (80, 400))

# 加载金币图像
coin_image = pygame.image.load(resource_path('pic/coin.png'))
coin_image = pygame.transform.scale(coin_image, (15, 30))

# 加载宝箱和法杖图像
chest_image = pygame.image.load(resource_path('pic/chest.png'))
chest_image = pygame.transform.scale(chest_image, (100, 100))
chest_rect = chest_image.get_rect(center=(WIDTH // 2, HEIGHT // 2))

wand_image = pygame.image.load(resource_path('pic/wand.png'))
wand_image = pygame.transform.scale(wand_image, (100, 100))
wand_rect = wand_image.get_rect(center=(WIDTH // 2, HEIGHT // 2))

# **加载“再来一次”按钮图像**
restart_button_image = pygame.image.load(resource_path('pic/restart_button.png'))  # **添加这行**
restart_button_image = pygame.transform.scale(restart_button_image, (100, 100))  # **调整按钮大小**
restart_button_rect = restart_button_image.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))  # **按钮位置**

# 游戏时钟
clock = pygame.time.Clock()

# 加载动画帧 
frames = [ 
    pygame.image.load(resource_path('pic/frame1.png')), 
    pygame.image.load(resource_path('pic/frame2.png')), 
    pygame.image.load(resource_path('pic/frame3.png')), 
    # 添加更多帧... 
]

# 加载并缩放按钮图像 
button_image = pygame.image.load(resource_path('pic/start_button.png'))
button_image = pygame.transform.scale(button_image, (200, 200))  # 调整按钮大小 
button_rect = button_image.get_rect(center=(WIDTH // 2, HEIGHT // 1.5))

# 缩放动画帧 
frames = [pygame.transform.scale(frame, (WIDTH, HEIGHT)) for frame in frames]

#展示宝箱
def show_chest():
    screen.blit(chest_image, chest_rect.topleft)
    pygame.display.flip()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if chest_rect.collidepoint(event.pos):
                    fade_out(chest_image)
                    show_wand()
                    return
                


#展示魔杖
def show_wand():
    alpha = 0
    while alpha < 255:
        temp_image = wand_image.copy()
        temp_image.set_alpha(alpha)
        screen.blit(temp_image, wand_rect.topleft)
        pygame.display.flip()
        alpha += 5
        clock.tick(30)



# 渐入效果
def fade_in(frame, duration=1.0):
    for alpha in range(0, 256, int(256 / (duration * 30))):
        temp_frame = frame.copy()
        temp_frame.set_alpha(alpha)
        screen.blit(temp_frame, (0, 0))
        screen.blit(button_image, button_rect.topleft)  # 在动画帧上绘制按钮
        pygame.display.flip()
        clock.tick(30)

# 渐出效果
def fade_out(frame, duration=1.0):
    for alpha in range(255, -1, -int(256 / (duration * 30))):
        temp_frame = frame.copy()
        temp_frame.set_alpha(alpha)
        screen.blit(temp_frame, (0, 0))
        screen.blit(button_image, button_rect.topleft)  # 在动画帧上绘制按钮
        pygame.display.flip()
        clock.tick(30)

# **修改检测按钮是否点击的函数**
def check_button_click(rect):  # **修改函数以接受按钮的矩形参数**
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if rect.collidepoint(event.pos):
                return True
    return False

# 播放开场动画
def play_intro():
    while True:
        for frame in frames:
            fade_in(frame)
            time.sleep(0.5)
            fade_out(frame)
            if check_button_click(button_rect):
                pygame.mixer.music.stop()  # 停止当前音乐
                pygame.mixer.music.load(resource_path('music/game_music.mp3'))  # 加载游戏进行中的音乐
                pygame.mixer.music.play(-1)  # 循环播放
                return


# 颜色
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)

# 鸟类
class Bird:
    def __init__(self):
        self.x = 100
        self.y = HEIGHT // 2
        self.gravity = 0.6
        self.lift = -15
        self.velocity = 0

    def show(self):
        screen.blit(bird_image, (self.x - 20, self.y - 20))

    def update(self):
        self.velocity += self.gravity
        self.y += self.velocity

        if self.y > HEIGHT:
            self.y = HEIGHT
            self.velocity = 0

        if self.y < 0:
            self.y = 0
            self.velocity = 0

    def up(self):
        self.velocity += self.lift

# 管道类
class Tube:
    def __init__(self):
        self.x = WIDTH
        self.width = 80
        self.gap = 200
        self.top = random.randint(50, HEIGHT - self.gap - 50)
        self.bottom = self.top + self.gap
        self.speed = 5

    def show(self): 
        screen.blit(pipe_top_image, (self.x, self.top - pipe_top_image.get_height())) 
        screen.blit(pipe_bottom_image, (self.x, self.bottom))

    def update(self):
        self.x -= self.speed

    def offscreen(self):
        return self.x < -self.width

    def hits(self, bird):
        if bird.y < self.top or bird.y > self.bottom:
            if bird.x + 20 > self.x and bird.x - 20 < self.x + self.width:
                return True
        return False

# 金币类
class Coin:
    def __init__(self,tubes):
        self.x = random.randint(WIDTH, WIDTH + 1000)
        self.y = random.randint(50, HEIGHT - 50)
        self.generate_position(tubes)
        self.speed = 5

    def generate_position(self, tubes):
        while True:
            self.x = random.randint(WIDTH, WIDTH + 1000)
            self.y = random.randint(50, HEIGHT - 50)
            overlapping = False

            for tube in tubes:
                if (self.x > tube.x and self.x < tube.x + tube.width) and \
                   (self.y > tube.top and self.y < tube.bottom):
                    overlapping = True
                    break

            if not overlapping:
                break
    def show(self):
        screen.blit(coin_image, (self.x, self.y))

    def update(self):
        self.x -= self.speed

    def collect(self, bird): 
        return self.x < bird.x + 20 and self.x > bird.x - 20 and self.y < bird.y + 20 and self.y > bird.y - 20

    def offscreen(self):
        return self.x < -30

# 背景定义
background_image = pygame.image.load(resource_path('pic/background.png'))
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))
bg_x1 = 0
bg_x2 = WIDTH
bg_speed = 2

# **添加函数：重置游戏**
def reset_game():
    global bird, coins, tubes, score, bg_x1, bg_x2, running
    bird = Bird()
    tubes = [Tube()]
    coins = [Coin(tubes) for _ in range(5)]
    tubes = [Tube()]
    score = 0
    bg_x1 = 0
    bg_x2 = WIDTH
    running = True

# **添加函数：显示游戏结束画面**
def show_game_over():
    pygame.mixer.music.stop()  # 停止背景音乐
    game_over_sound.play(loops=-1)  # 循环播放游戏结束音效

    game_over_text = font.render("Game Over", True, (255, 0, 0))
    text_rect = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 3))
    screen.blit(game_over_text, text_rect)
    screen.blit(restart_button_image, restart_button_rect.topleft)
    pygame.display.flip()

    while True:
        if check_button_click(restart_button_rect):
            game_over_sound.stop()  # 停止游戏结束音效
            reset_game()
            pygame.mixer.music.play(-1)  # 重新播放背景音乐
            break
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

# **初始化游戏**
reset_game()

play_intro()  # 播放开头动画 

# **修改循环结构**
while True:
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bird.up()
                    jump_sound.play()  # 播放跳跃音效

        bird.update()

        if tubes[-1].x < WIDTH - 300:
            tubes.append(Tube())

        for tube in tubes:
            tube.update()
            if tube.hits(bird):
                game_over_sound.play()  # 播放游戏结束音效
                running = False
            if tube.offscreen():
                tubes.remove(tube)
                score += 1
        if bird.y >= HEIGHT or bird.y <= 0:
            game_over_sound.play()  # 播放游戏结束音效
            running = False
        bg_x1 -= bg_speed
        bg_x2 -= bg_speed
        if bg_x1 < -WIDTH:
            bg_x1 = WIDTH
        if bg_x2 < -WIDTH:
            bg_x2 = WIDTH

        # 绘制背景
        screen.blit(background_image, (bg_x1, 0))
        screen.blit(background_image, (bg_x2, 0))

        bird.show()
        for tube in tubes:
            tube.show()

        # 更新并绘制金币 
        for coin in coins: 
            coin.update() 
            coin.show() 
            if coin.offscreen(): 
                coins.remove(coin) 
                coins.append(Coin(tubes))
            if coin.collect(bird): 
                coins.remove(coin) 
                score += 5  # 吃掉金币加5分
                coin_sound.play()  # 播放吃金币音效

        # 显示分数
        score_text = font.render(f'Score: {score}', True, (0, 0, 0))
        screen.blit(score_text, (10, 10))

        #分数大于100到达结算界面
        if score>=10:
            show_chest()
            running=False

        pygame.display.flip()
        clock.tick(30)

    # **显示游戏结束画面**
        if not running:
            show_game_over()

pygame.quit()