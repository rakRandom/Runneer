"""Objetivo:
Treinamento do módulo pygame, com a criação de um jogo do tipo endless runner
chamado "Runneer", usando como referência e auxílio o vídeo "The ultimate introduction to Pygame"¹

- Versão com classes

Feito por: Fellipe Leonardo Peixoto Cunha²

Com auxílio de: Clear Code³⁴

Data de inicio: 14/07/2023
Data de término: XX/XX/XXXX

Referências:

1. https://www.youtube.com/watch?v=AY9MnQ4x3zk
2. https://github.com/rakRandom
3. https://www.youtube.com/@ClearCode
4. https://github.com/clear-code-projects

----------------------------------------- Sections Markers -----------------------------------------

Only shows the name of a sub-section - lowest importance - indented
- '=' 10 time after and before the name
# ========== Area ==========


Only shows the name of a section - low importance - indented
- '=' 20 time after and before the name
# ==================== Area ====================


Shows the name of a section and that it is not complete or usable - medium importance - indented
- '/' 20 time after and before the name
# //////////////////// Under Construction ////////////////////


Shows the name of a section and that it is complete - high importance - indentless
- 100 col length in total
# --------------------------------------------- Area ----------------------------------------------


Shows that the area is totally complete and only change it to expand with caution - highest importance - indentless
- '-' 147 times on the line above and below
- '-' 28 times after, 'BEGGINING OF IMPORTANT AREA - DO NOT CHANGE' in the middle and '-' 74 times after
- '-' 31 times after, 'END OF IMPORTANT AREA - DO NOT CHANGE' in the middle and '-' 77 times after
# ---------------------------------------------------------------------------------------------------------------------------------------------------
# ---------------------------- BEGGINING OF IMPORTANT AREA - DO NOT CHANGE --------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------------------------------------

# ---------------------------------------------------------------------------------------------------------------------------------------------------
# ------------------------------- END OF IMPORTANT AREA - DO NOT CHANGE -----------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------------------------------------


----------------------------------------- Sections Markers -----------------------------------------"""


# Falta a classe do botão para opções e o áudio


# -------------------------------------------- Import ---------------------------------------------

try:
    from settings import *
except: raise ImportError("Error 1: Cannot import settings module")


# ----------------------------------------- Player Class ------------------------------------------

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        walk1 = pygame.image.load("graphics/Player/player_walk_1.png").convert_alpha()
        walk2 = pygame.image.load("graphics/Player/player_walk_2.png").convert_alpha()

        self.jump = pygame.image.load("graphics/Player/jump.png").convert_alpha()
        self.frames = [walk1, walk2]

        self.index = 0

        self.image = self.frames[self.index]
        self.rect = self.image.get_rect(midbottom = (80, 300))

        self.gravityForce = 0
        self.onGround = True

    def playerAnimation(self):
        if self.onGround:                                          # If the player is on the ground
            if self.index < 1.9: self.index += ANIMATION_SPEED     # If index is less than 1.9 it will be increased by a given constant
            else: self.index = 0                                   # But if not it will be equal to zero

            self.image = self.frames[int(self.index)]              # The current image will be the one in index position
        else:                                                      # But if not
            self.image = self.jump                                 # The current image will be the jump image
    
    def jumpAction(self):
        keys = pygame.key.get_pressed()                            # The game will get the state of all keys
        if keys[pygame.K_SPACE] and self.onGround:                 # If the SPACE is pressed and the player is on the ground
            self.gravityForce = JUMP_FORCE                         # He will suffer a negative gravityForce given by a constant
    
    def gravityApply(self):
        if self.rect.bottom < ground_y_pos:                        # If the player if above the ground
            self.gravityForce += GRAVITY_ACCELERATION              # Gravity will raises by a constant
            self.onGround = False                                  # And the game will be alerted that the player is not on the ground
        if self.rect.bottom >= ground_y_pos and not self.onGround: # If the player touched the ground
            self.gravityForce = 0                                  # The gravitational force will be nullified
            self.onGround = True                                   # And the game will be alerted that the player is on the ground

        if self.rect.bottom + self.gravityForce > ground_y_pos:    # If, in the next frame, the gravity makes the player be below the ground
            self.rect.bottom = ground_y_pos                        # He will not suffer gravityForce and will be teleported to the ground
        else:                                                      # But if not
            self.rect.bottom += self.gravityForce                  # Gravity will work as always
    
    def update(self):
        self.playerAnimation() 
        self.jumpAction()
        self.gravityApply()


