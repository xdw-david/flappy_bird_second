import pygame
import random
import time

# 初始化 Pygame
pygame.init()
pygame.font.init()
font=pygame.font.SysFont('Arial',32)

# 屏幕尺寸
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# 加载并缩放鸟类图像 
bird_image = pygame.image.load('pic/bird.png') 
bird_image = pygame.transform.scale(bird_image, (40, 40))

# 加载管道图像 
pipe_top_image = pygame.image.load('pic/tube_up.png')
pipe_top_image = pygame.transform.scale(pipe_top_image, (80, 400))
pipe_bottom_image = pygame.image.load('pic/tube_down.png')
pipe_bottom_image = pygame.transform.scale(pipe_bottom_image, (80, 400))

#加载金币图像
coin_image = pygame.image.load('pic/coin.png')
coin_image = pygame.transform.scale(coin_image, (15, 30))


# 游戏时钟
clock = pygame.time.Clock()

# 加载动画帧 
frames = [ 
    pygame.image.load('pic/frame1.png'), 
    pygame.image.load('pic/frame2.png'), 
    pygame.image.load('pic/frame3.png'), 
    # 添加更多帧... 
]

# 加载并缩放按钮图像 
button_image = pygame.image.load('pic/start_button.png') 
button_image = pygame.transform.scale(button_image, (100, 50)) # 调整按钮大小 
button_rect = button_image.get_rect(center=(WIDTH // 1.5, HEIGHT // 1.5))

# 缩放动画帧 
frames = [pygame.transform.scale(frame, (WIDTH, HEIGHT)) for frame in frames]

#渐入效果
def fade_in(frame, duration=1.0):
    for alpha in range(0, 256, int(256 / (duration * 30))):
        temp_frame = frame.copy()
        temp_frame.set_alpha(alpha)
        screen.blit(temp_frame, (0, 0))
        screen.blit(button_image, button_rect.topleft) # 在动画帧上绘制按钮
        pygame.display.flip()
        clock.tick(30)

#渐出效果
def fade_out(frame, duration=1.0):
    for alpha in range(255, -1, -int(256 / (duration * 30))):
        temp_frame = frame.copy()
        temp_frame.set_alpha(alpha)
        screen.blit(temp_frame, (0, 0))
        screen.blit(button_image, button_rect.topleft) # 在动画帧上绘制按钮
        pygame.display.flip()
        clock.tick(30)


#检测按钮是否点击
def check_button_click(): 
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT: 
            pygame.quit() 
            exit() 
        if event.type == pygame.MOUSEBUTTONDOWN: 
            if button_rect.collidepoint(event.pos): 
                return True 
    return False

#播放开场动画
def play_intro():
    while True:
        for frame in frames:
            fade_in(frame)
            time.sleep(0.5)
            fade_out(frame)
            if check_button_click():
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

#金币类
class Coin:
    def __init__(self):
        self.x = random.randint(WIDTH, WIDTH + 1000)
        self.y = random.randint(50, HEIGHT - 50)
        self.speed = 5
    def random_y_position(self, tubes): 
        while True: 
            y = random.randint(50, HEIGHT - 50) 
            for tube in tubes: 
                if tube.x < self.x < tube.x + tube.width and tube.top < y < tube.bottom: 
                    valid = False 
                    break 
                if valid:
                    return y

    def show(self):
        screen.blit(coin_image, (self.x, self.y))

    def update(self):
        self.x -= self.speed

    def collect(self, bird): 
        return self.x < bird.x + 20 and self.x > bird.x - 20 and self.y < bird.y + 20 and self.y > bird.y - 20

    def offscreen(self):
        return self.x < -30

# 背景定义
background_image = pygame.image.load('pic/background.png')
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))
bg_x1 = 0
bg_x2 = WIDTH
bg_speed = 2

# 游戏循环
bird = Bird()
coins = [Coin() for _ in range(5)] # 生成初始的金币
tubes = [Tube()] # 生成管道
score = 0
running = True
play_intro() # 播放开头动画 
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird.up()

    bird.update()

    if tubes[-1].x < WIDTH - 300:
        tubes.append(Tube())

    for tube in tubes:
        tube.update()
        if tube.hits(bird):
            running = False
        if tube.offscreen():
            tubes.remove(tube)
            score += 1
    bg_x1 -= bg_speed
    bg_x2 -= bg_speed
    if bg_x1 < -WIDTH:
        bg_x1 = WIDTH
    if bg_x2 < -WIDTH:
        bg_x2 = WIDTH

    #绘制背景
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
            coins.append(Coin())
        if coin.collect(bird): 
            coins.remove(coin) 
            score += 5 # 吃掉金币加5分
    #显示分数
    score_text = font.render(f'Score: {score}', True, (0, 0, 0))
    screen.blit(score_text,(10,10))
    pygame.display.flip()
    clock.tick(30)

pygame.quit()
