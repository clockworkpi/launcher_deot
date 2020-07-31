# -*- coding: utf-8 -*-

import pygame
from pygame.locals import *
from sys import exit
import os
import sys
import math
import fnmatch
import random
import time

from libs import easing

# import base64
# from beeprint import pp

# local import
from constants import ALIGN, icon_width, icon_height, Width, Height, ICON_TYPES
from util_funcs import midRect,FileExists
from keys_def import CurKeys, IsKeyStartOrA, IsKeyMenuOrB
from icon_pool import MyIconPool
from lang_manager import MyLangManager
from skin_manager import MySkinManager
from widget import Widget
import config

class PageStack:
    def __init__(self):
        self.stack = list()

    def Push(self, data):
        if data not in self.stack:
            self.stack.append(data)
            return True
        return False

    def Pop(self):
        if len(self.stack) <= 0:
            return None, False
        return self.stack.pop(), True

    def Length(self):
        return len(self.stack)


class PageSelector(Widget):

    _Parent = None
    _Alpha = 0
    _OnShow = True
    _IconSurf = None

    def __init__(self):
        pass

    def Init(self, x, y, w, h, alpha):
        self._PosX = x
        self._PosY = y
        self._Width = w
        self._Height = h
        self._Alpha = alpha

    def Adjust(self, x, y, w, h, alpha):
        self._PosX = x
        self._PosY = y
        self._Width = w
        self._Height = h
        self._Alpha = alpha

    def Draw(self):
        canvas = self._Parent._CanvasHWND
        idx = self._Parent._PsIndex
        iconidx = self._Parent._IconIndex

        if idx < len(self._Parent._Icons):
            x = self._Parent._Icons[idx]._PosX+self._Parent._PosX
            # only use current icon's PosY
            y = self._Parent._Icons[iconidx]._PosY

            rect = midRect(x, y, self._Width, self._Height,
                           self._Parent._Width, self._Parent._Height)
            if rect.width <= 0 or rect.height <= 0:
                return

            # color = (244,197,66,50)
            # pygame.draw.rect(canvas,color,rect,1)
            if self._IconSurf != None:
                self._Parent._CanvasHWND.blit(self._IconSurf, rect)


