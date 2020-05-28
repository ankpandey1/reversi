import json

# people_string = '''
# {
#     "language index" : "1",
#     "music volume" : "50",
#     "voice volume" : "50",
#     "language text":[
#     {
#         "hud text": ["Load Game", "New Game", "Options"],
#         "options text": ["Music Volume", "Voice Volume", "Language", "<<Back"]
#     },
#     {
#         "hud text": ["Lastspel", "Nytt Spel", "Alternativ"],
#         "options text": ["Musikvolym", "Röstvolym", "Språk", "<<Tillbaka"]
#     }
#     ]
# }
# '''

data = {}
volume_numbers = []


# print(type(data['language text'][0]))
# print(data['language text'][0]['hud text'])

# language_index = int(data['language index'])
#
# hud_names = data['language text'][language_index]['hud text']
# options = data['language text'][language_index]['options text']
# for i in range(len(hud_names)):
#     print(hud_names[i])
#
# for i in range(len(options)):
#     print(options[i])

def saveDataToJSON(languageIndex, music_volume, voice_volume):
    global data
    data['language index'] = languageIndex
    data['music volume'] = music_volume
    data['voice volume'] = voice_volume
    with open('game_settings.json', 'w') as outfile:
        json.dump(data, outfile)


# saveDataToJSON()

def readDataFromJSON():
    global data
    with open('game_settings.json') as json_file:
        data = json.load(json_file)

    volume_numbers.append(data['music volume'])
    volume_numbers.append(data['voice volume'])
    # print(data)


# def changeSomeJSONData(language_index):
#     global data
#     data['language index'] = language_index
#     print(data['language index'])

def returnLanguageIndex():
    return data['language index']


def returnMainMenuTextList(language_index):
    return data['language text'][language_index]['hud text']


def returnOptionsTextList(language_index):
    return data['language text'][language_index]['options text']

def returnBoardTextList(language_index):
    return data['language text'][language_index]['board text']

# readDataFromJSON()
# changeSomeJSONData(22)
# saveDataToJSON()
