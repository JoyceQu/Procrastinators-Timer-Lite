import pygame, sys, time, math
import pygame.gfxdraw
from datetime import datetime
import calendar

SCREEN_WIDTH, SCREEN_HEIGHT = 600, 500

# the ith object of DIGIT_INDEX shows arrangement of number i
'''
  ——     -0-
 |  |   1   2
  ——     -3-
 |  |   4   5
  ——     -6-
'''
DIGIT_INDEX = [\
    [1, 1, 1, 0, 1, 1, 1], \
    [0, 0, 1, 0, 0, 1, 0], \
    [1, 0, 1, 1, 1, 0, 1], \
    [1, 0, 1, 1, 0, 1, 1], \
    [0, 1, 1, 1, 0, 1, 0], \
    [1, 1, 0, 1, 0, 1, 1], \
    [1, 1, 0, 1, 1, 1, 1], \
    [1, 0, 1, 0, 0, 1, 0], \
    [1, 1, 1, 1, 1, 1, 1], \
    [1, 1, 1, 1, 0, 1, 1]]

WHITE, BLACK = (255, 255, 255), (0, 0, 0)
GR1 = (240, 240, 240) # FOR THE BACKGROUND OF PRESSED/MOUSEON BUTTON
GR2 = (230, 230, 230) # FOR CALENDAR - DAYS THAT ARE NOT TIMED
GR3 = (200, 200, 200) # FOR CALENDAR - DAYS THAT DOESN'T BELONG TO THIS MONTH
GR4 = (100, 100, 100) # FONT COLOR

RED = (255, 85, 115)
ORANGE = (255, 128, 66)
YELLOW = (255, 181, 51)
GREEN = (146, 220, 55)
CYAN = (24, 218, 189)
BLUE = (54, 143, 231)
PURPLE = (160, 105, 255) # THE ORIGINAL COLOR STYLE

# from brightest to darkest
GREY_LIST = (WHITE, GR2, GR3, GR4, (0, 0, 0))
#               white                gr1             gr2            gr3             black
PURPLE_LIST = ((200, 170, 255), (180, 135, 255), PURPLE)
RED_LIST = ((255, 185, 220), (255, 150, 165), RED)
ORANGE_LIST = ((255, 200, 167), (255, 150, 91), ORANGE)
YELLOW_LIST = ((255, 225, 145), (255, 207, 100), YELLOW)
GREEN_LIST = ((185, 255, 118), GREEN, (90, 160, 45))
CYAN_LSIT = ((90, 220, 200), CYAN, (8, 150, 140))
BLUE_LIST = ((140, 185, 235), (70, 145, 225), BLUE)


COLOR_LIST = (PURPLE, RED, ORANGE, YELLOW, GREEN, CYAN, BLUE)
CLD_COLOR_LIST = (PURPLE_LIST, RED_LIST, ORANGE_LIST, YELLOW_LIST, GREEN_LIST, CYAN_LSIT, BLUE_LIST)

sin_list, cos_list = [], []
for i in range(1440):
    angle = i / 720 * math.pi
    sin_list.append(math.sin(angle + math.pi / 2))
    cos_list.append(math.cos(angle + math.pi / 2))


def load_img(filename, actual_size, target_size):
    surf = pygame.Surface((actual_size, actual_size), pygame.SRCALPHA, 32)
    surf2 = pygame.Surface((actual_size, actual_size), pygame.SRCALPHA, 32)
    img = pygame.image.load(filename)
    surf2.blit(img, (0, 0))
    for y in range(actual_size):
        for x in range(actual_size):
            clr = surf2.get_at((x, y))
            surf.set_at((x, y), (255, 255, 255, clr[0]))
            #print(clr)
    surf = pygame.transform.scale(surf, (target_size, target_size))
    return surf