# ----------------------------------------- Enemy Class -------------------------------------------

class Enemy(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()
        if type == 'snail':
            snail1 = pygame.image.load("graphics/Snail/snail1.png").convert_alpha()
            snail2 = pygame.image.load("graphics/Snail/snail2.png").convert_alpha()

            self.speed = 0.1
            self.frames = [snail1, snail2]
            posY = ground_y_pos
        elif type == 'fly':
            fly1 = pygame.image.load("graphics/Fly/fly1.png").convert_alpha()
            fly2 = pygame.image.load("graphics/Fly/fly2.png").convert_alpha()

            self.speed = 0.2
            self.frames = [fly1, fly2]
            posY = ground_y_pos - 100
        
        self.index = 0
        self.image = self.frames[self.index]
        self.rect = self.image.get_rect(midbottom = (randint(900, 1200), posY))

        self.onScreen = True
    
    def enemyAnimation(self):
        if self.index < 1.9: self.index += self.speed
        else: self.index = 0

        self.image = self.frames[int(self.index)]
    
    def walk(self):
        global playerScore
        # ========== Score Gain ==========
        if self.rect.right < 0 and self.onScreen:
            self.onScreen = False
            playerScore +=1

        # If the snail is too far it will be removed, else it will move
        elif self.rect.right < -100: self.kill()
        else: self.rect.x -= ENEMY_SPEED
    
    def update(self):
        self.enemyAnimation()
        self.walk()


# Button Class


# ==================== Main Class ====================

class Main:
    def drawLink(self, text:str, pos:tuple, font, defaultColor:tuple, activeColor:tuple = (), link:str = ""):
        notPressed = True

        text_Surface = font.render(text, False, activeColor)
        text_Rectangle = text_Surface.get_rect(center = (pos))

        if text_Rectangle.collidepoint(pygame.mouse.get_pos()) and activeColor != ():
            if pygame.mouse.get_pressed()[0] and notPressed and link != "":
                notPressed = False
                op(link)
            else:
                notPressed = True
        else:
            text_Surface = font.render(text, False, defaultColor)

        screen.blit(text_Surface, text_Rectangle)
    
        
# ---------------------------------------- Quit Function ------------------------------------------
    def quit(self, higherScore, hasPlayed, playerScore):
        with open("data/save.json", "w", encoding="UTF-8") as save:
            save.write(dumps({
            "playerScore":playerScore,
            "higherScore":higherScore,
            "hasPlayed":hasPlayed
        }, indent=4))
            

    def run(self):
# ---------------------------------------- Initialization -----------------------------------------
        pygame.init()

        # ========== General Globals ==========
        global screen, ground_y_pos, playerScore
        
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

        clock = pygame.time.Clock()

        pygame.display.set_caption(GAME_NAME)
        pygame.display.set_icon(pygame.image.load(GAME_ICON).convert_alpha())
        pygame.mouse.set_cursor(pygame.cursors.diamond)


# -------------------------------------------- Events ---------------------------------------------

        # ========== Update FPS Label ==========
        updateFPS = pygame.USEREVENT + 1
        pygame.time.set_timer(updateFPS, 1000)

        spawnEnemy = pygame.USEREVENT + 2
        pygame.time.set_timer(spawnEnemy, SPAWN_RATE)

        # ========== Snail Spawn ==========
        snailTimer = pygame.USEREVENT + 3
        pygame.time.set_timer(snailTimer, SNAIL_ANIMATION_SPEED)


        # ========== Fly Spawn ==========
        flyTimer = pygame.USEREVENT + 4
        pygame.time.set_timer(flyTimer, FLY_ANIMATION_SPEED)


# -------------------------------------- Loading Save File ----------------------------------------

        with open("data/save.json", "r", encoding="UTF-8") as save:
            gameData = loads(save.read())


        # ==================== Variables ====================
        playerScore = gameData["playerScore"]
        higherScore = gameData["higherScore"]
        hasPlayed = gameData["hasPlayed"]
        gameRunning = False
        inLinks = False
        playerOnGround = True
        showFPS = False

        player = pygame.sprite.GroupSingle() 
        enemys = pygame.sprite.Group()
        player.add(Player())
        

# --------------------------------------------- Font ----------------------------------------------

        main_Font = pygame.font.Font("font\Pixeltype.ttf", 50)
        title_Font = pygame.font.Font("font\Pixeltype.ttf", 80)
        small_Font = pygame.font.Font("font\Pixeltype.ttf", 30)


# --------------------------------------------- Color ---------------------------------------------

        limeGreen_Color = (111, 196, 169)
        gray_Color = (64, 64, 64)
        grayBlue_Color = (94, 129, 162)
        skyBlue_Color = (192, 232, 236)


# ------------------------------------------- Surface ---------------------------------------------

        sky_Surface = pygame.image.load("graphics/sky.png").convert()
        skyInverse_Surface = pygame.transform.flip(sky_Surface, flip_x=True, flip_y=False)
        ground_Surface = pygame.image.load("graphics/ground.png").convert()
        groundInverse_Surface = pygame.transform.flip(ground_Surface, flip_x=True, flip_y=False)

        fly_Surface = pygame.image.load("graphics/Fly/fly2.png").convert_alpha()

        playerStand_Surface = pygame.image.load("graphics/Player/player_stand.png").convert_alpha()
        playerStand_Surface = pygame.transform.scale(playerStand_Surface, (170, 210))


# --------------------------------------------- Text ----------------------------------------------

        titleLabel_Surface = title_Font.render("The Runner", False, limeGreen_Color)
        respawnLabel_Surface = main_Font.render("PRESS SPACE", False, gray_Color)
        higherScore_Surface = main_Font.render(f"Higher Score: {higherScore}", False, limeGreen_Color)
        lastScore_Surface = main_Font.render(f"Last Score: {playerScore}", False, gray_Color)
        linksLabel_Surface = small_Font.render("P to Links", False, gray_Color)

        instructionsLabel_Surface = main_Font.render("SPACE or CLICK: Jump", False, gray_Color)
        creditsLabel_Surface = small_Font.render("GitHub: rakRandom | clear-code-projects", False, gray_Color)
        
        score_Surface = main_Font.render("SCORE: 0", False, gray_Color)
        fps_Surface = small_Font.render("FPS: 0", False, "Black")


# ------------------------------------------- Position --------------------------------------------

        sky_x_pos = 0
        ground_x_pos, ground_y_pos = 0, 300
        score_x_pos, score_y_pos = SCREEN_WIDTH/2, 50


# ------------------------------------------ Rectangle --------------------------------------------

        titleLabel_Rectangle = respawnLabel_Surface.get_rect(center = (SCREEN_WIDTH/2 - 40, 50))
        respawnLabel_Rectangle = respawnLabel_Surface.get_rect(center = (SCREEN_WIDTH/2, SCREEN_HEIGHT - 50))
        higherScore_Rectangle = higherScore_Surface.get_rect(midleft = (2, SCREEN_HEIGHT/2 - 20))
        lastScore_Rectangle = lastScore_Surface.get_rect(midleft = (2, SCREEN_HEIGHT/2 + 20))
        linksLabel_Rectangle = linksLabel_Surface.get_rect(midbottom = (SCREEN_WIDTH/2, SCREEN_HEIGHT))

        instructionsLabel_Rectangle = instructionsLabel_Surface.get_rect(midtop = (SCREEN_WIDTH/2, 10))
        creditsLabel_Rectangle = creditsLabel_Surface.get_rect(bottomleft = (2, SCREEN_HEIGHT - 0))

        score_Rectangle = score_Surface.get_rect(center = (score_x_pos, score_y_pos))
        fps_Rectangle = fps_Surface.get_rect(topleft = (1,1))
        playerStand_Rectangle = playerStand_Surface.get_rect(center = (SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
        
        
        while True:
# ------------------------------------- Game Events Handler ---------------------------------------
            for event in pygame.event.get():
                # ========== Quit ==========
                if event.type == pygame.QUIT:
                    self.quit(higherScore, hasPlayed, playerScore)
                    pygame.quit()
                    exit()
                
                # ========== FPS events ==========
                # If is the event is a click and the mouse in over the FPS label rectangle showFPS variable will be toggle
                if event.type == pygame.MOUSEBUTTONDOWN and fps_Rectangle.collidepoint(event.pos): showFPS = False if showFPS else True
                
                # If the event is the updateFPS (1s) and showFPS variable is True, the FPS Surface will be updated
                if event.type == updateFPS and showFPS: fps_Surface = small_Font.render(f"FPS: {clock.get_fps():.0f}", False, "Black")
                
                # ========== GameRunning events ==========
                if gameRunning and event.type == spawnEnemy:
                    if randint(0, 2):
                        # If randint is not 0, will spawn a fly, but if it is, will spawn a snail
                        if not randint(0, FLY_RARITY): enemys.add(Enemy('fly'))
                        else: enemys.add(Enemy('snail'))


                # ========== Menu events ==========
                elif not gameRunning:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE and not inLinks:
                            player.sprite.gravityForce = 0
                            player.sprite.rect.bottom = ground_y_pos
                            
                            playerScore = 0
                            gameRunning = True

                        if event.key == pygame.K_p:
                            inLinks = False if inLinks else True
            
            
            # ==================== Game Running ====================
            if gameRunning:
                # ==================== Showing Environment ====================
                # ========== Background ==========
                screen.blit(sky_Surface, (sky_x_pos, 0))
                screen.blit(skyInverse_Surface, (sky_x_pos + SCREEN_WIDTH, 0))
                screen.blit(sky_Surface, (sky_x_pos + 2 * SCREEN_WIDTH, 0))

                screen.blit(ground_Surface, (ground_x_pos, ground_y_pos))
                screen.blit(groundInverse_Surface, (ground_x_pos + SCREEN_WIDTH, ground_y_pos))
                screen.blit(ground_Surface, (ground_x_pos + 2 * SCREEN_WIDTH, ground_y_pos))

                # ========== Scoreboard ==========
                score_Surface = main_Font.render(f"SCORE: {playerScore}", False, gray_Color)
                score_Rectangle = score_Surface.get_rect(center = (score_x_pos, score_y_pos))
                pygame.draw.rect(screen, skyBlue_Color, score_Rectangle.inflate(15, 15), 0, 10)
                screen.blit(score_Surface, score_Rectangle)


                # ==================== Background Animation ====================

                if sky_x_pos <= -SCREEN_WIDTH * 2: sky_x_pos = 0
                else: sky_x_pos -= ANIMATION_SPEED * BACKGROUND_SPEED
                
                if ground_x_pos <= -SCREEN_WIDTH * 2: ground_x_pos = 0
                else: ground_x_pos -= ANIMATION_SPEED * BACKGROUND_SPEED * 5


                # ==================== Showing Characters ====================

                enemys.draw(screen)
                player.draw(screen)

                enemys.update()
                player.update()


                # ==================== Game Over/Collision Check ====================
                
                if pygame.sprite.spritecollideany(player.sprite, enemys):
                    hasPlayed = True
                    
                    enemys.empty()
                    if playerScore > higherScore: higherScore = playerScore

                    gameRunning = False


            # ==================== Links ====================

            elif inLinks:
                screen.fill(grayBlue_Color)

                if not showFPS:
                    screen.blit(fly_Surface, (10, 10))
                
                screen.blit(creditsLabel_Surface, creditsLabel_Rectangle)
                screen.blit(instructionsLabel_Surface, instructionsLabel_Rectangle)

                self.drawLink("The ultimate introduction to Pygame", (SCREEN_WIDTH/2, SCREEN_HEIGHT/2 - 60), main_Font, gray_Color, limeGreen_Color, "https://www.youtube.com/watch?v=AY9MnQ4x3zk")
                self.drawLink("GitHub Game Repository", (SCREEN_WIDTH/2, SCREEN_HEIGHT/2), main_Font, gray_Color, limeGreen_Color, "https://github.com/rakRandom/Runneer")
                self.drawLink("GitHub Original Repository", (SCREEN_WIDTH/2, SCREEN_HEIGHT/2 + 60), main_Font, gray_Color, limeGreen_Color, "https://github.com/clear-code-projects/UltimatePygameIntro")


            # ==================== Menu ====================

            else:
                screen.fill(grayBlue_Color)

                higherScore_Surface = main_Font.render(f"Higher Score: {higherScore}", False, limeGreen_Color)
                lastScore_Surface = main_Font.render(f"Last Score: {playerScore}", False, gray_Color)


                screen.blit(titleLabel_Surface, titleLabel_Rectangle)
                screen.blit(playerStand_Surface, playerStand_Rectangle)
                screen.blit(respawnLabel_Surface, respawnLabel_Rectangle)
                screen.blit(linksLabel_Surface, linksLabel_Rectangle)

                if hasPlayed:
                    screen.blit(higherScore_Surface, higherScore_Rectangle)
                    screen.blit(lastScore_Surface, lastScore_Rectangle)
            
            if showFPS:
                screen.blit(fps_Surface, fps_Rectangle)


            # ==================== Display update ====================
            pygame.display.update()

            # ==================== Clock tick ====================
            clock.tick(FRAMES_PER_SECOND)


# ------------------------------------------ Execution --------------------------------------------

if __name__ == '__main__':
    main = Main()
    main.run()
else: raise PermissionError("Error 2: __name__ is not '__main__'")
