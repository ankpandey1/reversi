# coding=utf-8

import pygame
from pygame import mixer
import GameSettings
from reversi import *

# initialize pygame
pygame.init()
pygame.display.set_caption("Reversi")  # set the title of the game window
screen_width = 800
screen_height = 700
screen = pygame.display.set_mode((screen_width, screen_height))  # create the game window
titleImage = pygame.image.load('title.png')  # set the title image
font = pygame.font.Font('freesansbold.ttf', 32)  # select the font for the program
bg_music = mixer.Sound("bg_music.wav")  # start the main game music
gameOver = False
pickedMenuItem = False
pickedOptionsItem = False
pickedNewGameItem = False
pickedLoadGameItem = False

gotArrowsPostions = False

languages = ["English", "Svenska"]
GameSettings.readDataFromJSON()  # get all data in JSON format
soundInfo = GameSettings.volume_numbers  # get the sound that was last saved by the user
languageIndex = GameSettings.returnLanguageIndex()  # get the system language
# get the text to display on based on language
hud_names = GameSettings.returnMainMenuTextList(languageIndex)
options = GameSettings.returnOptionsTextList(languageIndex)


class StartMenu:

    def __init__(self):
        self.hud_images = []
        self.hud_rect_info = []
        self.hud_count = 3
        self.hud_number = 0
        self.hud_width = 300
        self.hud_height = 100
        self.pickedMenuItem = False
        self.showTransparentRect = False
        self.setPositionOfHUDItems()

    def setPositionOfHUDItems(self):
        # offset between the game title image and the menu items
        space_between = 300 + 50

        # load the image or sprite for the menu items
        for i in range(self.hud_count):
            self.hud_images.append(pygame.image.load('hud.png'))
            self.hud_images[i] = pygame.transform.scale(self.hud_images[i], (self.hud_width, self.hud_height))

            # set the x and y coordinates of the sprites
            x = (screen_width / 2) - (self.hud_width / 2)
            if i > 0:
                space_between += self.hud_height + 10

            y = space_between

            # save the x and y coordiantes of each menu item
            self.hud_rect_info.append(self.hud_images[i].get_rect(topleft=(x, y)))

    def displayGraphics(self):
        for i in range(self.hud_count):
            # get the x and y coordinates of the menu item
            x = self.hud_rect_info[i].topleft[0]
            y = self.hud_rect_info[i].topleft[1]
            screen.blit(self.hud_images[i], (x, y))
            # place text on the hud items
            hud_text = font.render(hud_names[i], True, (238, 195, 67))
            screen.blit(hud_text, (x + (self.hud_width / 2) - (hud_text.get_width() / 2),
                                   y + (self.hud_height / 2) - (hud_text.get_height() / 2)))

        # display the outline of the hud item
        pygame.draw.rect(screen, (238, 195, 67), [self.hud_rect_info[self.hud_number].topleft[0],
                                                  self.hud_rect_info[self.hud_number].topleft[1],
                                                  self.hud_width, self.hud_height], 5)

    def getUserInput(self):
        global e
        global pickedMenuItem
        global pickedOptionsItem
        global pickedNewGameItem
        global pickedLoadGameItem
        global gameOver

        for e in pygame.event.get():
            # closes the game window
            if e.type == pygame.QUIT:
                gameOver = True
            if e.type == pygame.KEYDOWN:
                # pressed down arrow key
                if e.key == pygame.K_DOWN and self.hud_number < self.hud_count - 1:
                    self.hud_number += 1
                # pressed up arrow key
                if e.key == pygame.K_UP and self.hud_number > 0:
                    self.hud_number -= 1
                # pressed enter
                if e.key == pygame.K_RETURN:
                    pickedMenuItem = True
                    if self.hud_number == 0:
                        pickedLoadGameItem = True
                    elif self.hud_number == 1:
                        pickedNewGameItem = True
                    else:
                        pickedOptionsItem = True
                    self.showTransparentRect = True
            if e.type == pygame.KEYUP:
                if e.key == pygame.K_RETURN:
                    self.showTransparentRect = False

            # mouse control
            for i in range(self.hud_count):
                # check mouse cursor over menu item
                if self.hud_images[i].get_rect(
                        topleft=(self.hud_rect_info[i].topleft[0], self.hud_rect_info[i].topleft[1])).collidepoint(
                    pygame.mouse.get_pos()):
                    self.hud_number = i
                    # right mouse button click causes the following actions based on which menu item was clicked
                    if e.type == pygame.MOUSEBUTTONDOWN:
                        if e.button == 1 and self.hud_number == 0:
                            pickedMenuItem = True
                            pickedLoadGameItem = True

                        if e.button == 1 and self.hud_number == 1:
                            pickedMenuItem = True
                            pickedNewGameItem = True

                        elif e.button == 1 and self.hud_number == 2:
                            pickedMenuItem = True
                            pickedOptionsItem = True


