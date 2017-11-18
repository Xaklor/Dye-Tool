#Dye tool by Xaklor
#you may not delete this comment nor the one above

from PIL import Image, ImageOps
from urllib.request import *
from os import path, makedirs, listdir
from colorsys import rgb_to_hsv, hsv_to_rgb
from random import randint
import pygame, sys
import xml.etree.ElementTree as ET

#crops skin sheets until no more can be found
#takes in PIL.Image, returns list of PIL.Image's
def loadSheets(skins):   
    skinSheets = []
    offset = 0
    loading = True
    count = 0
    while loading:
        skinSheet = skins.crop((0, offset, 56, offset + 24))
        if skinSheet.getbbox() != None:
            skinSheets.append(skinSheet)
            offset += 24

        else:
            loading = False

    return skinSheets

#adds a single pixel wide black outline to the image
#takes in PIL.Image, returns PIL.Image
def addOutline(img):
    width, height = img.size
    copy = img.copy()
    for x in range(width):
        for y in range(height):
            point = img.getpixel((x, y))[3]
            if point == 0:
                try:
                    test1 = img.getpixel((x-1, y-1))[3]
                except:
                    test1 = 0
                try:
                    test2 = img.getpixel((x-1, y))[3]
                except:
                    test2 = 0
                try:
                    test3 = img.getpixel((x-1, y+1))[3]
                except:
                    test3 = 0
                try:
                    test4 = img.getpixel((x, y-1))[3]
                except:
                    test4 = 0
                try:
                    test5 = img.getpixel((x, y+1))[3]
                except:
                    test5 = 0
                try:
                    test6 = img.getpixel((x+1, y-1))[3]
                except:
                    test6 = 0
                try:
                    test7 = img.getpixel((x+1, y))[3]
                except:
                    test7 = 0
                try:
                    test8 = img.getpixel((x+1, y+1))[3]
                except:
                    test8 = 0
                if test1 or test2 or test3 or test4 or test5 or test6 or test7 or test8:
                    copy.putpixel((x, y), (0, 0, 0, 255))

    return copy

#crops out individual frames from the skin sheets and saves them to hard drive
#takes in list of PIL.Image's, returns None
def makeSprites(skinSheets, note=''):
    for i in range(len(skinSheets)):
        filePath = 'sheets/' + str(i) + '/'
        img = skinSheets[i]
        if not path.exists(filePath):
            makedirs(filePath)

        img.save(filePath + note + 'Sheet.png')
        
        #standing side
        temp = img.crop((0, 0, 8, 8))
        temp.save(filePath + note + '0.png')

        #walking side 1
        temp = img.crop((8, 0, 16, 8))
        temp.save(filePath + note + '1.png')

        #walking side 2
        temp = img.crop((16, 0, 24, 8))
        if temp.getbbox() == None:
            temp = img.crop((0, 0, 8, 8))

        temp.save(filePath + note + '2.png')

        #attacking side 1
        temp = img.crop((32, 0, 40, 8))
        temp.save(filePath + note + '3.png')

        #attacking side 2
        temp = img.crop((40, 0, 56, 8))
        temp.save(filePath + note + '4.png')

        #standing front
        temp = img.crop((0, 8, 8, 16))
        temp.save(filePath + note + '5.png')

        #walking front 1
        temp = img.crop((8, 8, 16, 16))
        temp.save(filePath + note + '6.png')

        #walking front 2
        temp = img.crop((16, 8, 24, 16))
        temp.save(filePath + note + '7.png')

        #attacking front 1
        temp = img.crop((32, 8, 40, 16))
        temp.save(filePath + note + '8.png')

        #attacking front 2
        temp = img.crop((40, 8, 56, 16))
        temp.save(filePath + note + '9.png')

        #standing back
        temp = img.crop((0, 16, 8, 24))
        temp.save(filePath + note + '10.png')

        #walking back 1
        temp = img.crop((8, 16, 16, 24))
        temp.save(filePath + note + '11.png')

        #walking back 2
        temp = img.crop((16, 16, 24, 24))
        temp.save(filePath + note + '12.png')

        #attacking back 1
        temp = img.crop((32, 16, 40, 24))
        temp.save(filePath + note + '13.png')

        #attacking back 2
        temp = img.crop((40, 16, 56, 24))
        temp.save(filePath + note + '14.png')

