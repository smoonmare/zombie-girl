import pygame
import os

pygame.init()

screen_width = 1200
screen_height = 750
animation = 4

class Character(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        all_images = os.listdir(self.path)
        self.images = {image: pygame.transform.scale(pygame.image.load(self.path + image).convert_alpha(), (50, 50)) for image in all_images}
        self.image = self.images['Idle (1).png']
        self.rect = self.image.get_rect()
        self.mode_num = 1

    def move(self, surface, location):
        x, y = location
        self.rect.x = x
        self.rect.y = y

    def walk(self, velocity, frame):
        if frame == animation:
            if self.mode_num == self.max_walk:
                self.mode_num = 0
            self.mode_num += 1
        current_img = 'Walk (' + str(self.mode_num) + ').png'

        if velocity < 0:
            self.image = pygame.transform.flip(self.images[current_img], True, False)
        else:
            self.image = self.images[current_img]

        if self.rect.x + velocity >=0 and self.rect.x + 50 + velocity <= screen_width:
            self.rect.x += velocity

class Girl(Character):

    def __init__(self):
        self.path = 'png/Girl/'
        Character.__init__(self)
        self.rect.x = 0
        self.rect.y = 0

class Zombie(Character):

    def __init__(self):
        self.path = 'png/Zombie/female/'
        Character.__init__(self)
        self.rect.x = 100
        self.rect.y = 100
        self.max_walk = 10
        self.jump_velocity = 15

    def jump(self, level_rects):
        mass = 3
        force = (int)(0.5 * mass) * self.jump_velocity^2
        self.rect.y -= force
        self.jump_velocity -= 1

        # if jump velocity is less than 0, we've reached the top of the jump, so
        # need to negate the mass so negative velocity doesn't affect movement
        if self.jump_velocity < 0:
            mass = -1
        # check to see if velocity has returned exceeded original upward velocity so acceleration doesn't continue
        if self.jump_velocity == -16:
            self.jump_velocity == -15
        
        # check for a collision with a platform
        collision = self.rect.collidelist(level_rects)
        if collision == -1 and self.rect.y < screen_height:
            if (self.rect.x + 54 <= screen_width):
                self.rect.x += 4
            return True  #still jumping
        if collision >= 0:
            mass = 3
            self.jump_velocity = 15
            self.rect.y = level_rects[collision][1] - 50 # subtracting the height of the image
            return False

class Level(object):
    coordinates = [[['Tile1.png', screen_width - 1200, screen_height - 50],
                    ['Tile2.png', screen_width - 1150, screen_height - 50],
                    ["Tile2.png", screen_width - 1100, screen_height - 50],
                    ["Tile2.png", screen_width - 1050, screen_height - 50],
                    ["Tile3.png", screen_width - 1000, screen_height - 50], \
                    ["Tile14.png", screen_width - 900, screen_height - 150],
                    ["Tile15.png", screen_width - 850, screen_height - 150],
                    ["Tile15.png", screen_width - 800, screen_height - 150],
                    ["Tile15.png", screen_width - 750, screen_height - 150],
                    ["Tile16.png", screen_width - 700, screen_height - 150], \
                    ["Tile14.png", screen_width - 700, screen_height - 250],
                    ["Tile15.png", screen_width - 650, screen_height - 250],
                    ["Tile15.png", screen_width - 600, screen_height - 250],
                    ["Tile15.png", screen_width - 550, screen_height - 250],
                    ["Tile15.png", screen_width - 500, screen_height - 250],
                    ["Tile16.png", screen_width - 450, screen_height - 250], \
                    ["Tile14.png", screen_width - 350, screen_height - 300],
                    ["Tile15.png", screen_width - 300, screen_height - 300],
                    ["Tile15.png", screen_width - 250, screen_height - 300],
                    ["Tile15.png", screen_width - 200, screen_height - 300],
                    ["Tile15.png", screen_width - 150, screen_height - 300],
                    ["Tile15.png", screen_width - 100, screen_height - 300],
                    ["Tile16.png", screen_width - 50, screen_height - 300] \
                        ]]
    limits = {screen_height - 50: (screen_width - 1200, screen_width - 1000), \
        screen_height - 150: (screen_width - 900, screen_width - 700), \
            screen_height - 250: (screen_width - 700, screen_width - 450), \
                screen_height - 300: (screen_width - 350, screen_width - 50)}

    def __init__(self,id):
        self.id = id
        path = 'png/Tiles/'
        all_images = os.listdir(path)
        self.img = {image: pygame.transform.scale(pygame.image.load(path + image).convert_alpha(), (50, 50)) for image in all_images}

    def build_level(self, surface):
        for tile in self.coordinates[self.id]:
            surface.blit(self.img[tile[0]], (tile[1], tile[2]))

    def get_pc_starting_points(self):
        player_character = (self.coordinates[self.id][0][1], self.coordinates[self.id][0][2] - 50)
        return player_character

    def get_npc_starting_points(self):
        npc = (self.coordinates[self.id][5][1] + 50, self.coordinates[self.id][5][2] - 50)
        return npc

    def platform_check(self, x, y):
        y += 50
        if y in self.limits:
            min, max = self.limits[y]
            if x >= min - 25 and x <= max + 25:
                return True
        return False

    def get_rects(self):
        level_rects = []
        for item in self.limits.items():
            x1, x2 = item[1]
            length = x2 - x1 + 50
            level_rects.append(pygame.Rect(x1, item[0], length, 50))
        return level_rects

class HUD(object):

    def __init__(self):
        self.score = 0
        self.level = 1
        self.message = 'Game on!'
        self.lives = 9

    def increment_level(self):
        self.level += 1

    def decrement_lives(self):
        self.lives -= 1
    
    def update_message(self, message):
        self.message = message

    def display(self, display, message, help):
        font_title = pygame.font.Font(None, 24)
        if help:
            msg = font_title.render('Use A, D, [left-arrow], [right-arrow], [SPACE] to move', True, (255, 255, 255))
            msg_rect = msg.get_rect(center=(int(screen_width / 2), screen_height))
            display.blit(msg, msg_rect)
        lives = font_title.render('Lives: ' + str(self.lives), True, (255, 255, 255))
        lives_rect = lives.get_rect(center=(int(screen_width / 5), 15))
        display.blit(lives, lives_rect)

        score = font_title.render('Score: ' + str(self.score), True, (255, 255, 255))
        score_rect = score.get_rect(center=(int(screen_width * 0.8), 15))
        display.blit(score, score_rect)

        msg = font_title.render(message, True, (255, 255, 255))
        msg_rect = msg.get_rect(center=(int(screen_width / 2), 15))
        display.blit(msg, msg_rect)

def main():
    help_action = False
    help_time = 0
    walking = 1
    velocity = 0
    message_current = 'Avoid the girl and get to the exit!'
    game_clock= pygame.time.Clock()
    screen_size = (screen_width, screen_height)
    screen = pygame.display.set_mode(screen_size, 0, 32)
    background = pygame.image.load('png/BG.png').convert()
    is_jumping = False

    level = Level(0)
    zombie = Zombie()
    girl = Girl()
    char_list = pygame.sprite.Group()
    char_list.add(girl, zombie)
    headsup = HUD()

    glocation = level.get_npc_starting_points()
    zlocation = level.get_pc_starting_points()
    girl.move(screen, glocation)
    zombie.move(screen, zlocation)

    #pick up the platform rects
    level_rects = level.get_rects()

    while True:
        game_clock.tick(45)

        pressed_key = pygame.key.get_pressed()
        right_action = pressed_key[pygame.K_RIGHT] or pressed_key[pygame.K_d]
        left_action = pressed_key[pygame.K_LEFT] or pressed_key[pygame.K_a]
        jump_action = pressed_key[pygame.K_SPACE]

        if right_action:
            if not is_jumping:
                velocity = 2
                zombie.walk(velocity, walking)
                walking += 1
            
        
        if left_action:
            if not is_jumping:
                velocity = -2
                zombie.walk(velocity, walking)
                walking += 1

        if jump_action:
            is_jumping = True


        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                needs_help = event.key != pygame.K_RIGHT and event.key != pygame.K_d and event.key != pygame.K_LEFT and event.key != pygame.K_a and event.key != pygame.K_SPACE
                if needs_help:
                    help_action = True
                    help_time = pygame.time.get_ticks()
            if event.type == pygame.QUIT:
                pygame.quit()
            if help_action == True and help_time == 0 or pygame.time.get_ticks() - help_time >= 5000:
                help_action = False

        if not level.platform_check(zombie.rect.x, zombie.rect.y) and not is_jumping:
            zombie.rect.x += 25
            while zombie.rect.y < screen_height - 75:
                zombie.image = pygame.transform.rotate(zombie.image, velocity * -90)
                screen.blit(pygame.transform.scale(background, screen_size), (0, 0))
                level.build_level(screen)
                char_list.draw(screen)
                pygame.display.flip()
                zombie.rect.x += velocity
                zombie.rect.y += 5
                pygame.time.delay(250)
            pygame.quit()
        elif is_jumping:
            is_jumping = zombie.jump(level_rects)

        screen.blit(pygame.transform.scale(background, screen_size), (0, 0))
        level.build_level(screen)
        char_list.draw(screen)
        headsup.display(screen, message_current, help_action)
        pygame.display.flip()
        if walking == animation + 1:
            walking = 1

if __name__ == "__main__":
    main()