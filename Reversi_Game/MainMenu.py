import pygame
from pygame import mixer
import GameSettings
import re
import os

pygame.init()
pygame.display.set_caption("Reversi")
screen_width = 800
screen_height = 700
screen = pygame.display.set_mode((screen_width, screen_height))
titleImage = pygame.image.load('title.png')
font = pygame.font.Font('freesansbold.ttf', 32)
bg_music = mixer.Sound("bg_music.wav")
gameOver = False
pickedMenuItem = False
gotArrowsPostions = False

languages = ["English", "Svenska"]
# print(GameSettings.volume_numbers)
GameSettings.readDataFromJSON()
soundInfo = GameSettings.volume_numbers
languageIndex = GameSettings.returnLanguageIndex()
# print(languageIndex)
hud_names = GameSettings.returnMainMenuTextList(languageIndex)
options = GameSettings.returnOptionsTextList(languageIndex)


class NewGame:
    def __init__(self):
        self.textContainer = ""

    def getUserInput(self):
        global gameOver, e

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                gameOver = True
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_RETURN and len(self.textContainer) == 2:
                    self.playVoiceSound(2)
                elif len(self.textContainer) < 2 and e.key != pygame.K_BACKSPACE:
                    self.textContainer += str(pygame.key.name(e.key))
                elif e.key == pygame.K_BACKSPACE and len(self.textContainer) > 0:
                    self.textContainer = self.textContainer[:-1]

    def playVoiceSound(self, playerNumber):
        self.textContainer.lower()
        if re.search('[a-h]', self.textContainer[0]) and re.search('[0-7]', self.textContainer[1]):
            alpha = self.textContainer[0]
            numeric = self.textContainer[1]
            sound_folder_path = os.path.dirname((os.path.realpath(__file__))) + "\Voice\\" + languages[languageIndex]
        else:
            print("Invalid input")
            return

        soundFiles = []
        file_extension = ".wav"
        if playerNumber == 1:
            soundFiles.append(sound_folder_path + "\\" + "player_1" + file_extension)
        else:
            soundFiles.append(sound_folder_path + "\\" + "player_2" + file_extension)

        soundFiles.append(sound_folder_path + "\\" + alpha + file_extension)
        soundFiles.append(sound_folder_path + "\\" + numeric + file_extension)

        for i in range(len(soundFiles)):
            mixer.music.load(soundFiles[i])
            mixer.music.set_volume(soundInfo[1])
            mixer.music.play(0)
            while pygame.mixer.music.get_busy():
                pass
                # print("Playing 'Player 1 to'")
        # print("Current language: " + languages[languageIndex])
        # print(dir_path)
        # print("Voice volume: " + str(soundInfo[1]))

        # for root, dirs, files in os.walk(dir_path):
        #     for file in files:
        #         voice_sound = dir_path + "\\" + file
        #         if "0" in file:
        #             mixer.music.load(voice_sound)
        #             mixer.music.play(0)
        #             while pygame.mixer.music.get_busy():
        #                 print("Playing 'Player 1 to'")

        # print("Done")

    def displayText(self):
        space_between = 300 + 50

        text = font.render("Enter some text: " + self.textContainer, True, ((238, 195, 67)))
        screen.blit(text, (50, space_between + text.get_height() + 30))


class StartMenu:

    def __init__(self):
        self.hud_images = []
        self.hud_rect_info = []
        # self.hud_names = ["Load Game", "New Game", "Options"]
        self.hud_count = 3
        self.hud_number = 1
        self.hud_width = 300
        self.hud_height = 100
        self.pickedMenuItem = False
        self.showTransparentRect = False
        self.setPositionOfHUDItems()

    def setPositionOfHUDItems(self):
        space_between = 300 + 50

        for i in range(self.hud_count):
            self.hud_images.append(pygame.image.load('hud.png'))
            self.hud_images[i] = pygame.transform.scale(self.hud_images[i], (self.hud_width, self.hud_height))

            x = (screen_width / 2) - (self.hud_width / 2)
            if i > 0:
                space_between += self.hud_height + 10

            y = space_between
            self.hud_rect_info.append(self.hud_images[i].get_rect(topleft=(x, y)))

    def displayGraphics(self):
        for i in range(self.hud_count):
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
        # # if a hud item is clicked
        # if self.showTransparentRect:
        #     rect = pygame.Surface((self.hud_width, self.hud_height))
        #     rect.set_alpha(100)
        #     rect.fill((255, 255, 255))
        #     screen.blit(rect, (
        #         self.hud_rect_info[self.hud_number].topleft[0], self.hud_rect_info[self.hud_number].topleft[1]))

    def getUserInput(self):
        global e
        global pickedMenuItem
        global gameOver

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                gameOver = True
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_DOWN and self.hud_number < self.hud_count - 1:
                    self.hud_number += 1
                if e.key == pygame.K_UP and self.hud_number > 0:
                    self.hud_number -= 1
                if e.key == pygame.K_RETURN:
                    pickedMenuItem = True
                    self.showTransparentRect = True
            if e.type == pygame.KEYUP:
                if e.key == pygame.K_RETURN:
                    self.showTransparentRect = False

        for i in range(self.hud_count):
            if self.hud_images[i].get_rect(
                    topleft=(self.hud_rect_info[i].topleft[0], self.hud_rect_info[i].topleft[1])).collidepoint(
                pygame.mouse.get_pos()):
                self.hud_number = i
                if e.type == pygame.MOUSEBUTTONDOWN:
                    if e.button == 1:
                        pickedMenuItem = True
                    # self.showTransparentRect = True
                # elif e.type == pygame.MOUSEBUTTONUP:
                #     self.showTransparentRect = False


