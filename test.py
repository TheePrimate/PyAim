import pygame
from network import Network
import pickle
import random
from constants import WIDTH
from constants import HEIGHT
from constants import FPS
from constants import BACKGROUND_COLOUR
from constants import MENU_COLOUR
pygame.font.init()

window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Test Client")


class Target:
    def __init__(self):
        self.text = "Hit Me!"
        self.radius = 50
        self.x = random.randint(self.radius + self.radius / 2, WIDTH - self.radius)
        self.y = random.randint(self.radius + self.radius / 2, HEIGHT - self.radius)
        self.color = (random.randint(0,255), random.randint(0, 255), random.randint(0, 255))

    def draw(self, window):
        pygame.draw.circle(window, self.color, (self.x,self.y), self.radius)
        font = pygame.font.SysFont("Times New Roman", 20)
        text = font.render(self.text, 1, (255,255,255))
        window.blit(text, (self.x - round(self.radius/20) - round(text.get_width()/2), self.y - round(self.radius/20) - round(text.get_height()/2)))

    def click(self, pos):
        x1 = pos[0]
        y1 = pos[1]
        if ((x1 - self.x) ** 2 + (y1 - self.y) ** 2)**0.5 <= self.radius:
            print("hit")
            return True
        else:
            print("miss")
            return False

class Button:
    def __init__(self):
        self.text = "Start"

        self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        self.width = 300
        self.height = 150
        self.x = WIDTH / 2 - self.width / 2
        self.y = HEIGHT / 2

    def draw(self, window):
        pygame.draw.rect(window, self.color, (self.x, self.y, self.width, self.height))
        font = pygame.font.SysFont("Times New Roman", 40)
        text = font.render(self.text, 1, (255,255,255))
        window.blit(text, (self.x + round(self.width/2) - round(text.get_width()/2), self.y + round(self.height/2) - round(text.get_height()/2)))

    def click(self, pos):
        x2 = pos[0]
        y2 = pos[1]
        if self.x <= x2 <= self.x + self.width and self.y <= y2 <= self.y + self.height:
            print("Start")
            return True
        else:
            print("How'd you miss")
            return False


targets = []
def redrawWindow(window, game, p):
    window.fill(BACKGROUND_COLOUR)

    if not(game.connected()):
        font = pygame.font.SysFont("Times No Roman", 80)
        text = font.render("Waiting for Another Client to Connect...", 1, (255,0,0))
        window.blit(text, (WIDTH/2 - text.get_width()/2, HEIGHT/2 - text.get_height()/2))

    else:
        font = pygame.font.SysFont("Times New Roman", 60)
        text = font.render("Your Move", 1, (0, 255,255))
        window.blit(text, (80, 200))

        text = font.render("Opponents", 1, (0, 255, 255))
        window.blit(text, (380, 200))

        move1 = game.get_player_move(0)
        move2 = game.get_player_move(1)
        if game.bothWent():
            text1 = font.render(move1, 1, (0,0,0))
            text2 = font.render(move2, 1, (0, 0, 0))
        else:
            if game.p1Went and p == 0:
                text1 = font.render(move1, 1, (0,0,0))
            elif game.p1Went:
                text1 = font.render("Locked In", 1, (0, 0, 0))
            else:
                text1 = font.render("Waiting...", 1, (0, 0, 0))

            if game.p2Went and p == 1:
                text2 = font.render(move2, 1, (0,0,0))
            elif game.p2Went:
                text2 = font.render("Locked In", 1, (0, 0, 0))
            else:
                text2 = font.render("Waiting...", 1, (0, 0, 0))

        if p == 1:
            window.blit(text2, (100, 350))
            window.blit(text1, (400, 350))
        else:
            window.blit(text1, (100, 350))
            window.blit(text2, (400, 350))

        target_sprite = Target()

        if len(targets) < 1:
            targets.append(target_sprite)
        for target in targets:
            target.draw(window)

    pygame.display.update()

def menu_screen():
    run = True
    clock = pygame.time.Clock()
    start_sprite = Button()
    while run:
        clock.tick(FPS)
        window.fill(MENU_COLOUR)
        font = pygame.font.SysFont("Times New Roman", 60)
        text = font.render("Click to Play!", 1, (255,0,0))
        window.blit(text, (WIDTH / 2 - text.get_width()/2, HEIGHT / 2 - HEIGHT / 4))
        start_sprite.draw(window)
        pygame.display.update()

        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN and start_sprite.click(pos) is True:
                run = False

    main()


def main():
    run = True
    clock = pygame.time.Clock()
    n = Network()
    player = int(n.getP())
    print("You are player", player + 1)
    counter = 0
    counter_seconds= 0

    while run:
        clock.tick(FPS)
        counter += 1
        try:
            game = n.send("get")
        except:
            run = False
            print("Couldn't get game")
            break

        if game.bothWent():
            redrawWindow(window, game, player)
            pygame.time.delay(500)
            try:
                game = n.send("reset")
            except:
                run = False
                print("Couldn't get game")
                break

            font = pygame.font.SysFont("Times New Roman", 90)
            if (game.winner() == 1 and player == 1) or (game.winner() == 0 and player == 0):
                text = font.render("You Won!", 1, (255,0,0))
            elif game.winner() == -1:
                text = font.render("Tie Game!", 1, (255,0,0))
            else:
                text = font.render("You Lost...", 1, (255, 0, 0))

            window.blit(text, (WIDTH/2 - text.get_width()/2, HEIGHT/2 - text.get_height()/2))
            pygame.display.update()
            pygame.time.delay(2000)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()

                for target in targets:
                    if target.click(pos) and game.connected():
                        counter_seconds = 0
                        targets.remove(target)
                        if player == 0:
                            if not game.p1Went:
                                n.send(target.text)
                        else:
                            if not game.p2Went:
                                n.send(target.text)

        if counter % FPS == 0:
            counter_seconds += 1
            if counter_seconds % 2 == 0:
                for target in targets:
                    targets.remove(target)
                    print("Too Late...")
        redrawWindow(window, game, player)


while True:
    menu_screen()
