
from contextlib import nullcontext
from email.policy import default
import re
from string import ascii_uppercase
from tabnanny import check
from collections import OrderedDict, defaultdict
import pygame, sys, csv
import pandas as pd
pygame.init()

class Setup():
    def __init__(self):
        self.myfont = pygame.font.SysFont("monospace", 22) 
        self.seat_font = pygame.font.SysFont("monospace", 15)
        seats_dict = Stadium().seats_dict
        size = width, height = 1200, 920
        rect_color = 255, 0, 0
        self.res_check = 0
        screen_color = 211, 211, 211
        clicked_rects = []
        self.saved_seats = []
        total = 0
        self.screen = pygame.display.set_mode(size)
        self.square_size = 50
        self.screen.fill(screen_color)
        self.Extra_Layout(self.screen, rect_color)
        self.Create_Grid(self.screen, width, height, self.square_size, seats_dict)
        while 1:
            for event in pygame.event.get():
                pos = pygame.mouse.get_pos()
                if event.type == pygame.MOUSEBUTTONUP:
                    self.Update_grid(pos, clicked_rects, seats_dict, total, self.screen)
                if event.type == pygame.QUIT: 
                    sys.exit()
            pygame.display.flip()
    def seat_Compare(self, letter, seat_num, check_total):   
        addition = 1      
        for record in df:
            if letter == record and df.empty != True:
                letter_index = ascii_uppercase.index(letter)
                #print("THIS DUDE: ",df.iloc[:, ascii_uppercase.index(letter)][1]) # this finds the second index of the column starting at 0,
                # need to increase count by 1 each time it goes through a num in the df to go to the next row
                num = df.iloc[:, letter_index][check_total]
                values = df.iloc[:, letter_index].value_counts()
                if float(seat_num) == float(num): 
                    #if numbers match, set seat color to red and add 1 to counter to move onto next seat
                    #print("NUM: ", num)
                    self.saved_seats.append(str(letter_index) + "," + str(int(num)))
                    #print("CHECK: ", check_total, "Vals: ", len(values))
                    if (len(values)-1) == (check_total):
                        #print("hit 3")
                        addition = 0
                    return (255, 0 , 0), addition
                        
                else: 
                    #if numbers don't match, set color to black
                    return (0, 0, 0), 0


    def Create_Grid(self, screen, width, height, square_size, seats_dict):
        row_count = 0
        check = 0
        check_total = 0
        color = (0,0,0)
        self.row_list = []
        self.rect_obj_row = []
        row_count = 0
        column_count = 0
        for row in range(4, 14): #x coordinates of grid, each number represents a square, numbers represent positioning, difference between start and stop is number of seats in row           
            letter = ascii_uppercase[row_count]
            seat_count = 0
            column_list = []
            self.rect_obj_col = []
            check_total = 0

            for column in range(2, 22): #y coordinates of grid, difference is number of seats in column
                column_count += 1

                if df.empty != True:
                    color, check = self.seat_Compare(str(ascii_uppercase[row_count]), str(column_count), check_total)
                check_total += check

                rect = pygame.Rect(column*self.square_size, row*self.square_size, self.square_size, self.square_size) #creates a square relative to position
                pygame.draw.rect(screen, color, rect, width = 2, border_radius=5 )

                seat_count +=1             
                seat_identity = letter + str(seat_count) 
                seat_identity_visual = self.seat_font.render(seat_identity, 1, (0,0,0))
                self.screen.blit(seat_identity_visual, (column*self.square_size + 13, row*self.square_size+13))
                rect_pos = [column*self.square_size, row*self.square_size]
                column_list.append(rect_pos)
                self.rect_obj_col.append(rect)

            row_count +=1
            column_count = 0
            self.rect_obj_row.append(self.rect_obj_col)
            self.row_list.append(column_list)
        self.del_row_list()

    def del_row_list(self):
        print(self.row_list)        
        for elements in self.saved_seats:
            let, number = elements.split(",")
            diff = 20 - len(self.row_list[int(let)])
            number = int(number) - 1 - diff
            self.row_list[int(let)].pop(number)

    def Extra_Layout(self, screen, rect_color):
        pygame.draw.rect(screen, rect_color, (270, 20, 650, 20), 3, border_radius=20)
        label = self.myfont.render("Screen", 1, (0,0,0))
        screen.blit(label, (550, 17))

        pygame.draw.rect(screen, (0, 255, 0), (538, 820, 130, 90), 4, border_radius=50)
        label4 = self.myfont.render("RESERVE", 1, (0,0,0))
        screen.blit(label4, (558, 850))

    def res_button(self, pos, clicked_rects, seats_dict, total, screen):
        if pos[0] > 538 and pos[0] < 668 and pos[1] > 820 and pos[1] < 910: #RESERVE BUTTON, could be its own function 
            pygame.draw.rect(self.screen, (211, 211, 211), (538, 820, 130, 90), 50)
            pygame.draw.rect(self.screen, (0, 255, 255), (538, 820, 130, 90), 4, border_radius=50)
            final_label = self.myfont.render("THANK YOU", 1, (0,0,0))
            screen.blit(final_label, (545, 850))
            for item in clicked_rects:
                for r in self.row_list:
                    for stuff in r:
                        if stuff == item:   # stuff was r                        
                            place1 = self.row_list.index(r)
                            place2 = r.index(stuff) #stuff was r
                            print(ascii_uppercase[place1], 3)
                            APEX.reserve(ascii_uppercase[place1], place2)
                            total += seats_dict[ascii_uppercase[place1]]
                            fixed_total = "{:.2f}".format(total)
                            pygame.draw.rect(self.screen, (211, 211, 211), (183, 820, 250, 90), 50)
                            sublabel = self.myfont.render(str("Subtotal: $" + fixed_total), 1, (0,0,0))
                            self.screen.blit(sublabel, (183, 850))
            self.res_check = 1    

    def Update_grid(self, pos, clicked_rects, seats_dict, total, screen):
        count = -1
        innercount = -1
        check = 0
        if self.res_check != 1:
            self.res_button(pos, clicked_rects, seats_dict, total, screen)
            for rects in self.row_list:
                count +=1
                for rect in rects:
                    innercount +=1
                    if pos[0] > rect[0] and pos[0] < (rect[0] + 50) and pos[1] > rect[1] and pos[1] < (rect[1] + 50): #SEAT BUTTONS
                        x = rect[0]
                        y = rect[1]
                        pygame.draw.rect(self.screen, (0, 255, 255), (x, y, 50, 50), 2, border_radius=5 )
                        rcords = [x,y] 
                    
                        if rcords in clicked_rects:
                            pygame.draw.rect(self.screen, (0, 0, 0), (x, y, 50, 50), 2, border_radius=5 )
                            price, name = APEX.seat_info(seats_dict, self.row_list, total, rcords)
                            sublabel = self.myfont.render(("Seat: " + name + " | Seat Price: $" + price), 1, (0,0,0))
                            check = 1
                            
                        if rcords not in clicked_rects:
                            pygame.draw.rect(self.screen, (211, 211, 211), (683, 820, 500, 90))
                            clicked_rects.append(rcords)
                            price, name = APEX.seat_info(seats_dict, self.row_list, total,rcords)
                            sublabel = self.myfont.render(("Seat: " + name + " | Seat Price: $" + price), 1, (0,0,0))                       
                            self.screen.blit(sublabel, (700, 850))
                        
                        if check == 1:
                            clicked_rects.remove(rcords)

                        if len(clicked_rects) < 1:
                            pygame.draw.rect(self.screen, (0, 255, 0), (538, 820, 130, 90), 4, border_radius=50)
                            pygame.draw.rect(self.screen, (211, 211, 211), (183, 820, 250, 90), 50)
                            total = 0                                 
                    innercount = -1

