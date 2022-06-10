"""
20 rows of seats
different algorithms for seat pricing, user can select variation depending on event

***Classic Algorithm***
each row has a ranking that increases in price relative to closeness to stage
Ex: base price (x), seat price (y), y = x * 1.10 ** (something * count)

Stadium class
-name of stadium
-assigns algorithm of choice
-stores different stadium layouts

Seat class
-stores dictionary of seats, rows going from A-Z with base price & actual seat number corresponding to letter
-records which seats are available
"""
#button class that stores each rect object, have button method within that takes x,y parameters and compares rect coords with click cords
#have button method that takes parameters: x, y

#TBD
'''
-Reserve Funciton
    -start from scratch
    -save input row letter and number to csv
    -have csv file be read on launch and change color of seat to red if file matches seat
    -NOTES************
        -Use Pandas to Convert CSV File to Dictionary in Python - would pandas be better? FUCK ALL THAT USE PANDAS AND CLEAN THIS SHIT EASY
        After importing pandas, make use of its built-in function read_csv() with a few parameters to specify the csv file format. 
        After calling read_csv() , convert the result to a dictionary using the built-in pandas function to_dict() .

-red is drawn on seats saved into excell file, need to set it so those seats are removed from the rects list to not allow for selection (drawing another rect to cover up the red)

'''

from contextlib import nullcontext
from string import ascii_uppercase
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
        screen_color = 211, 211, 211
        clicked_rects = []
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
                    self.Update_grid(pos, clicked_rects, seats_dict, total)
                if event.type == pygame.QUIT: 
                    sys.exit()
            pygame.display.flip()

    def seat_Compare(self, letter, seat_num):
        for record in df:
            if letter == record:
                print("MATCH")
                for num in df[record]:
                    print("SEAT NUM", seat_num, " == ", num)
                    if float(seat_num) == num:
                        print("RED")
                        return (255, 0 , 0)
                        
                    else:
                        print("BLACK")
                        return (0, 0, 0)


    def Create_Grid(self, screen, width, height, square_size, seats_dict):
        row_count = 0
        rect_color = 255, 0, 0
        BLACK = (0, 0, 0)
        WHITE = (200, 200, 200) 
        self.row_list = []
        self.rect_obj_row = []
        row_count = 0
        column_count = 0
        for row in range(4, 14): #x coordinates of grid, each number represents a square, numbers represent positioning, difference between start and stop is number of seats in row           
            letter = ascii_uppercase[row_count]
            seat_count = 0
            column_list = []
            self.rect_obj_col = []
            for column in range(2, 22): #y coordinates of grid, difference is number of seats in column
                column_count += 1
                #print(row_count)
                #print(letter)
                current_seat = str(ascii_uppercase[row_count]) + str(column_count)#THIS IS THE ADDITION
                print("ROW COUNT", row_count)
                print("COLUMN COUNT", column_count)
                color = self.seat_Compare(str(ascii_uppercase[row_count]), str(column_count))
                print("CURRENT SEAT:", current_seat, " - COLOR: ", color)

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

        #print("ROW LIST: ",self.row_list)
        #print("\n\n\n OBJS: ", self.rect_obj_row)

    def Extra_Layout(self, screen, rect_color):
        pygame.draw.rect(screen, rect_color, (270, 20, 650, 20), 3, border_radius=20)
        label = self.myfont.render("Screen", 1, (0,0,0))
        screen.blit(label, (550, 17))

        pygame.draw.rect(screen, (0, 0, 0), (415, 730, 70, 70), 2) #budget buttons
        label1 = self.myfont.render("<$8", 1, (0,0,0))
        screen.blit(label1, (425, 750))

        pygame.draw.rect(screen, (0, 0, 0), (515, 730, 70, 70), 2)
        label2 = self.myfont.render("<$10", 1, (0,0,0))
        screen.blit(label2, (525, 750))

        pygame.draw.rect(screen, (0, 0, 0), (615, 730, 70, 70), 2)
        label3 = self.myfont.render("<$12", 1, (0,0,0))
        screen.blit(label3, (625, 750))

        pygame.draw.rect(screen, (0, 0, 0), (715, 730, 70, 70), 2)
        label4 = self.myfont.render("<$14", 1, (0,0,0))
        screen.blit(label4, (725, 750))

        pygame.draw.rect(screen, (0, 255, 0), (538, 820, 130, 90), 4, border_radius=50)
        label4 = self.myfont.render("RESERVE", 1, (0,0,0))
        screen.blit(label4, (558, 850))


    def Update_grid(self, pos, clicked_rects, seats_dict, total):
        count = -1
        innercount = -1
        check = 0
        if pos[0] > 538 and pos[0] < 668 and pos[1] > 820 and pos[1] < 910: #RESERVE BUTTON, could be its own function tbh
            pygame.draw.rect(self.screen, (0, 255, 255), (538, 820, 130, 90), 4, border_radius=50)
            for item in clicked_rects:
                print(item)
                for r in self.row_list:
                    for stuff in r:
                        if stuff == item:
                            print("ITS IN")                            
                            place1 = self.row_list.index(r)
                            place2 = r.index(stuff)
                            print(ascii_uppercase[place1], 3)
                            APEX.reserve(ascii_uppercase[place1], place2)
                            total += seats_dict[ascii_uppercase[place1]]
                            fixed_total = "{:.2f}".format(total)
                            pygame.draw.rect(self.screen, (211, 211, 211), (183, 820, 250, 90), 50)
                            sublabel = self.myfont.render(str("Subtotal: $" + fixed_total), 1, (0,0,0))
                            self.screen.blit(sublabel, (183, 850))
                                   
        for rects in self.row_list:
            count +=1
            for rect in rects:
                innercount +=1
                if pos[0] > rect[0] and pos[0] < (rect[0] + 50) and pos[1] > rect[1] and pos[1] < (rect[1] + 50): #SEAT BUTTONS
                    x = rect[0]
                    y = rect[1]
                    pygame.draw.rect(self.screen, (0, 255, 200), (x, y, 50, 50), 2, border_radius=5 )
                    rcords = [x,y] 
                
                    if rcords in clicked_rects:
                        pygame.draw.rect(self.screen, (0, 0, 0), (x, y, 50, 50), 2, border_radius=5 )
                        pygame.draw.rect(self.screen, (211, 211, 211), (683, 820, 500, 90))
                        price, name = APEX.seat_info(clicked_rects, seats_dict, self.row_list, total, rcords)
                        print(name, price)
                        sublabel = self.myfont.render(("Seat: " + name + " | Seat Price: $" + price), 1, (0,0,0))
                        check = 1
                        
                    if rcords not in clicked_rects:
                        pygame.draw.rect(self.screen, (211, 211, 211), (683, 820, 500, 90))
                        clicked_rects.append(rcords)
                        price, name = APEX.seat_info(clicked_rects, seats_dict, self.row_list, total,rcords)
                        print(name, price)
                        sublabel = self.myfont.render(("Seat: " + name + " | Seat Price: $" + price), 1, (0,0,0))                       
                        self.screen.blit(sublabel, (700, 850))
                    
                    if check == 1:
                        clicked_rects.remove(rcords)
                    print("Clicked Rects: ", clicked_rects)

                    if len(clicked_rects) < 1:
                        pygame.draw.rect(self.screen, (0, 255, 0), (538, 820, 130, 90), 4, border_radius=50)
                        pygame.draw.rect(self.screen, (211, 211, 211), (183, 820, 250, 90), 50)
                        total = 0                                 
                innercount = -1

