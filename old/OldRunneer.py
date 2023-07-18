"""Objetivo:
Treinamento do módulo pygame, com a criação de um jogo do tipo endless runner
chamado "Runneer", usando como referência e auxílio o vídeo "The ultimate introduction to Pygame"¹

- Versão desatualizada

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


# ==================== Import ====================

try:
    from data.settings import *
except: raise ImportError("Error 1: Cannot import settings module")


# ==================== Main Class ====================
class Main:
    def drawButton(self, text:str, pos:tuple, font, defaultColor:tuple, activeColor:tuple = (), link:str = ""):
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


    def checkCollision(self, mainRect, rectList):
        if rectList:
            for rect in rectList:
                if mainRect.colliderect(rect): return True
        return False


    def drawEnemy(self, enemyList, snail_Surface, fly_Surface):
        if enemyList:
            for enemy in enemyList:
                enemy.x -= enemySpeed / FRAMES_PER_SECOND

                if enemy.bottom == ground_y_pos:
                    screen.blit(snail_Surface, enemy)
                else:
                    screen.blit(fly_Surface, enemy)
            
            return enemyList
        else:
            return []
        

    def quit(self, higherScore, hasPlayed, playerScore):
        with open("data/save.json", "w", encoding="UTF-8") as save:
            save.write(dumps({
            "playerScore":playerScore,
            "higherScore":higherScore,
            "hasPlayed":hasPlayed,
            "difficulty": 1,
            "enemySpeed": 350
        }, indent=4))
            

    def run(self):
        # ==================== Initialization ====================
        pygame.init()

        # ========== General Globals ==========
        global screen, ground_y_pos, enemySpeed

        # ========== Player Globals ==========
        global player_Surface, playerIndex, walkState

        # Snail Globals
        global snail_Surface, snailIndex

        # ========== Fly Globals ==========
        global fly_Surface, flyIndex

        
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

        clock = pygame.time.Clock()

        pygame.display.set_caption(GAME_NAME)
        pygame.display.set_icon(pygame.image.load(GAME_ICON).convert_alpha())
        pygame.mouse.set_cursor(pygame.cursors.diamond)

        updateFPS = pygame.USEREVENT + 1
        pygame.time.set_timer(updateFPS, 1000)

        spawnEnemy = pygame.USEREVENT + 2
        pygame.time.set_timer(spawnEnemy, SPAWN_RATE)

        with open("data/save.json", "r", encoding="UTF-8") as save:
            gameData = loads(save.read())


        # ==================== Variables ====================
        playerScore = gameData["playerScore"]
        higherScore = gameData["higherScore"]
        hasPlayed = gameData["hasPlayed"]
        enemySpeed = gameData["enemySpeed"]
        playerGravity = 0
        gameRunning = False
        inLinks = False
        playerOnGround = True
        showFPS = False
        enemyList = []


        # ==================== Player Animation ====================
        playerWalk1_Surface = pygame.image.load("graphics/Player/player_walk_1.png").convert_alpha()
        playerWalk2_Surface = pygame.image.load("graphics/Player/player_walk_2.png").convert_alpha()
        playerJump_Surface = pygame.image.load("graphics/Player/jump.png").convert_alpha()

        playerWalk = [playerWalk1_Surface, playerWalk2_Surface]
 
        playerIndex = 0

        player_Surface = playerWalk[playerIndex]
        player_Rectangle = player_Surface.get_rect(midbottom = (80, 300))

        def playerAnimation():
            global playerIndex, player_Surface, walkState

            player_Surface = playerWalk[int(playerIndex)]
            if playerOnGround:
                screen.blit(player_Surface, player_Rectangle)
                
                if playerIndex <= 0.1: walkState = 0
                elif playerIndex >= 1.9: walkState = 1

                playerIndex += ANIMATION_SPEED if walkState == 0 else -ANIMATION_SPEED
            else:
                screen.blit(playerJump_Surface, player_Rectangle)


        playerStand_Surface = pygame.image.load("graphics/Player/player_stand.png").convert_alpha()
        playerStand_Surface = pygame.transform.scale(playerStand_Surface, (170, 210))
        

        # ==================== Enemy Animation ====================
        # ========== Snail ==========
        snailWalk1_Surface = pygame.image.load("graphics/Snail/snail1.png").convert_alpha()
        snailWalk2_Surface = pygame.image.load("graphics/Snail/snail2.png").convert_alpha()

        snailWalk = [snailWalk1_Surface, snailWalk2_Surface]
        snailIndex = 0

        snail_Surface = snailWalk[snailIndex]

        snailTimer = pygame.USEREVENT + 3
        pygame.time.set_timer(snailTimer, SNAIL_ANIMATION_SPEED)


        # ========== Fly ==========
        flyWalk1_Surface = pygame.image.load("graphics/Fly/fly1.png").convert_alpha()
        flyWalk2_Surface = pygame.image.load("graphics/Fly/fly2.png").convert_alpha()

        flyWalk = [flyWalk1_Surface, flyWalk2_Surface]
        flyIndex = 0

        fly_Surface = flyWalk[flyIndex]

        flyTimer = pygame.USEREVENT + 4
        pygame.time.set_timer(flyTimer, FLY_ANIMATION_SPEED)


        # ==================== Font ====================
        main_Font = pygame.font.Font("font\Pixeltype.ttf", 50)
        title_Font = pygame.font.Font("font\Pixeltype.ttf", 80)
        small_Font = pygame.font.Font("font\Pixeltype.ttf", 30)


        # ==================== Surface ====================
        sky_Surface = pygame.image.load("graphics/sky.png").convert()
        skyInverse_Surface = pygame.transform.flip(sky_Surface, flip_x=True, flip_y=False)
        ground_Surface = pygame.image.load("graphics/ground.png").convert()
        groundInverse_Surface = pygame.transform.flip(ground_Surface, flip_x=True, flip_y=False)


        # ==================== Text ====================
        titleLabel_Surface = title_Font.render("The Runner", False, (111, 196, 169))
        respawnLabel_Surface = main_Font.render("PRESS SPACE", False, (64, 64, 64))
        higherScore_Surface = main_Font.render(f"Higher Score: {higherScore}", False, (111, 196, 169))
        lastScore_Surface = main_Font.render(f"Last Score: {playerScore}", False, (64, 64, 64))
        linksLabel_Surface = small_Font.render("P to Links", False, (64, 64, 64))

        instructionsLabel_Surface = main_Font.render("SPACE or CLICK: Jump", False, (64, 64, 64))
        creditsLabel_Surface = small_Font.render("GitHub: rakRandom | clear-code-projects", False, (64, 64, 64))
        
        score_Surface = main_Font.render("SCORE: 0", False, (64, 64, 64))
        fps_Surface = small_Font.render("FPS: 0", False, "Black")


        # ==================== Position ====================
        sky_x_pos = 0
        ground_x_pos, ground_y_pos = 0, 300
        score_x_pos, score_y_pos = SCREEN_WIDTH/2, 50


        # ==================== Rectangle ====================
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
            # ==================== Event Handler ====================
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit(higherScore, hasPlayed, playerScore)
                    pygame.quit()
                    exit()
                
                # ========== FPS events ==========
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if fps_Rectangle.collidepoint(event.pos):
                        showFPS = False if showFPS else True
                if event.type == updateFPS and showFPS:
                    fps_Surface = small_Font.render(f"FPS: {clock.get_fps():.0f}", False, "Black")
                
                # ========== GameRunning events ==========
                if gameRunning:
                    if event.type == pygame.MOUSEBUTTONDOWN and playerOnGround:
                        playerGravity = JUMP_FORCE
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and playerOnGround:
                        playerGravity = JUMP_FORCE

                    if event.type == spawnEnemy:
                        if randint(0, 2):
                            if randint(0, FLY_RARITY):
                                enemyList.append(snail_Surface.get_rect(midbottom = (randint(900, 1200), ground_y_pos)))
                            else:
                                enemyList.append(fly_Surface.get_rect(midbottom = (randint(900, 1200), ground_y_pos - 90)))

                    if event.type == snailTimer:
                        snailIndex = 0 if snailIndex == 1 else 1

                        snail_Surface = snailWalk[snailIndex]

                    if event.type == flyTimer:
                        flyIndex = 0 if flyIndex == 1 else 1

                        fly_Surface = flyWalk[flyIndex]

                # ========== Menu events ==========
                else:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            playerGravity = 0
                            player_Rectangle.bottom = ground_y_pos
                            
                            playerScore = 0
                            score_Surface = main_Font.render(f"SCORE: {playerScore}", False, (64, 64, 64))

                            gameRunning = True
                        if event.key == pygame.K_p:
                            inLinks = False if inLinks else True
            
            
            # ==================== Game Running ====================
            if gameRunning:
                # ==================== Snail/Score Mechanics ====================
                for enemy in enemyList:
                    if enemy.x < -100:
                        enemyList.remove(enemy)
                        
                        playerScore += 1
                        score_Surface = main_Font.render(f"SCORE: {playerScore}", False, (64, 64, 64))
                        score_Rectangle = score_Surface.get_rect(center = (score_x_pos, score_y_pos))


                # ==================== Gravity ====================
                if player_Rectangle.bottom < ground_y_pos:
                    playerGravity += GRAVITY_ACCELERATION
                    playerOnGround = False
                if player_Rectangle.bottom >= ground_y_pos and not playerOnGround:
                    playerGravity = 0
                    playerOnGround = True

                if player_Rectangle.bottom + playerGravity > ground_y_pos:
                    player_Rectangle.bottom = ground_y_pos
                else:
                    player_Rectangle.bottom += playerGravity


                # ==================== Showing Surface ====================
                screen.blit(sky_Surface, (sky_x_pos, 0))
                screen.blit(skyInverse_Surface, (sky_x_pos + SCREEN_WIDTH, 0))
                screen.blit(sky_Surface, (sky_x_pos + 2 * SCREEN_WIDTH, 0))

                screen.blit(ground_Surface, (ground_x_pos, ground_y_pos))
                screen.blit(groundInverse_Surface, (ground_x_pos + SCREEN_WIDTH, ground_y_pos))
                screen.blit(ground_Surface, (ground_x_pos + 2 * SCREEN_WIDTH, ground_y_pos))

                pygame.draw.rect(screen, "#c0e8ec", score_Rectangle.inflate(15, 15), 0, 10)
                screen.blit(score_Surface, score_Rectangle)

                enemyList = self.drawEnemy(enemyList, snail_Surface, fly_Surface)
                playerAnimation()


                # ==================== Pos-Functionalities ====================

                if sky_x_pos <= -SCREEN_WIDTH * 2: sky_x_pos = 0
                else: sky_x_pos -= ANIMATION_SPEED * BACKGROUND_SPEED
                
                if ground_x_pos <= -SCREEN_WIDTH * 2: ground_x_pos = 0
                else: ground_x_pos -= ANIMATION_SPEED * BACKGROUND_SPEED * 5

                if self.checkCollision(player_Rectangle, enemyList):
                    hasPlayed = True
                    
                    enemyList.clear()
                    if playerScore > higherScore: higherScore = playerScore

                    gameRunning = False


            # ==================== Options ====================
            elif inLinks:
                screen.fill((94, 129, 162))

                if not showFPS:
                    screen.blit(fly_Surface, (10, 10))
                
                screen.blit(creditsLabel_Surface, creditsLabel_Rectangle)
                screen.blit(instructionsLabel_Surface, instructionsLabel_Rectangle)

                self.drawButton("The ultimate introduction to Pygame", (SCREEN_WIDTH/2, SCREEN_HEIGHT/2 - 60), main_Font, (64, 64, 64), (111, 196, 169), "https://www.youtube.com/watch?v=AY9MnQ4x3zk")
                self.drawButton("GitHub Game Repository", (SCREEN_WIDTH/2, SCREEN_HEIGHT/2), main_Font, (64, 64, 64), (111, 196, 169), "https://github.com/rakRandom/Runneer")
                self.drawButton("GitHub Original Repository", (SCREEN_WIDTH/2, SCREEN_HEIGHT/2 + 60), main_Font, (64, 64, 64), (111, 196, 169), "https://github.com/clear-code-projects/UltimatePygameIntro")


            # ==================== Menu ====================
            else:
                screen.fill((94, 129, 162))

                higherScore_Surface = main_Font.render(f"Higher Score: {higherScore}", False, (111, 196, 169))
                lastScore_Surface = main_Font.render(f"Last Score: {playerScore}", False, (64, 64, 64))


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


# ==================== Execution ====================
if __name__ == '__main__':
    main = Main()
    main.run()
else: raise PermissionError("Error 2: __name__ is not '__main__'")
