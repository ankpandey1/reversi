# coding=utf-8

import json

data = {}
volume_numbers = []


# saves settings information into the json file
# these changes will show up on startup
def saveDataToJSON(languageIndex, music_volume, voice_volume):
    global data
    data['language index'] = languageIndex  # system language
    data['music volume'] = music_volume  # system music volume
    data['voice volume'] = voice_volume  # system voice volume
    # write data to the JSON file
    with open('game_settings.json', 'w') as outfile:
        json.dump(data, outfile)


def readDataFromJSON():
    global data
    # get all data from the JSON file
    with open('game_settings.json') as json_file:
        data = json.load(json_file)

    # return the volume for music and voice
    volume_numbers.append(data['music volume'])
    volume_numbers.append(data['voice volume'])


def returnLanguageIndex():
    return data['language index']


# get the text that will be displayed on the main menu's menu items
def returnMainMenuTextList(language_index):
    return data['language text'][language_index]['hud text']


# get the text that will be displayed for particular options
def returnOptionsTextList(language_index):
    return data['language text'][language_index]['options text']


def returnBoardTextList(language_index):
    return data['language text'][language_index]['board text']
