import pygame
import random
from network import Network
from constants import WIDTH
from constants import HEIGHT
from constants import FPS
from constants import BACKGROUND_COLOUR
from constants import MENU_COLOUR
from constants import TEXT_IN_MAIN_X1
from constants import TEXT_IN_MAIN_X2
from constants import TEXT_IN_MAIN_Y
from constants import PLAY_TIME
from constants import HIT_VALUE
from constants import MISS_VALUE
from constants import LATE_VALUE
from constants import Crosshair
pygame.font.init()

# Set window to width and height with constants
window = pygame.display.set_mode((WIDTH, HEIGHT))
# Names the window as "Client"
pygame.display.set_caption("Client")


# Make a class named target, which will be responsible for drawing each target
# and responsible for if the player has successfully hit the target or not
class Target:
    def __init__(self):
        # Display text "Hit Me!" within each target
        self.text = "Hit Me!"
        self.radius = 50
        self.x = random.randint(self.radius + int(self.radius / 2), WIDTH - self.radius)
        self.y = random.randint(self.radius + int(self.radius / 2), HEIGHT - self.radius)
        # Make each target a random colour each time it spawns
        self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

    def draw(self, drawing_surface):
        # Draw a circle at the designated screen, with the information from the __init__ function.
        pygame.draw.circle(drawing_surface, self.color, (self.x, self.y), self.radius)
        # Define what font type to use and the size
        font = pygame.font.SysFont("Times New Roman", 20)
        # Assign the text that needs to be displayed with
        # the font information, with anti-alias and the given colour.
        text = font.render(self.text, 1, (255, 255, 255))
        # Transfer the text data to the designated screen to be drawn
        # with its center at the center of the rectangle.
        drawing_surface.blit(text, (self.x - round(self.radius / 20) - round(text.get_width() / 2),
                                    self.y - round(self.radius/20) - round(text.get_height()/2)))

    # If the mouse click position is within the circle, return True
    # The math uses Pythagorean Theorem to calculate if the hypotenuse (distance from
    # mouse click position to circle) is less than, equal to, or greater than the radius.
    # If the calculated hypotenuse is smaller or equal to the radius of the circle, the target is hit.
    def click(self, pos):
        x1 = pos[0]
        y1 = pos[1]
        if ((x1 - self.x) ** 2 + (y1 - self.y) ** 2)**0.5 <= self.radius:
            return True
        else:
            return False


# Class for the start game button
class Button:
    def __init__(self):
        self.text = "Start"
        self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        self.width = 300
        self.height = 150
        self.x = WIDTH / 2 - self.width / 2
        self.y = HEIGHT / 2

    def draw(self, drawing_surface):
        pygame.draw.rect(drawing_surface, self.color, (self.x, self.y, self.width, self.height))
        font = pygame.font.SysFont("Times New Roman", 40)
        text = font.render(self.text, 1, (255, 255, 255))
        drawing_surface.blit(text, (self.x + round(self.width / 2) - round(text.get_width() / 2),
                                    self.y + round(self.height / 2) - round(text.get_height() / 2)))

    def click(self, pos):
        x2 = pos[0]
        y2 = pos[1]
        if self.x <= x2 <= self.x + self.width and self.y <= y2 <= self.y + self.height:
            print("Game start")
            return True
        else:
            print("How'd you miss... maybe... don't play this game")
            return False


targets = []
# Load the image of the crosshair and assign it to a variable
crosshair = pygame.image.load(Crosshair)
# Make the crosshair an object which can interact with the game
crosshair_img_rect = crosshair.get_rect()