#####todo
def gen_icon_img(clr, bgclr, r, w, flag, fclr = None, img = None):

    surf = pygame.Surface((r * 2, r * 2))
    surf.fill(bgclr)
    
    if flag == 1: # play
        pygame.draw.circle(surf, clr, (r, r), r, w)   
        pygame.draw.circle(surf, bgclr, (r, r), r - w)
        pygame.gfxdraw.aapolygon(surf, [(r * 0.7, r * 0.6), (r * 0.7, r * 1.4), (r * 1.5, r)], clr)
        pygame.draw.polygon(surf, clr, [(r * 0.7, r * 0.6), (r * 0.7, r * 1.4), (r * 1.5, r)])
    elif flag == 2: # pause
        pygame.draw.circle(surf, clr, (r, r), r, w)   
        pygame.draw.circle(surf, bgclr, (r, r), r - w)
        pygame.draw.rect(surf, clr, (r * 0.7, r * 0.5, r * 0.2, r))
        pygame.draw.rect(surf, clr, (r * 1.1, r * 0.5, r * 0.2, r))
    elif flag == 3: # stop
        pass
    elif flag == 4: # color choice
        pygame.draw.circle(surf, clr, (r, r), r, w)   
        pygame.draw.circle(surf, bgclr, (r, r), r - w)
        if fclr == None:
            fclr = clr
        pygame.draw.circle(surf, fclr, (r, r), r - w * 2)
    elif flag == 5: # leftplay
        pygame.gfxdraw.aapolygon(surf, [(r * 1.3, r * 1.4), (r * 1.3, r * 0.6), (r * 0.5, r)], clr)
        pygame.draw.polygon(surf, clr, [(r * 1.3, r * 1.4), (r * 1.3, r * 0.6), (r * 0.5, r)])
    elif flag == 6:
        pygame.gfxdraw.aapolygon(surf, [(r * 0.7, r * 0.6), (r * 0.7, r * 1.4), (r * 1.5, r)], clr)
        pygame.draw.polygon(surf, clr, [(r * 0.7, r * 0.6), (r * 0.7, r * 1.4), (r * 1.5, r)])
    elif flag == 7:
        pygame.gfxdraw.aapolygon(surf, [(r * 1.1, r * 1.4), (r * 1.1, r * 0.6), (r * 0.5, r)], clr)
        pygame.draw.polygon(surf, clr, [(r * 1.1, r * 1.4), (r * 1.1, r * 0.6), (r * 0.5, r)])
        pygame.gfxdraw.aapolygon(surf, [(r * 1.4, r * 1.4), (r * 1.4, r * 0.6), (r * 0.7, r)], clr)
        pygame.draw.polygon(surf, clr, [(r * 1.4, r * 1.4), (r * 1.4, r * 0.6), (r * 0.7, r)])
    elif flag == 8:
        pygame.gfxdraw.aapolygon(surf, [(r * 0.6, r * 0.6), (r * 0.6, r * 1.4), (r * 1.3, r)], clr)
        pygame.draw.polygon(surf, clr, [(r * 0.6, r * 0.6), (r * 0.6, r * 1.4), (r * 1.3, r)])
        pygame.gfxdraw.aapolygon(surf, [(r * 0.9, r * 0.6), (r * 0.9, r * 1.4), (r * 1.5, r)], clr)
        pygame.draw.polygon(surf, clr, [(r * 0.9, r * 0.6), (r * 0.9, r * 1.4), (r * 1.5, r)])
    elif flag == 9:
        pygame.draw.circle(surf, clr, (r, r), r, w)   
        pygame.draw.circle(surf, bgclr, (r, r), r - w)
        pygame.draw.circle(surf, clr, (r, r), r - w * 2)
        surf.blit(switch_img, (10, 10))
    elif flag == 10:
        pygame.draw.circle(surf, clr, (r, r), r, w)   
        pygame.draw.circle(surf, bgclr, (r, r), r - w)
        pygame.draw.circle(surf, clr, (r, r), r - w * 2)
        surf.blit(tabbar_img, (10, 10))
    elif flag == 11: #intentioanlly lefted blank for words
        pygame.draw.circle(surf, clr, (r, r), r, w)   
        pygame.draw.circle(surf, bgclr, (r, r), r - w)
    if img != None:
        if img <= 4:
            sz = imglist[img].get_size()
            s = sz[0]
            surf.blit(imglist[img], (r-s/2,r-s/2))

    surf.set_colorkey(bgclr)
    return surf

def draw_arc(scr, x, y, w, r, clr, start_angle, end_angle):
    if start_angle == 0 and end_angle == 0 or end_angle - start_angle >= 360:
        pygame.draw.circle(scr, clr, (x, y), r, w)
        return
    start_angle, end_angle = start_angle % 360, end_angle % 360
    if start_angle == end_angle:
        return
    pos_list = []
    for i in range(int(start_angle * 4), int(end_angle * 4)):
        pos_list.append([round(x + r * cos_list[i % 1440]), round(y + r * sin_list[i % 1440])])
    for i in range(int(end_angle * 4), int(start_angle * 4), -1):
        pos_list.append([round(x + (r - w) * cos_list[i % 1440]), round(y + (r - w) * sin_list[i % 1440])])
    pygame.draw.polygon(scr, clr, pos_list)
    pygame.gfxdraw.aapolygon(scr, pos_list, clr)
    return
    