class Stadium():
    b_price = 6   #base price, can be changed
    def __init__(self):
        self.seats_dict = {}
        self.reserved = {}
        self.__assignment()

    def __assignment(self):
        for i in ascii_uppercase[:10]:
            self.reserved[i] = []
            self.seats_dict[i] = []
            for seat_num in range(0,20):
                self.seats_dict[i] = (Seat(i, seat_num+1).get_price())

    def write_to_file(self, reserved):
        #TBD: set row letters to actual rows within excell file - easy fix
        global df
        df2=pd.DataFrame(dict([ (k,pd.Series(v)) for k,v in reserved.items() ]))
        x  = df.append(df2)
        print("DF AFTER: \n", x)
        x.reset_index(drop=True, inplace=True)
        x.to_excel("C:\\Users\\Will-Meister\\Desktop\\stuff99\\Stadium_PROJECT\\Seats.xlsx", index = False)               

    def reserve(self, row_letter, seat_num): 
        seat_num = seat_num + 1
        if seat_num not in self.reserved[row_letter]:
            print("SEAT ", seat_num)
            self.reserved[row_letter].append(seat_num)
            for rows in self.reserved:
                self.reserved[rows].sort()
                print(self.reserved[rows])
            a = self.reserved
            self.write_to_file(a)
        else:
            print("Seat already taken")
            return False

        print (row_letter, " - ", self.reserved[row_letter])
    
    def budget(self, min, max):
        for row in self.seats_dict:
            for seat in self.seats_dict[row]:
                if Seat.get_price(seat) > min and Seat.get_price(seat) < max: 
                    print(seat, "is in budget")
    
    def seat_info(self, seats_dict, row_list, total, rcords):
        for r in row_list:
            for stuff in r:
                if stuff == rcords:
                    print("ITS IN") 
                    place1 = row_list.index(r)
                    place2 = r.index(stuff) + 1
                    name = str(ascii_uppercase[place1]) + str(place2)
                    total += seats_dict[ascii_uppercase[place1]] 
                    fixed_total = "{:.2f}".format(total)
                    return str(fixed_total), str(name)

class Seat():
    def __init__(self, row_letter, seat_num):
        self.seat_list = []
        self.row_letter = row_letter
        self.seat_num = seat_num
        self.price = self.__seat_price()
        self.seat_list.append(self.seat_num)
        self.seat_list.append(self.price)

    def __seat_price(self):
        x = 2 - (round(abs(69.5 - ord(self.row_letter)))/10) 
        y = Stadium.b_price * (x)
        y = "{:.2f}".format(y)
        return float(y)

    def get_price(self):
        return self.price      

    def __repr__(self):
        return (str(self.seat_list))

if __name__ == "__main__":
    read = pd.read_excel("C:\\Users\\Will-Meister\\Desktop\\stuff99\\Stadium_PROJECT\\Seats.xlsx")
    df = pd.DataFrame(read)
    APEX = Stadium()
    window = Setup()