class Stadium():
    b_price = 6   #this eventually will be an input in constructor
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
        
        print(self.seats_dict)

    def reserve(self, row_letter, seat_num): #to do: add I/O for reserving, show total price of each seat in cart, store who has what seats_dict
        if seat_num not in self.reserved[row_letter]:
            self.reserved[row_letter].append(seat_num)
            print("Row: " , row_letter, "|", "Seat #: " , seat_num, "|",  "Price: " , Seat(row_letter, seat_num).get_price())
            print(self.reserved)

        else:
            print("Seat already taken")
            return False
        print (row_letter, " - ", self.reserved[row_letter])
    
    def budget(self, min, max):
        for row in self.seats_dict:
            for seat in self.seats_dict[row]:
                if Seat.get_price(seat) > min and Seat.get_price(seat) < max: 
                    print(seat, "is in budget")
    
    def seat_info(self, clicked_rects, seats_dict, row_list, total, rcords):
        for r in row_list:
            for stuff in r:
                if stuff == rcords:
                    print("ITS IN") 
                    place1 = row_list.index(r)
                    place2 = r.index(stuff) + 1
                    name = str(ascii_uppercase[place1]) + str(place2)
                    APEX.reserve(ascii_uppercase[place1], place2)
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
    df = pd.read_excel("C:\\Users\\Will-Meister\\Desktop\\stuff99\\Stadium_PROJECT\\Seats.xlsx")
    df.to_dict('records')
    APEX = Stadium()
    window = Setup()
# APEX.reserve("B", 1)
# APEX.reserve("B", 5)
# APEX.reserve("B", 1)
# APEX.reserve("A", 13)
# APEX.budget(50, 110)