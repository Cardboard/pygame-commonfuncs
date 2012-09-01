#############################
#       VERSION .2  (061512)#
#  new in this version:     #
#   -modified Menu.__init__ #
#   -modified Menu.Select   #
#   -added ImageMenu        #
#############################

import pygame #comment out if pygame already imported?
import sys

#Class for handling all text and image input/output
class TextImage:
    #set up colors
    init=0
    BLACK = (0,0,0)
    WHITE = (255,255,255)
    RED = (255,0,0)
    GREEN = (0,255,0)
    BLUE = (0,0,255)
    #setup screensize, font, and update the screen once
    def __init__(self,windowsizex=400,windowsizey=400):
        pygame.init()
        basicFont = pygame.font.SysFont(None, 48)
        self.screenx = pygame.display.Info().current_w
        self.screeny = pygame.display.Info().current_h
        self.screen = pygame.display.set_mode((self.screenx,self.screeny),0, 32)
        self.SetupWindow(windowsizex,windowsizey)
        pygame.display.flip()
    #change the sizex and sizey to change the window size, or caption to change the window's title
    def SetupWindow(self, sizex=400, sizey=400, caption='DEFAULT'):
        screen = pygame.display.set_mode((sizex,sizey), 0 , 32)
        pygame.display.set_caption(caption)
        self.screen.fill(self.WHITE)
        return self.screen
    def AddText(self,text='DEFAULT',x=0,y=0,textsize=14,fillcolor=(255,255,255)):
        font = pygame.font.SysFont('couriernew', textsize)
        fg = self.BLACK
        bg = fillcolor
        text = font.render(text, False, fg, bg)
        textRect = text.get_rect()
        textRect.topleft = (x,y)
        self.screen.blit(text, textRect)
    def AddImage(self, filename, x=0,y=0,COLORKEY=-1):
        imagePos = (x,y)
        image = pygame.image.load('data/' + filename)
        image.set_colorkey(COLORKEY)
        image.set_alpha(255)
        pygame.display.get_surface().blit(image, imagePos)
    def Update(self):
        pygame.display.update()
    def ClearScreen(self,fillcolor=(255,255,255)): #change fillcolor to change the color of the screen after an update
        self.screen.fill(fillcolor)
        pygame.display.flip()
    def Exit(self):
        sys.exit()

#A simple menu
#As of now, what each option does needs to be set up outside the class, in a main loop or something
class Menu:
    def __init__(self,textimage,optionlist=[['empty',(0,0)],['options',(0,14)],['list!',(0,28)]],size=14):
        self.options = optionlist
        self.selected = 0
        self.ti = textimage
        self.size = size
    #move selection either up or down a menu
    def Select(self, direction='update'):
        if direction == 'update':
##            x = 0
##            y = 0
            for option in self.options:
                #get details for each option in the optionlist
                string = option[0]
                xpos = option[1][0]
                ypos = option[1][1]
                
                if option == self.options[self.selected]:
                    self.ti.AddText(string,xpos,ypos,self.size,(255,0,0))
                    ypos += 18
                elif option != self.options[self.selected]:
                    self.ti.AddText(string,xpos,ypos,self.size)
                    ypos += 18
            self.ti.Update()
        if direction == 'down':
            if self.selected < len(self.options) - 1:
                self.selected += 1
                #print('down')
        if direction == 'up':
            if self.selected > 0:
                self.selected -= 1
                #print('up')

class ImageMenu(Menu):
    def __init__(self,textimage,optionlist,OFFSET=0):
        #optionlist = [ [unselected.png, selected.png, (x,y)] , [unselected2.png, selected2.png, (x2,y2)] ... ]
        self.options = optionlist
        self.selected = 0
        self.ti = textimage
        self.imageRects = []
        self.selected = 0
        self.offset = OFFSET
    #run setup if the menu options change size when selected
    def Setup(self,FILL=(0,0,0)):
        self.fill = FILL
        for option in self.options:
            unselectedRect = pygame.image.load('data/' + option[0]).convert().get_rect()
            selectedRect = pygame.image.load('data/' + option[1]).convert().get_rect()
            self.imageRects.append([unselectedRect,selectedRect])
    def Select(self, direction='update'):
        if direction == 'update':
            currentOption = 0
            for option in self.options:
                #get x and y coords for each option in the optionlist
                xpos = option[2][0]
                ypos = option[2][1]
                width_selected = self.imageRects[currentOption][1].width
                unselected = option[0]
                selected = option[1]
                if option == self.options[self.selected]:
                    self.ti.AddImage(selected,xpos-self.offset,ypos)
                elif option != self.options[self.selected]:
                    pygame.draw.rect(pygame.display.get_surface(), self.fill, (xpos-self.offset,ypos,width_selected,ypos))
                    self.ti.AddImage(unselected,xpos,ypos)
                currentOption += 1
            #self.ti.Update()
        if direction == 'down':
            if self.selected < len(self.options) - 1:
                self.selected += 1
        if direction == 'up':
            if self.selected > 0:
                self.selected -= 1
    

#Class for reading and writing text files               
class FileAccess:
    def __init__(self):
        self.string = ''
        self.filename = ''
        self.mode = ''
    #open a file to have operation performed on it
    def OpenFile(self, filename, mode):
        #create a variable to hold the name of the last file opened
        self.filename = filename
        #create a variable to hold the last mode
        self.mode = mode
        #open the user-specified file in the user-specified mode
        self.file = open(filename, mode)
    #end operations on a file
    def CloseFile(self):
        self.file.close()
    #read all lines of a file
    #FILE MUST BE IN A READABLE MODE
    def ReadFile(self):
        self.file.seek(0)
        string = ''
        for line in self.file.readlines():
            string+=line
        print(string)
    #similar to ReadFile, but returns a string
    def ToString(self):
        for line in self.file:
            self.string+=line
        return self.string
    #adds text to the end of a text file if in append/'a' mode. Otherwise, overwrites data
    def AddLine(self, new):
        self.file.write(new)
    #deletes the last line of a file
    def DeleteLine(self,lastline=True):
        if lastline == True:
            self.file.seek(0)
            #create a blank list to hold each line of the file
            linelist = []
            #get each line from the file and add it to a list
            for line in self.file.readlines():
                linelist.append(line)
            #delete last item in the list
            linelist = linelist[0:-1]
            #create a new string to hold all the lines
            string = ''
            #convert the list back into a string
            for line in linelist:
                string += line
            self.file.seek(0)
            #write to the file by closing current mode, opening write mode, closing write mode, then opening read mode
            self.CloseFile()
            self.OpenFile(self.filename,'w')
            self.file.write(string)
            self.CloseFile()
            self.OpenFile(self.filename,'r+')
                        
            
'''
fa = FileAccess()
fa.OpenFile('char1.char','r+')
fa.ReadFile()
'''  
'''
ti=TextImage()
newmenu = Menu(TextImage())
newmenu.Select()
'''

#EXAMPLE
'''
ti = TextImage()
ti.AddText('LOLOLOLOLOLOLOLOLOLOLOLOL',10,30)
ti.Update()
'''
