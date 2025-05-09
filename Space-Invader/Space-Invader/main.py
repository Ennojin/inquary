import pygame, sys, math
from player import Player
import obstacles, instructions
from alien import Alien, Extra
from random import choice, randint
from laser import Laser
from explosion import Explosion
from missile import Missile
from fire_spark import Fire_spark
from supply import Special_supply

class Game:
    def __init__(self):
        self.game_start = False
        self.game_active = False
        self.game_pause = False
        self.extra_spawn = False
        self.instruction = False
        self.instruction_index = 0
        self.pause_time = 0
        self.game_difficulty = 1
        # player setup
        player_sprite = Player((screen_width/2, screen_height), screen_width, screen_height, 5)
        self.player = pygame.sprite.GroupSingle(player_sprite)
        self.penetration_timer = pygame.time.get_ticks()
        self.laser_penetration = False
        self.penetration_icon = pygame.image.load('Space-invaders-main/graphics/stronger attack.png').convert_alpha()
        self.penetration_icon = pygame.transform.scale(self.penetration_icon, (60, 60))

        # heath and score setup
        self.lives = 3
        self.lives_surf = pygame.image.load('Space-invaders-main/graphics/player.png').convert_alpha()
        self.live_x_start_pos = screen_width - (self.lives_surf.get_size()[0] * 2 + 20)
        self.score = 0
        self.font = pygame.font.Font('Space-invaders-main/font/Pixeled.ttf', 20)

        # obstacle setup
        self.shape = obstacles.shape
        self.block_size = 6
        self.blocks = pygame.sprite.Group()
        self.obstacle_amount = 4
        self.obstacle_x_positions = [num*(screen_width / self.obstacle_amount) for num in range(self.obstacle_amount)]
        self.create_multiple_obstacles(screen_width/15, screen_height - 120,*self.obstacle_x_positions)

        # alien setup
        self.aliens = pygame.sprite.Group()
        self.alien_lasers = pygame.sprite.Group()
        self.alien_direction = 1

        # yellow aliens setup
        self.yellow_aliens = pygame.sprite.Group()
        self.locking_sound_playing = False

        # extra setup
        self.extra = pygame.sprite.GroupSingle()
        self.extra_spawn_time = randint(400, 800)

        # Audio
        self.laser_sound = pygame.mixer.Sound('Space-invaders-main/audio/laser.wav')
        self.laser_sound.set_volume(0.5)
        self.explosion_sound = pygame.mixer.Sound('Space-invaders-main/audio/explosion.wav')
        self.explosion_sound.set_volume(0.3)
        self.missile_launch_sound = pygame.mixer.Sound('Space-invaders-main/audio/missile_launch.mp3')
        self.missile_launch_sound.set_volume(1)
        self.extra_enter = pygame.mixer.Sound('Space-invaders-main/audio/special fly.mp3')
        self.extra_enter.set_volume(0.5)
        self.extra_die = pygame.mixer.Sound('Space-invaders-main/audio/special_killed.mp3')
        self.extra_die.set_volume(1)
        self.player_hurt = pygame.mixer.Sound('Space-invaders-main/audio/player hurt.mp3')
        self.player_hurt.set_volume(0.5)
        self.locking_sound = pygame.mixer.Sound('Space-invaders-main/audio/yellow_alien_shoot.MP3')
        self.locking_sound.set_volume(0.5)
        self.yellow_shoot_sound = pygame.mixer.Sound('Space-invaders-main/audio/yellow_laser_shoot.mp3')
        self.yellow_shoot_sound.set_volume(1)

        # explosion setup
        self.explosions = pygame.sprite.Group()

        # fire spark setup
        self.fire_sparks = pygame.sprite.Group()

        # missile setup
        self.missiles = pygame.sprite.Group()

        # special supply setup
        self.special_supplies = pygame.sprite.Group()

        # player got hit setup
        self.red_overlay = pygame.Surface((screen_width, screen_height))
        self.overlay_transparency = 0
        self.red_overlay.set_alpha(self.overlay_transparency)
        self.red_overlay.fill((255, 0, 0))
        self.show_red_flash = False
        self.flash_duration = 30
        self.flash_timer = self.flash_duration

        # energy level setup
        self.energy = 0
        self.max_energy = 150
        self.last_energy_update_time = pygame.time.get_ticks()

        # button setup
        self.big_button_unpressed = pygame.image.load('Space-invaders-main/graphics/buttons/big button unpressed.png').convert_alpha()
        self.big_button_pressed = pygame.image.load('Space-invaders-main/graphics/buttons/big button pressed.png').convert_alpha()
        self.small_button_unpressed = pygame.image.load('Space-invaders-main/graphics/buttons/small button unpressed.png').convert_alpha()
        self.small_button_pressed = pygame.image.load('Space-invaders-main/graphics/buttons/small button pressed.png').convert_alpha()

        # graphics
        self.start_menu_background = pygame.image.load('Space-invaders-main/graphics/starting_menu.png')
        self.start_menu_background = pygame.transform.scale(self.start_menu_background, (600, 700))
        self.red_alien = pygame.image.load('Space-invaders-main/graphics/red.png')
        self.red_alien = pygame.transform.scale(self.red_alien, (80, 64))
        self.red_alien_rect = self.red_alien.get_rect(center = (200, 400))
        self.red_alien_hurt = pygame.image.load('Space-invaders-main/graphics/red_hurt.png')
        self.red_alien_hurt = pygame.transform.scale(self.red_alien_hurt, (80, 64))
        self.red_alien_hurt_rect = self.red_alien_hurt.get_rect(center=(400, 400))
        self.player_image = pygame.image.load('Space-invaders-main/graphics/player.png')
        self.player_image = pygame.transform.scale(self.player_image, (90, 45))
        self.player_rect = self.player_image.get_rect(center = (screen_width/2, 400))
        self.green_alien = pygame.image.load('Space-invaders-main/graphics/green.png')
        self.green_alien = pygame.transform.scale(self.green_alien, (80, 64))
        self.green_alien_rect = self.green_alien.get_rect(center=(screen_width/2, 400))
        self.yellow_alien = pygame.image.load('Space-invaders-main/graphics/yellow.png')
        self.yellow_alien = pygame.transform.scale(self.yellow_alien, (80, 64))
        self.yellow_alien_rect = self.yellow_alien.get_rect(center=(screen_width/2, 400))
        self.extra_alien = pygame.image.load('Space-invaders-main/graphics/extra.png')
        self.extra_alien = pygame.transform.scale(self.extra_alien, (150, 50))
        self.extra_alien_rect = self.extra_alien.get_rect(center=(screen_width / 2, 430))
        self.attack_supply = pygame.image.load('Space-invaders-main/graphics/stronger attack.png')
        self.attack_supply = pygame.transform.scale(self.attack_supply, (80, 80))
        self.attack_supply_rect = self.attack_supply.get_rect(center=(180, 430))
        self.health_supply = pygame.image.load('Space-invaders-main/graphics/health restore.png')
        self.health_supply = pygame.transform.scale(self.health_supply, (80, 80))
        self.health_supply_rect = self.health_supply.get_rect(center=(screen_width / 2, 430))
        self.obstacle_supply = pygame.image.load('Space-invaders-main/graphics/obstcal restore.png')
        self.obstacle_supply = pygame.transform.scale(self.obstacle_supply, (80, 80))
        self.obstacle_supply_rect = self.obstacle_supply.get_rect(center=(430, 430))


    def create_obstacle(self, x_start, y_start, offset_x):
        for row_index, row in enumerate(self.shape):
            for col_index, col in enumerate(row):
                if col == "x":
                    x = x_start + col_index * self.block_size + offset_x
                    y = y_start + row_index * self.block_size
                    block = obstacles.Block(self.block_size, (241, 79, 80), x, y)
                    self.blocks.add(block)

    def create_multiple_obstacles(self, x_start, y_start, *offset):
        for offset_x in offset:
            self.create_obstacle(x_start, y_start, offset_x)

    def alien_setup(self, rows, cols, color, x_distance = 60, y_distance = 48, x_offset = 70, y_offset = 100):
        if color == 'red': y_offset = 100 + 3 * y_distance
        elif color == 'green': y_offset = 100 + y_distance
        for row_index, row in enumerate(range(rows)):
            for col_index, col in enumerate(range(cols)):
                x = col_index * x_distance + x_offset
                y = row_index * y_distance + y_offset
                alien_sprite = Alien(color, x, y, self.player, self.alien_lasers, screen, screen_height, self.game_difficulty)
                if color != 'yellow':
                    self.aliens.add(alien_sprite)
                else:
                    self.yellow_aliens.add(alien_sprite)

    def alien_init(self):
        self.alien_setup(2, 8, 'green')
        self.alien_setup(3, 8, 'red')
        self.alien_setup(1, 8, 'yellow')

    def alien_position_checker(self):
        all_aliens = self.aliens.sprites() + self.yellow_aliens.sprites()
        for alien in all_aliens:
            if alien.rect.right >= screen_width:
                self.alien_direction = -1
                self.alien_move_down(2)
            elif alien.rect.left <= 0:
                self.alien_direction = 1
                self.alien_move_down(2)

    def alien_move_down(self, distance):
        all_aliens = self.yellow_aliens.sprites() + self.aliens.sprites()
        if all_aliens:
            for alien in all_aliens:
                alien.rect.y += distance

    def alien_shoot(self):
        if self.aliens.sprites() and self.game_start:
            random_alien = choice(self.aliens.sprites())
            laser_sprite = Laser(random_alien.rect.center,screen_height,6, 'alien')
            self.alien_lasers.add(laser_sprite)
            #self.green_alien_death_shoot(random_alien.rect.midbottom, self.alien_lasers)
            fire_spark = Fire_spark(random_alien.rect.x, random_alien.rect.bottom, 50, self.alien_direction)
            self.fire_sparks.add(fire_spark)
            self.laser_sound.play()

    def green_alien_death_shoot(self, pos, laser_group):
        if self.game_difficulty == 1:
            angles = [0]
        elif self.game_difficulty == 2:
            angles = [-30, 30, 0]
        else:
            angles = [-30, -15, 0, 15, 30]
        for angle in angles:
            laser = Laser(pos, screen_height, 8, 'alien', angle)
            laser_group.add(laser)

    def extra_alien_timer(self):
        if self.extra_spawn:
            self.extra_spawn_time -= 1
            if self.extra_spawn_time <= 0:
                self.extra.add(Extra(choice(['right','left']), screen_width, screen))
                self.extra_enter.play()
                self.extra_spawn_time = randint(400, 800)

    def extra_missile_shoot(self):
        if self.extra:
            for extra in self.extra:
                if extra.rect.x <= screen_width and extra.rect.x >= 0:
                    missile_sprite = Missile(extra.rect.center, screen_height)
                    self.missile_launch_sound.play()
                    self.missiles.add(missile_sprite)
                    fire_spark = Fire_spark(extra.rect.x, extra.rect.bottom, 75, extra.speed)
                    self.fire_sparks.add(fire_spark)

    def player_got_hit(self):
        if self.show_red_flash:
            self.red_overlay.set_alpha(self.overlay_transparency)
            screen.blit(self.red_overlay, (0, 0))
            self.flash_timer -= 1
            if self.flash_timer >= self.flash_duration/2:
                self.overlay_transparency += 5
            else:
                self.overlay_transparency -= 5
            if self.flash_timer <= 0:
                self.show_red_flash = False
                self.flash_timer = self.flash_duration
                self.overlay_transparency = 0

    def collision_checks(self):

        # player lasers
        if self.player.sprite.lasers:
            for laser in self.player.sprite.lasers:
                # obstacle collisions
                if pygame.sprite.spritecollide(laser, self.blocks, True):
                    laser.kill()
                    self.explosion_sound.play()
                    self.explosion = Explosion(laser.rect.x, laser.rect.y, 50)
                    self.explosions.add(self.explosion)

                # alien collisions
                all_aliens = self.aliens.sprites() + self.yellow_aliens.sprites()
                aliens_hit = pygame.sprite.spritecollide(laser, all_aliens, False)
                for alien in aliens_hit:
                    if aliens_hit and id(alien) not in laser.hit_alien:
                        alien.health_point -= 1
                        laser.hit_alien.append(id(alien))
                        if alien.color == 'red':
                            alien.image = pygame.image.load('Space-invaders-main/graphics/red_hurt.png')
                        if alien.health_point <= 0:
                            if alien.color == 'green':
                                self.green_alien_death_shoot(alien.rect.center, self.alien_lasers)
                            self.score += alien.value
                            self.energy += 10
                            alien.kill()
                        if self.laser_penetration and laser.penetrate_time < 1:
                            laser.penetrate_time += 1
                        else:
                            laser.kill()
                        self.explosion_sound.play()
                        self.explosion = Explosion(laser.rect.x, laser.rect.y, 100)
                        self.explosions.add(self.explosion)

                # extra collision
                if pygame.sprite.spritecollide(laser, self.extra, True):
                    laser.kill()
                    self.explosion_sound.play()
                    self.score += 500
                    self.energy = self.max_energy
                    self.explosion = Explosion(laser.rect.x, laser.rect.y, 150)
                    self.extra_die.play()
                    self.explosions.add(self.explosion)

        # alien lasers
        if self.alien_lasers:
            for laser in self.alien_lasers:
                # obstacle collisions
                if pygame.sprite.spritecollide(laser, self.blocks, True):
                    laser.kill()
                    self.explosion = Explosion(laser.rect.x, laser.rect.y, 50)
                    self.explosions.add(self.explosion)

                # player collision
                if pygame.sprite.spritecollide(laser, self.player, False):
                    laser.kill()
                    self.lives -= 1
                    self.player_hurt.play()
                    self.show_red_flash = True
                    self.explosion = Explosion(laser.rect.x, laser.rect.y, 100)
                    self.explosions.add(self.explosion)
                    if self.lives <= 0:
                        self.game_active = False

        # aliens
        if self.aliens:
            for alien in self.aliens:
                # obstacle collisions
                pygame.sprite.spritecollide(alien, self.blocks, True)

                # player collision
                if pygame.sprite.spritecollide(alien, self.player, False):
                    self.game_active = False

                if alien.rect.y > screen_height:
                    self.game_active = False

        # missile
        if self.missiles:
            for missiles in self.missiles:
                if pygame.sprite.spritecollide(missiles, self.blocks, False):
                    self.missile_explosion = Explosion(missiles.rect.x, missiles.rect.y, 200)
                    self.explosions.add(self.missile_explosion)
                if pygame.sprite.spritecollide(missiles, self.player, False):
                    self.game_active = False

        # supply
        if self.special_supplies:
            for supply in self.special_supplies:
                if pygame.sprite.spritecollide(supply, self.player, False):
                    if supply.type == 'health':
                        self.lives += 1
                    elif supply.type == 'obstacle':
                        self.create_multiple_obstacles(screen_width/15, screen_height - 120,*self.obstacle_x_positions)
                    elif supply.type == 'attack':
                        self.laser_penetration = True
                        self.penetration_timer = self.penetration_current_time
                    self.score += 250
                    supply.kill()

    def display_lives(self):
        for live in range(self.lives - 1):
            x = self.live_x_start_pos + (live * (self.lives_surf.get_size()[0] + 10))
            screen.blit(self.lives_surf, (x, 8))

    def display_score(self, x_pos = 10, y_pos = -10):
        score_surf = self.font.render(f'score: {self.score}', False, 'white')
        score_rect = score_surf.get_rect(topleft = (x_pos, y_pos))
        screen.blit(score_surf, score_rect)

    def victory_message(self):
        if not self.aliens.sprites() and not self.alien_lasers and not self.yellow_aliens and not self.missiles:
            victory_surf = self.font.render('YOU WON', False, 'white')
            victory_rect = victory_surf.get_rect(center = (screen_width/2, screen_height/2))
            screen.blit(victory_surf, victory_rect)
            self.extra_spawn = False

    def game_over_screen(self, screen_width, screen_height):
        # Text surfaces
        text1 = self.font.render("YOU LOST", True, (255, 0, 0))
        text2 = self.font.render("Press Enter to Restart", True, (255, 255, 255))
        # Center the text
        text1_rect = text1.get_rect(center=(screen_width // 2, screen_height // 2 - 50))
        text2_rect = text2.get_rect(center=(screen_width // 2, screen_height // 2 + 20))
        while self.game_active == False:
            screen.fill((0, 0, 0))  # Clear screen with black
            screen.blit(text1, text1_rect)
            screen.blit(text2, text2_rect)
            self.display_score(screen_width // 2, screen_height // 2 + 150)
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.game_active = True

    def yellow_locking_sound(self):
        any_locking = any(yellow.yellow_behavior() == 'locking' for yellow in self.yellow_aliens)

        if any_locking and not self.locking_sound_playing:
            self.locking_sound.play()
            self.locking_sound_playing = True

        if not any_locking and self.locking_sound_playing:
            self.locking_sound_playing = False
            self.yellow_shoot_sound.play()

    def spawn_supply(self, type):
        special_supply = Special_supply(type, (randint(0, screen_width), 0), screen_height)
        self.special_supplies.add(special_supply)

    def energy_level(self):
        if self.extra_spawn:
            current_time = pygame.time.get_ticks()
            if current_time - self.last_energy_update_time >= 1000:
                self.energy += 5
                self.last_energy_update_time = current_time
            if self.energy > self.max_energy:
                self.energy = 0
                if self.lives < 3:
                    self.spawn_supply(choice(['obstacle', 'health', 'attack']))
                else:
                    self.spawn_supply(choice(['attack', 'obstacle']))

    def display_energy_bar(self):
        bar_width = 200
        bar_height = 20
        bar_x = 250
        bar_y = 20
        pygame.draw.rect(screen, (255, 255, 255), (bar_x, bar_y, bar_width, bar_height), 2)
        fill_width = (self.energy / self.max_energy) * bar_width
        pygame.draw.rect(screen, (0, 255, 0), (bar_x, bar_y, fill_width, bar_height))

    def laser_penetration_timer(self):
        self.penetration_current_time = pygame.time.get_ticks()
        if self.laser_penetration:
            if self.penetration_current_time - self.penetration_timer >= 10000:
                self.laser_penetration = False

    def draw_penetration_indicator(self):
        if self.laser_penetration:
            current_time = pygame.time.get_ticks()
            elapsed_time = (current_time - self.penetration_timer) / 1000
            remaining_time = max(0, 10 - int(elapsed_time))
            screen.blit(self.penetration_icon, (10, 500))
            font = pygame.font.Font('Space-invaders-main/font/Pixeled.ttf', 20)
            timer_text = font.render(str(remaining_time), True, (255, 255, 255))  # White color
            text_rect = timer_text.get_rect(center=(10 + 30, 500 + 30))  # Center text on the icon
            screen.blit(timer_text, text_rect)

    def life_indicator(self):
        life_text = self.font.render(str(self.lives), True, 'white')
        text_rect = life_text.get_rect(center = (40, 400))
        screen.blit(life_text, text_rect)

    def button_draw(self, pos, message, events, size = 'big'):
        if size == 'big':
            image_unpressed = pygame.transform.scale(self.big_button_unpressed, (300, 60))
            image_pressed = pygame.transform.scale(self.big_button_pressed, (300, 60))
            font = pygame.font.Font('Space-invaders-main/font/Pixeled.ttf', 20)
        else:
            image_unpressed = pygame.transform.scale(self.small_button_unpressed, (150, 60))
            image_pressed = pygame.transform.scale(self.small_button_pressed, (150, 60))
            font = pygame.font.Font('Space-invaders-main/font/Pixeled.ttf', 20)
        mouse_pos = pygame.mouse.get_pos()
        rect = image_unpressed.get_rect(center = pos)

        if rect.collidepoint(mouse_pos):
            screen.blit(image_pressed, rect)
        else:
            screen.blit(image_unpressed, rect)

        # show message
        text_surf = font.render(message, False, 'black')
        text_rect = text_surf.get_rect(center=rect.center)
        screen.blit(text_surf, text_rect)

        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if rect.collidepoint(mouse_pos):
                    if message == 'RESTART':
                        self.__init__()
                        self.game_start = True
                        self.game_active = True
                        self.extra_spawn = True
                        self.game_difficulty = difficulty
                        self.alien_init()
                    elif message == f'DIFFICULTIES: {self.game_difficulty}':
                        if self.game_difficulty == 4:
                            self.game_difficulty = 1
                        else: self.game_difficulty += 1
                    elif message == 'QUIT GAME':
                        self.__init__()
                    elif message == 'START':
                        self.game_start = True
                        self.game_active = True
                        self.extra_spawn = True
                        self.alien_init()
                    elif message == 'INSTRUCTIONS':
                        self.instruction = True
                    elif message == 'NEXT':
                        self.instruction_index += 1
                    elif message == 'BACK':
                        self.instruction_index -= 1
                    elif message == 'EXIT':
                        self.instruction = False
                        self.instruction_index = 0

    def game_pause_surface(self):
        overlay = pygame.Surface((screen_width, screen_height))
        overlay.set_alpha(150)
        overlay.fill('black')
        screen.blit(overlay, (0, 0))
        # game pause message
        font = pygame.font.Font('Space-invaders-main/font/Pixeled.ttf', 40)
        text_surf = font.render('GAME PAUSED', False, 'white')
        text_rect = text_surf.get_rect(center=(screen_width/2, 150))
        screen.blit(text_surf, text_rect)

        self.button_draw((screen_width / 2, 300), 'QUIT GAME', events)
        self.button_draw((screen_width/2, 400), 'RESTART', events)
        self.button_draw((screen_width / 2, 500), 'INSTRUCTIONS', events)

    def draw_start_menu(self):
        screen.fill((0, 0, 0))
        background_rect = self.start_menu_background.get_rect(center = (screen_width/2, screen_height/2))
        screen.blit(self.start_menu_background, background_rect)

        # Title
        font = pygame.font.Font('Space-invaders-main/font/Pixeled.ttf', 60)
        title_surf_1 = self.render_glow_text('SPACE', font)
        title_surf_2 = self.render_glow_text('INVADERS', font, 'white', (64, 224, 240))
        title_rect_1 = title_surf_1.get_rect(center=(screen_width / 2, 50))
        title_rect_2 = title_surf_2.get_rect(center=(screen_width / 2, 150))
        screen.blit(title_surf_1, title_rect_1)
        screen.blit(title_surf_2, title_rect_2)

        # Buttons
        self.button_draw((screen_width / 2, 420), "START", events)
        self.button_draw((screen_width / 2, 490), f'DIFFICULTIES: {self.game_difficulty}', events)
        self.button_draw((screen_width / 2, 560), "INSTRUCTIONS", events)

    def render_glow_text(self, text, font, text_color='white', glow_color=(255, 0, 0), glow_radius=10):
        base_text = font.render(text, True, text_color)
        size = base_text.get_width() + glow_radius * 2, base_text.get_height() + glow_radius * 2
        surface = pygame.Surface(size, pygame.SRCALPHA)
        for i in range(glow_radius, 0, -1):
            alpha = int(255 * (i / glow_radius) * 0.2)
            glow = font.render(text, True, glow_color)
            glow.set_alpha(alpha)
            offset = glow_radius - i
            surface.blit(glow, (offset, offset))
            surface.blit(glow, (offset + 2, offset))
            surface.blit(glow, (offset, offset + 2))
            surface.blit(glow, (offset + 2, offset + 2))
        surface.blit(base_text, (glow_radius, glow_radius))
        return surface

    def show_instructions(self):
        if self.instruction:
            screen.fill((30, 30, 30))
            frame_image = pygame.image.load('Space-invaders-main/graphics/frame.png').convert_alpha()
            frame_image = pygame.transform.scale(frame_image, (600, 550))
            frame_rect = frame_image.get_rect(center=(screen_width / 2, 300))
            screen.blit(frame_image, frame_rect)

            font = pygame.font.Font('Space-invaders-main/font/Pixeled.ttf', 10)
            current_slide = instructions.instruction[self.instruction_index]
            for i, line in enumerate(current_slide):
                text_surf = font.render(line, True, 'white')
                text_rect = text_surf.get_rect(center=(screen_width / 2, 150 + i * 40))  # Adjust vertical spacing
                screen.blit(text_surf, text_rect)

            if self.instruction_index == 1 or self.instruction_index == 2: screen.blit(self.player_image, self.player_rect)
            elif self.instruction_index == 3:
                screen.blit(self.red_alien, self.red_alien_rect)
                screen.blit(self.red_alien_hurt, self.red_alien_hurt_rect)
            elif self.instruction_index == 4: screen.blit(self.green_alien, self.green_alien_rect)
            elif self.instruction_index == 5: screen.blit(self.yellow_alien, self.yellow_alien_rect)
            elif self.instruction_index == 6: screen.blit(self.extra_alien, self.extra_alien_rect)
            elif self.instruction_index == 8:
                screen.blit(self.attack_supply, self.attack_supply_rect)
                screen.blit(self.health_supply, self.health_supply_rect)
                screen.blit(self.obstacle_supply, self.obstacle_supply_rect)

            if self.instruction_index > 0:
                self.button_draw((150, 620), 'BACK', events, 'small')
            if self.instruction_index < 8:
                self.button_draw((450, 620), 'NEXT', events, 'small')
            else:
                self.button_draw((450, 620), 'EXIT', events, 'small')

    def run(self):
        if self.game_active:
            if not self.game_pause:
                self.player.update()
                self.alien_lasers.update()
                self.extra.update()
                self.explosions.update()
                self.fire_sparks.update()
                self.special_supplies.update()
                self.missiles.update(self.blocks)

                self.aliens.update(self.alien_direction, self.pause_time)
                self.yellow_aliens.update(self.alien_direction, self.pause_time)
                self.alien_position_checker()
                self.extra_alien_timer()
                self.collision_checks()
                self.player_got_hit()

                # other functions
                self.yellow_locking_sound()
                self.energy_level()
                self.laser_penetration_timer()
                self.draw_penetration_indicator()

            # draw sprites on screen
            self.player.sprite.lasers.draw(screen)
            self.player.draw(screen)
            self.blocks.draw(screen)
            self.aliens.draw(screen)
            self.alien_lasers.draw(screen)
            self.yellow_aliens.draw(screen)
            self.extra.draw(screen)
            self.explosions.draw(screen)
            self.fire_sparks.draw(screen)
            self.missiles.draw(screen)
            self.special_supplies.draw(screen)
            self.display_energy_bar()
            self.display_lives()
            self.display_score()
            self.victory_message()
            # self.life_indicator()

            if self.game_pause: self.game_pause_surface()
        else:
            if self.game_start == False:
                self.draw_start_menu()
            else:
                self.game_over_screen(screen_width, screen_height)
                self.__init__()
                self.game_start = True
                self.game_active = True
                self.extra_spawn = True
                self.game_difficulty = difficulty
                self.alien_init()
        self.show_instructions()

# other functions
def set_timers():
    if game.game_difficulty == 1:
        pygame.time.set_timer(ALIENLASER, 1000)
    elif game.game_difficulty == 2 or game.game_difficulty == 3:
        pygame.time.set_timer(ALIENLASER, 800)
    else:
        pygame.time.set_timer(ALIENLASER, 600)

    if game.game_difficulty == 4:
        pygame.time.set_timer(SPECIALMISSILE, randint(1000, 1500))
    else:
        pygame.time.set_timer(SPECIALMISSILE, randint(1500, 2000))

if __name__ == '__main__':
    pygame.init()
    screen_width = 600
    screen_height = 700
    screen = pygame.display.set_mode((screen_width, screen_height), pygame.HWSURFACE|pygame.DOUBLEBUF|pygame.SCALED|pygame.RESIZABLE)
    clock = pygame.time.Clock()
    game = Game()

    # music
    music = pygame.mixer.Sound('Space-invaders-main/audio/music.wav')
    music.set_volume(0.2)
    music.play(loops=-1)

    ALIENLASER = pygame.USEREVENT + 1
    SPECIALMISSILE = pygame.USEREVENT + 2

    # main game loop
    while True:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == ALIENLASER and not game.game_pause:
                game.alien_shoot()
            if event.type == SPECIALMISSILE and not game.game_pause:
                game.extra_missile_shoot()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                game.game_pause = not game.game_pause
                if game.game_pause:
                    start_pause = pygame.time.get_ticks()
                else:
                    end_pause = pygame.time.get_ticks()
                    game.pause_time += end_pause - start_pause

        # difficulty changes
        if not game.game_start:
            set_timers()
            difficulty = game.game_difficulty

        screen.fill((30, 30, 30))
        game.run()
        pygame.display.flip()
        clock.tick(60)