def redrawWindow(drawing_surface, game, p, mouse_pos):
    drawing_surface.fill(BACKGROUND_COLOUR)
    target_sprite = Target()

    # While the game is not connected, display a waiting for another player screen.
    if not game.connected():
        font = pygame.font.SysFont("Times No Roman", 80)
        text = font.render("Waiting for Another Client to Connect...", 1, (255, 0, 0))
        drawing_surface.blit(text, (WIDTH / 2 - text.get_width() / 2, HEIGHT / 2 - text.get_height() / 2))

    # If the game has two players, draw the GUI of the game.
    else:
        font = pygame.font.SysFont("Times New Roman", 60)
        text = font.render("Your Move", 1, (0, 255, 255))
        drawing_surface.blit(text, (TEXT_IN_MAIN_X1 - text.get_width() / 2, TEXT_IN_MAIN_Y))

        text = font.render("Opponents", 1, (0, 255, 255))
        drawing_surface.blit(text, (TEXT_IN_MAIN_X2 - text.get_width() / 2, TEXT_IN_MAIN_Y))

        # Get the other client's player score from the Game.py file.
        score1 = game.get_player_score(0)
        score2 = game.get_player_score(1)
        # If both players submitted their scores, assign those scores into variables
        if game.bothWent():
            text1 = font.render(f"Score: {score1}", 1, (0, 0, 0))
            text2 = font.render(f"Score: {score2}", 1, (0, 0, 0))
        else:
            # If player 1 is done, and you are player 1, display your score.
            if game.p1Went and p == 0:
                text1 = font.render(f"Score: {score1}", 1, (0, 0, 0))
            # If player 1 is done, and you are player 2, display that player 1 is done.
            elif game.p1Went:
                text1 = font.render("Done", 1, (0, 0, 0))
            # If no one is done, display waiting.
            else:
                text1 = font.render("Waiting...", 1, (0, 0, 0))

            # Same as before, but for the perspective of player 2.
            if game.p2Went and p == 1:
                text2 = font.render(f"Score: {score2}", 1, (0, 0, 0))
            elif game.p2Went:
                text2 = font.render("Done", 1, (0, 0, 0))
            else:
                text2 = font.render("Waiting...", 1, (0, 0, 0))

        # Actually draws the aforementioned text, depending on which player you are.
        if p == 0:
            drawing_surface.blit(text1, (TEXT_IN_MAIN_X1 - text.get_width() / 2, TEXT_IN_MAIN_Y * 2))
            drawing_surface.blit(text2, (TEXT_IN_MAIN_X2 - text.get_width() / 2, TEXT_IN_MAIN_Y * 2))
        if p == 1:
            drawing_surface.blit(text2, (TEXT_IN_MAIN_X1 - text.get_width() / 2, TEXT_IN_MAIN_Y * 2))
            drawing_surface.blit(text1, (TEXT_IN_MAIN_X2 - text.get_width() / 2, TEXT_IN_MAIN_Y * 2))

        # Detect if there are any targets within the list, if
        # there are less than one add a target to the list.
        if len(targets) < 1:
            targets.append(target_sprite)
        # Draw the one target.
        for target in targets:
            target.draw(drawing_surface)

        # Constantly draw the crosshair at the position of the mouse.
        crosshair_img_rect.center = mouse_pos
        drawing_surface.blit(crosshair, crosshair_img_rect)

    # Updates the window.
    pygame.display.update()


def menu_screen():
    run = True
    clock = pygame.time.Clock()
    start_sprite = Button()
    while run:
        # Make the menu screen run at the designated tick rate.
        clock.tick(FPS)
        window.fill(MENU_COLOUR)
        font = pygame.font.SysFont("Times New Roman", 60)
        text = font.render("Click to Play!", 1, (255, 0, 0))
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
    print("You are Player", player + 1)
    frame_counter = 0
    general_counter_seconds = 0
    late_counter_seconds = 0
    points_hit = 0
    points_missed = 0
    points_late = 0
    pygame.mouse.set_visible(False)

    while run:
        clock.tick(FPS)
        frame_counter += 1
        mouse_pos = pygame.mouse.get_pos()
        try:
            game = n.send("get")
        except OSError:
            print("Connection lost...")
            break

        if game.bothWent():
            redrawWindow(window, game, player, mouse_pos)
            pygame.time.delay(500)
            try:
                game = n.send("reset")
                points_missed = 0
                points_hit = 0
                points_late = 0
                general_counter_seconds = 0
            except OSError:
                print("Connection lost...")
                break

            font = pygame.font.SysFont("Times New Roman", 90)
            # If this client is the player than won, display that you won.
            if (game.winner() == 1 and player == 1) or (game.winner() == 0 and player == 0):
                text = font.render("You Won!", 1, (255, 0, 0))
            elif game.winner() == -1:
                text = font.render("Tie Game!", 1, (255, 0, 0))
            else:
                text = font.render("You Lost...", 1, (255, 0, 0))

            window.blit(text, (WIDTH/2 - text.get_width()/2, HEIGHT/2 - text.get_height()/2))
            pygame.display.update()
            # Wait for 2000 milliseconds before restarting the game.
            pygame.time.delay(2000)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                # Get the position of the mouse click, and assign it to a variable.
                pos = pygame.mouse.get_pos()

                for target in targets:
                    # If successful hit on a target, remove that target...
                    # Another will be drawn in the reDraw window.
                    if target.click(pos):
                        # Counts how many seconds that the current target has existed for.
                        late_counter_seconds = 0
                        targets.remove(target)
                        points_hit += 1
                        print("You have hit:", points_hit, "times")
                    if target.click(pos) is False:
                        points_missed += 1
                        print("You have missed:", points_missed, "times")

        if frame_counter % FPS == 0:
            late_counter_seconds += 1
            general_counter_seconds += 1
            if late_counter_seconds % 2 == 0:
                for target in targets:
                    targets.remove(target)
                    points_late += 1
                    print("Too Late...\n", "You were late", points_late, "times")

        if general_counter_seconds >= PLAY_TIME:
            score = HIT_VALUE * points_hit + MISS_VALUE * points_missed + LATE_VALUE * points_late
            if player == 0:
                # If false (turn has not passed)... send data
                if not game.p1Went:
                    n.send(str(score))
            else:
                if not game.p2Went:
                    n.send(str(score))

        redrawWindow(window, game, player, mouse_pos)


while True:
    menu_screen()