class Options:

    def __init__(self):
        self.option_fonts = []
        self.option_fonts_rect_info = []
        self.arrow_rect_info = []
        self.hud_rect_info = []
        self.foo = []
        bg_music.set_volume(soundInfo[0])
        bg_music.play(-1)
        self.optionNumber = 0
        self.setupPositionOfHUDItems()

    def setupPositionOfHUDItems(self):
        space_between = 350

        for i in range(len(options)):
            # place the x and y coordinates for the options menu items
            self.option_fonts.append(font.render(options[i], True, (238, 195, 67)))
            x = 50
            if i > 0:
                space_between += self.option_fonts[i].get_height() + 30

            y = space_between

            # save their coordinates
            self.option_fonts_rect_info.append(self.option_fonts[i].get_rect(topleft=(x, y)))

            rect = pygame.Surface((500, 50))
            rect.get_rect(topleft=(x, y))
            self.hud_rect_info.append(rect)

    def getUserInput(self):
        global gameOver, e, pickedMenuItem, pickedOptionsItem
        global music_volume, languageIndex

        for e in pygame.event.get():
            # closes the game window
            if e.type == pygame.QUIT:
                gameOver = True
            if e.type == pygame.KEYDOWN:
                # move up or down using KB
                if e.key == pygame.K_DOWN and self.optionNumber < len(options) - 1:
                    self.optionNumber += 1
                elif e.key == pygame.K_UP and self.optionNumber > 0:
                    self.optionNumber -= 1
                if e.key == pygame.K_RETURN and self.optionNumber == len(options) - 1:
                    pickedMenuItem = False
                    self.optionNumber = 0
                # volume control with KB
                if self.optionNumber == 0 or self.optionNumber == 1:
                    # left arrow key pressed
                    if e.key == pygame.K_LEFT and soundInfo[self.optionNumber] > 0:
                        soundInfo[self.optionNumber] -= 10
                    # right arrow key pressed
                    elif e.key == pygame.K_RIGHT and soundInfo[self.optionNumber] < 100:
                        soundInfo[self.optionNumber] += 10
                # language control with KB
                elif self.optionNumber == 2:
                    # left arrow key pressed
                    if e.key == pygame.K_LEFT and languageIndex > 0:
                        languageIndex -= 1
                        self.changeLanguageSettings()
                        changeLanguage()
                        # save this setting to JSON
                        GameSettings.saveDataToJSON(languageIndex, soundInfo[0], soundInfo[1])
                    # right arrow key pressed
                    elif e.key == pygame.K_RIGHT and languageIndex < len(languages) - 1:
                        languageIndex += 1
                        self.changeLanguageSettings()
                        changeLanguage()
                        # save this setting to JSON
                        GameSettings.saveDataToJSON(languageIndex, soundInfo[0], soundInfo[1])
            # volume control with mouse
            if e.type == pygame.MOUSEBUTTONDOWN:
                if e.button == 1:
                    if self.optionNumber == 0 or self.optionNumber == 1:
                        for j in range(len(self.foo)):
                            if self.foo[j].get_rect(topleft=(self.arrow_rect_info[j].topleft[0],
                                                             self.arrow_rect_info[j].topleft[1])).collidepoint(
                                pygame.mouse.get_pos()):
                                if j % 2 == 0 and soundInfo[self.optionNumber] > 0:
                                    soundInfo[self.optionNumber] -= 10
                                elif j % 2 == 1 and soundInfo[self.optionNumber] < 100:
                                    soundInfo[self.optionNumber] += 10
                    # language control with mouse
                    else:
                        for j in range(len(self.foo)):
                            if self.foo[j].get_rect(topleft=(self.arrow_rect_info[j].topleft[0],
                                                             self.arrow_rect_info[j].topleft[1])).collidepoint(
                                pygame.mouse.get_pos()):
                                if j % 2 == 0 and languageIndex > 0:
                                    languageIndex -= 1
                                    self.changeLanguageSettings()
                                    changeLanguage()
                                    GameSettings.saveDataToJSON(languageIndex, soundInfo[0], soundInfo[1])
                                elif j % 2 == 1 and languageIndex < len(languages) - 1:
                                    languageIndex += 1
                                    self.changeLanguageSettings()
                                    changeLanguage()
                                    GameSettings.saveDataToJSON(languageIndex, soundInfo[0], soundInfo[1])

        # if back option is clicked
        for i in range(len(options)):
            if self.hud_rect_info[i].get_rect(
                    topleft=(self.option_fonts_rect_info[i].topleft[0], self.option_fonts_rect_info[i].topleft[1])
            ).collidepoint(pygame.mouse.get_pos()):
                self.optionNumber = i
                if e.type == pygame.MOUSEBUTTONDOWN:
                    if e.button == 1 and self.optionNumber == len(options) - 1:
                        pickedMenuItem = False
                        pickedOptionsItem = False
                        self.optionNumber = 0

        # set the music based on the user's changes
        bg_music.set_volume(soundInfo[0] / 100)

    def changeLanguageSettings(self):
        global hud_names, options
        # poulate these 2 lists based on the system language
        hud_names = GameSettings.returnMainMenuTextList(languageIndex)
        options = GameSettings.returnOptionsTextList(languageIndex)

    def displayGraphics(self):
        skin_height = 12
        triangle_width = 16
        space_between_elements = 30
        global gotArrowsPostions
        self.arrow_rect_info = []

        for i in range(len(options)):
            # display the text for the particular control
            theFont = font.render(options[i], True, (238, 195, 67))
            screen.blit(theFont, (
                self.option_fonts_rect_info[i].topleft[0], self.option_fonts_rect_info[i].topleft[1] + skin_height))

            if i < len(options) - 1:
                # draw the left control arrow
                p1 = (
                    self.option_fonts_rect_info[i].topleft[0] + theFont.get_width() + space_between_elements,
                    self.option_fonts_rect_info[i].topleft[1] + skin_height + theFont.get_height() / 2)
                p2 = (p1[0] + triangle_width, p1[1] - triangle_width)
                p3 = (p1[0] + triangle_width, p1[1] + triangle_width)
                pygame.draw.polygon(screen, (238, 195, 67), [p1, p3, p2])

                # create an invisible rectangle that will be used when the left arrow is clicked
                if not gotArrowsPostions:
                    rect = pygame.Surface((triangle_width, theFont.get_height()))
                    self.foo.append(rect)
                else:
                    rect = pygame.Surface((triangle_width, theFont.get_height()))

                    # save the position of the rectangle
                    self.arrow_rect_info.append(
                        rect.get_rect(topleft=(p1[0], p1[1] - (theFont.get_height() / 2))))

                # place the text to in between the left and right arrows
                if i == 1 or i == 0:
                    control_text = font.render(str(soundInfo[i]) + "%", True, (238, 195, 67))
                else:
                    control_text = font.render(str(languages[languageIndex]), True, (238, 195, 67))

                screen.blit(control_text, (self.option_fonts_rect_info[i].topleft[
                                               0] + theFont.get_width() + triangle_width + space_between_elements + 10,
                                           self.option_fonts_rect_info[i].topleft[1] + skin_height))

                # draw the right control mouse
                p1 = (self.option_fonts_rect_info[i].topleft[
                          0] + theFont.get_width() + space_between_elements + triangle_width + (
                              control_text.get_width() + space_between_elements),
                      self.option_fonts_rect_info[i].topleft[1] + skin_height + theFont.get_height() / 2)
                p2 = (p1[0] - triangle_width, p1[1] + triangle_width)
                p3 = (p1[0] - triangle_width, p1[1] - triangle_width)
                pygame.draw.polygon(screen, (238, 195, 67), [p1, p3, p2])

                # create another invisible rectangle that will be used when the right arrow is clicked
                if not gotArrowsPostions:
                    rect = pygame.Surface((triangle_width, theFont.get_height()))
                    self.foo.append(rect)
                else:
                    rect = pygame.Surface((triangle_width, self.option_fonts[i].get_height()))
                    self.arrow_rect_info.append(
                        rect.get_rect(topleft=(p1[0] - triangle_width, p1[1] - (theFont.get_height() / 2))))

        pygame.draw.rect(screen, (238, 195, 67),
                         [self.option_fonts_rect_info[self.optionNumber].topleft[0],
                          self.option_fonts_rect_info[self.optionNumber].topleft[1],
                          500, 50], 5)

        gotArrowsPostions = True