class Page(Widget):
    _Icons = []
    _Ps = None
    _PsIndex = 0
    _IconNumbers = 0
    _IconIndex = 0  # shows which icon current selected, the Selector can not move here
    _PrevIconIndex = 0  # for remember the  Highlighted Icon ,restore it's PosY to average
    _Index = 0
    _Align = ALIGN["SLeft"]
    _CanvasHWND = None
    _HWND = None
    _OnShow = False
    _Name = ""
    _Screen = None  # Should be the Screen Class
    _PageIconMargin = 20
    _FootMsg = ["Nav", "", "", "", "Enter"]  # Default Page Foot info
    _Wallpaper = None
    _SelectedIconTopOffset = 20
    _EasingDur = 30
    _Padding = pygame.Rect(0, 0, 0, 0)  # x,y,w,h
    _Margin = pygame.Rect(0, 0, 0, 0)
    _ScrollStep = 1
    _Scrolled = 0
    _ItemsPerPage = 6

    def __init__(self):
        self._Icons = []
        ## so every theme can have a background.png for displaying as the background of the launcher,except the topbar and footbar
        ## https://forum.clockworkpi.com/t/give-your-gs-a-custom-wallpaper/3724
        bg_img_path = config.SKIN+"/background.png"

        if FileExists(bg_img_path):
            self._Wallpaper = pygame.transform.scale(pygame.image.load(bg_img_path).convert(), (320,240))  
        
    def AdjustHLeftAlign(self): ## adjust coordinator and append the PageSelector
        self._PosX = self._Index*self._Screen._Width
        self._Width = self._Screen._Width
        self._Height = self._Screen._Height
        
        cols = int(Width /icon_width)
        rows = int( (self._IconNumbers * icon_width)/Width + 1)
        if rows < 1:
            rows = 1

        cnt = 0

        for i in range(0,rows):
            for j in range(0,cols):
                start_x = icon_width/2  + j*icon_width
                start_y = icon_height/2 + i*icon_height
                icon = self._Icons[cnt]
                icon.Adjust(start_x,start_y,icon_width-4,icon_height-4,0)
                icon._Index = cnt
                icon._Parent = self
                if cnt >= (self._IconNumbers -1):
                    break
                cnt+=1
        
        ps = PageSelector()
        ps._IconSurf = MyIconPool.GiveIconSurface("blueselector")
        ps._Parent = self
        ps.Init(icon_width/2, TitleBar._BarHeight+icon_height/2,92,92,128)
        self._Ps = ps
        self._PsIndex = 0
        self._OnShow = False


    def AdjustSLeftAlign(self): ## adjust coordinator and append the PageSelector
        self._PosX = self._Index*self._Screen._Width
        self._Width = self._Screen._Width
        self._Height = self._Screen._Height
        
        start_x = (self._PageIconMargin + icon_width+self._PageIconMargin) /2
        start_y = self._Height/2
        
        for i in range(0,self._IconNumbers):
            it = self._Icons[i]
            it._Parent = self
            it._Index = i
            it.Adjust(start_x+i*self._PageIconMargin+i*icon_width,start_y,icon_width-6,icon_height-6,0)
            it._ImgSurf = pygame.transform.smoothscale(it._ImgSurf,(it._Width,it._Height))

        ps = PageSelector()
        ps._IconSurf = MyIconPool.GiveIconSurface("blueselector")
        ps._Parent = self
        ps.Init(start_x,start_y,92,92,128)
        
        self._Ps = ps
        self._PsIndex = 0
        self._OnShow = False
        
        if self._IconNumbers > 1:
            self._PsIndex = 1
            self._IconIndex = self._PsIndex
            self._PrevIconIndex = self._IconIndex
            self._Icons[self._IconIndex]._PosY -= self._SelectedIconTopOffset

    def AdjustSAutoLeftAlign(self): ## adjust coordinator and append the PageSelector
        self._PosX = self._Index*self._Screen._Width
        self._Width = self._Screen._Width
        self._Height = self._Screen._Height
        
        start_x = (self._PageIconMargin + icon_width+self._PageIconMargin) /2
        start_y = self._Height/2

        if self._IconNumbers == 1:
            start_x = self._Width / 2
            start_y = self._Height/2
            
            it = self._Icons[0]
            it._Parent = self
            it._Index = 0
            it.Adjust(start_x,start_y,icon_width,icon_height,0)
            # it._ImgSurf = pygame.transform.smoothscale(it._ImgSurf,(it._Width,it._Height))

        elif self._IconNumbers == 2:
            start_x = (self._Width - self._PageIconMargin - self._IconNumbers*icon_width) / 2 + icon_width/2
            start_y = self._Height /2

            for i in range(0,self._IconNumbers):
                it = self._Icons[i]
                it._Parent = self
                it._Index = i
                it.Adjust(start_x+i*self._PageIconMargin + i*icon_width,start_y, icon_width, icon_height,0)
                # it._ImgSurf = pygame.transform.smoothscale(it._ImgSurf,(it._Width,it._Height))
                
        elif self._IconNumbers > 2:
            for i in range(0,self._IconNumbers):
                it = self._Icons[i]
                it._Parent = self
                it._Index = i
                it.Adjust(start_x+i*self._PageIconMargin + i*icon_width,start_y,icon_width,icon_height,0)
                # it._ImgSurf = pygame.transform.smoothscale(it._ImgSurf,(it._Width,it._Height))

        ps = PageSelector()
        ps._IconSurf = MyIconPool.GiveIconSurface("blueselector")
        ps._Parent = self
        ps.Init(start_x,start_y,92,92,128)
        
        self._Ps = ps
        self._PsIndex = 0
        self._OnShow = False

        if self._IconNumbers > 1:
            self._PsIndex = 1
            self._IconIndex = self._PsIndex
            self._PrevIconIndex = self._IconIndex
            self._Icons[self._IconIndex]._PosY -= self._SelectedIconTopOffset

    def InitLeftAlign(self):
        self._PosX = self._Index*Width
        self._Width = self._Screen._Width
        self._Height = self._Screen._Height
        
        cols = int(self._Width /icon_width)
        rows = int((self._IconNumbers * icon_width)/self._Width + 1)
        if rows < 1:
            rows = 1
        cnt = 0
        for i in range(0,rows):
            for j in range(0,cols):
                start_x = icon_width/2  + j*icon_width
                start_y = TitleBar._BarHeight + icon_height/2 + i*icon_height
                icon = IconItem()
                icon.Init(start_x,start_y,icon_width-4,icon_height-4,0)
                icon._Index = cnt
                icon._Parent = self
                self._Icons.append(icon)
                if cnt >= (self._IconNumbers -1):
                    break
                cnt+=1
                
        ps = PageSelector()
        ps._IconSurf = MyIconPool.GiveIconSurface("blueselector")
        ps._Parent = self
        ps.Init(icon_width/2,icon_height/2,92,92,128)
        self._Ps = ps
        self._PsIndex = 0
        self._OnShow = False

    def Adjust(self): ## default init way, 
        self._PosX = self._Index*self._Screen._Width 
        self._Width = self._Screen._Width ## equal to screen width
        self._Height = self._Screen._Height

        if self._Align == ALIGN["HLeft"]:
            start_x = (self._Width - self._IconNumbers*icon_width)/2 + icon_width/2
            start_y = self._Height/2

            for i in range(0,self._IconNumbers):
                it = self._Icons[i]
                it._Parent = self
                it._Index = i
                it.Adjust(start_x+i*icon_width,start_y,icon_width,icon_height,0)

            ps = PageSelector()
            ps._IconSurf = MyIconPool.GiveIconSurface("blueselector")
            ps._Parent = self
            ps.Init(start_x,start_y,92,92,128)
            self._Ps = ps
            self._PsIndex = 0
            self._OnShow = False
        elif self._Align == ALIGN["SLeft"]:
            start_x = (self._PageIconMargin + icon_width+self._PageIconMargin) /2
            start_y = self._Height/2
            
            for i in range(0,self._IconNumbers):
                it = self._Icons[i]
                it._Parent = self
                it._Index = i
                it.Adjust(start_x+i*self._PageIconMargin+i*icon_width,start_y,icon_width,icon_height,0)
                

       
            ps = PageSelector()
            ps._IconSurf = MyIconPool.GiveIconSurface("blueselector")
            ps._Parent = self
            ps.Init(start_x,start_y-self._SelectedIconTopOffset,92,92,128)
            
            self._Ps = ps
            self._PsIndex = 0
            self._OnShow = False
            
            if self._IconNumbers > 1:
                self._PsIndex = 1
                self._IconIndex = self._PsIndex
                self._PrevIconIndex = self._IconIndex
                self._Icons[self._IconIndex]._PosY -= self._SelectedIconTopOffset
                
                
    def Init(self): ## default init way, 
        if self._Screen != None:
            if self._Screen._CanvasHWND != None and self._CanvasHWND == None:
                self._CanvasHWND = self._Screen._CanvasHWND

        self._PosX = self._Index*self._Screen._Width 
        self._Width = self._Screen._Width ## equal to screen width
        self._Height = self._Screen._Height

        start_x = (self._Width - self._IconNumbers*icon_width)/2 + icon_width/2
        start_y = self._Height/2

        for i in range(0,self._IconNumbers):
            it = IconItem()
            it._Parent = self
            it._Index = i
            it.Init(start_x+i*icon_width,start_y,icon_width,icon_height,0)
            self._Icons.append(it)
            
        if self._IconNumbers > 0:
            ps = PageSelector()
            ps._IconSurf = MyIconPool.GiveIconSurface("blueselector")
            ps._Parent = self
            ps.Init(start_x,start_y,icon_width+4,icon_height+4,128)
            self._Ps = ps
            self._PsIndex = 0
            self._OnShow = False
            
    def IconStepMoveData(self,icon_eh,cuts):## no Sine,No curve,plain movement steps data
        all_pieces = []
        piece = icon_eh / cuts

        c = 0.0
        prev = 0.0
        for i in range(0,cuts):
            c+=piece
            dx = c-prev
            if dx < 0.5:
                dx = 1.0
                
            all_pieces.append( math.ceil(dx) )
            if c >= icon_eh:
                break

        c = 0
        bidx = 0
        for i in all_pieces:
            c+=i
            bidx+=1
            if c >= icon_eh:
                break

        all_pieces = all_pieces[0:bidx]

        if len(all_pieces) < cuts:
            dff = cuts - len(all_pieces)
            diffa = []
            for i in range(0,dff):
                diffa.append(0)
            all_pieces.extend( diffa)
                
        return all_pieces

    def EasingData(self,start,distance):##generate easing steps data
        current_time  = 0.0
        start_posx    = 0.0
        current_posx  = start_posx
        final_posx    = float(distance)
        posx_init     = start
        dur           = self._EasingDur
        last_posx     = 0.0
        all_last_posx = []
        for i in range(0,distance*dur):
            current_posx = easing.SineIn(current_time,start_posx,final_posx-start_posx,float(dur))
            if current_posx >= final_posx:
                current_posx = final_posx

            dx = current_posx - last_posx
            all_last_posx.append(int(dx))
            current_time+=1
            last_posx = current_posx
            if current_posx >= final_posx:
                break
            c = 0
        for i in all_last_posx:
            c+=i
        if c < final_posx -start_posx:
            all_last_posx.append(final_posx - c)

        return all_last_posx

    # def IconSmoothUp(self,icon_ew):
    def IconSmoothUp(self, icon_ew, fast = False):
        data = self.EasingData(self._PosX,icon_ew)
        data2 = self.IconStepMoveData(self._SelectedIconTopOffset,len(data))
        
        for i,v in enumerate(data):
            
            self.ClearCanvas()
            
            self._Icons[self._IconIndex]._PosY -= data2[i]
            
            if self._Icons[self._PrevIconIndex]._PosY < self._Height/2:
                self._Icons[self._PrevIconIndex]._PosY+=data2[i]

            # self.DrawIcons()
            # self._Screen.SwapAndShow()
            if not fast:
                self.DrawIcons()
                self._Screen.SwapAndShow()

    # def IconsEasingLeft(self,icon_ew):
    def IconsEasingLeft(self, icon_ew, fast = False):

        data = self.EasingData(self._PosX,icon_ew)
        data2 = self.IconStepMoveData(self._SelectedIconTopOffset,len(data))
        
        for i,v in enumerate(data):
            
            self.ClearCanvas()
            self._PosX -= v
            
            self._Icons[self._IconIndex]._PosY -= data2[i]
            
            if self._Icons[self._PrevIconIndex]._PosY < self._Height/2:
                self._Icons[self._PrevIconIndex]._PosY+=data2[i]

            # self.DrawIcons()
            # self._Screen.SwapAndShow()
            if not fast:
                self.DrawIcons()
                self._Screen.SwapAndShow()

    # def IconsEasingRight(self,icon_ew):
    def IconsEasingRight(self, icon_ew, fast = False):
        
        data = self.EasingData(self._PosX,icon_ew)
        data2 = self.IconStepMoveData(self._SelectedIconTopOffset,len(data))
        
        for i,v in enumerate(data):
            self.ClearCanvas()
            self._PosX += v

            
            self._Icons[self._IconIndex]._PosY-=data2[i]

            if self._Icons[self._PrevIconIndex]._PosY < self._Height/2:
                self._Icons[self._PrevIconIndex]._PosY+=data2[i]

            # self.DrawIcons()
            # self._Screen.SwapAndShow()
            if not fast:
                self.DrawIcons()
                self._Screen.SwapAndShow()

    def EasingLeft(self,ew): #ew int

        data = self.EasingData(self._PosX,ew)
        
        for i in data:
            self._PosX -=i
            self.Draw()
            self._Screen.SwapAndShow()
            
    def EasingRight(self,ew):

        data = self.EasingData(self._PosX,ew)
        
        for i in data:
            self._PosX += i
            self.Draw()
            self._Screen.SwapAndShow()
            
    def MoveLeft(self,ew):
        self._PosX -= ew
    def MoveRight(self,ew):
        self._PosX += ew
        
    def ResetPageSelector(self):
        self._PsIndex = 0
        self._IconIndex = 0
        self._Ps._OnShow = True

    def DrawPageSelector(self):
        if self._Ps._OnShow == True:
            self._Ps.Draw()
            
    def MoveIconIndexPrev(self):
        self._PrevIconIndex = self._IconIndex
        self._IconIndex-=1
        if self._IconIndex < 0:
            self._IconIndex = max(0, self._IconNumbers - 1) # Wrap Icon Index
            return False
        return True
    
    def MoveIconIndexNext(self):
        self._PrevIconIndex = self._IconIndex
        self._IconIndex+=1
        if self._IconIndex > (self._IconNumbers - 1):
            self._IconIndex = 0 # Wrap Icon Index
            return False
        return True
    
    def IconClick(self):
        
        if self._IconIndex > (len(self._Icons) -1):
            return

        cur_icon = self._Icons[self._IconIndex]
        if self._Ps._OnShow == False:
            return
        if cur_icon._MyType == ICON_TYPES["EXE"]:
            print("IconClick: %s %d"%(cur_icon._CmdPath,cur_icon._Index))
            self._Screen.RunEXE(cur_icon._CmdPath)
            
        elif cur_icon._MyType == ICON_TYPES["DIR"]:
            child_page = self._Icons[self._IconIndex]._LinkPage
            if child_page != None:
                child_page.Draw()
                self._Screen._MyPageStack.Push(self._Screen._CurrentPage)
                self._Screen._CurrentPage = child_page
        elif cur_icon._MyType == ICON_TYPES["FUNC"]:
            print("IconClick API: %d"%(cur_icon._Index))
            # print("%s"% cur_icon._CmdPath)
            api_cb = getattr(cur_icon._CmdPath,"API",None)
            if api_cb != None:
                if callable(api_cb):
                    cur_icon._CmdPath.API(self._Screen)
        elif cur_icon._MyType == ICON_TYPES["Emulator"] or cur_icon._MyType == ICON_TYPES["Commercial"]:
            cur_icon._CmdPath.API(self._Screen)
            
    def ReturnToUpLevelPage(self):
        pop_page,ok = self._Screen._MyPageStack.Pop()
        if ok == True:
            # self._Screen._CurrentPage.ResetPageSelector()
            pop_page.Draw()
            self._Screen._CurrentPage = pop_page
            on_return_back_cb = getattr(self._Screen._CurrentPage,"OnReturnBackCb",None)
            if on_return_back_cb != None:
                if callable(on_return_back_cb):
                    self._Screen._CurrentPage.OnReturnBackCb()
        else:
            if self._Screen._MyPageStack.Length() == 0:
                if len(self._Screen._Pages) > 0:
                    self._Screen._CurrentPage = self._Screen._Pages[self._Screen._PageIndex]
                    self._Screen._CurrentPage.Draw()
                    print("OnTopLevel ",self._Screen._PageIndex)

    def ClearCanvas(self):
        if self._Wallpaper:
            self._CanvasHWND.blit(self._Wallpaper,(0,0))
        else:
            self._CanvasHWND.fill(self._Screen._SkinManager.GiveColor("White")) 
        
       
    def ClearIcons(self):
        for i in range(0,self._IconNumbers):
            self._Icons[i].Clear()

    def DrawIcons(self):
        for i in range(0,self._IconNumbers):
            self._Icons[i].Draw()

    # make sure the Class has the _MyList
    # def ScrollDown(self):
        # if len(self._MyList) == 0:
            # return
        # self._PsIndex +=1
        # if self._PsIndex >= len(self._MyList):
            # self._PsIndex = len(self._MyList) -1

        # cur_li = self._MyList[self._PsIndex]
        # if cur_li._PosY +cur_li._Height > self._Height:
            # for i in range(0,len(self._MyList)):
                # self._MyList[i]._PosY -= self._MyList[i]._Height
    
    # def ScrollUp(self):
        # if len(self._MyList) == 0:
            # return
        # self._PsIndex -= 1
        # if self._PsIndex < 0:
            # self._PsIndex = 0
        # cur_li = self._MyList[self._PsIndex]
        # if cur_li._PosY < 0:
            # for i in range(0, len(self._MyList)):
                # self._MyList[i]._PosY += self._MyList[i]._Height
    
    def ScrollUp(self, step = 1):
        if len(self._MyList) <= 1:
            return

        # check step
        if step > self._ItemsPerPage:
            step = self._ItemsPerPage - 1
        if step > len(self._MyList) - 1:
            step = 1

        # first to end
        if self._PsIndex - step < 0 and step == 1:
            # index of the last item on current screen 
            self._PsIndex = 0 + self._ItemsPerPage - 1

            # loop scroll, to end
            if len(self._MyList) > self._ItemsPerPage:
                self.FScrollDown(len(self._MyList) - self._ItemsPerPage, True)
            self._PsIndex = len(self._MyList) - 1
            self._Scrolled = self._PsIndex
            return
        else:
            self.FScrollUp(step)

    def ScrollDown(self, step = 1):
        if len(self._MyList) <= 1:
            return

        # check step
        if step > self._ItemsPerPage:
            step = self._ItemsPerPage - 1
        if step > len(self._MyList) - 1:
            step = 1

        # end to first
        if self._PsIndex + step >= len(self._MyList) and step == 1:
            # index of the first item on current screen
            self._PsIndex = (len(self._MyList) - 1) - (self._ItemsPerPage - 1)

            # loop scroll, to first
            if len(self._MyList) > self._ItemsPerPage:
                self.FScrollUp(len(self._MyList) - self._ItemsPerPage, True)
            self._PsIndex = 0
            self._Scrolled = self._PsIndex
            return
        else:
            self.FScrollDown(step)

    # do not directly call this function, please use "ScrollUp(step)"
    def FScrollUp(self, step = 1, loop_scroll = False):
        # if len(self._MyList) == 0:
        if len(self._MyList) <= 1:
            return

        if step < self._ItemsPerPage and not loop_scroll:
            if (self._PsIndex - step + 1) - 1 < step:
                step = 1

        tmp = self._PsIndex
        self._PsIndex -= step
        
        if self._PsIndex < 0:
            self._PsIndex = 0

        # dy = tmp-self._PsIndex
        dy = abs(tmp - self._PsIndex)
        cur_li = self._MyList[self._PsIndex]
        if cur_li._PosY < 0:
            for i in range(0, len(self._MyList)):
                self._MyList[i]._PosY += self._MyList[i]._Height * dy
            self._Scrolled += dy

    # do not directly call this function, please use "ScrollDown(step)"
    def FScrollDown(self, step = 1, loop_scroll = False):
        # if len(self._MyList) == 0:
        if len(self._MyList) <= 1:
            return
        
        if step < self._ItemsPerPage and not loop_scroll:
            if len(self._MyList) - (self._PsIndex + step + 1) < step:
                step = 1

        tmp = self._PsIndex
        self._PsIndex += step

        if self._PsIndex >= len(self._MyList):
            self._PsIndex = len(self._MyList) - 1

        # dy = self._PsIndex - tmp
        dy = abs(self._PsIndex - tmp)
        cur_li = self._MyList[self._PsIndex]
        if cur_li._PosY + cur_li._Height > self._Height:
            for i in range(0, len(self._MyList)):
                self._MyList[i]._PosY -= self._MyList[i]._Height * dy
            self._Scrolled -= dy

    def SyncScroll(self):
        if self._Scrolled == 0:
            return

        if self._PsIndex < len(self._MyList):
            cur_li = self._MyList[self._PsIndex]
            if self._Scrolled > 0:
                if cur_li._PosY < 0:
                    for i in range(0, len(self._MyList)):
                        self._MyList[i]._PosY += self._Scrolled * self._MyList[i]._Height
            elif self._Scrolled < 0:
                if cur_li._PosY +cur_li._Height > self._Height:
                    for i in range(0,len(self._MyList)):
                        self._MyList[i]._PosY += self._Scrolled * self._MyList[i]._Height

    def SpeedScroll(self, thekey):
        if self._Screen._LastKey == thekey:
            self._ScrollStep += 1
            if self._ScrollStep >= self._ItemsPerPage:
                self._ScrollStep = self._ItemsPerPage - 1
        else:
            self._ScrollStep = 1
           
        cur_time = time.time()
            
        if cur_time - self._Screen._LastKeyDown > 0.3:
            self._ScrollStep = 1

        if len(self._MyList) < self._ItemsPerPage:
            self._ScrollStep = 1

    def RefreshPsIndex(self):
        if len(self._MyList) == 0:
            self._PsIndex = 0
        if self._PsIndex > (len(self._MyList) -1):
            self._PsIndex = len(self._MyList) -1
    
    # def KeyDown(self,event):##default keydown, every inherited page class should have it's own KeyDown
    # fast: fast display mode
    def KeyDown(self, event, fast = False):##default keydown, every inherited page class should have it's own KeyDown

        if IsKeyMenuOrB(event.key):
            self.ReturnToUpLevelPage()
            self._Screen.Draw()
            self._Screen.SwapAndShow()

        if event.key == CurKeys["Right"]:
            if self.MoveIconIndexNext() == True:
                if self._IconIndex == (self._IconNumbers -1) or self._PrevIconIndex == 0:
                    # self.IconSmoothUp(icon_width + self._PageIconMargin)
                    self.IconSmoothUp(icon_width + self._PageIconMargin, fast)
                else:
                    # self.IconsEasingLeft(icon_width + self._PageIconMargin)
                    self.IconsEasingLeft(icon_width + self._PageIconMargin, fast)
            else:
                screen_icons = int(math.floor(self._Screen._Width / (icon_width + self._PageIconMargin)))
                if self._IconNumbers > screen_icons:
                    # self.IconsEasingRight((icon_width + self._PageIconMargin) * (self._IconNumbers - screen_icons))
                    self.IconsEasingRight((icon_width + self._PageIconMargin) * (self._IconNumbers - screen_icons), fast)
                elif self._IconNumbers > 0:
                    # self.IconSmoothUp(icon_width+ self._PageIconMargin)
                    self.IconSmoothUp(icon_width+ self._PageIconMargin, fast)

            self._PsIndex  = self._IconIndex
            # self._Screen.Draw()
            # self._Screen.SwapAndShow()
            if not fast:
                self._Screen.Draw()
                self._Screen.SwapAndShow()
            
        if event.key == CurKeys["Left"]:
            if self.MoveIconIndexPrev() == True:
                if self._IconIndex == 0 or self._PrevIconIndex == (self._IconNumbers -1):
                    # self.IconSmoothUp(icon_width + self._PageIconMargin)
                    self.IconSmoothUp(icon_width + self._PageIconMargin, fast)
                else:
                    # self.IconsEasingRight(icon_width + self._PageIconMargin)
                    self.IconsEasingRight(icon_width + self._PageIconMargin, fast)
            else:
                screen_icons = int(math.floor(self._Screen._Width / (icon_width + self._PageIconMargin)))
                if self._IconNumbers > screen_icons:
                    # self.IconsEasingLeft((icon_width + self._PageIconMargin) * (self._IconNumbers - screen_icons))
                    self.IconsEasingLeft((icon_width + self._PageIconMargin) * (self._IconNumbers - screen_icons), fast)
                elif self._IconNumbers > 0:
                    # self.IconSmoothUp(icon_width+ self._PageIconMargin)
                    self.IconSmoothUp(icon_width+ self._PageIconMargin, fast)

            self._PsIndex = self._IconIndex
            # self._Screen.Draw()
            # self._Screen.SwapAndShow()
            if not fast:
                self._Screen.Draw()
                self._Screen.SwapAndShow()

        if event.key == CurKeys["Up"]:
            move = 3
            pageup = pygame.event.Event(pygame.KEYDOWN, key = CurKeys["Left"])

            for i in range(move):
                self.KeyDown(pageup, True)

            self.DrawIcons()            # redraw icons
            self._Screen.Draw()         # show selected icon
            self._Screen.SwapAndShow()

        if event.key == CurKeys["Down"]:
            move = 3
            pagedown = pygame.event.Event(pygame.KEYDOWN, key = CurKeys["Right"])
            
            for i in range(move):
                self.KeyDown(pagedown, True)

            self.DrawIcons()            # redraw icons
            self._Screen.Draw()         # show selected icon
            self._Screen.SwapAndShow()

        if IsKeyStartOrA(event.key):
            self.IconClick()
            self._Screen.Draw()
            self._Screen.SwapAndShow()

    ##for gcores
    def DrawCross(self,topleft,top):
        start_x = topleft
        start_y = top
        width = 2
        height = 10 
        padding = 4

        rect1 = pygame.Rect(start_x+padding,start_y,width,height)
        rect2 = pygame.Rect(start_x,start_y+padding,height,width)

        pygame.draw.rect(self._CanvasHWND,MySkinManager.GiveColor('Text'),rect1, 0)   
        pygame.draw.rect(self._CanvasHWND,MySkinManager.GiveColor('Text'),rect2, 0)  

    def Draw(self):
        self.ClearCanvas()
        self.DrawIcons()
        self.DrawPageSelector()