#makes icons from the standing side frame for each skin and saves to hard drive
#takes in list of char folders, returns None
def makeIcons(sheets):
    for i in range(len(sheets)):
        icon = Image.open('sheets/' + str(i) + '/0.png')
        icon = icon.resize((24, 24))
        icon = ImageOps.expand(icon, 1)
        icon = addOutline(icon)
        icon.save('sheets/' + str(i) + '/Icon.png')

#turns the hex string into an rgb tuple
#takes in hex string in the form '0x01XXXXXX', returns 3-tuple
def hex_to_rgb(rgb):
    rgb = rgb[4:]
    red = rgb[0:2]
    green = rgb[2:4]
    blue = rgb[4:]

    red = int(red, 16)
    green = int(green, 16)
    blue = int(blue, 16)
    
    return (red, green, blue)

#creates a list of (name, color) tuples from xml
#takes in xml filepath/filename, returns list of 2-tuples
def loadDyes(xml):
    dyeList = []
    with open(xml) as dyes:
        tree = ET.parse(dyes)
        root = tree.getroot()
        for dye in root:
            for tex in dye.iter('Tex1'):
                color = tex.text
                color = hex_to_rgb(color)
                dyeList.append((dye.attrib['id'], color))

    dyeList.append(('None', (0, 0, 0, 0)))

    return dyeList

#crops out individual cloth patters from the sheet
#takes in PIL.Image and int, returns list of PIL.Image's
def loadCloths(img, size):
    xoffset = 0
    yoffset = 0
    clothList = []
    loading = True
    while loading:
        tex = img.crop((xoffset, yoffset, xoffset + size, yoffset + size))
        if tex.getbbox() == None:
            xoffset = 0
            yoffset += size
            
        else:
            w, h = tex.size
            copy = tex.copy()
            for x in range(w):
                for y in range(h):
                    temp = copy.getpixel((x, y))
                    if temp == (255, 255, 255, 255):
                        copy.putpixel((x, y), (0, 0, 0, 0))

            if copy.getbbox() != None:
                clothList.append(tex)
                xoffset += size

            else:
                loading = False

    return clothList