class CLS_button(object):
    def __init__(self, x, y, r, w, clr, bgclr, stat, flag, display_stat, fclr = None, font_name = None, font_size = None, font_clr = None):
        self.x, self.y, self.r, self.w = x, y, r, w
        self.clr, self.bgclr = clr, bgclr
        self.focus = False
        self.callback_click = None
        self.callback_redraw = None
        self.stat = stat
        self.surf = gen_icon_img(clr, bgclr, r, w, flag, fclr)
        self.dflag = 0
        self.display_stat = display_stat
        self.fnt = None
        if font_name != None:
            self.fnt = pygame.font.Font(font_name, font_size)
            self.font_clr = font_clr
        self.txt = ''
        return
    def draw(self, scr, angle = 0):
        if self.display_stat == True:
            if angle == 0:
                scr.blit(self.surf, (self.x, self.y))
            else:
                tsurf = pygame.transform.rotate(self.surf, angle)
                tw = tsurf.get_width()
                scr.blit(tsurf, (self.x - (tw - self.r * 2) // 2, self.y - (tw - self.r * 2) // 2))
        return
    def change_txt(self, txt):
        self.surf = gen_icon_img(self.clr, self.bgclr, self.r, self.w, 11, None)
        txt_img = self.fnt.render(txt, True, self.font_clr)
        tw, th = txt_img.get_width(), txt_img.get_height()
        self.surf.blit(txt_img, (self.r - tw // 2, self.r - th // 2))
        return
    
    def isme (self, pos):
        mx, my = pos # mouse x, mouse y
        if (mx - (self.x + self.r)) ** 2 + (my - (self.y + self.r)) ** 2 <= self.r ** 2:
            ##print(self.stat)
            if self.callback_click != None and self.stat == True and self.display_stat == True:
                self.callback_click()
            return True
        return False

class CLS_text_box(object):
    def __init__(self, x, y, w, h, clr, bglcr, font_name, ftsz, font_clr):
        self.x, self.y, self.w, self.h = x, y, w, h
        self.clr, self.bgclr = clr, bglcr
        self.fnt = pygame.font.Font(font_name, ftsz)
        self.font_clr = font_clr
        self.focus = False
        self.mouse_index = 1
        self.display_stat = False
        self.txt = '10'
        self.render_text()
        self.callback_changetime = None
        return

    def render_text(self):
        self.txt_image = self.fnt.render(self.txt, True, self.font_clr)
        return

    def draw(self, scr):
        if self.display_stat == False:
            return
        #print(self.focus)
        pygame.draw.rect(scr, self.bgclr, (self.x, self.y, self.w, self.h), width=0)
        bdw = self.w // 2 - 5
        if self.txt != '':
            bdw = (self.w - self.txt_image.get_width()) // 2
            self.bdh = (self.h - self.txt_image.get_height()) // 2
            scr.blit(self.txt_image, (self.x + bdw, self.y + self.bdh))
        if self.focus == True:
            pygame.draw.rect(scr, self.font_clr, (self.x + bdw + self.txt_image.get_width(), self.y + self.bdh + self.txt_image.get_height() - 10, 10, 4))
        return
    
    def change_text(self, time):
        target_time = int(self.txt) + time
        if target_time < 0:
            target_time = 0
        self.txt = str(target_time)
        self.render_text()
        return

    def isme(self, pos):
        mx, my = pos
        if mx >= self.x and mx <= self.x + self.w and my >= self.y and my <= self.y + self.h:
            self.focus = True
            return True
        #print('me')
        self.focus = False
        return False

    def keydown(self, key):
        #print(key)
        if self.focus == False:
            return
        if key >= 48 and key <= 57:
            if len(self.txt) < 3:
                self.txt += str(key - 48)
                self.mouse_index += 1
        elif key == pygame.K_BACKSPACE:
            #print('sth')
            if self.mouse_index > -1:
                self.txt = self.txt[0 : self.mouse_index] + self.txt[self.mouse_index + 1 : len(self.txt)]
                self.mouse_index -= 1
        elif key == 13: # enter
            if self.txt == '':
                self.txt = '10'
                self.mouse_index = 1
            if self.callback_changetime != None:
                self.callback_changetime()
        '''
        elif key == pygame.K_DELETE:
            if len(self.txt) - self.mouse_index > 1:
                self.txt.pop(self.mouse_index + 1)
        elif key == pygame.K_LEFT:
            if self.mouse_index > -1:
                self.mouse_index -= 1
        elif key == pygame.K_RIGHT:
            if len(self.txt) - self.mouse_index > 1:
                self.mouse_index += 1
        '''
        self.render_text()
        
        return

# to display the time as XX:XX, X: number digit
class CLS_digit_display(object):
    def __init__(self, x, y, w, h, clr, bgclr, grclr, weight, bspace, dspace, csize):
        self.x = [x, x + w + dspace, x + w * 2 + dspace * 5 + csize, x + w * 3 + dspace * 6 + csize, x + w * 2 + dspace * 3]
        # the timer is displayed as X_X__:__X_X, where X: digit, _: dspace
        # x: x-coordinate of [digit1, digit2, digit3, digit4, colon]
        self.y, self.w, self.h = y, w, h
        # (x, y): coordinate of top left corner
        # w, h: width and height a single digit
        self.weight, self.bspace, self.dspace= weight, bspace, dspace
        # weight: the width of bars that make up the digits
        # bspace: space between bars
        # dspace: space between digits
        self.clr, self.bgclr, self.grclr = clr, bgclr, grclr
        # clr: color of digits
        # bgclr: background color
        self.csize = csize
        # csize: the size of colon in XX:XX
        self.dimension = (w * 4 + dspace * 6 + csize, h)
        # dimension: (width, height) of the combined digit display module
        self.initialize()
        return
    
    def initialize(self):
        self.gen_digit_list(self.clr, self.grclr, self.w, self.h, self.weight, self.bspace)
        return

    def gen_bar_list(self, w, h, wt, sp):
        #    0  1        2             3   4        5            6       7                 8            9
        X = [0, wt // 2, wt // 2 + sp, wt, wt + sp, w - wt - sp, w - wt, w - wt // 2 - sp, w - wt // 2, w]
        #    0  1        2             3   4        5                          6                 7            8
        Y = [0, wt // 2, wt // 2 + sp, wt, wt + sp, h // 2 - sp - wt // 2, h // 2 - wt // 2, h // 2 - sp, h // 2, \
            h // 2 + sp, h // 2 + wt // 2,  h // 2 + sp + wt // 2, h - wt - sp, h - wt, h - wt // 2 - sp, h - wt // 2, h]
        #   9            10                 11                         12           13      14                15      16
        bar_list = [\
            [(X[4], Y[0]), (X[5], Y[0]), (X[7], Y[1]), (X[5], Y[3]), (X[4], Y[3]), (X[2], Y[1])],\
            [(X[1], Y[2]), (X[3], Y[4]), (X[3], Y[5]), (X[1], Y[7]), (X[0], Y[5]), (X[0], Y[4])],\
            [(X[8], Y[2]), (X[9], Y[4]), (X[9], Y[5]), (X[8], Y[7]), (X[6], Y[5]), (X[6], Y[4])],\
            [(X[4], Y[6]), (X[5], Y[6]), (X[7], Y[8]), (X[5], Y[10]), (X[4], Y[10]), (X[2], Y[8])],\
            [(X[1], Y[9]), (X[3], Y[11]), (X[3], Y[12]), (X[1], Y[14]), (X[0], Y[12]), (X[0], Y[11])],\
            [(X[8], Y[9]), (X[9], Y[11]), (X[9], Y[12]), (X[8], Y[14]), (X[6], Y[12]), (X[6], Y[11])],\
            [(X[4], Y[13]), (X[5], Y[13]), (X[7], Y[15]), (X[5], Y[16]), (X[4], Y[16]), (X[2], Y[15])]]
        return bar_list

    def gen_digit_list(self, clr, grclr, w, h, wt, sp):
        bar_list = self.gen_bar_list(w, h, wt, sp)
        anticlr = (255 - clr[0], 255 - clr[1], 255 - clr[2])
        self.digit_list = []
        for i in range(10):
            surf = pygame.Surface((w, h))
            surf.fill(anticlr)
            for j in range(7):
                if DIGIT_INDEX[i][j] == 1:
                    pygame.draw.polygon(surf, clr, bar_list[j])
                else:
                    pygame.draw.polygon(surf, grclr, bar_list[j])
            surf.set_colorkey(anticlr)
            self.digit_list.append(surf)
        return

    def draw(self, scr, num, flag):
        #scr.fill(self.bgclr)
        for i in range(4):
            scr.blit(self.digit_list[num[i]], (self.x[i], self.y))
        clr = [self.clr, self.bgclr][flag]
        pygame.draw.rect(scr, clr, (self.x[4], self.y + self.h // 3 - self.csize // 3 * 2, self.csize, self.csize))
        pygame.draw.rect(scr, clr, (self.x[4], self.y + self.h // 3 * 2 - self.csize // 3, self.csize, self.csize))
        return

class CLS_dial(object):
    def __init__(self, x, y, w, r, clr, bgclr, grclr, dgt):
        self.x, self.y = x, y
        self.w, self.r = w, r
        self.clr, self.bgclr, self.grclr = clr, bgclr, grclr
        self.digit_display = dgt
        return
    def draw(self, scr, num, flag, stangle, edangle):
        scr.fill(self.bgclr)
        draw_arc(scr, self.x, self.y, self.w, self.r, self.grclr, 0, 400)
        draw_arc(scr, self.x, self.y, self.w, self.r, self.clr, stangle, edangle)
        self.digit_display.draw(scr, num, flag)
        return

class CLS_record(object):
    def __init__(self, filename):
        self.filename = filename
        self.record = {}
        # record is a dict, with yyyy as a key, and [month[date[color[time]]]] as value
        self.readfile()
        return

    # append a piece of data to the record
    def append_record(self, y, m, d, t, c):
        if y not in self.record:
            self.record[y] = [[[[]for clr in range(7)] for day in range (32)] for month in range(13)]
        self.record[y][m][d][c].append(t)
        self.save()
        return

    def check_record(self, y, m, d, c):
        if y not in self.record:
            return []
        if c == 0: 
            return self.record[y][m][d]
        return self.record[y][m][d][c]

    def readfile(self):
        f = open(self.filename, 'r')
        txtlist = f.readlines()
        f.close()
        if txtlist == []:
            return
        for i in txtlist:
            rclist = i.strip('\n').split()
            y, m, d, c, t = int(rclist[0]), int(rclist[1]), int(rclist[2]), int(rclist[3]), int(rclist[4])
            self.append_record(y, m, d, t, c)
        return

    def save(self):
        f = open(self.filename,'w')
        for y in self.record:
            for m in range(13):
                for d in range(32):
                    for c in range(7):
                        if self.record[y][m][d][c] == []:
                            continue
                        for t in range(len(self.record[y][m][d][c])):
                            f.write(str(y) + ' ' + str(m) + ' ' + str(d) + ' ' + str(c) + ' ' + str(self.record[y][m][d][c][t]) + '\n')
        f.close()
        return

class CLS_timer(object):
    def __init__(self):
        self.timer_time = [0,0,0,0]
        self.timer_stat = False
        # True: is recording the time, False: is not
        self.target_time = 60
        # in min
        self.current_time = None
        self.initial_time = None
        # [yyyy, mm, dd, hh, mm, ss]
        return

    def get_time(self):
        y, mt, d = int(time.strftime('%Y')), int(time.strftime('%m')), int(time.strftime('%d'))
        h, m, s = int(time.strftime('%H')), int(time.strftime('%M')), int(time.strftime('%S'))
        #t = time.time()
        #ms = t - int(t)
        return [y, mt, d, h, m, s]

    def set_target(self, target):
        self.target_time = target
        return

    def start_time(self):
        self.initial_time = self.get_time()
        self.timer_stat = True
        return

    def clear_time(self):
        self.initial_time = None
        self.target_time = None
        return

    def check_time(self):
        self.current_time = self.get_time()
        ctime = datetime.strptime(str(self.current_time), "[%Y, %m, %d, %H, %M, %S]")
        if self.timer_stat == False:
            return [int(self.current_time[3] // 10), int(self.current_time[3] % 10), int(self.current_time[4] // 10), int(self.current_time[4] % 10)], \
                self.current_time[5] % 2, 0, 0, False
        itime = datetime.strptime(str(self.initial_time), "[%Y, %m, %d, %H, %M, %S]")
        duration = (ctime - itime).total_seconds()
        t = time.time()
        duration += t - int(t)
        if duration >= self.target_time * 60:
            self.timer_stat = False
            return self.illustration_format(self.target_time * 60, True)
        return self.illustration_format(duration, False)

    def illustration_format(self, duration, flag):
        edangle = 360 * duration / (self.target_time * 60)
        if int(edangle) == 0:
            edangle = 1
        return [int(duration // 60 // 10), int(duration // 60 % 10), int(duration % 60 // 10), int(duration % 60 % 10)], \
            0, 0, edangle, flag


class CLS_calendar(object):
    def __init__(self, x, y, clr, bgclr, rw, r, font_name, font_clr, record, sz):
        self.x, self.y, self.w, self.h = x, y, SCREEN_HEIGHT, SCREEN_HEIGHT
        self.rw, self.r = rw, r
        self.clr, self.bgclr = clr, bgclr
        self.font_name, self.font_clr = font_name, font_clr
        self.grid = [[[-1, -1] for y in range(6)] for x in range(7)]
        self.display_time = time.strftime('%Y%m')
        self.record = record
        self.sz = sz
        self.clr_state = 0
        self.fill_grid()
        return
    
    def change_state(self, flag):
        self.clr_state = (self.clr_state + flag) % 7
        self.fill_grid()
        return
    
    def change_time(self, command, nt = None):
        #command: 1 = next month, -1 = prevmonth, 0 = newtime, 2 = next year, -2 = last year
        y, m = int(self.display_time[:4]), int(self.display_time[4:])
        if command == 1 or command == -1:
            y += (m - 1 + command) // 12
            m = (m -1 + command) % 12 + 1
        elif command == 2 or command == -2:
            y += command // 2
        self.display_time = str(y) + ('0' + str(m))[-2:]
        self.fill_grid()
        return

    def render_text(self, x, y, scr, txt, size, align = 'center'):
        fnt = pygame.font.Font(self.font_name, size)
        if align == 'center':
            txt_image = fnt.render(txt, True, self.font_clr)
            scr.blit(txt_image, (x - txt_image.get_width() / 2, y - txt_image.get_height() / 2))
        return

    def fill_grid(self):
        self.grid = [[[-1, -1] for x in range(7)] for y in range(6)]
        y, m = int(self.display_time[:4]), int(self.display_time[4:])
        initw = datetime.strptime(self.display_time + '01', "%Y%m%d").weekday()
        for d in range(calendar.monthrange(y, m)[1]):
            if self.clr_state == 0:
                t = 0
                r = self.record.check_record(y, m, d + 1, self.clr_state)
                for i in range(len(r)):
                    t += sum(r[i])
            else:
                t = sum(self.record.check_record(y, m, d + 1, self.clr_state))
            if t >= 8 * 60:
                darkness = 3
            elif t >= 4 * 60:
                darkness = 2
            elif t > 0:
                darkness = 1
            elif t == 0:
                darkness = 0
            self.grid[(d + initw) // 7][(d + initw) % 7][1] = darkness
            self.grid[(d + initw) // 7][(d + initw) % 7][0] = d + 1
        return
        
    def draw(self, scr):
        for y in range(6):
            for x in range(7):
                if self.grid[y][x][1] == -1:
                    clr = GR3
                    pygame.draw.circle(scr, clr, (self.x + (2 * x + 1) * self.sz , self.y + (2 * y + 3) * self.sz), self.r)
                    #pygame.gfxdraw.aacircle(scr, self.x + x * 70 + 35, 70 + self.y + y * 70 + 35, self.r, clr)
                else:
                    
                    if self.grid[y][x][1] == 0:
                        clr = GR2
                    elif self.grid[y][x][1] == 1:
                        clr = CLD_COLOR_LIST[self.clr_state][0]
                    elif self.grid[y][x][1] == 2:
                        clr = CLD_COLOR_LIST[self.clr_state][1]
                    elif self.grid[y][x][1] == 3:
                        clr = CLD_COLOR_LIST[self.clr_state][2]
                    pygame.draw.circle(scr, clr, (self.x + (2 * x + 1) * self.sz , self.y + (2 * y + 3) * self.sz), self.r)
                    #pygame.gfxdraw.aacircle(scr, self.x + x * 70 + 35, 70 + self.y + y * 70 + 35, self.r, clr) 
                    pygame.draw.circle(scr, self.bgclr, (self.x + (2 * x + 1) * self.sz , self.y + (2 * y + 3) * self.sz), self.r - self.rw)
                    #pygame.gfxdraw.aacircle(scr, self.x + x * 70 + 35, 70 + self.y + y * 70 + 35, self.r - self.rw, self.bgclr) 
                    self.render_text(self.x + (2 * x + 1) * self.sz , self.y + (2 * y + 3) * self.sz, scr, str(self.grid[y][x][0]), 20)
        self.render_text(250, 70, scr, self.display_time[:4] + ' ' + self.display_time[4:], 50)
        return

class CLS_window(object):
    def __init__(self, btnlist_1, btnlist_2, btnlist_3, btnlist_4, btnlist_5, record, timer, dial, calendar, textbox):
        self.btnlist_1, self.btnlist_2, self.btnlist_3, self.btnlist_4, self.btnlist_5 = btnlist_1, btnlist_2, btnlist_3, btnlist_4, btnlist_5
        self.record = record
        self.timer = timer
        self.dial = dial
        self.screen_stat = 0
        self.calendar = calendar
        self.textbox = textbox
        self.motion_state = False
        self.motion_cnt = 0
        self.motion_flag = True
        
        return

    def draw(self, scr):
        #print(self.motion_state)
        if self.screen_stat == 0:
            #btn_calendar_label.display_stat = False
            num, flag, stangle, edangle, endflag = self.timer.check_time()
            self.dial.draw(scr, num, flag, stangle, edangle)
            if endflag == True: #计时结束
                t = self.timer.get_time()
                self.record.append_record(t[0], t[1], t[2], self.timer.target_time, btn_label.dflag)
                self.timer.clear_time()
                self.timer.timer_stat == False
                self.btnlist_1[0].stat = True

            for i in self.btnlist_1:
                i.draw(scr)
            for i in self.btnlist_5:
                i.draw(scr)

        elif self.screen_stat == 1:
            scr.fill(WHITE)
            self.calendar.draw(scr)
            for i in self.btnlist_2:
                i.draw(scr)
        for i in self.btnlist_4:
            i.draw(scr)
        self.textbox.draw(scr)

        if self.motion_state == True:
            #print('True')
            pygame.draw.rect(scr, PURPLE, (520, self.motion_cnt, 100, 10))
            pygame.draw.rect(scr, GR1, (520, 0, 100, self.motion_cnt))
            ang = 180 * self.motion_cnt // 500
            btn_tabbar.draw(scr, ang)
            if self.motion_flag == True:
                self.motion_cnt += 50
            else:
                self.motion_cnt -= 50

            if self.motion_cnt <= 0 or self.motion_cnt >= 500:
                self.motion_state = False
                if self.motion_flag == True:
                    for i in range(len(self.btnlist_3)):
                        self.btnlist_3[i].display_stat = True

                else:
                    for i in range(len(self.btnlist_3)):
                        self.btnlist_3[i].display_stat = False
                self.motion_flag = 1 - self.motion_flag
                #print(self.motion_flag)

        elif self.motion_flag == False:
            pygame.draw.rect(scr, GR1, (520, 0, 100, 500))
            btn_tabbar.draw(scr)
            for i in self.btnlist_3:
                i.draw(scr)

        return

    def update(self, scr):
        self.draw(scr)
        return

    def mousedown(self, event, scr):
        for i in self.btnlist_1:
            i.isme(event.pos)
        for i in self.btnlist_2:
            i.isme(event.pos)
        for i in self.btnlist_3:
            i.isme(event.pos)
        for i in self.btnlist_4:
            i.isme(event.pos)
        for i in self.btnlist_5:
            i.isme(event.pos)
        self.textbox.isme(event.pos)
        return

    def keydown(self, event, scr):
        '''
        if event.key == pygame.K_z:
            self.screen_stat = 1
            for i in self.btnlist_2:
                i.display_stat = True
            for i in self.btnlist_1:
                i.display_stat = False

        elif event.key == pygame.K_x:
            self.screen_stat = 0
            for i in self.btnlist_2:
                i.display_stat = False
            for i in self.btnlist_1:
                i.display_stat = True
        
        if self.screen_stat == 1:
            if event.key == pygame.K_LEFT:
                self.calendar.change_time(-1)
            elif event.key == pygame.K_RIGHT:
                self.calendar.change_time(1)
            elif event.key == pygame.K_DOWN:
                self.calendar.change_time(-2)
            elif event.key == pygame.K_UP:
                self.calendar.change_time(2)
            elif event.key == pygame.K_q:
                self.calendar.change_state(1)
            elif event.key == pygame.K_w:
                self.calendar.change_state(-1)
        '''
        if self.screen_stat == 0:
            self.textbox.keydown(event.key)
        return
    
#
def callback_btn_play():
    if btn_play.stat == True and timer.timer_stat == False:
        btn_timedsp.change_txt(textbox.txt)
        target_time = int(textbox.txt)
        timer.set_target(target_time)
        btn_play.stat == False
        timer.start_time()
        for i in range(4):
            btnlist_5[i].display_stat = False
    elif btn_play.stat == False:
        #todo 暂停继续
        return
    textbox.display_stat = False
    return

def callback_btn_tabbar():
    window.motion_state = True
    return

def callback_btn_timedsp():
    textbox.display_stat = 1 - textbox.display_stat
    if textbox.display_stat == True:
        textbox.isme((210,140))
        #print('sth')
    else:
        btn_timedsp.change_txt(textbox.txt)
    for i in range(4):
        btnlist_5[i].display_stat = 1 - btnlist_5[i].display_stat
    return

def callback_textbox():
    btn_timedsp.change_txt(textbox.txt)
    return

def callback_btn_textbox_rs():
    textbox.change_text(5)
    return

def callback_btn_textbox_rb():
    textbox.change_text(15)
    return

def callback_btn_textbox_ls():
    textbox.change_text(-5)
    return

def callback_btn_textbox_lb():
    textbox.change_text(-15)
    return

def callback_btn_label():
    btn_label.dflag = (btn_label.dflag + 1) % len(COLOR_LIST)
    btn_label.surf = gen_icon_img((PURPLE), WHITE, btn_label.r, btn_label.w, 4, fclr = COLOR_LIST[btn_label.dflag], img=btn_label.dflag)
    return

def callback_btn_calendar_label():
    btn_calendar_label.dflag = (btn_calendar_label.dflag + 1) % len(COLOR_LIST)
    btn_calendar_label.surf = gen_icon_img((GREY_LIST[2]), WHITE, btn_calendar_label.r, btn_calendar_label.w, 4, fclr = COLOR_LIST[btn_calendar_label.dflag], img=btn_calendar_label.dflag)
    cld.change_state(1)
    return

def callback_btn_calendar_rmonth():
    cld.change_time(1)
    return

def callback_btn_calendar_lmonth():
    cld.change_time(-1)
    return

def callback_btn_calendar_ryear():
    cld.change_time(2)
    return

def callback_btn_calendar_lyear():
    cld.change_time(-2)
    return

def callback_btn_switch():
    #print('sth')
    if window.screen_stat == 0:
        window.screen_stat = 1
        for i in window.btnlist_2:
            i.display_stat = True
        for i in window.btnlist_1:
            i.display_stat = False
        for i in window.btnlist_5:
            i.display_stat = False
        textbox.display_stat = False
        return
    elif window.screen_stat == 1:
        window.screen_stat = 0
        for i in window.btnlist_2:
            i.display_stat = False
        for i in window.btnlist_1:
            i.display_stat = True
        return

#==========================================================================================================================================

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
pygame.font.init()

screen.fill(WHITE)
digit_display = CLS_digit_display(114, 195, 50, 90, GR4, WHITE, GR1, 10, 3, 10, 12)
dial = CLS_dial(250, 250, 25, 190, PURPLE, WHITE, GR2, digit_display)

imglist = []
for i in range(5):
    imglist.append(load_img(str(i) + '.png', 418, 34))

switch_img = load_img('switch.png', 418, 40)
tabbar_img = load_img('change.png', 418, 40)

btn_play = CLS_button(210, 310, 40, 5, PURPLE, WHITE, True, 1, True)
btn_pause = CLS_button(210, 310, 40, 5, PURPLE, WHITE, True, 2, False)
btn_label = CLS_button(300, 320, 30, 5, PURPLE, WHITE, True, 4, True)
btn_timedsp = CLS_button(140, 320, 30, 5, PURPLE, WHITE, True, 11, True, font_name= "AGENCYB.TTF", font_clr=GR4, font_size=30)
btn_switch = CLS_button(530, 410, 30, 5, PURPLE, WHITE, True, 9, False)
btn_tabbar = CLS_button(530, 50, 30, 5, PURPLE, WHITE, True, 10, True)
btn_textbox_rs = CLS_button(300, 135, 20, 5, GREY_LIST[3], WHITE, True, 6, False)
btn_textbox_ls = CLS_button(150, 135, 20, 5, GREY_LIST[3], WHITE, True, 5, False)
btn_textbox_rb = CLS_button(325, 135, 20, 5, GREY_LIST[2], WHITE, True, 8, False)
btn_textbox_lb = CLS_button(125, 135, 20, 5, GREY_LIST[2], WHITE, True, 7, False)


btn_calendar_label = CLS_button(465, 415, 25, 5, GREY_LIST[2], WHITE, True, 4, False, PURPLE)
btn_calendar_rmonth = CLS_button(350, 40, 30, 5, GREY_LIST[3], WHITE, True, 6, False)
btn_calendar_lmonth = CLS_button(90, 40, 30, 5, GREY_LIST[3], WHITE, True, 5, False)
btn_calendar_ryear = CLS_button(400, 40, 30, 5, GREY_LIST[2], WHITE, True, 8, False)
btn_calendar_lyear = CLS_button(40, 40, 30, 5, GREY_LIST[2], WHITE, True, 7, False)

btn_play.callback_click = callback_btn_play
btn_label.callback_click = callback_btn_label
btn_switch.callback_click = callback_btn_switch
btn_tabbar.callback_click = callback_btn_tabbar
btn_timedsp.callback_click = callback_btn_timedsp
btn_calendar_label.callback_click = callback_btn_calendar_label
btn_calendar_rmonth.callback_click = callback_btn_calendar_rmonth
btn_calendar_lmonth.callback_click = callback_btn_calendar_lmonth
btn_calendar_ryear.callback_click = callback_btn_calendar_ryear
btn_calendar_lyear.callback_click = callback_btn_calendar_lyear
btn_textbox_lb.callback_click = callback_btn_textbox_lb
btn_textbox_ls.callback_click = callback_btn_textbox_ls
btn_textbox_rb.callback_click = callback_btn_textbox_rb
btn_textbox_rs.callback_click = callback_btn_textbox_rs


trecord = CLS_record('record.txt')
timer = CLS_timer()
btnlist_1 = [btn_play, btn_label, btn_timedsp]
btnlist_2 = [btn_calendar_label, btn_calendar_rmonth, btn_calendar_lmonth, btn_calendar_ryear, btn_calendar_lyear]
btnlist_3 = [btn_switch]
btnlist_4 = [btn_tabbar]
btnlist_5 = [btn_textbox_rs, btn_textbox_ls, btn_textbox_rb, btn_textbox_lb, btn_pause]

textbox = CLS_text_box(200, 130, 100, 50, PURPLE, GREY_LIST[1], "AGENCYB.TTF", 30, GREY_LIST[3])
textbox.callback_changetime = callback_textbox
textbox.callback_changetime()

cld = CLS_calendar(40, 50, PURPLE, WHITE, 10, 25, "AGENCYB.TTF", GR4, trecord, 30)
window = CLS_window(btnlist_1, btnlist_2, btnlist_3, btnlist_4, btnlist_5, trecord, timer, dial, cld, textbox)
#cld.display_time = '202101'
#cld.fill_grid()


#sf = load_img('1.png', 418, 60)

while True:
    #print(btn_switch0.stat, btn_switch1.stat)
    #dial.draw(screen, num, s % 2, 0, (s + ms) * 6)
    window.draw(screen)
    #screen.fill((0,0,0))
    #screen.blit(sf, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            window.mousedown(event, screen)
        if event.type == pygame.KEYDOWN:
            window.keydown(event, screen)

    #screen.blit(gen_icon_img(PURPLE, (240,240,240), 40, 5, 1), (0, 0))
    #screen.blit(gen_icon_img(PURPLE, (240,240,240), 40, 5, 4), (100, 0))

    pygame.display.update()
    clock.tick(20)