class Options:
    def __init__(self):
        # self.options = ["Music Volume", "Voice Volume", "Language", "<<Back"]
        self.option_fonts = []
        self.option_fonts_rect_info = []
        self.arrow_rect_info = []
        self.hud_rect_info = []
        self.foo = []
        # index 0 = music volume, index 1 = voice volume
        # self.soundInfo = [50, 50]
        bg_music.set_volume(soundInfo[0])
        bg_music.play(-1)
        self.optionNumber = 0
        self.setupPositionOfHUDItems()

    def setupPositionOfHUDItems(self):
        space_between = 350
        # self.option_fonts = []
        # self.option_fonts_rect_info = []

        for i in range(len(options)):
            self.option_fonts.append(font.render(options[i], True, (238, 195, 67)))
            x = 50
            if i > 0:
                space_between += self.option_fonts[i].get_height() + 30

            y = space_between
            self.option_fonts_rect_info.append(self.option_fonts[i].get_rect(topleft=(x, y)))

            rect = pygame.Surface((500, 50))
            # screen.blit(rect, (self.option_fonts_rect_info[i].topleft[0], self.option_fonts_rect_info[i].topleft[1]))
            rect.get_rect(topleft=(x, y))
            self.hud_rect_info.append(rect)

    def getUserInput(self):
        global gameOver, e, pickedMenuItem
        global music_volume, languageIndex

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                gameOver = True
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_DOWN and self.optionNumber < len(options) - 1:
                    self.optionNumber += 1
                elif e.key == pygame.K_UP and self.optionNumber > 0:
                    self.optionNumber -= 1
                if e.key == pygame.K_RETURN and self.optionNumber == len(options) - 1:
                    pickedMenuItem = False
                    self.optionNumber = 0
                # volume control with KB
                if self.optionNumber == 0 or self.optionNumber == 1:
                    if e.key == pygame.K_LEFT and soundInfo[self.optionNumber] > 0:
                        soundInfo[self.optionNumber] -= 10
                    elif e.key == pygame.K_RIGHT and soundInfo[self.optionNumber] < 100:
                        soundInfo[self.optionNumber] += 10
                # language control with KB
                elif self.optionNumber == 2:
                    if e.key == pygame.K_LEFT and languageIndex > 0:
                        languageIndex -= 1
                        self.changeLanguageSettings()
                    elif e.key == pygame.K_RIGHT and languageIndex < len(languages) - 1:
                        languageIndex += 1
                        self.changeLanguageSettings()
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
                                elif j % 2 == 1 and languageIndex < len(languages) - 1:
                                    languageIndex += 1
                                    self.changeLanguageSettings()

        for i in range(len(options)):
            if self.hud_rect_info[i].get_rect(
                    topleft=(self.option_fonts_rect_info[i].topleft[0], self.option_fonts_rect_info[i].topleft[1])
            ).collidepoint(pygame.mouse.get_pos()):
                self.optionNumber = i
                if e.type == pygame.MOUSEBUTTONDOWN:
                    if e.button == 1 and self.optionNumber == len(options) - 1:
                        pickedMenuItem = False
                        self.optionNumber = 0

        bg_music.set_volume(soundInfo[0] / 100)

    def changeLanguageSettings(self):
        global hud_names, options
        hud_names = GameSettings.returnMainMenuTextList(languageIndex)
        options = GameSettings.returnOptionsTextList(languageIndex)
        # self.setupPositionOfHUDItems()
        # self.option_fonts = []
        # for i in range(len(options)):
        #     self.option_fonts.append(font.render(options[i], True, (238, 195, 67)))

    def displayGraphics(self):
        skin_height = 12
        triangle_width = 16
        space_between_elements = 30
        global gotArrowsPostions
        # rect = None
        self.arrow_rect_info = []

        for i in range(len(options)):
            theFont = font.render(options[i], True, (238, 195, 67))
            screen.blit(theFont, (
                self.option_fonts_rect_info[i].topleft[0], self.option_fonts_rect_info[i].topleft[1] + skin_height))

            if i < len(options) - 1:
                # left control arrow
                p1 = (
                    self.option_fonts_rect_info[i].topleft[0] + theFont.get_width() + space_between_elements,
                    self.option_fonts_rect_info[i].topleft[1] + skin_height + theFont.get_height() / 2)
                p2 = (p1[0] + triangle_width, p1[1] - triangle_width)
                p3 = (p1[0] + triangle_width, p1[1] + triangle_width)
                pygame.draw.polygon(screen, (238, 195, 67), [p1, p3, p2])

                if not gotArrowsPostions:
                    rect = pygame.Surface((triangle_width, theFont.get_height()))
                    self.foo.append(rect)
                    # # rect.set_alpha(0)
                    # rect.fill((255, 255, 255))
                    # screen.blit(rect, (p1[0], p1[1] - self.option_fonts[i].get_height() / 2))
                    # self.arrow_rect_info.append(
                    #     rect.get_rect(topleft=(p1[0], p1[1] - theFont.get_height() / 2)))
                else:
                    rect = pygame.Surface((triangle_width, theFont.get_height()))
                    # rect.fill((255, 255, 255))
                    # screen.blit(rect, (p1[0], p1[1] - theFont.get_height() / 2))
                    self.arrow_rect_info.append(
                        rect.get_rect(topleft=(p1[0], p1[1] - (theFont.get_height() / 2))))
                    # print(str(len(self.arrow_rect_info)))
                    # for j in range(len(self.arrow_rect_info)):
                    #     print(self.arrow_rect_info[j])
                    #     # if j % 2 == 0:
                    #     #     self.arrow_rect_info[j][0] = p1[0]
                    #     # self.arrow_rect_info[j][1] = p1[1] - theFont.get_height() / 2

                if i == 1 or i == 0:
                    control_text = font.render(str(soundInfo[i]) + "%", True, (238, 195, 67))
                else:
                    control_text = font.render(str(languages[languageIndex]), True, (238, 195, 67))

                screen.blit(control_text, (self.option_fonts_rect_info[i].topleft[
                                               0] + theFont.get_width() + triangle_width + space_between_elements + 10,
                                           self.option_fonts_rect_info[i].topleft[1] + skin_height))

                p1 = (self.option_fonts_rect_info[i].topleft[
                          0] + theFont.get_width() + space_between_elements + triangle_width + (
                              control_text.get_width() + space_between_elements),
                      self.option_fonts_rect_info[i].topleft[1] + skin_height + theFont.get_height() / 2)
                p2 = (p1[0] - triangle_width, p1[1] + triangle_width)
                p3 = (p1[0] - triangle_width, p1[1] - triangle_width)
                pygame.draw.polygon(screen, (238, 195, 67), [p1, p3, p2])

                # print(control_text.get_width())

                # screen.blit(rect, (p1[0] - triangle_width, p1[1] - self.option_fonts[i].get_height() / 2))
                # right control arrow
                if not gotArrowsPostions:
                    rect = pygame.Surface((triangle_width, theFont.get_height()))
                    self.foo.append(rect)
                    # self.arrow_rect_info.append(
                    #     rect.get_rect(topleft=(p1[0] - triangle_width, p1[1] - (theFont.get_height() / 2))))
                else:
                    # self.arrow_rect_info = []
                    rect = pygame.Surface((triangle_width, self.option_fonts[i].get_height()))
                    # rect.fill((255, 255, 255))
                    # screen.blit(rect, (p1[0] - triangle_width, p1[1] - theFont.get_height() / 2))
                    # for j in range(len(self.arrow_rect_info)):
                    #     if j % 2 == 1:
                    #         self.arrow_rect_info[j][0] = p1[0] - triangle_width
                    self.arrow_rect_info.append(
                        rect.get_rect(topleft=(p1[0] - triangle_width, p1[1] - (theFont.get_height() / 2))))

        pygame.draw.rect(screen, (238, 195, 67),
                         [self.option_fonts_rect_info[self.optionNumber].topleft[0],
                          self.option_fonts_rect_info[self.optionNumber].topleft[1],
                          500, 50], 5)

        gotArrowsPostions = True


startMenu = StartMenu()
optionsMenu = Options()
newGame = NewGame()

pickedMenuItem = True


def runGameLoop():
    global gameOver

    while not gameOver:
        screen.fill((55, 142, 11))
        # place the title image on the screen
        screen.blit(titleImage, (0, 0))

        if not pickedMenuItem:
            startMenu.getUserInput()
            startMenu.displayGraphics()
        else:
            if startMenu.hud_number == 0:
                gameOver = True
            elif startMenu.hud_number == 1:
                newGame.getUserInput()
                newGame.displayText()
            else:
                optionsMenu.getUserInput()
                optionsMenu.displayGraphics()

        pygame.display.update()


runGameLoop()
GameSettings.saveDataToJSON(languageIndex, soundInfo[0], soundInfo[1])