#expands cloth patterns to fill the space required for pasting
#takes in list of PIL.Image's and int, retuns list of PIL.Image's
def enlargeCloths(cloths, size):
    bigCloths = []
    for i in range(len(cloths)):
        new = Image.new('RGBA', (80, 40))
        w, h = cloths[i].size
        for x in range(80//w + 1):
            for y in range(40//h + 1):
                new.paste(cloths[i], (x * size, y * size))

        bigCloths.append(new)

    return bigCloths

#repeats the two above functions for all 4 types of cloth,
#then saves each pattern to the hard drive in the data/cloths/ directory
def makeCloths():
    cloths44 = Image.open('data/textile4x4.png')
    cloths55 = Image.open('data/textile5x5.png')
    cloths99 = Image.open('data/textile9x9.png')
    cloths1010 = Image.open('data/textile10x10.png')

    list44 = loadCloths(cloths44, 4)
    list55 = loadCloths(cloths55, 5)
    list99 = loadCloths(cloths99, 9)
    list1010 = loadCloths(cloths1010, 10)

    list44 = enlargeCloths(list44, 4)
    list55 = enlargeCloths(list55, 5)
    list99 = enlargeCloths(list99, 9)
    list1010 = enlargeCloths(list1010, 10)

    if not path.exists('data/cloths/4x4'):
        makedirs('data/cloths/4x4')

    for i in range(len(list44)):
        list44[i].save('data/cloths/4x4/' + str(i) + '.png')

    if not path.exists('data/cloths/5x5'):
        makedirs('data/cloths/5x5')

    for i in range(len(list55)):
        list55[i].save('data/cloths/5x5/' + str(i) + '.png')

    if not path.exists('data/cloths/9x9'):
        makedirs('data/cloths/9x9')

    for i in range(len(list99)):
        list99[i].save('data/cloths/9x9/' + str(i) + '.png')

    if not path.exists('data/cloths/10x10'):
        makedirs('data/cloths/10x10')

    for i in range(len(list1010)):
        list1010[i].save('data/cloths/10x10/' + str(i) + '.png')

#loads character and skin sheets, dyes and cloths from static.drips.pw and saves
#it all to the sprites/ and data/ directories
def updateData():        
    print('Loading sheets...')
    
    url = urlopen('http://static.drips.pw/rotmg/production/current/sheets/players.png')
    with open('data/Players.png', 'wb') as f:
        f.write(url.read())
        
    url = urlopen('http://static.drips.pw/rotmg/production/current/sheets/playersMask.png')
    with open('data/PlayersMask.png', 'wb') as f:
        f.write(url.read())
    
    url = urlopen('http://static.drips.pw/rotmg/production/current/sheets/playersSkins.png')
    with open('data/PlayerSkins.png', 'wb') as f:
        f.write(url.read())

    url = urlopen('http://static.drips.pw/rotmg/production/current/sheets/playersSkinsMask.png') 
    with open('data/PlayerSkinsMask.png', 'wb') as f:
        f.write(url.read())

    classes = Image.open('data/Players.png')
    masks1 = Image.open('data/PlayersMask.png')
    skins = Image.open('data/PlayerSkins.png')
    masks2 = Image.open('data/PlayerSkinsMask.png')

    #cutting out the extra iceman skin
    w, h = skins.size
    temp = Image.new('RGBA', (w, h))
    cut = skins.crop((0, 0, w, 2543))
    temp.paste(cut)
    cut = skins.crop((0, 2568, w, h))
    temp.paste(cut, (0, 2544))
    skins = temp

    w, h = masks2.size
    temp = Image.new('RGBA', (w, h))
    cut = masks2.crop((0, 0, w, 2543))
    temp.paste(cut)
    cut = masks2.crop((0, 2568, w, h))
    temp.paste(cut, (0, 2544))
    masks2 = temp

    charSheets = loadSheets(classes)
    charMasks = loadSheets(masks1)
    skinSheets = loadSheets(skins)
    skinMasks = loadSheets(masks2)

    charSheets = charSheets + skinSheets
    charMasks = charMasks + skinMasks

    print('Making sprites...')
    makeSprites(charSheets)
    makeSprites(charMasks, 'Mask')

    print('Making icons...')
    makeIcons(charSheets)

    print('Loading Dyes.xml...')
    url = urlopen('http://static.drips.pw/rotmg/production/current/xml/Dyes.xml')
    with open('data/Dyes.xml', 'wb') as f:
        f.write(url.read())

    print('Loading Cloths...')
    url = urlopen('http://static.drips.pw/rotmg/production/current/sheets/textile4x4.png')
    with open('data/textile4x4.png', 'wb') as f:
        f.write(url.read())

    url = urlopen('http://static.drips.pw/rotmg/production/current/sheets/textile5x5.png')
    with open('data/textile5x5.png', 'wb') as f:
        f.write(url.read())

    url = urlopen('http://static.drips.pw/rotmg/production/current/sheets/textile9x9.png')
    with open('data/textile9x9.png', 'wb') as f:
        f.write(url.read())

    url = urlopen('http://static.drips.pw/rotmg/production/current/sheets/textile10x10.png')
    with open('data/textile10x10.png', 'wb') as f:
        f.write(url.read())

    makeCloths()

    print('Done, please re-launch the application.')
    input('Press enter to close.')

#gets a list of the folders that the skins are in, ~280 numbers
#returns list of int's sorted by number
def loadCharList():
    chars = listdir('sheets/')
    for i in range(len(chars)):
        chars[i] = int(chars[i])

    chars = sorted(chars)
    return chars

#returns a list of two lists, one containing the skins frames
#and the other containg the masks. also resizes the 8x8 sprites into 40x40 sprites
#takes in int, returns list of two lists of PIL.Image's and an ID int
def loadChar(char):
    charSprites = []
    charMasks = []
    for i in range(15):
        charSprites.append(Image.open('sheets/' + str(char) + '/' +str(i) + '.png'))
        charMasks.append(Image.open('sheets/' + str(char) + '/Mask' + str(i) + '.png'))

    for i in range(len(charSprites)):
        w, h = charSprites[i].size
        charSprites[i] = charSprites[i].resize((w*5, h*5))

    for i in range(len(charMasks)):
        w, h = charMasks[i].size
        charMasks[i] = charMasks[i].resize((w*5, h*5))
        
    return [charSprites, charMasks, char]

#loads the large cloth patters into a list
#returns list of PIL.Image's
def loadClothPatterns():
    clothList = []
    list44 = listdir('data/cloths/4x4/')
    for i in range(len(list44)):
        cloth = Image.open('data/cloths/4x4/' + list44[i])
        clothList.append(cloth)

    list55 = listdir('data/cloths/5x5/')
    for i in range(len(list55)):
        cloth = Image.open('data/cloths/5x5/' + list55[i])
        clothList.append(cloth)

    list99 = listdir('data/cloths/9x9/')
    for i in range(len(list99)):
        cloth = Image.open('data/cloths/9x9/' + list99[i])
        clothList.append(cloth)

    list1010 = listdir('data/cloths/10x10/')
    for i in range(len(list1010)):
        cloth = Image.open('data/cloths/10x10/' + list1010[i])
        clothList.append(cloth)

    return clothList

#creates small icons based on the cloth pattern and saves them to data/cloths/icons/
#takes in list of PIL.Image's, returns None
def makeClothIcons(cloths):
    if not path.exists('data/cloths/icons/'):
        makedirs('data/cloths/icons/')

    for i in range(len(cloths)):
        icon = cloths[i].crop((0, 0, 20, 20))
        icon.save('data/cloths/icons/' + str(i) + '.png')

#applies the selected dye to the list of sprites using the selected dye mask.
#if given a 4-tuple, it will assume full transparancy and reset the image with no dye
#takes in loadChar()'s array, 3-tuple, and int that is either 0 or 1
def applyDye(char, dye, mask):
    dyedChar = []
    
    if mask == 0:
        if len(dye) == 4:
            copy = loadChar(char[2])
                   
        for i in range(len(char[0])):
            w, h = char[0][i].size
            for x in range(w):
                for y in range(h):
                    if len(dye) == 3:
                        red, green, blue = dye
                        maskColor = char[1][i].getpixel((x, y))
                        if maskColor[0] != 0:
                            hue, saturation, value = rgb_to_hsv(red, green, blue)
                            value = (maskColor[0]/255) * value
                            red, green, blue = hsv_to_rgb(hue, saturation, value)
                            red = int(red)
                            green = int(green)
                            blue = int(blue)
                            char[0][i].putpixel((x, y), (red, green, blue))

                    elif len(dye) == 4:
                        maskColor = char[1][i].getpixel((x, y))                           
                        if maskColor[0] != 0:
                            color = copy[0][i].getpixel((x, y))
                            char[0][i].putpixel((x, y), color)

            dyedChar.append(char[0][i])

        return [dyedChar, char[1], char[2]]

    elif mask == 1:
        if len(dye) == 4:
            copy = loadChar(char[2])
            
        for i in range(len(char[0])):
            w, h = char[0][i].size
            for x in range(w):
                for y in range(h):
                    if len(dye) == 3:
                        red, green, blue = dye
                        maskColor = char[1][i].getpixel((x, y))
                        if maskColor[1] != 0:
                            hue, saturation, value = rgb_to_hsv(red, green, blue)
                            value = (maskColor[1]/255) * value
                            red, green, blue = hsv_to_rgb(hue, saturation, value)
                            red = int(red)
                            green = int(green)
                            blue = int(blue)
                            char[0][i].putpixel((x, y), (red, green, blue))

                    elif len(dye) == 4:
                        maskColor = char[1][i].getpixel((x, y))                           
                        if maskColor[1] != 0:
                            color = copy[0][i].getpixel((x, y))
                            char[0][i].putpixel((x, y), color)

            dyedChar.append(char[0][i])

        return [dyedChar, char[1], char[2]]

    else:
        return []

#applies the selected cloth pattern to the list of sprites using the selected dye mask
#takes in loadChar()'s array, PIL.Image, and int that is either 0 or 1
def applyCloth(char, cloth, mask):
    MASK = 1
    SPRITE = 0
    shadeMasks = []
    blackMasks = []
    clothChar = []
    if mask == 0:
        for i in range(len(char[MASK])):
            w, h = char[MASK][i].size
            shadeMask = Image.new('RGBA', (w//5, h//5))
            for x in range(w//5):
                for y in range(h//5):
                    temp = char[MASK][i].getpixel((x*5, y*5))
                    if temp[0] == 0:
                        shadeMask.putpixel((x, y), (0, 0, 0, 0))

                    else:
                        shadeMask.putpixel((x, y), (0, 0, 0, temp[0]))

            shadeMask = shadeMask.resize((w, h))
            shadeMasks.append(shadeMask)
                        
        for i in range(len(char[MASK])):
            w, h = char[MASK][i].size
            blackMask = Image.new('RGBA', (w//5, h//5))
            for x in range(w//5):
                for y in range(h//5):
                    temp = char[MASK][i].getpixel((x*5, y*5))
                    if temp[0] > 0:
                        blackMask.putpixel((x, y), (0, 0, 0, 255))

                    else:
                        blackMask.putpixel((x, y), (0, 0, 0, 0))

            blackMask = blackMask.resize((w, h))
            blackMasks.append(blackMask)

        for i in range(len(char[SPRITE])):
            w, h = char[SPRITE][i].size

            tex = cloth.crop((0, 0, w, h))
            temp = char[SPRITE][i].copy()
            
            temp.paste(blackMasks[i])
            temp.paste(tex, None, shadeMasks[i])
            char[SPRITE][i].paste(temp, None, temp)
            clothChar.append(char[SPRITE][i])

        return [clothChar, char[1], char[2]]

    elif mask == 1:
        for i in range(len(char[MASK])):
            w, h = char[MASK][i].size
            shadeMask = Image.new('RGBA', (w//5, h//5))
            for x in range(w//5):
                for y in range(h//5):
                    temp = char[MASK][i].getpixel((x*5, y*5))
                    if temp[1] == 0:
                        shadeMask.putpixel((x, y), (0, 0, 0, 0))

                    else:
                        shadeMask.putpixel((x, y), (0, 0, 0, temp[1]))

            shadeMask = shadeMask.resize((w, h))
            shadeMasks.append(shadeMask)
                        
        for i in range(len(char[MASK])):
            w, h = char[MASK][i].size
            blackMask = Image.new('RGBA', (w//5, h//5))
            for x in range(w//5):
                for y in range(h//5):
                    temp = char[MASK][i].getpixel((x*5, y*5))
                    if temp[1] > 0:
                        blackMask.putpixel((x, y), (0, 0, 0, 255))

                    else:
                        blackMask.putpixel((x, y), (0, 0, 0, 0))

            blackMask = blackMask.resize((w, h))
            blackMasks.append(blackMask)

        for i in range(len(char[SPRITE])):
            w, h = char[SPRITE][i].size

            tex = cloth.crop((0, 0, w, h))
            temp = char[SPRITE][i].copy()
            
            temp.paste(blackMasks[i])
            temp.paste(tex, None, shadeMasks[i])
            char[SPRITE][i].paste(temp, None, temp)
            clothChar.append(char[SPRITE][i])

        return [clothChar, char[1], char[2]]

    else:
        return []

#converts a list of PIL.Image's to pygame.surf's
#takes in list of PIL.Image's and int, returns list of pygame.surf's
def image_to_surf(char, ID):
    if not path.exists('data/temp/'):
        makedirs('data/temp/')

    surfChar = []
    temp = []
    for i in range(len(char)):
        temp.append(None)
        temp[i] = char[i].copy()
        temp[i] = ImageOps.expand(temp[i], 1)
        temp[i] = addOutline(temp[i])
        temp[i].save('data/temp/' + str(i) + '.png')

        surfChar.append(pygame.image.load('data/temp/' + str(i) + '.png'))

    surfChar.append(ID)
    return surfChar
    

#main function displaying interactive dye selection tool
def main():
    #initialization and loading assets
    pygame.init()
    dyes = loadDyes('data/Dyes.xml')
    cloths = loadClothPatterns()
    chars = loadCharList()

    #preparing the screen, font and clock
    displayIcon = pygame.image.load('sheets/' + str(randint(0, 13)) +'/Icon.png')
    pygame.display.set_icon(displayIcon)
    pygame.display.set_caption('Dye Tool')
    
    screen = pygame.display.set_mode((800, 640))
    font = pygame.font.Font('data/comic.ttf', 15)
    clock = pygame.time.Clock()

    #the backdrops against which skins will be displayed
    backdrop = pygame.image.load('data/backdrop.png')
    backdrop2 = pygame.image.load('data/backdrop2.png')

    #the update button
    button = pygame.image.load('data/button.png')
    buttonRect = button.get_rect()
    buttonRect.topleft = (680, 156)

    #the dye palettes you can click on
    dyeIcons = []
    for i in range(len(dyes)):
        temp = pygame.Surface((20, 20))
        temp.fill(dyes[i][1])
        tempRect = temp.get_rect()
        dyeIcons.append((temp, tempRect))

    #the cloth palettes you can click on
    makeClothIcons(cloths)
    clothIcons = []
    for i in range(len(cloths)):
        temp = pygame.image.load('data/cloths/icons/' + str(i) + '.png')
        tempRect = temp.get_rect()
        clothIcons.append((temp, tempRect))

    alphaButton = []
    temp = pygame.image.load('data/alpha.png')
    tempRect = temp.get_rect()
    alphaButton.append((temp, tempRect))

    #the character icons you can click on
    charIcons = loadCharList()
    for i in range(len(charIcons)):
        temp = pygame.image.load('sheets/' + str(charIcons[i]) + '/Icon.png')
        tempRect = temp.get_rect()
        charIcons[i] = (temp, tempRect)

    #the selected character
    currentCharImage = loadChar(0)
    currentCharSurf = image_to_surf(currentCharImage[0], 0)

    #the selected main and secondary dyes/cloths
    currentMain = 'None'
    currentSecond = 'None'

    SPRITE = 0
    RECT = 1

    STILL_SIDE = 0
    WALK_SIDE1 = 1
    WALK_SIDE2 = 2
    ATTACK_SIDE1 = 3
    ATTACK_SIDE2 = 4
    
    STILL_FRONT = 5
    WALK_FRONT1 = 6
    WALK_FRONT2 = 7
    ATTACK_FRONT1 = 8
    ATTACK_FRONT2 = 9

    STILL_BACK = 10
    WALK_BACK1 = 11
    WALK_BACK2 = 12
    ATTACK_BACK1 = 13
    ATTACK_BACK2 = 14

    direction = 'right'
    walking = False
    attacking = False
    currentSprite = STILL_SIDE
    time = 0

    ID = 15
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                mousex, mousey = pygame.mouse.get_pos()
                if buttonRect.collidepoint((mousex, mousey)):
                    pygame.display.quit()
                    updateData()
                    running = False
                
                for i in range(len(dyeIcons)):
                    if dyeIcons[i][RECT].collidepoint((mousex, mousey)):
                        if event.button == 1:
                            currentMain = dyes[i][0]
                            currentCharImage = applyDye(currentCharImage, dyes[i][1], 0)
                            currentCharSurf = image_to_surf(currentCharImage[SPRITE], currentCharSurf[ID])

                        elif event.button == 3:
                            currentSecond = dyes[i][0]
                            currentCharImage = applyDye(currentCharImage, dyes[i][1], 1)
                            currentCharSurf = image_to_surf(currentCharImage[SPRITE], currentCharSurf[ID])

                for i in range(len(clothIcons)):
                    if clothIcons[i][RECT].collidepoint((mousex, mousey)):
                        if event.button == 1:
                            currentMain = 'Large Cloth'
                            currentCharImage = applyCloth(currentCharImage, cloths[i], 0)
                            currentCharSurf = image_to_surf(currentCharImage[SPRITE], currentCharSurf[ID])

                        elif event.button == 3:
                            currentSecond = 'Small Cloth'
                            currentCharImage = applyCloth(currentCharImage, cloths[i], 1)
                            currentCharSurf = image_to_surf(currentCharImage[SPRITE], currentCharSurf[ID])

                if alphaButton[0][RECT].collidepoint((mousex, mousey)):
                    if event.button == 1:
                        currentMain = 'None'
                        currentCharImage = applyDye(currentCharImage, dyes[-1][1], 0)
                        currentCharSurf = image_to_surf(currentCharImage[SPRITE], currentCharSurf[ID])
                    
                    elif event.button == 3:
                        currentSecond = 'None'
                        currentCharImage = applyDye(currentCharImage, dyes[-1][1], 1)
                        currentCharSurf = image_to_surf(currentCharImage[SPRITE], currentCharSurf[ID])

                for i in range(len(charIcons)):
                    if charIcons[i][RECT].collidepoint((mousex, mousey)):
                        if event.button == 1 or event.button == 3:
                            currentCharImage = loadChar(i)
                            currentCharSurf = image_to_surf(currentCharImage[0], i)
                            currentMain = 'None'
                            currentSecond = 'None'

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_d:
                    direction = 'right'
                    walking = True

                elif event.key == pygame.K_s:
                    direction = 'down'
                    walking = True

                elif event.key == pygame.K_a:
                    direction = 'left'
                    walking = True

                elif event.key == pygame.K_w:
                    direction = 'up'
                    walking = True

                elif event.key == pygame.K_SPACE:
                    attacking = True

            if event.type == pygame.KEYUP:                   
                if event.key == pygame.K_SPACE:
                    attacking = False
        try:
            keys = pygame.key.get_pressed()

        except:
            break
        
        if not keys[pygame.K_w] and not keys[pygame.K_a] and not keys[pygame.K_s] and not keys[pygame.K_d]:
            walking = False

        screen.fill((0, 0, 0))

        screen.blit(backdrop, (10, 10))
        screen.blit(backdrop2, (10, 220))
        screen.blit(button, buttonRect)
        
        main = font.render('Current main dye: ' + currentMain, True, (255, 255, 255), (0, 0, 0))
        screen.blit(main, (10, 170))
        secondary = font.render('Current secondary dye: ' + currentSecond, True, (255, 255, 255), (0, 0, 0))
        screen.blit(secondary, (10, 190))
        update = font.render('Update!', True, (255, 255, 255), (85, 85, 85))
        screen.blit(update, (700, 165))

        for i in range(len(dyeIcons)-1):
            remainder = i +1
            x = ((i * 20) % 640) + 150
            y = ((i // 32) * 20) + 10
            dyeIcons[i][RECT].topleft = (x,y)
            screen.blit(dyeIcons[i][SPRITE], dyeIcons[i][RECT])
            pygame.draw.rect(screen, (0, 0, 0), dyeIcons[i][RECT], 1)

        for i in range(len(clothIcons)):
            remainder2 = i +1
            x = (((i + remainder) * 20) % 640) + 150
            y = (((i + remainder) // 32) * 20) + 10
            clothIcons[i][RECT].topleft = (x, y)
            screen.blit(clothIcons[i][SPRITE], clothIcons[i][RECT])
            pygame.draw.rect(screen, (0, 0, 0), clothIcons[i][RECT], 1)

        x = (((remainder + remainder2) * 20) % 640) + 150
        y = (((remainder + remainder2) // 32) * 20) + 10
        alphaButton[0][RECT].topleft = (x, y)
        screen.blit(alphaButton[0][SPRITE], alphaButton[0][RECT])
        pygame.draw.rect(screen, (0, 0, 0), alphaButton[0][RECT], 1)

        for i in range(len(charIcons)):
            x = ((i * 28) % 728) + 35
            y = ((i // 26) * 28) + 240
            charIcons[i][RECT].topleft = (x,y)
            screen.blit(charIcons[i][SPRITE], charIcons[i][RECT])

        if direction == 'right' or direction == 'left':
            if attacking == False:
                if walking == False:
                    currentSprite = STILL_SIDE

                else:
                    temp = (time % 10) - 5
                    if temp >= 0:
                        currentSprite = WALK_SIDE1
                    else:
                        currentSprite = WALK_SIDE2

            else:
                temp = (time % 10) - 5
                if temp >= 0:
                    currentSprite = ATTACK_SIDE1
                else:
                    currentSprite = ATTACK_SIDE2

        if direction == 'up':
            if attacking == False:
                if walking == False:
                    currentSprite = STILL_BACK

                else:
                    temp = (time % 10) - 5
                    if temp >= 0:
                        currentSprite = WALK_BACK1
                    else:
                        currentSprite = WALK_BACK2

            else:
                temp = (time % 10) - 5
                if temp >= 0:
                    currentSprite = ATTACK_BACK1
                else:
                    currentSprite = ATTACK_BACK2

        if direction == 'down':
            if attacking == False:
                if walking == False:
                    currentSprite = STILL_FRONT

                else:
                    temp = (time % 10) - 5
                    if temp >= 0:
                        currentSprite = WALK_FRONT1
                    else:
                        currentSprite = WALK_FRONT2

            else:
                temp = (time % 10) - 5
                if temp >= 0:
                    currentSprite = ATTACK_FRONT1
                else:
                    currentSprite = ATTACK_FRONT2

        if direction != 'left':            
            screen.blit(currentCharSurf[currentSprite], (54, 54))

        else:
            temp = pygame.transform.flip(currentCharSurf[currentSprite], True, False)
            tempRect = temp.get_rect()
            tempRect.topright = (96, 54)
            screen.blit(temp, tempRect)

        pygame.display.update()
        time += 1
        clock.tick(40)

    pygame.quit()
    sys.exit()

if not path.exists('sheets/') or not path.exists('data/cloths/'):
    updateData()

else:
    main()

