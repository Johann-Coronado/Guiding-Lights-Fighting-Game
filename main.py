import pygame, sys
import os
import random

pygame.init()
pygame.mixer.pre_init(44100, 16, 2, 4096)

# temporary global variables

# game setup toggles
scroll = 0
p1_chosen = False
p2_chosen = False
battle_not_started = True
trigger_players_spawn = False
options_start = False

# battle options toggles
main_menu_toggled = True
attacks_menu_toggled = False
spells_menu_toggled = False
roleplay_menu_toggled = False
movement_menu_toggled = False
inventory_menu_toggled = False
charsheet_menu_toggled = False
turnactions_menu_toggled = False
sub_menu_active = False


# handle game stages
class GameState:
    """Toggles and manages gamestate"""


    def __init__(self) -> None:
        self.state = "char_select"

        self.attack_options_manager = None

    def char_select(self):
        global p1_chosen, p2_chosen, scroll
        mouse_pos = pygame.mouse.get_pos()
        # define local functions
        def select_clear():
            global p1_chosen, p2_chosen
            for member in token_list:
                member.chosen_first = False
                member.chosen_second = False
            p1_chosen = False
            p2_chosen = False


        background_manager.scroll(WIN, mountain_list, 0.4)
        if p1_chosen and p2_chosen:
            fight_button.draw(WIN)
            fight_button.check_mouse(WIN, mouse_pos)

        for member in token_list:
            member.draw(WIN)
            member.check_mouse(WIN, mouse_pos)
            if p1_chosen and member.chosen_first:
                member.chosen_p1(WIN)
            if p2_chosen and member.chosen_second:
                member.chosen_p2(WIN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONUP:
                for member in token_list:
                    num_of_chosen = [False]
                    num_of_chosen.append(p1_chosen)
                    num_of_chosen.append(p2_chosen)
                    if member.check_mouse(WIN, mouse_pos):
                        print(f"{member.name} Selected")
                        sound_channel_2.play(button_click_sfx, maxtime=600)
                        if not member.chosen_first and sum(num_of_chosen) == 0:
                            p1_chosen = member.chosen_p1(WIN)
                        elif not member.chosen_second and sum(num_of_chosen) == 1:
                            p2_chosen = member.chosen_p2(WIN)
                
                if p1_chosen and p2_chosen:
                    fight_button.draw(WIN)
                    if fight_button.check_mouse(WIN, mouse_pos):
                        sound_channel_2.play(button_click_sfx, maxtime=600)
                        self.state = "transition"
                        self.state_manager()

            if event.type == pygame.MOUSEMOTION:
                mouse_position = event.pos
                for member in token_list:
                    member.handleMouseOver(mouse_position)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    select_clear()
            
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 3:
                    select_clear()

        WIN.blit(game_cursor, mouse_pos)

            
        

    def transition(self):
            
        background_manager.fade_out(WIN, 3, "origbig", WIDTH, HEIGHT)
        sound_channel_0.stop()
        sound_channel_0.play(battle_theme_1, -1)
        sound_channel_0.set_volume(0.3)
        sound_channel_1.play(train_whistle, 1)
        sound_channel_1.set_volume(0.2)

        # generate guiding lights members to fight
        def generate_player_1():
            for member in token_list:
                if member.chosen_first == True:
                    return member.name
        
        def generate_player_2():
            for member in token_list:
                if member.chosen_second == True:
                    return member.name

        player_1 = generate_player_1()
        player_2 = generate_player_2()

        # player generation dictionary
        p_dict = {CHAR_NAMES_LIST[0]: lyre_sprite, CHAR_NAMES_LIST[1]: marcee_sprite, CHAR_NAMES_LIST[2]: maurlo_sprite, CHAR_NAMES_LIST[3]: nailea_sprite,
                  CHAR_NAMES_LIST[4]: pynncone_sprite, CHAR_NAMES_LIST[5]: varick_sprite, CHAR_NAMES_LIST[6]: yayan_sprite}

        for name in CHAR_NAMES_LIST:
            if player_1 == name:
                guiding_lights_group.add(GuidingLight(name, p_dict[name], 1))
                self.attack_options_manager = AttackOptionsManager(player_1, ATTACKS_DATA[CHAR_NAMES_LIST.index(name)])
                self.spell_options_manager = SpellOptionsManager(player_1, SPELLS_DATA[CHAR_NAMES_LIST.index(name)])
                self.roleplay_options_manager = RoleplayOptionsManager(player_1, ROLEPLAY_DATA[CHAR_NAMES_LIST.index(name)])
                self.movement_options_manager = MovementOptionsManager()
                self.inventory_options_manager = InventoryOptionsManager(START_ITEMS[f"{player_1}_items"])
                self.charsheet_manager = CharsheetManager(CHARSHEET_DATA[f"{player_1}_sheet"])
            if player_2 == name:
                guiding_lights_group.add(GuidingLight(name, pygame.transform.flip(p_dict[name], True, False), 2))

        background_manager.fade_in(WIN, 5, "origbig", WIDTH, HEIGHT)
        sound_channel_2.play(train_sounds, -1,fade_ms = 3000)
        sound_channel_2.set_volume(0.01)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        print(self.state)

        self.state = "combat"
        self.state_manager()

    def combat(self):
        global main_menu_toggled, attacks_menu_toggled, spells_menu_toggled, roleplay_menu_toggled, movement_menu_toggled
        global inventory_menu_toggled, charsheet_menu_toggled, turnactions_menu_toggled

        def clear_options():
            global main_menu_toggled, attacks_menu_toggled, spells_menu_toggled, roleplay_menu_toggled, movement_menu_toggled
            global inventory_menu_toggled, charsheet_menu_toggled, turnactions_menu_toggled
            main_menu_toggled = True
            attacks_menu_toggled = False
            spells_menu_toggled = False
            roleplay_menu_toggled = False
            movement_menu_toggled = False
            inventory_menu_toggled = False
            charsheet_menu_toggled = False
            turnactions_menu_toggled = False
            buttons_group.update(mouse_pos, main_menu_toggled)
            attack_options_group.update(mouse_pos, attacks_menu_toggled)
            spell_options_group.update(mouse_pos, spells_menu_toggled)
            roleplay_options_group.update(mouse_pos, spells_menu_toggled)
            movement_options_group.update(mouse_pos, spells_menu_toggled)
            inventory_options_group.update(mouse_pos, inventory_menu_toggled)
            charsheet_info_group.update()

        # set scene
        mouse_pos = pygame.mouse.get_pos()
        background_manager.scroll(WIN, plains_list, 2)
        train_and_tracks.set_train()
        train_and_tracks.set_tracks()
        guiding_lights_group.draw(WIN)
        guiding_lights_group.update()

        # GUI toggles
        if options_start:
            healthbars_group.draw(WIN)
            healthbars_group.update()
            magicbars_group.draw(WIN)
            magicbars_group.update()
            if main_menu_toggled:
                buttons_group.draw(WIN)
                buttons_group.update(mouse_pos, main_menu_toggled)

        if attacks_menu_toggled:
            attacks_menu_group.draw(WIN)
            attacks_menu_group.update(mouse_pos, attacks_menu_toggled)
            attack_options_group.draw(WIN)
            attack_options_group.update(mouse_pos, attacks_menu_toggled)
            attack_options_descriptions_group.draw(WIN)
            attack_options_descriptions_group.update(mouse_pos, attacks_menu_toggled)

        if spells_menu_toggled:
            spells_menu_group.draw(WIN)
            spells_menu_group.update(mouse_pos)
            spell_options_group.draw(WIN)
            spell_options_group.update(mouse_pos, spells_menu_toggled)
            spell_options_descriptions_group.draw(WIN)
            spell_options_descriptions_group.update(mouse_pos, spells_menu_toggled)

        if roleplay_menu_toggled:
            roleplay_menu_group.draw(WIN)
            roleplay_menu_group.update(mouse_pos)
            roleplay_options_group.draw(WIN)
            roleplay_options_group.update(mouse_pos, roleplay_menu_toggled)
            roleplay_options_descriptions_group.draw(WIN)
            roleplay_options_descriptions_group.update(mouse_pos, roleplay_menu_toggled)

        if movement_menu_toggled:
            movement_menu_group.draw(WIN)
            movement_menu_group.update(mouse_pos)
            movement_options_group.draw(WIN)
            movement_options_group.update(mouse_pos, movement_menu_toggled)

            for zone in movement_options_group.sprites():
                if zone.is_toggled:
                    WIN.blit(zone_icons_dict[zone.name], (WIDTH/2 - 125, HEIGHT/2 - 150))

        if inventory_menu_toggled:
            inventory_menu_group.draw(WIN)
            inventory_menu_group.update(mouse_pos)
            inventory_options_group.draw(WIN)
            inventory_options_group.update(mouse_pos, inventory_menu_toggled)
            inventory_options_descriptions_group.draw(WIN)
            inventory_options_descriptions_group.update(mouse_pos, inventory_menu_toggled)

        if charsheet_menu_toggled:
            charsheet_menu_group.draw(WIN)
            charsheet_menu_group.update(mouse_pos)
            charsheet_info_group.draw(WIN)
            charsheet_info_group.update()

        # if turnactions_menu_toggled:
        #     turnactions_menu_group.draw(WIN)
        #     turnactions_menu_group.update(mouse_pos)


        # event loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    for button in buttons_group:
                        if button.name == "attacks_button" and button.is_hovered:
                            main_menu_toggled = False
                            attacks_menu_toggled = True
                            print("attacks selected")
                            buttons_group.update(mouse_pos, main_menu_toggled)

                        if button.name == "spells_button" and button.is_hovered:
                            main_menu_toggled = False
                            spells_menu_toggled = True
                            print("spells selected")
                            buttons_group.update(mouse_pos, main_menu_toggled)

                        if button.name == "roleplay_button" and button.is_hovered:
                            main_menu_toggled = False
                            roleplay_menu_toggled = True
                            print("roleplay selected")
                            buttons_group.update(mouse_pos, main_menu_toggled)

                        if button.name == "move_button" and button.is_hovered:
                            movement_menu_toggled = True
                            main_menu_toggled = False
                            print("movement selected")
                            buttons_group.update(mouse_pos, main_menu_toggled)

                        if button.name == "inventory_button" and button.is_hovered:
                            inventory_menu_toggled = True
                            main_menu_toggled = False
                            print("inventory selected")
                            buttons_group.update(mouse_pos, main_menu_toggled)

                        if button.name == "charsheet_button" and button.is_hovered:
                            charsheet_menu_toggled = True
                            main_menu_toggled = False
                            print("character sheet selected")
                            buttons_group.update(mouse_pos, main_menu_toggled)


                    if attacks_menu_toggled:
                        attacks_list = attack_options_group.sprites()
                        for attack in attacks_list:
                            print(f"attack is hovered is {attack.is_hovered}")
                            if attack.is_hovered and attack.is_toggled == False:
                                attack.is_toggled = True
                                attack_options_group.draw(WIN)
                                attack_options_group.update(mouse_pos, attacks_menu_toggled)
                            elif attack.second_is_hovered and attack.is_toggled == True:
                                attack.is_toggled = False
                                attack_options_group.draw(WIN)
                                attack_options_group.update(mouse_pos, attacks_menu_toggled)
                    
                    if spells_menu_toggled:
                        spells_list = spell_options_group.sprites()
                        for spell in spells_list:
                            print(f"spell is hovered is {spell.is_hovered}")
                            if spell.is_hovered and spell.is_toggled == False:
                                spell.is_toggled = True
                                spell_options_group.draw(WIN)
                                spell_options_group.update(mouse_pos, spells_menu_toggled)
                            elif spell.second_is_hovered and spell.is_toggled == True:
                                spell.is_toggled = False
                                spell_options_group.draw(WIN)
                                spell_options_group.update(mouse_pos, spells_menu_toggled)
                    
                    if roleplay_menu_toggled:
                        roleplay_list = roleplay_options_group.sprites()
                        for rp in roleplay_list:
                            print(f"roleplay is hovered is {rp.is_hovered}")
                            if rp.is_hovered and rp.is_toggled == False:
                                rp.is_toggled = True
                                roleplay_options_group.draw(WIN)
                                roleplay_options_group.update(mouse_pos, roleplay_menu_toggled)
                            elif rp.second_is_hovered and rp.is_toggled == True:
                                rp.is_toggled = False
                                roleplay_options_group.draw(WIN)
                                roleplay_options_group.update(mouse_pos, roleplay_menu_toggled)

                    if movement_menu_toggled:
                        movement_list = movement_options_group.sprites()
                        for zone in movement_list:
                            print(f"movement is hovered is {zone.is_hovered}")
                            if zone.is_hovered and zone.is_toggled == False:
                                zone.is_toggled = True
                                zone_index = movement_list.index(zone)
                                movement_list[zone_index - 1].is_toggled = False
                                movement_list[zone_index - 2].is_toggled = False
                                movement_options_group.draw(WIN)
                                movement_options_group.update(mouse_pos, movement_menu_toggled)
                    
                    if inventory_menu_toggled:
                        inventory_list = inventory_options_group.sprites()
                        for slot in inventory_list:
                            if slot.is_hovered and slot.is_toggled == False:
                                slot.is_toggled = True
                                inventory_options_group.draw(WIN)
                                inventory_options_group.update(mouse_pos, inventory_menu_toggled)
                            elif slot.second_is_hovered and slot.is_toggled == True:
                                slot.is_toggled = False
                                inventory_options_group.draw(WIN)
                                inventory_options_group.update(mouse_pos, inventory_menu_toggled)
                            
                        
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    clear_options()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 3:
                    clear_options()
        
        WIN.blit(game_cursor, mouse_pos)

     
    def state_manager(self):
        if self.state == "char_select":
            self.char_select()
        if self.state == "combat":
            self.combat()
        if self.state == "transition":
            self.transition()



class Train():
    def __init__(self,screen, train, tracks) -> None:
        self.train = train
        self.tracks1 = tracks
        self.tracks2 = tracks
        self.screen = screen

        self.train_start_flag = -6000
        self.train_end_flag = -475

        self.track_size = tracks.get_size()
        self.w = self.track_size[0]
        self.abs_difference = self.w - WIDTH

        self.speed = 30
        self.track_start_flag_x = 500
        self.track_end_flag_x = -self.abs_difference
        self.track_start_flag_y = 290
        self.track_end_flag_y = 270

        self.track1_x = 0
        self.track2_x = 0
        self.track_loop_on = False


    def set_train(self):
        global battle_not_started, roll_init_logo, trigger_players_spawn
        if self.train_start_flag < self.train_end_flag:
            self.screen.blit(self.train, (self.train_start_flag,430))
            self.train_start_flag += 30
        else:
            self.screen.blit(self.train, (self.train_end_flag,430))
            stage_graphics.draw(WIN)
            stage_graphics.update()
        
        if self.train_start_flag > -1500:
            trigger_players_spawn = True
            

    def set_tracks(self):
        global track_loop_on
        if self.track_start_flag_y > self.track_end_flag_y and self.track_start_flag_x > self.track_end_flag_x:
            self.screen.blit(self.tracks1, (self.track_start_flag_x,self.track_start_flag_y))
            self.track_start_flag_x -= self.speed
            self.track_start_flag_y -= 0.1
            self.track1_x = self.track_start_flag_x
        elif self.track_start_flag_x > self.track_end_flag_x:
            if self.track_loop_on:
                if self.track2_x <= -self.w + WIDTH and self.track2_x >= -self.w and self.track2_x != 0:
                    self.screen.blit(self.tracks2,(self.track2_x + WIDTH, self.track_end_flag_y))
                    self.track2_x -=self.speed
                else: 
                    self.track2_x = 0
            self.screen.blit(self.tracks1, (self.track_start_flag_x,self.track_end_flag_y))
            self.track_start_flag_x -= self.speed
            self.track1_x = self.track_start_flag_x
        else:
            self.screen.blit(self.tracks1, (self.track_start_flag_x,self.track_end_flag_y))
            self.track_start_flag_x -= self.speed
            self.track1_x = self.track_start_flag_x
            if self.track1_x <= -self.w + WIDTH and self.track2_x >= -self.w + WIDTH:
                self.screen.blit(self.tracks2,(self.track2_x + WIDTH, self.track_end_flag_y))
                self.track2_x  -= self.speed
            else:
                self.track1_x = WIDTH
                self.track_start_flag_x = WIDTH
                self.track_loop_on = True
       

class CharacterTokens:

    def __init__(self, name, token_image, position, info_dict):
        self.name = name
        self.token = pygame.transform.scale(token_image, (125, 125))
        self.token_highlighted = pygame.transform.scale(token_image, (150, 150))
        self.x = position[0]
        self.y = position[1]
        self.rect = self.token.get_rect(center=(self.x + 62.5, self.y + 62.5))

        self.picture = info_dict[f"{name}_image"]
        self.summary = info_dict[f"{name}_summary"]
        self.ability_1_icon = info_dict[f"{name}_abilities"][("ability1","icon")]
        self.ability_1_name = info_dict[f"{name}_abilities"][("ability1","name")]
        self.ability_1_description = info_dict[f"{name}_abilities"][("ability1","description")]
        self.ability_2_icon = info_dict[f"{name}_abilities"][("ability2","icon")]
        self.ability_2_name = info_dict[f"{name}_abilities"][("ability2","name")]
        self.ability_2_description = info_dict[f"{name}_abilities"][("ability2","description")]
        self.ability_3_icon = info_dict[f"{name}_abilities"][("ability3","icon")]
        self.ability_3_name = info_dict[f"{name}_abilities"][("ability3","name")]
        self.ability_3_description = info_dict[f"{name}_abilities"][("ability3","description")]

        self.player_1 = pygame.transform.scale(pygame.image.load(r"./Assets/Tokens/player_1_token.png").convert_alpha(), (50, 50))
        self.player_2 = pygame.transform.scale(pygame.image.load(r"./Assets/Tokens/player_2_token.png").convert_alpha(), (50, 50))
        
        self.chosen_first = False
        self.chosen_second = False
        self.hovered = False

    def draw(self,screen):
        screen.blit(self.token,(self.x , self.y))
    
    def chosen_p1(self, screen):
        screen.blit(self.player_1, (self.x+75, self.y+75))
        self.chosen_first = True
        return True

    def chosen_p2(self,screen):
        screen.blit(self.player_2, (self.x+75, self.y+75))
        self.chosen_second = True
        return True

    def check_mouse(self, screen, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            screen.blit(self.token_highlighted,(self.x-12.5 , self.y-12.5))
            self.summon_info_scroll(screen)

            self.hovered = True
            return True
        else:
            screen.blit(self.token,(self.x , self.y))
            self.hovered = False
            return False
        
    def handleMouseOver( self, mouse_position ):
        """ If the given co-ordinate inside our rect,
            Do all the mouse-hovering work"""
        if ( self.mouseIsOver( mouse_position ) ):
            if ( self.hovered == False ):
                self.hovered = True   
                sound_channel_1.play(button_hover_sfx, maxtime=600)

        else:
            if ( self.hovered == True ):
                self.hovered = False
    
    def mouseIsOver( self, mouse_position ):
        """ Is the given co-ordinate inside our rect """
        return self.rect.collidepoint( mouse_position )
    
    def summon_info_scroll(self, screen):
        info_book = pygame.image.load(r"./Assets/pixel_scroll.png").convert_alpha()
        info_book = pygame.transform.scale(info_book, (900,525))
        screen.blit(info_book, (190, 0))

        char_image_positions_dict = {CHAR_NAMES_LIST[0]:(320, 100), CHAR_NAMES_LIST[1]:(340,100), CHAR_NAMES_LIST[2]:(320,250), CHAR_NAMES_LIST[3]:(340,83),
                                     CHAR_NAMES_LIST[4]:(305,125), CHAR_NAMES_LIST[5]:(342,90), CHAR_NAMES_LIST[6]:(342,110),}
        
        self.format_scroll(screen, char_image_positions_dict[self.name][0], char_image_positions_dict[self.name][1])
    
    def display_multi_line(self, screen, x, y, font, color, text_list):
        for text in text_list:
            screen.blit(font.render(text, True, color), (x, y))
            y += 12
    
    def format_scroll(self,screen, picture_x, picture_y):
        #title and description
        screen.blit(self.picture,(picture_x, picture_y))
        screen.blit(heading1.render(self.name, True, "black"), (520, 100))
        self.display_multi_line(screen, 520, 140, description, "black", self.summary)

        #abilities
        h2_x = 195
        screen.blit(heading2.render("Abilities:", True, "black"), (520, h2_x))

        screen.blit(self.ability_1_icon, (520, h2_x+30))
        screen.blit(heading2.render(self.ability_1_name, True, "black"), (560, h2_x+37))
        screen.blit(description.render(self.ability_1_description, True, "black"), (520, h2_x+70))

        screen.blit(self.ability_2_icon, (520,h2_x+90))
        screen.blit(heading2.render(self.ability_2_name, True, "black"), (560, h2_x+97))
        screen.blit(description.render(self.ability_2_description, True, "black"), (520, h2_x+130))

        screen.blit(self.ability_3_icon, (520,h2_x+150))
        screen.blit(heading2.render(self.ability_3_name, True, "black"), (560, h2_x+157))
        screen.blit(description.render(self.ability_3_description, True, "black"), (520, h2_x+190))


class BackgroundManager:

    def __init__(self) -> None:
        pass

    def init_background(self, folder_number, bg_name, frames):
        bg_list = []

        for i in range(1, frames+1):
            bg_image = pygame.image.load(fr"./Assets/Nature Landscapes Free Pixel Art/nature_{str(folder_number)}/{bg_name}_{i}.png").convert_alpha()
            bg_image = pygame.transform.scale(bg_image, (WIDTH, HEIGHT))
            bg_list.append(bg_image)

        return bg_list

    def scroll(self, screen, list_name, scroll_speed):
        global scroll
        scroll += scroll_speed
        for x in range(100):
            speed = 1
            for i in list_name:
                screen.blit(i, ((x * WIDTH) - scroll * speed, 0))
                speed += 0.4

    def fade_out(self, screen, folder_number, bg_name, width, height): 
        fade = pygame.Surface((width, height))
        bg = pygame.image.load(fr"./Assets/Nature Landscapes Free Pixel Art/nature_{str(folder_number)}/{bg_name}.png").convert_alpha()
        bg = pygame.transform.scale(bg, (WIDTH,HEIGHT))
        for alpha in range(0, 300):
            fade.set_alpha(alpha)
            screen.blit(bg, (0,0))
            screen.blit(fade, (0,0))
            pygame.display.update()
            pygame.time.delay(5)
    
    def fade_in(self, screen, folder_number, bg_name, width, height): 
        fade = pygame.Surface((width, height))
        bg = pygame.image.load(fr"./Assets/Nature Landscapes Free Pixel Art/nature_{str(folder_number)}/{bg_name}.png").convert_alpha()
        bg = pygame.transform.scale(bg, (WIDTH,HEIGHT))
        for alpha in range(300, 0, -1):
            fade.set_alpha(alpha)
            screen.blit(bg, (0,0))
            screen.blit(fade, (0,0))
            pygame.display.update()
            pygame.time.delay(5)
        

class StageGraphics(pygame.sprite.Sprite):
    def __init__(self, loaded_images, sound_effect):
        super().__init__()
        self.loaded_images = loaded_images
        # check if list or single image and get image
        if isinstance(self.loaded_images, list):
            self.image = self.loaded_images[0]
        else:
            self.image = self.loaded_images

        # get rect
        self.size = self.image.get_size()
        self.rect = self.image.get_rect()

        # set position
        self.rect.center = (WIDTH/2, (HEIGHT/2)-100)

        self.sfx = pygame.mixer.Sound(sound_effect)
        self.frame_index = 0
        self.animation_speed = 0.55
        self.sfx_played = False
        self.end = False
        self.timer_over = 150

    def play_animation(self):
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.loaded_images):
            self.frame_index = 0
            self.end = True
        self.image = self.loaded_images[int(self.frame_index)]

    def play_sfx(self):
        if self.sfx_played == False:
            self.find_inactive_sfx_channel().play(self.sfx)
            self.sfx_played = True

    
    def find_inactive_sfx_channel(self):
        for channel in sound_channels:
            if channel.get_busy() == False:
                print(channel)
                return channel

    def update(self):
        global options_start
        self.play_sfx()
        if isinstance(self.loaded_images, list) and not self.end:
            self.play_animation()
        elif self.end:
            options_start = True
            self.kill()
        elif self.timer_over != 0:
            self.timer_over -= 1
        elif self.timer_over == 0:
            # options_start = True
            self.kill()
        else:
            pass


class GuidingLight(pygame.sprite.Sprite):
    def __init__(self, name, loaded_default_sprite, player_number):
        super().__init__()

        # get image
        self.loaded_default_sprite = loaded_default_sprite
        self.image = loaded_default_sprite

        # get rect
        self.size = self.image.get_size()
        self.rect = self.image.get_rect()

        # init attributes
        self.name = name
        self.player_number = player_number
        self.health = 100
        # zone positions: 1 = melee, 2 = thrown, 3 = snipe
        self.zone_position = 2


        # starting positions
        if self.player_number == 1:
            self.x_start = -701

        if self.player_number == 2:
            self.x_start = -50
        
        set_y_start_dict = {CHAR_NAMES_LIST[0]:380, CHAR_NAMES_LIST[1]:380, CHAR_NAMES_LIST[2]:422, CHAR_NAMES_LIST[3]:360,
                                     CHAR_NAMES_LIST[4]:390, CHAR_NAMES_LIST[5]:380, CHAR_NAMES_LIST[6]:380,}
        
        self.y_start = set_y_start_dict[self.name]
        self.rect.center = (self.x_start, self.y_start)

    def intro_load(self):
        if trigger_players_spawn:
            # 315
            player_1_startx = 301
            player_2_startx = 980
            if self.x_start < player_1_startx and self.player_number == 1:
                self.rect.center = (self.x_start, self.y_start)
                self.x_start += 30
            if self.x_start >= player_1_startx and self.player_number == 1: 
                self.x_start = player_1_startx
                self.rect.center = (self.x_start, self.y_start)

            if self.x_start < player_2_startx and self.player_number == 2: 
                self.rect.center = (self.x_start, self.y_start)
                self.x_start += 30
            if self.x_start >= player_2_startx and self.player_number == 2: 
                self.x_start = player_2_startx
                self.rect.center = (self.x_start, self.y_start)

    def update(self):
        self.intro_load()
            

class HealthBar(pygame.sprite.Sprite):
    def __init__(self, image_box, image_health, hp, position):
        super().__init__()
        # get image
        self.image = pygame.transform.scale(image_box, (400,50))
        self.health_bars = pygame.transform.scale(image_health, (58,17))
        # get rect
        self.rect = self.image.get_rect()
        
        # set position
        self.rect.topleft = position

        self.hp = hp

    def starting_health(self):
        for i in range (1,9):
            self.image.blit(self.health_bars, (38*i,17))

    def update(self):
        self.starting_health()

class MagicBar(pygame.sprite.Sprite):
    def __init__(self, image_box, image_magic, mp, position):
        super().__init__()
        # get image
        self.image = pygame.transform.scale(image_box, (400,50))
        self.magic_bars = pygame.transform.scale(image_magic, (58,17))
        # get rect
        self.rect = self.image.get_rect()
        
        # set position
        self.rect.topleft = position

        self.mp = mp

    def starting_magic(self):
        for i in range (1,9):
            self.image.blit(self.magic_bars, (38*i,17))

    def update(self):
        self.starting_magic()

# UI CLASSES
# general button class
class Button(pygame.sprite.Sprite):

    def __init__(self, name, image, scale, add_dimensions, pos, text_input, font, base_color, hovering_color):
        super().__init__()
        # define images
        #resize button bg
        temp_size = image.get_size()
        self.normal_image = pygame.transform.scale(image, (temp_size[0] * scale, temp_size[1] * scale))
        temp_size = self.normal_image.get_size()
        if add_dimensions:
            self.normal_image = pygame.transform.scale(self.normal_image, (temp_size[0] + add_dimensions[0], temp_size[1] + add_dimensions[1]))
        self.size = self.normal_image.get_size()
        self.image = self.normal_image
        self.hovered_image = pygame.transform.scale(self.normal_image, (self.size[0]+20, self.size[1]+20))
        #define rectangles
        self.rect = self.image.get_rect()
        #define position
        self.x_pos = pos[0]
        self.y_pos = pos[1]

        self.rect.center = pos
        #define font type
        self.font = font
        self.base_color, self.hovering_color = base_color, hovering_color
        self.text_input = text_input
        self.text = self.font.render(self.text_input, True, self.base_color)

        self.name = name
        self.is_hovered = False

    def check_hover(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            return True
        return False

    def hover_animation(self, position):
        if self.check_hover(position):
            self.text = self.font.render(self.text_input, True, self.hovering_color)
            self.image.blit(self.text, (20, 20))
            self.image = self.hovered_image
            self.is_hovered = True
    
        else:
            self.text = self.font.render(self.text_input, True, self.base_color)
            self.image.blit(self.text, (20, 20))
            self.image = self.normal_image
            self.is_hovered = False
    
    def update(self, mouse_position, visibility = True):
        if visibility:
            self.hover_animation(mouse_position)
            self.rect.center = (self.x_pos, self.y_pos)
        else:
            self.rect.center = (self.x_pos, -200)

class FightButton():
    def __init__(self, image, position):
        self.image = pygame.transform.scale(image, (440, 168))
        self.image_highlighted = pygame.transform.scale(image, (465, 193))
        self.x = position[0]
        self.y = position [1]
        self.rect = self.image.get_rect(center=(self.x + 220, self.y + 84))

    def draw(self, screen):
        screen.blit(self.image,(self.x , self.y))

    def check_mouse(self, screen, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            screen.blit(self.image_highlighted,(self.x-12.5 , self.y-12.5))
            return True

# parent class of menus UI
class Menus(pygame.sprite.Sprite):

    def __init__(self, menu_image, dimensions, **kwargs):
        super().__init__()
        # get image
        self.image = pygame.transform.scale(menu_image, dimensions)

        # get rect
        self.position = (WIDTH/2, HEIGHT/2)
        self.rect = self.image.get_rect()
        self.rect.center = self.position

        self.is_hovered = False

    def check_hover(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            self.is_hovered = True
            return True
        else:
            self.is_hovered = False
            return False

    def update(self, mouse_pos, visibility = True):
        if visibility:
            self.check_hover(mouse_pos)
            self.position = (WIDTH/2, HEIGHT/2)
        else:
            self.position = (WIDTH/2, 1000)


# parent class of toggle buttons, referred to as options  

class DragButtons(pygame.sprite.Sprite):
    def __init__(self, image):
        super().__init__()
        pass

class DragSlots():
    def __init__(self):
        pass


class ToggleButtons(pygame.sprite.Sprite):
    def __init__(self, name, image, toggled_image, scale, add_dimensions, pos, text_input, font, base_color, hovering_color, toggled_color, **kwargs):
        super().__init__()
        self.name = name
        # define images
        #resize button bg
        temp_size = image.get_size()
        self.normal_image = pygame.transform.scale(image, (temp_size[0] * scale, temp_size[1] * scale))
        temp_size = self.normal_image.get_size()
        if add_dimensions:
            self.normal_image = pygame.transform.scale(self.normal_image, (temp_size[0] + add_dimensions[0], temp_size[1] + add_dimensions[1]))
        self.size = self.normal_image.get_size()
        self.image = self.normal_image
        self.hovered_image = pygame.transform.scale(self.normal_image, (self.size[0]+10, self.size[1]+10))
        self.toggled_image = pygame.transform.scale(toggled_image, (temp_size[0] + add_dimensions[0], temp_size[1] + add_dimensions[1]))
        self.toggled_color = toggled_color

        #define rectangles
        self.rect = self.image.get_rect()

        #define position
        self.original_pos = pos
        self.hovered_pos = (pos[0]-5, pos[1]-5)
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.rect.center = pos
        self.rect_range = (self.rect.left, self.rect.top, self.rect.right - self.rect.left, self.rect.bottom - self.rect.top)
        
        #define font type
        self.text_input_present = text_input
        if text_input:
            self.font = font
            self.base_color, self.hovering_color = base_color, hovering_color
            self.text_input = text_input
            self.text = self.font.render(self.text_input, True, self.base_color)

        # toggle attributes
        self.is_hovered = False
        self.second_is_hovered = False
        self.is_toggled = False
        self.is_active = False

    def check_hover(self, position):
        if self.text_input_present:
            self.text = self.font.render(self.text_input, True, self.base_color)
            self.image.blit(self.text, (20, 20))
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            self.is_hovered = True
            self.second_is_hovered = True
            return True
        else:
            self.is_hovered = False
            self.second_is_hovered = False
            return False

    def hover_animation(self, position):
        if self.check_hover(position) and self.is_toggled == False:
            if self.text_input_present:
                self.text = self.font.render(self.text_input, True, self.hovering_color)
                self.image.blit(self.text, (20, 20))
            self.image = self.hovered_image
            self.rect.center = self.hovered_pos
        else:
            if self.text_input_present:
                self.text = self.font.render(self.text_input, True, self.base_color)
                self.image.blit(self.text, (20, 20))
            self.image = self.normal_image
            self.rect.center = self.original_pos

    def toggled_check(self,position):
        if self.check_hover(position) and self.is_toggled or self.is_toggled:
            if self.text_input_present:
                self.text = self.font.render(self.text_input, True, self.toggled_color)
                self.image.blit(self.text, (20, 20))
            self.image = self.toggled_image
            self.is_hovered = False
        else:
            if self.text_input_present:
                self.text = self.font.render(self.text_input, True, self.base_color)
                self.image.blit(self.text, (20, 20))
            self.image = self.normal_image
    
    def update(self, mouse_position, visibility = True):
        if visibility:
            if self.is_toggled:
                self.rect.center = (self.x_pos, self.y_pos)
                self.toggled_check(mouse_position)
            else:
                self.rect.center = (self.x_pos, self.y_pos)
                self.hover_animation(mouse_position) 
        else:
            self.is_hovered = False
            self.second_is_hovered = False
            self.rect.center = (self.x_pos, 1000)


# parent class of hovering descriptions, referred to as options descriptions
class OptionDescription(pygame.sprite.Sprite):
    def __init__(self, bg_image, scale, add_dimensions, text_desc, font, fontcolor, text_pos, effect_pos, details_pos, activity_rect, **kwargs):
        super().__init__()

        # get image
        temp_size = bg_image.get_size()
        self.image = pygame.transform.scale(bg_image, (temp_size[0]*scale, temp_size[1]*scale))
        temp_size = self.image.get_size()
        if add_dimensions != False:
            self.image = pygame.transform.scale(self.image, (temp_size[0] + add_dimensions[0], temp_size[1] + add_dimensions[1]))
        
        # get rectangle
        self.rect = self.image.get_rect()

        # fonts
        self.font = font
        self.fontcolor = fontcolor
        self.text_pos = text_pos
        self.text_pos_x = self.text_pos[0]
        self.text_pos_y = self.text_pos[1]
        self.effect_text_pos = effect_pos
        if self.effect_text_pos:
            self.effect_text_pos_x = self.effect_text_pos[0]
            self.effect_text_pos_y = self.effect_text_pos[1]
        self.details_pos = details_pos
        self.details_pos_x = self.details_pos[0]
        self.details_pos_y = self.details_pos[1]
        # description info
        self.text_description_list = text_desc

        self.details_list = False

        # active area rect
        self.activity_rect = pygame.Rect(activity_rect[0], activity_rect[1], activity_rect[2], activity_rect[3])
        self.active = False
        self.show = False
        self.not_drawn = True
        self.bottom_limit = HEIGHT - self.image.get_size()[1]
        self.right_limit = WIDTH - self.image.get_size()[0]
    
    def set_description(self, mouse_pos):
        if self.check_hover(mouse_pos) and self.show and self.not_drawn:
            for line in self.text_description_list:
                self.image.blit(self.font.render(line, True, self.fontcolor), (self.text_pos_x, self.text_pos_y))
                self.text_pos_y += 20
            if self.effect_text_pos:
                for line in self.effect:
                    self.image.blit(self.font.render(line, True, self.fontcolor), (self.effect_text_pos_x, self.effect_text_pos_y))
                    self.effect_text_pos_y += 20
            if self.details_list:
                for detail in self.details_list:
                    self.image.blit(self.font.render(detail, True, self.fontcolor), (self.details_pos_x, self.details_pos_y))
                    self.details_pos_y += 20
            self.not_drawn = False
        if self.check_hover(mouse_pos) and self.show and mouse_pos[1] > self.bottom_limit and mouse_pos[0] < self.right_limit:
            self.rect.topleft = (mouse_pos[0], self.bottom_limit)
        elif self.check_hover(mouse_pos) and self.show and mouse_pos[1] < self.bottom_limit and mouse_pos[0] > self.right_limit:
            self.rect.topleft = (self.right_limit, mouse_pos[1])
        elif self.check_hover(mouse_pos) and self.show and mouse_pos[1] > self.bottom_limit and mouse_pos[0] > self.right_limit:
            self.rect.topleft = (self.right_limit, self.bottom_limit)
        elif self.check_hover(mouse_pos) and self.show:
            self.rect.topleft = mouse_pos
    
    def check_hover(self, mouse_pos):
        if self.active:
            if mouse_pos[0] in range(self.activity_rect.left, self.activity_rect.right) and mouse_pos[1] in range(self.activity_rect.top, self.activity_rect.bottom):
                self.show = True
                return True
            else:
                self.show = False
                return False

    def update(self, mouse_pos, visibility = False):
        self.rect.center = (0, 1000)
        if visibility:
            self.active = True
            self.set_description(mouse_pos)
        else:
            self.rect.center = (0, 1000)
            self.active = False
            self.show = False


class AttacksMenu(Menus):


    def __init__(self, attacks_menu_image, attacks_dimensions):
        super().__init__(menu_image= attacks_menu_image, dimensions= attacks_dimensions)
    

class AttackOptions(ToggleButtons):

    def __init__(self, attack_name, attack_image, attack_toggled_image, attack_scale, attack_add_dimensions, attack_pos, attack_text_input,
            attack_font, attack_base_color, attack_hovering_color, attack_toggled_color):
        
        super().__init__(name= attack_name, image= attack_image, toggled_image= attack_toggled_image, scale= attack_scale, add_dimensions= attack_add_dimensions,
            pos= attack_pos, text_input= attack_text_input, font= attack_font, base_color= attack_base_color, hovering_color= attack_hovering_color,
            toggled_color= attack_toggled_color)

class AttackOptionsDescription(OptionDescription):
    def __init__(self, attack_bg_image, attack_scale, attack_add_dimensions, attack_text_desc, attack_stats_dict, attack_font, attack_fontcolor, 
                 attack_text_pos, attack_effect_pos, attack_details_pos, attack_activity_rect):
        super().__init__(bg_image= attack_bg_image, scale= attack_scale, add_dimensions= attack_add_dimensions, text_desc= attack_text_desc, 
                        font= attack_font, fontcolor= attack_fontcolor, text_pos=attack_text_pos, effect_pos= attack_effect_pos,
                        details_pos=attack_details_pos, activity_rect=attack_activity_rect)
        
        self.damage = f"Damage: [ {str(attack_stats_dict['damage'])} ]"
        self.to_hit = f"To hit: [ {str(attack_stats_dict['to_hit'])} ]"
        self.extra_effect = f"Extra Effects: [ {str(attack_stats_dict['extra_effects'])} ]"
        self.range = f"Range: [ {attack_stats_dict['range']} ]"
        self.action_cost = f"Action Cost: [ {str(attack_stats_dict['action_cost'])} ]"

        self.details_list =[self.damage, self.to_hit, self.extra_effect, self.range, self.range, self.action_cost]

class AttackOptionsManager():
    def __init__(self, char_name, attacks_dict_data):
        self.position = (WIDTH/2, HEIGHT/2)
        self.attacks_number = attacks_dict_data[f"Number_of_attacks"]
        self.attacks_data = attacks_dict_data[f"{char_name}_attacks"]

        self.attacks_not_set = True
        self.attacks_description_not_set = True
        self.attacks_choices = []

        self.attacks_rect_ranges = []
        self.attacks_choices_descriptions = []

        self.set_attacks()
        self.set_attack_descriptions()
    
    def set_attacks(self):
        if self.attacks_not_set:
            for i in range(1, self.attacks_number+1):
                attack_option = AttackOptions(
                    self.attacks_data[f"attack{i}_name"],
                    attack_options_button_bg,
                    attack_options_button_toggled_bg,
                    1.5,
                    (75,0),
                    (self.position[0], self.position[1] - 285 + (i*70)),
                    self.attacks_data[f"attack{i}_name"],
                    description,
                    DARK_OAK,
                    DARK_OAK,
                    GREEN
                )
                self.attacks_choices.append(attack_option)
                self.attacks_rect_ranges.append(attack_option.rect_range)
            attack_options_group.add(self.attacks_choices)
            self.attacks_not_set = False
    
    def set_attack_descriptions(self):
        if self.attacks_description_not_set:
            for i in range(1, self.attacks_number+1):
                attack_option_description = AttackOptionsDescription(
                    attacks_description_panel_bg,
                    5,
                    (150,30),
                    self.attacks_data[f"attack{i}_description"],
                    self.attacks_data[f"attack{i}_stats"],
                    description,
                    WHITE,
                    (70, 55),
                    False,
                    (70, 100),
                    self.attacks_rect_ranges[i-1]
                )
                attack_option_description.rect
                self.attacks_choices_descriptions.append(attack_option_description)
            attack_options_descriptions_group.add(self.attacks_choices_descriptions)
            self.attacks_description_not_set = False




class SpellsMenu(Menus):

    def __init__(self, spells_menu_image, spells_dimensions):
        super().__init__(menu_image= spells_menu_image, dimensions= spells_dimensions)

class SpellOptions(ToggleButtons):
    def __init__(self, spell_name, spell_image, spell_toggled_image, spell_scale, spell_add_dimensions, spell_pos, spell_text_input,
            spell_font, spell_base_color, spell_hovering_color, spell_toggled_color):
        
        super().__init__(name= spell_name, image= spell_image, toggled_image= spell_toggled_image, scale= spell_scale, add_dimensions= spell_add_dimensions,
            pos= spell_pos, text_input= spell_text_input, font= spell_font, base_color= spell_base_color, hovering_color= spell_hovering_color,
            toggled_color= spell_toggled_color)

class SpellOptionsDescription(OptionDescription):
    def __init__(self, spell_bg_image, spell_scale, spell_add_dimensions, spell_text_desc, spell_stats_dict, spell_font, spell_fontcolor, 
                 spell_text_pos, spell_effect_pos, spell_details_pos, spell_activity_rect):
        super().__init__(bg_image= spell_bg_image, scale= spell_scale, add_dimensions= spell_add_dimensions, text_desc= spell_text_desc, 
                        font= spell_font, fontcolor= spell_fontcolor, text_pos=spell_text_pos, effect_pos= spell_effect_pos,
                        details_pos=spell_details_pos, activity_rect=spell_activity_rect)
        
        self.effect = spell_stats_dict['spell_effect']
        self.damage = f"Damage: [ {str(spell_stats_dict['damage'])} ]"
        self.save_dc = f"Save DC: [ {str(spell_stats_dict['save_dc'])} ]"
        self.dc_type = f"Save Ability: [ {str(spell_stats_dict['dc_type'])} ]"
        self.range = f"Range: [ {spell_stats_dict['range']} ]"
        self.action_cost = f"Action Cost: [ {str(spell_stats_dict['action_cost'])} ]"
        self.magic_cost = f"Magic Cost: [ {str(spell_stats_dict['magic_cost'])} ]"

        self.details_list =[self.damage, self.save_dc, self.dc_type, self.range, self.action_cost, self.magic_cost]


class SpellOptionsManager():
    def __init__(self, char_name, spells_dict_data):
        self.position = (WIDTH/2, HEIGHT/2)
        self.spells_number = spells_dict_data[f"Number_of_spells"]
        self.spells_data = spells_dict_data[f"{char_name}_spells"]

        self.spells_not_set = True
        self.spells_description_not_set = True
        self.spells_choices = []

        self.spells_rect_ranges = []
        self.spells_choices_descriptions = []

        self.set_spells()
        self.set_spell_descriptions()
    
    def set_spells(self):
        if self.spells_not_set:
            for i in range(1, self.spells_number+1):
                if i <= 5:
                    spell_option = SpellOptions(
                        self.spells_data[f"spell{i}_name"],
                        spell_options_button_bg,
                        spell_options_button_toggled_bg,
                        1.5,
                        (100,0),
                        (self.position[0]-245, self.position[1] - 238 + (i*65)),
                        self.spells_data[f"spell{i}_name"],
                        description,
                        DARK_OAK,
                        DARK_OAK,
                        GREEN
                    )
                    self.spells_choices.append(spell_option)
                    self.spells_rect_ranges.append(spell_option.rect_range)
                else:
                    spell_option = SpellOptions(
                        self.spells_data[f"spell{i}_name"],
                        spell_options_button_bg,
                        spell_options_button_toggled_bg,
                        1.5,
                        (100,0),
                        (self.position[0]+245, self.position[1] - 238 + ((i-5)*65)),
                        self.spells_data[f"spell{i}_name"],
                        description,
                        DARK_OAK,
                        DARK_OAK,
                        GREEN
                    )
                    self.spells_choices.append(spell_option)
                    self.spells_rect_ranges.append(spell_option.rect_range)
            spell_options_group.add(self.spells_choices)
            self.spells_not_set = False
    
    def set_spell_descriptions(self):
        if self.spells_description_not_set:
            for i in range(1, self.spells_number+1):
                spell_option_description = SpellOptionsDescription(
                    spells_description_panel_bg,
                    7,
                    (100,30),
                    self.spells_data[f"spell{i}_description"],
                    self.spells_data[f"spell{i}_stats"],
                    description,
                    BLACK,
                    (100, 90),
                    (100, 180),
                    (100, 270),
                    self.spells_rect_ranges[i-1]
                )
                spell_option_description.rect
                self.spells_choices_descriptions.append(spell_option_description)
            spell_options_descriptions_group.add(self.spells_choices_descriptions)
            self.spells_description_not_set = False

class RoleplayMenu(Menus):

    def __init__(self, roleplay_menu_image, roleplay_dimensions):
        super().__init__(menu_image= roleplay_menu_image, dimensions= roleplay_dimensions)

class RoleplayOptions(ToggleButtons):
    def __init__(self, roleplay_name, roleplay_image, roleplay_toggled_image, roleplay_scale, roleplay_add_dimensions, roleplay_pos, roleplay_text_input,
            roleplay_font, roleplay_base_color, roleplay_hovering_color, roleplay_toggled_color):
        
        super().__init__(name= roleplay_name, image= roleplay_image, toggled_image= roleplay_toggled_image, scale= roleplay_scale, add_dimensions= roleplay_add_dimensions,
            pos= roleplay_pos, text_input= roleplay_text_input, font= roleplay_font, base_color= roleplay_base_color, hovering_color= roleplay_hovering_color,
            toggled_color= roleplay_toggled_color)


class RoleplayOptionsDescription(OptionDescription):
    def __init__(self, roleplay_bg_image, roleplay_scale, roleplay_add_dimensions, roleplay_text_desc, roleplay_stats_dict, roleplay_font, roleplay_fontcolor, 
                 roleplay_text_pos, roleplay_effect_pos, roleplay_details_pos, roleplay_activity_rect):
        super().__init__(bg_image= roleplay_bg_image, scale= roleplay_scale, add_dimensions= roleplay_add_dimensions, text_desc= roleplay_text_desc, 
                        font= roleplay_font, fontcolor= roleplay_fontcolor, text_pos=roleplay_text_pos, effect_pos= roleplay_effect_pos,
                        details_pos=roleplay_details_pos, activity_rect=roleplay_activity_rect)
        
        self.effect = roleplay_stats_dict['roleplay_effect']

        self.save_dc = f"Save DC: [ {str(roleplay_stats_dict['save_dc'])} ]"
        self.dc_type = f"Save Ability: [ {str(roleplay_stats_dict['dc_type'])} ]"
        self.range = f"Range: [ {roleplay_stats_dict['range']} ]"
        self.action_cost = f"Action Cost: [ {str(roleplay_stats_dict['action_cost'])} ]"

        self.details_list = [self.save_dc, self.dc_type, self.range, self.action_cost]


class RoleplayOptionsManager():
    def __init__(self, char_name, roleplay_dict_data):
        self.position = (WIDTH/2, HEIGHT/2)
        self.roleplays_number = roleplay_dict_data[f"Number_of_roleplays"]
        self.roleplay_data = roleplay_dict_data[f"{char_name}_roleplays"]

        self.roleplay_not_set = True
        self.roleplay_description_not_set = True
        self.roleplay_choices = []

        self.roleplay_rect_ranges = []
        self.roleplay_choices_descriptions = []

        self.set_roleplay()
        self.set_roleplay_descriptions()
    
    def set_roleplay(self):
        if self.roleplay_not_set:
            for i in range(1, self.roleplays_number+1):
                if i <= 5:
                    roleplay_option = RoleplayOptions(
                        self.roleplay_data[f"roleplay{i}_name"],
                        roleplay_options_button_bg,
                        roleplay_options_button_toggled_bg,
                        1.5,
                        (100,0),
                        (self.position[0]-275, self.position[1] - 228 + (i*70)),
                        self.roleplay_data[f"roleplay{i}_name"],
                        description,
                        DARK_OAK,
                        DARK_OAK,
                        GREEN
                    )
                    self.roleplay_choices.append(roleplay_option)
                    self.roleplay_rect_ranges.append(roleplay_option.rect_range)
                else:
                    roleplay_option = RoleplayOptions(
                        self.roleplay_data[f"roleplay{i}_name"],
                        roleplay_options_button_bg,
                        roleplay_options_button_toggled_bg,
                        1.5,
                        (100,0),
                        (self.position[0]+275, self.position[1] - 228 + ((i-5)*70)),
                        self.roleplay_data[f"roleplay{i}_name"],
                        description,
                        DARK_OAK,
                        DARK_OAK,
                        GREEN
                    )
                    self.roleplay_choices.append(roleplay_option)
                    self.roleplay_rect_ranges.append(roleplay_option.rect_range)
            roleplay_options_group.add(self.roleplay_choices)
            self.roleplay_not_set = False
    
    def set_roleplay_descriptions(self):
        if self.roleplay_description_not_set:
            for i in range(1, self.roleplays_number+1):
                roleplay_option_description = RoleplayOptionsDescription(
                    roleplay_description_panel_bg,
                    7,
                    (100,30),
                    self.roleplay_data[f"roleplay{i}_description"],
                    self.roleplay_data[f"roleplay{i}_stats"],
                    description,
                    BLACK,
                    (100, 70),
                    (100, 180),
                    (100, 350),
                    self.roleplay_rect_ranges[i-1]
                )
                roleplay_option_description.rect
                self.roleplay_choices_descriptions.append(roleplay_option_description)
            roleplay_options_descriptions_group.add(self.roleplay_choices_descriptions)
            self.roleplay_description_not_set = False

class MovementMenu(Menus):

    def __init__(self, movement_menu_image, movement_dimensions):
        super().__init__(menu_image= movement_menu_image, dimensions= movement_dimensions)

class MovementOptions(ToggleButtons):
    def __init__(self, movement_name, movement_image, movement_toggled_image, movement_scale, movement_add_dimensions, 
                 movement_pos, movement_text_input, movement_font, movement_base_color, movement_hovering_color, 
                 movement_toggled_color):
        
        super().__init__(name= movement_name, image= movement_image, toggled_image= movement_toggled_image, scale= movement_scale, 
                         add_dimensions= movement_add_dimensions, pos= movement_pos, text_input= movement_text_input, 
                         font= movement_font, base_color= movement_base_color, hovering_color= movement_hovering_color, 
                         toggled_color= movement_toggled_color)

class MovementOptionsManager():
    def __init__(self):
        self.position = (WIDTH/2, HEIGHT/2)
        self.zones = {0: "Melee", 1: "Thrown", 2: "Snipe"}

        self.zones_not_set = True
        self.roleplay_choices = []
        self.movement_choices = []

        self.set_movement_zones()
    
    def set_movement_zones(self):
        if self.zones_not_set:
            for i in range(3):
                movement_option = MovementOptions(
                    self.zones[i],
                    movement_options_button_bg,
                    movement_options_button_toggled_bg,
                    1.5,
                    (-50,0),
                    (self.position[0] - 250 + ((i+1)*125), self.position[1] + 150),
                    self.zones[i],
                    description,
                    DARK_OAK,
                    DARK_OAK,
                    GREEN
                )
                self.movement_choices.append(movement_option)
            movement_options_group.add(self.movement_choices)
            self.movement_not_set = False
            for zone in movement_options_group.sprites():
                if zone.name == "Thrown":
                    zone.is_toggled = True


class InventoryMenu(Menus):

    def __init__(self, inventory_menu_image, inventory_dimensions):
        super().__init__(menu_image= inventory_menu_image, dimensions= inventory_dimensions)

class InventoryOptions(ToggleButtons):
    def __init__(self, inventory_name, inventory_image, inventory_toggled_image, inventory_scale, inventory_add_dimensions, 
                 inventory_pos, inventory_text_input, inventory_font, inventory_base_color, inventory_hovering_color, 
                 inventory_toggled_color, item_image):
        
        super().__init__(name= inventory_name, image= inventory_image, toggled_image= inventory_toggled_image, scale= inventory_scale, 
                         add_dimensions= inventory_add_dimensions, pos= inventory_pos, text_input= inventory_text_input, 
                         font= inventory_font, base_color= inventory_base_color, hovering_color= inventory_hovering_color, 
                         toggled_color= inventory_toggled_color)
        
        self.item_image = item_image
    
    def set_item(self):
        if self.item_image:
            WIN.blit(self.item_image, (self.x_pos-37, self.y_pos-37))
    

    def update(self, mouse_position, visibility = True):
        if visibility:
            self.set_item()
            if self.is_toggled:
                self.rect.center = (self.x_pos, self.y_pos)
                self.toggled_check(mouse_position)
            else:
                self.rect.center = (self.x_pos, self.y_pos)
                self.hover_animation(mouse_position) 
        else:
            self.is_hovered = False
            self.second_is_hovered = False
            self.rect.center = (self.x_pos, 1000)
        
    
class InventoryOptionsDescription(OptionDescription):
    def __init__(self, inventory_bg_image, inventory_scale, inventory_add_dimensions, inventory_name, inventory_text_desc, inventory_effect, inventory_action_cost, inventory_font, inventory_fontcolor, 
                 inventory_name_pos, inventory_text_pos, inventory_effect_pos, inventory_action_cost_pos, inventory_details_pos, inventory_activity_rect):
        super().__init__(bg_image= inventory_bg_image, scale= inventory_scale, add_dimensions= inventory_add_dimensions, text_desc= inventory_text_desc, 
                        font= inventory_font, fontcolor= inventory_fontcolor, text_pos=inventory_text_pos, effect_pos= inventory_effect_pos,
                        details_pos=inventory_details_pos, activity_rect=inventory_activity_rect)

        self.item_name = inventory_name
        self.effect = inventory_effect
        self.action_cost = f"Action Cost: {str(inventory_action_cost)}"
        self.item_action_cost_pos_x = inventory_action_cost_pos[0]
        self.item_action_cost_pos_y = inventory_action_cost_pos[1]
        self.item_name_pos_x = inventory_name_pos[0]
        self.item_name_pos_y = inventory_name_pos[1]

    def set_description(self, mouse_pos):
        if self.check_hover(mouse_pos) and self.show and self.not_drawn:
            try:
                if self.item_name:
                    self.image.blit(self.font.render(self.item_name, True, self.fontcolor), (self.item_name_pos_x, self.item_name_pos_y))
                for line in self.text_description_list:
                    self.image.blit(self.font.render(line, True, self.fontcolor), (self.text_pos_x, self.text_pos_y))
                    self.text_pos_y += 20
                if self.effect_text_pos:
                    for line in self.effect:
                        self.image.blit(self.font.render(line, True, self.fontcolor), (self.effect_text_pos_x, self.effect_text_pos_y))
                        self.effect_text_pos_y += 20
                if self.action_cost:
                    self.image.blit(self.font.render(self.action_cost, True, self.fontcolor), (self.effect_text_pos_x, self.effect_text_pos_y+10))
                self.not_drawn = False
            except TypeError:
                self.image.blit(self.font.render("(Empty)", True, self.fontcolor), (self.item_name_pos_x, self.item_name_pos_y))
                self.not_drawn = False
        if self.check_hover(mouse_pos) and self.show and mouse_pos[1] > self.bottom_limit and mouse_pos[0] < self.right_limit:
            self.rect.topleft = (mouse_pos[0], self.bottom_limit)
        elif self.check_hover(mouse_pos) and self.show and mouse_pos[1] < self.bottom_limit and mouse_pos[0] > self.right_limit:
            self.rect.topleft = (self.right_limit, mouse_pos[1])
        elif self.check_hover(mouse_pos) and self.show and mouse_pos[1] > self.bottom_limit and mouse_pos[0] > self.right_limit:
            self.rect.topleft = (self.right_limit, self.bottom_limit)
        elif self.check_hover(mouse_pos) and self.show:
            self.rect.topleft = mouse_pos

class InventoryOptionsManager():
    def __init__(self, start_inventory):
        self.position = ((WIDTH/2)-105, (HEIGHT/2)-90)
        self.start_inventory = start_inventory
        self.inventory_choices = []
        self.inventory_not_set = True
        self.empty_inventory = [ALL_ITEMS[0], ALL_ITEMS[0], ALL_ITEMS[0], ALL_ITEMS[0],
                          ALL_ITEMS[0], ALL_ITEMS[0], ALL_ITEMS[0], ALL_ITEMS[0],
                          ALL_ITEMS[0]]
        
        self.inventory_rect_ranges = []
        self.inventory_choices_descriptions = []

        self.inventory_description_not_set = True

        self.set_inventory()
        self.set_inventory_descriptions()
    
    def set_inventory(self):
        if self.inventory_not_set:
            for i in range(9):
                if i < 3:
                    inventory_option = InventoryOptions(
                        "Lyre_inventory",
                        inventory_slot_bg,
                        inventory_slot_toggled_bg,
                        1,
                        (0,0),
                        (self.position[0] + i*98, self.position[1]),
                        False,
                        False,
                        False,
                        False,
                        False,
                        self.start_inventory[i]["item_icon"]
                        
                    )
                    self.inventory_choices.append(inventory_option)
                    self.inventory_rect_ranges.append(inventory_option.rect_range)
                elif i < 6:
                    inventory_option = InventoryOptions(
                        "Lyre_inventory",
                        inventory_slot_bg,
                        inventory_slot_toggled_bg,
                        1,
                        (0,0),
                        (self.position[0] - 294 + i*98, self.position[1] + 98),
                        False,
                        False,
                        False,
                        False,
                        False,
                        self.start_inventory[i]["item_icon"]
                    )
                    self.inventory_choices.append(inventory_option)
                    self.inventory_rect_ranges.append(inventory_option.rect_range)
                else:
                    inventory_option = InventoryOptions(
                        "Lyre_inventory",
                        inventory_slot_bg,
                        inventory_slot_toggled_bg,
                        1,
                        (0,0),
                        (self.position[0] - 588 + i*98, self.position[1] + 196),
                        False,
                        False,
                        False,
                        False,
                        False,
                        self.start_inventory[i]["item_icon"],
                    )
                    self.inventory_choices.append(inventory_option)
                    self.inventory_rect_ranges.append(inventory_option.rect_range)
            inventory_options_group.add(self.inventory_choices)
            self.inventory_not_set = False
    
    def set_inventory_descriptions(self):
        if self.inventory_description_not_set:
            for i in range(9):
                inventory_option_description = InventoryOptionsDescription(
                    inventory_description_bg,
                    7,
                    (0,-80),
                    self.start_inventory[i]["item_name"],
                    self.start_inventory[i]["item_description"],
                    self.start_inventory[i]["item_effect"],
                    self.start_inventory[i]["item_action_cost"],
                    description,
                    WHITE,
                    (30,30),
                    (30,60),
                    (30,90),
                    (30,120),
                    (0,0),
                    self.inventory_rect_ranges[i]
                )
                inventory_option_description.rect
                self.inventory_choices_descriptions.append(inventory_option_description)
            inventory_options_descriptions_group.add(self.inventory_choices_descriptions)
            self.inventory_description_not_set = False
        

class CharsheetMenu(Menus):

    def __init__(self, charsheet_menu_image, charsheet_dimensions):
        super().__init__(menu_image= charsheet_menu_image, dimensions= charsheet_dimensions)

class CharsheetInfo(pygame.sprite.Sprite):
    
    def __init__(self, info_type, info, pos):
        super().__init__()
        self.info_types = ["name", "ac", "hp", "mp", "str", "dex", "con", "int", "wis", "cha", "skill1", "skill2", "skill3"]
        self.info_type = info_type
        self.info = info
        if self.info_type in self.info_types[10:]:
            self.image = self.info
        else:
            self.image = charsheet_text.render(self.info, True, BLACK)
        self.rect = self.image.get_rect()
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.rect.center = pos
        self.rect_range = (self.rect.left, self.rect.top, self.rect.right - self.rect.left, self.rect.bottom - self.rect.top)

class CharsheetInfoDescription(OptionDescription):
    
    def __init__(self, charsheet_bg_image, charsheet_scale, charsheet_add_dimensions, charsheet_text_desc, charsheet_font, 
                 charsheet_fontcolor, charsheet_text_pos, charsheet_effect_pos, charsheet_details_pos, charsheet_activity_rect):
        super().__init__(bg_image=charsheet_bg_image, scale=charsheet_scale, add_dimensions=charsheet_add_dimensions, 
                         text_desc=charsheet_text_desc, font=charsheet_font, fontcolor=charsheet_fontcolor, text_pos=charsheet_text_pos,
                         effect_pos=charsheet_effect_pos, details_pos=charsheet_details_pos, activity_rect=charsheet_activity_rect)
        
class CharsheetManager():
    
    def __init__(self, char_info_dict):
        self.char_data = char_info_dict
        self.char_name = self.char_data["name"]
        self.info_types = ["name", "ac", "hp", "mp", "str", "dex", "con", "int", "wis", "cha", "skill1", "skill2", "skill3"]
        self.info_data = [self.char_data["name"], str(self.char_data["AC"]), str(self.char_data["max_hp"]),
                          str(self.char_data["max_mp"]), str(self.char_data["strength"]), str(self.char_data["dexterity"]),
                          str(self.char_data["constitution"]), str(self.char_data["intelligence"]), str(self.char_data["wisdom"]),
                          str(self.char_data["charisma"]), (self.char_data["skill1"]), (self.char_data["skill2"]),
                          (self.char_data["skill3"])]
        center = (WIDTH/2, HEIGHT/2)
        cx = center[0]
        cy = center[1]
        self.positions = [(cx-150,cy-250), (cx-70,cy-168), (cx+130,cy-185), (cx+130,cy-155), (cx-60,cy-78), (cx-60,cy-20),
                          (cx-60,cy+38), (cx-60,cy+96), (cx-60,cy+154), (cx-60,cy+212), (cx+105,cy+10), (cx+105,cy+110),
                          (cx+105,cy+210)]

        self.charsheetinfo_not_set = True
        # self.attacks_description_not_set = True
        self.charsheetinfo_items = []

        self.charsheetinfo_rect_ranges = []
        # self.attacks_choices_descriptions = []

        self.set_charsheetinfo()
        # self.set_attack_descriptions()
    
    def set_charsheetinfo(self):
        if self.charsheetinfo_not_set:
            for i in range(13):
                charsheet_info = CharsheetInfo(
                    self.info_types[i],
                    self.info_data[i],
                    self.positions[i]
                )
                self.charsheetinfo_items.append(charsheet_info)
                self.charsheetinfo_rect_ranges.append(charsheet_info.rect_range)
            charsheet_info_group.add(self.charsheetinfo_items)
            self.charsheetinfo_not_set = False


class TurnActionMenu(Menus):
    def __init__(self, menu_image, dimensions, **kwargs):
        super().__init__(menu_image, dimensions, **kwargs)

class TurnActionManager():
    def __init__(self) -> None:
        pass
    def update(self):
        pass
    

        

# initialize objects
# screen
WIDTH, HEIGHT = 1280, 720
FPS = 60
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ljoss Styris: Lights Out!")
clock = pygame.time.Clock()
BG = pygame.image.load(r"./Assets/loading_screen.png").convert_alpha()
BG = pygame.transform.scale(BG, (1280,720))
BG = pygame.transform.flip(BG,True, False)

# cursor
game_cursor = pygame.image.load(r"./Assets/Sprites/GUI/game_cursor.png").convert_alpha()
game_cursor = pygame.transform.scale(game_cursor, (game_cursor.get_size()[0]*1, game_cursor.get_size()[1]*1))
pygame.mouse.set_visible(False)
# game state
game_state = GameState()

# sounds
pygame.mixer.pre_init()
pygame.mixer.init()
sfx_not_played = True

sound_channel_0 = pygame.mixer.Channel(0)
sound_channel_1 = pygame.mixer.Channel(1)
sound_channel_2 = pygame.mixer.Channel(2)
sound_channel_3 = pygame.mixer.Channel(3)
sound_channel_4 = pygame.mixer.Channel(4)
sound_channel_5 = pygame.mixer.Channel(5)
sound_channel_6 = pygame.mixer.Channel(6)
sound_channel_7 = pygame.mixer.Channel(7)

sound_channels = [sound_channel_0, sound_channel_1, sound_channel_2, sound_channel_3, sound_channel_4,
                  sound_channel_5, sound_channel_6, sound_channel_7]


# load soundtrack
char_select_theme = pygame.mixer.Sound(r"./SFX/main_menu_song.mp3")
battle_theme_1 = pygame.mixer.Sound(r"./SFX/train_battle_song.mp3")

# load sfx
button_hover_sfx = pygame.mixer.Sound(r"./SFX/choose_char_sfx.wav")
button_click_sfx = pygame.mixer.Sound(r"./SFX/char_chosen_sfx.wav")
train_whistle = pygame.mixer.Sound(r"./SFX/train_whistle_sfx.mp3")
train_sounds = pygame.mixer.Sound(r"./SFX/train_sounds_sfx.mp3")
battle_start_voice = pygame.mixer.Sound(r"./SFX/battle_start_sfx.mp3")

explosion1 = pygame.mixer.Sound(r"./SFX/explosion_1_sfx.mp3")

# start playing the background music
sound_channel_0.play(char_select_theme, -1, fade_ms= 1000)
sound_channel_0.set_volume(0.2)

# pygame.mixer.music.set_volume(0.2)
# pygame.mixer.music.play(loops=-1)  # loop forever

# fonts
DARK_OAK = (41,26,3)
WHITE = (255, 255, 255)
GREEN = (102, 204, 0)
BLACK = (5, 5, 5)
button_text = pygame.font.Font(r"./Assets/depixel/DePixelHalbFett.ttf", 19)
charsheet_text = pygame.font.Font(r"./Assets/depixel/DePixelHalbFett.ttf", 25)
heading1 = pygame.font.Font(r"./Assets/depixel/DePixelHalbFett.ttf", 20)
heading2 = pygame.font.Font(r"./Assets/depixel/DePixelHalbFett.ttf", 15)
description = pygame.font.Font(r"./Assets/depixel/DePixelKlein.ttf", 12)
# set game data
from gamedata import CHARDATA, ANIMATION_DICT, ATTACKS_DATA, SPELLS_DATA, ROLEPLAY_DATA, ALL_ITEMS, START_ITEMS, CHARSHEET_DATA

# set background manager
background_manager = BackgroundManager()

# load character tokens
LYRE_TOKEN = pygame.image.load(r"./Assets/Tokens/lyre_token.png").convert_alpha()
lyre_token = CharacterTokens("Lyre", LYRE_TOKEN, (127.5, 550), CHARDATA[0])

MARCEE_TOKEN = pygame.image.load(r"./Assets/Tokens/marcee_token.png").convert_alpha()
marcee_token = CharacterTokens("Marcee De la Mer", MARCEE_TOKEN, (277.5, 550), CHARDATA[1])

MAURLO_TOKEN = pygame.image.load(r"./Assets/Tokens/maurlo_token.png").convert_alpha()
maurlo_token = CharacterTokens("Maurlo 'Maurlomallow' Liebermann", MAURLO_TOKEN, (427.5, 550), CHARDATA[2])

NAILEA_TOKEN = pygame.image.load(r"./Assets/Tokens/nailea_token.png").convert_alpha()
nailea_token = CharacterTokens("Nailea Arorangiurohanga", NAILEA_TOKEN, (577.5, 550), CHARDATA[3])

PYNNCONE_TOKEN = pygame.image.load(r"./Assets/Tokens/pynncone_token.png").convert_alpha()
pynncone_token = CharacterTokens("Pynncone Amanita", PYNNCONE_TOKEN, (727.5, 550), CHARDATA[4])

VARICK_TOKEN = pygame.image.load(r"./Assets/Tokens/varick_token.png").convert_alpha()
varick_token = CharacterTokens("Varick Ehre", VARICK_TOKEN, (877.5, 550), CHARDATA[5])

YAYAN_TOKEN = pygame.image.load(r"./Assets/Tokens/yayan_token.png").convert_alpha()
yayan_token = CharacterTokens("Yayan", YAYAN_TOKEN, (1027.5, 550), CHARDATA[6])

token_list = [lyre_token, marcee_token, maurlo_token, nailea_token, pynncone_token, varick_token, yayan_token]

CHAR_NAMES_LIST = ["Lyre", "Marcee De la Mer", "Maurlo 'Maurlomallow' Liebermann", "Nailea Arorangiurohanga", "Pynncone Amanita", "Varick Ehre", "Yayan"]
CHAR_SUBNAMES_LIST = ["lyre", "marcee", "maurlo", "nailea", "pynncone", "varick", "yayan"]

# load fight button
fight_button = FightButton(pygame.image.load(r"./Assets/Tokens/play_button.png").convert_alpha(), ((WIDTH/2)-220, (HEIGHT/2)-84))

# load bg image lists
mountain_list = background_manager.init_background(3, "mountain", 4)
plains_list = background_manager.init_background(5, "field", 5)

# load train and tracks
train_image = pygame.image.load(r"./Assets/Sprites/pixel_full_train.png").convert_alpha()
train_image = pygame.transform.scale(train_image, (4532, 315))
tracks_image = pygame.image.load(r"./Assets/Sprites/pixel_full_tracks.png").convert_alpha()
train_and_tracks = Train(WIN, train_image, tracks_image)

# load sprite groups
stage_graphics = pygame.sprite.Group()

# load sprite images

roll_init_logo = pygame.image.load(r"./Assets/Sprites/pixel_roll_intiative.png").convert_alpha()
roll_init_logo = pygame.transform.scale(roll_init_logo, (248.5, 400))
roll_init_graphics = StageGraphics(roll_init_logo, battle_start_voice)
stage_graphics.add(roll_init_graphics)

# load spritesheet lists
round_explosion = ANIMATION_DICT["round_explosion"]
round_explosion_graphics =StageGraphics(round_explosion, explosion1)
stage_graphics.add(round_explosion_graphics)

# load guiding lights group
guiding_lights_group = pygame.sprite.Group()

lyre_sprite = pygame.image.load(r"./Assets/Sprites/Characters/lyre_sprite.png").convert_alpha()
lyre_sprite = pygame.transform.scale(lyre_sprite, (lyre_sprite.get_size()[0]*0.2, lyre_sprite.get_size()[1]*0.2))
marcee_sprite = pygame.image.load(r"./Assets/Sprites/Characters/marcee_sprite.png").convert_alpha()
marcee_sprite = pygame.transform.scale(marcee_sprite, (marcee_sprite.get_size()[0]*0.2, marcee_sprite.get_size()[1]*0.2))
maurlo_sprite = pygame.image.load(r"./Assets/Sprites/Characters/maurlo_sprite.png").convert_alpha()
maurlo_sprite = pygame.transform.scale(maurlo_sprite, (maurlo_sprite.get_size()[0]*0.2, maurlo_sprite.get_size()[1]*0.2))
nailea_sprite = pygame.image.load(r"./Assets/Sprites/Characters/nailea_sprite.png").convert_alpha()
nailea_sprite = pygame.transform.scale(nailea_sprite, (nailea_sprite.get_size()[0]*0.2, nailea_sprite.get_size()[1]*0.2))
pynncone_sprite = pygame.image.load(r"./Assets/Sprites/Characters/pynncone_sprite.png").convert_alpha()
pynncone_sprite = pygame.transform.scale(pynncone_sprite, (pynncone_sprite.get_size()[0]*0.2, pynncone_sprite.get_size()[1]*0.2))
varick_sprite = pygame.image.load(r"./Assets/Sprites/Characters/varick_sprite.png").convert_alpha()
varick_sprite = pygame.transform.scale(varick_sprite, (varick_sprite.get_size()[0]*0.2, varick_sprite.get_size()[1]*0.2))
yayan_sprite = pygame.image.load(r"./Assets/Sprites/Characters/yayan_sprite.png").convert_alpha()
yayan_sprite = pygame.transform.scale(yayan_sprite, (yayan_sprite.get_size()[0]*0.2, yayan_sprite.get_size()[1]*0.2))

# load buttons
buttons_group = pygame.sprite.Group()

button_bg = pygame.image.load(r"./Assets/Sprites/GUI/button.png").convert_alpha()
turnactions_button_bg = pygame.image.load(r"./Assets/Sprites/GUI/turnactions_button.png").convert_alpha()

attacks_button = Button("attacks_button", button_bg, 0.3, False, (100, 50), "Attacks", button_text, DARK_OAK, WHITE)
buttons_group.add(attacks_button)
spells_button = Button("spells_button", button_bg, 0.3, False, (100, 140), "Spells", button_text, DARK_OAK, WHITE)
buttons_group.add(spells_button)
roleplay_button = Button("roleplay_button", button_bg, 0.3, False, (100, 230), "Roleplay", button_text, DARK_OAK, WHITE)
buttons_group.add(roleplay_button)
move_button = Button("move_button", button_bg, 0.3, (100,0), (370, 50), "Move Positions", button_text, DARK_OAK, WHITE)
buttons_group.add(move_button)
inventory_button = Button("inventory_button", button_bg, 0.3, (100, 0), (690, 50), "Bag of Holding", button_text, DARK_OAK, WHITE)
buttons_group.add(inventory_button)
charsheet_button = Button("charsheet_button", button_bg, 0.3, (100, 0), (1010, 50), "Character Sheet", button_text, DARK_OAK, WHITE)
buttons_group.add(charsheet_button)
# turnactions_button = Button("turnactions_button", turnactions_button_bg, 5, (0,0), (1150, 50), "10/10", button_text, WHITE, WHITE)
# buttons_group.add(turnactions_button)

# load healthbar
healthbars_group = pygame.sprite.Group()
health_box = pygame.image.load(r"./Assets/Sprites/GUI/health_box.png").convert_alpha()
health_bar_point = pygame.image.load(r"./Assets/Sprites/GUI/health_bar.png").convert_alpha()
player_1_health_bar = HealthBar(health_box,health_bar_point, 100, (50,640))
healthbars_group.add(player_1_health_bar)
player_2_health_bar = HealthBar(health_box,health_bar_point, 100, (830,640))
healthbars_group.add(player_2_health_bar)

#load magicbar
magicbars_group = pygame.sprite.Group()
magic_box = pygame.image.load(r"./Assets/Sprites/GUI/magic_box.png").convert_alpha()
magic_bar_point = pygame.image.load(r"./Assets/Sprites/GUI/magic_bar.png").convert_alpha()
player_1_magic_bar = MagicBar(magic_box,magic_bar_point, 100, (50,590))
magicbars_group.add(player_1_magic_bar)
player_2_magic_bar = MagicBar(magic_box,magic_bar_point, 100, (830,590))
magicbars_group.add(player_2_magic_bar)

# load menus
attacks_menu_group = pygame.sprite.Group()
spells_menu_group = pygame.sprite.Group()
roleplay_menu_group = pygame.sprite.Group()
movement_menu_group = pygame.sprite.Group()
inventory_menu_group = pygame.sprite.Group()
charsheet_menu_group = pygame.sprite.Group()
# turnactions_menu_group = pygame.sprite.Group()

attacks_menu_bg = pygame.image.load(r"./Assets/Sprites/GUI/attacks_menu_bg.png").convert_alpha()
spells_menu_bg = pygame.image.load(r"./Assets/Sprites/GUI/spells_menu_bg.png").convert_alpha()
roleplay_menu_bg = pygame.image.load(r"./Assets/Sprites/GUI/roleplay_menu_bg.png").convert_alpha()
movement_menu_bg = pygame.image.load(r"./Assets/Sprites/GUI/movement_menu_bg.png").convert_alpha()
inventory_menu_bg = pygame.image.load(r"./Assets/Sprites/GUI/inventory_menu_bg.png").convert_alpha()
charsheet_menu_bg = pygame.image.load(r"./Assets/Sprites/GUI/charsheet_menu_bg.png").convert_alpha()
# turnactions_menu_bg = pygame.image.load(r"./Assets/Sprites/GUI/turnactions_menu_bg.png").convert_alpha()

attacks_menu = AttacksMenu(attacks_menu_bg, (450, 600))
attacks_menu_group.add(attacks_menu)

spells_menu = SpellsMenu(spells_menu_bg, (1000,500))
spells_menu_group.add(spells_menu)

roleplay_menu = RoleplayMenu(roleplay_menu_bg, (1000,500))
roleplay_menu_group.add(roleplay_menu)

movement_menu = MovementMenu(movement_menu_bg, (450,450))
movement_menu_group.add(movement_menu)

inventory_menu = InventoryMenu(inventory_menu_bg, (600,600))
inventory_menu_group.add(inventory_menu)

charsheet_menu = CharsheetMenu(charsheet_menu_bg, (450,600))
charsheet_menu_group.add(charsheet_menu)

# turnactions_menu = TurnActionMenu(turnactions_menu_bg, (450, 600))
# turnactions_menu_group.add(turnactions_menu)

# load options per menu
attack_options_group = pygame.sprite.Group()
attack_options_button_bg = pygame.image.load(r"./Assets/Sprites/GUI/option_button.png").convert_alpha()
attack_options_button_toggled_bg = pygame.image.load(r"./Assets/Sprites/GUI/option_button_toggled.png").convert_alpha()
attack_options_descriptions_group = pygame.sprite.Group()
attacks_description_panel_bg = pygame.image.load(r"./Assets/Sprites/GUI/attacks_description_bg.png").convert_alpha()

spell_options_group = pygame.sprite.Group()
spell_options_button_bg = pygame.image.load(r"./Assets/Sprites/GUI/option_button.png").convert_alpha()
spell_options_button_toggled_bg = pygame.image.load(r"./Assets/Sprites/GUI/option_button_toggled.png").convert_alpha()
spell_options_descriptions_group = pygame.sprite.Group()
spells_description_panel_bg = pygame.image.load(r"./Assets/Sprites/GUI/spells_description_bg.png").convert_alpha()

roleplay_options_group = pygame.sprite.Group()
roleplay_options_button_bg = pygame.image.load(r"./Assets/Sprites/GUI/option_button.png").convert_alpha()
roleplay_options_button_toggled_bg = pygame.image.load(r"./Assets/Sprites/GUI/option_button_toggled.png").convert_alpha()
roleplay_options_descriptions_group = pygame.sprite.Group()
roleplay_description_panel_bg = pygame.image.load(r"./Assets/Sprites/GUI/roleplay_description_bg.png").convert_alpha()

movement_options_group = pygame.sprite.Group()
movement_options_button_bg = pygame.image.load(r"./Assets/Sprites/GUI/option_button.png").convert_alpha()
movement_options_button_toggled_bg = pygame.image.load(r"./Assets/Sprites/GUI/option_button_toggled.png").convert_alpha()
melee_zone_icon = pygame.image.load(r"./Assets/Sprites/GUI/melee_icon.png").convert_alpha()
melee_zone_icon = pygame.transform.scale(melee_zone_icon, (250,250))
thrown_zone_icon = pygame.image.load(r"./Assets/Sprites/GUI/thrown_icon.png").convert_alpha()
thrown_zone_icon = pygame.transform.scale(thrown_zone_icon, (250,250))
snipe_zone_icon = pygame.image.load(r"./Assets/Sprites/GUI/snipe_icon.png").convert_alpha()
snipe_zone_icon = pygame.transform.scale(snipe_zone_icon, (250,250))
zone_icons_dict = {"Melee": melee_zone_icon, "Thrown": thrown_zone_icon, "Snipe": snipe_zone_icon}

inventory_options_group = pygame.sprite.Group()
inventory_slot_bg =  pygame.image.load(r"./Assets/Sprites/GUI/inventory_slot.png").convert_alpha()
inventory_slot_bg = pygame.transform.scale(inventory_slot_bg, (90,90))
inventory_slot_toggled_bg =  pygame.image.load(r"./Assets/Sprites/GUI/inventory_slot_toggled.png").convert_alpha()
inventory_slot_toggled_bg = pygame.transform.scale(inventory_slot_toggled_bg, (90,90))
inventory_options_descriptions_group = pygame.sprite.Group()
inventory_description_bg =  pygame.image.load(r"./Assets/Sprites/GUI/inventory_description_bg.png").convert_alpha()

charsheet_info_group = pygame.sprite.Group()

# intialize functions
debug_font = pygame.font.Font(None, 30)
def debug(info, y = 10, x = 10):
    display_surf = pygame.display.get_surface()
    debug_surf = debug_font.render(str(info), True, "Black")
    debug_rect = debug_surf.get_rect(topleft = (x,y))
    display_surf.blit(debug_surf,debug_rect)

def main():
    run = True
    while run:
        clock.tick(60)
        game_state.state_manager()
        pygame.display.update()

    pygame.quit()
    sys.exit()

# run the game and have fun
# - Johann ;)
if __name__ == "__main__":
    main()