startMenu = StartMenu()
optionsMenu = Options()


# pickedMenuItem = True


def runGameLoop():
    global pickedNewGameItem, pickedMenuItem, pickedLoadGameItem
    while not gameOver:
        screen.fill((55, 142, 11))
        # place the title image on the screen
        screen.blit(titleImage, (0, 0))

        # if a menu item is selected from the main menu
        if not pickedMenuItem:
            startMenu.getUserInput()
            startMenu.displayGraphics()
        elif pickedOptionsItem:
            optionsMenu.getUserInput()
            optionsMenu.displayGraphics()
        elif pickedLoadGameItem:
            init_pygame()
            board, turn = load_game()

            drawBoard(board)

            while (len(getValidMoves(board, turn)) != 0) or (
                    len(getValidMoves(board, getOpponent(turn))) != 0) and turn != "save":
                turn = makeMoveUsingMouse(board, turn)
                # Recursive call if the user clicks on the new game button
                if turn == "new game":
                    pickedNewGameItem = True
                    pickedLoadGameItem = False
                    runGameLoop()

            pickedLoadGameItem = False
            pickedMenuItem = False

        elif pickedNewGameItem:
            init_pygame()
            board = getNewBoard()
            init_board(board)
            drawBoard(board)

            playerTile, opponentTile = enterPlayerTile()
            turn = playerTile
            while (len(getValidMoves(board, turn)) != 0) or (
                    len(getValidMoves(board, getOpponent(turn))) != 0) and turn != "save":
                turn = makeMoveUsingMouse(board, turn)
                #Recursive call if the user clicks on the new game button
                if turn == "new game":
                    pickedNewGameItem = True
                    runGameLoop()
            winner_dialog(board, turn)
            pickedNewGameItem = False
            pickedMenuItem = False
        pygame.display.update()


runGameLoop()
GameSettings.saveDataToJSON(languageIndex, soundInfo[0], soundInfo[1])
