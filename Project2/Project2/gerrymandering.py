"""
Name:Emnet Mekonnen
Date:10/26/2023
CSC 201
Project 2-Gerrymandering

This programs analyzes the voting in the state entered by the user for a particular election
whose data is stored in a file. The program displays that voting data from that state by district
in a stacked bar chart, displays the statistics by district used to determine gerrymandering,
and computes whether there was gerrymandering in this election in favor of the Democrats or Republicans.

Document Assistance: (who and what  OR  declare that you gave or received no assistance):
Proffesor Mueller helped me with the values for the for loop in order to get the values for district, democratic votes and republican votes


"""

from graphics2 import *

FILE_NAME = 'districts.txt'
MIN_NUM_DISTRICTS = 2
EFFICIENCY_GAP_LIMIT = 8

WINDOW_WIDTH = 500
WINDOW_HEIGHT = 750
DEFAULT_BAR_HEIGHT = 20
SPACE_BETWEEN = 5

def main():
    #opens file
    f_in = open(FILE_NAME, "r")
    
        
    state_input = input("Which state do you want to look up? " )
    state_input = state_input.title()

    #reads and splits the file 
    for line in f_in:
        line_list = line.split(",")
        state = line_list[0]
        if state == state_input:
            votes_list = line_list[1:]
            
    # make window
    window = GraphWin(f"District overview for {state_input}", WINDOW_WIDTH, WINDOW_HEIGHT)
    window.setBackground('white')
    
    #draw line
    line_mid = Line(Point(WINDOW_WIDTH/2,0), Point(WINDOW_WIDTH/2,WINDOW_HEIGHT))
    line_mid.draw(window)
            
      
    print() 
    print(f"District   Democratic Votes   Republican Votes   Surplus Democrat   Surplus Republican")
    
    #initializations
    total_surplus_dem = 0
    total_surplus_rep = 0
    total_votes = 0
    dem_counter = 0
    rep_counter = 0
    total_dem_votes = 0
    total_rep_votes = 0
    num_districts = len(votes_list)/3
    change = SPACE_BETWEEN
    bar_height = DEFAULT_BAR_HEIGHT
    
    for index in range(0, len(votes_list), 3):
        district = votes_list[index]
        dem_votes = int(votes_list[index + 1])
        rep_votes = int(votes_list[index + 2])
        total_dem_votes = total_dem_votes + dem_votes
        total_rep_votes = total_rep_votes + rep_votes
        total_votes = total_votes + dem_votes + rep_votes 
        total_district_votes = dem_votes + rep_votes  
        
        #counts how many districts democrats and republicans have won
        if dem_votes > rep_votes:
            dem_counter = dem_counter + 1
        elif rep_votes > dem_votes:
            rep_counter = rep_counter + 1
            
        #  calclulates the surplus         
        majority = (dem_votes + rep_votes) // 2 + 1
        if dem_votes > rep_votes:
            surplus_dem = dem_votes - majority
            surplus_rep = rep_votes
        elif rep_votes > dem_votes:
            surplus_rep = rep_votes - majority
            surplus_dem = dem_votes
        elif rep_votes == dem_votes:
            surplus_dem = 0
            surplus_rep = 0
        print(f"{district:>4}{dem_votes:19,}{rep_votes:19,}{surplus_dem:19,}{surplus_rep:19,}")
        
        # total surplus dem and rep votes
        total_surplus_dem = surplus_dem + total_surplus_dem
        total_surplus_rep = surplus_rep + total_surplus_rep
        
        
        #GRAPHICS
        
        # if num bars don't fit in the window
        if num_districts * (bar_height + SPACE_BETWEEN) > WINDOW_HEIGHT:
            bar_height = (WINDOW_HEIGHT - num_districts * SPACE_BETWEEN)/num_districts
        
        #rep and dem bars
        if total_district_votes != 0:
            dem_bar_width = (dem_votes / total_district_votes) * WINDOW_WIDTH
            
            upper_left_dem = Point(0, change) 
            lower_right_dem = Point(dem_bar_width, change + bar_height)
            dem_bar = Rectangle(upper_left_dem, lower_right_dem)
            dem_bar.setFill('blue')
            dem_bar.draw(window)
            
                
            upper_left_rep = Point(500, change) 
            lower_right_rep = Point(dem_bar_width, change + bar_height) 
            rep_bar = Rectangle(upper_left_rep, lower_right_rep)
            rep_bar.setFill('red')
            rep_bar.draw(window)
             
            
        change = change + bar_height + SPACE_BETWEEN

        
    #who gets more seats
    if dem_counter > rep_counter:
        winner = "Democrats"
    else:
        winner = "Republicans"
        
    print()
    print(f"Total surplus Democratic votes: {total_surplus_dem:,}")
    print(f"Total surplus Republican votes: {total_surplus_rep:,}")
    
    
    
    #gerrymandering test
    if num_districts > MIN_NUM_DISTRICTS:
        if total_surplus_dem > total_surplus_rep:
            efficiency_gap = round(((total_surplus_dem - total_surplus_rep) / total_votes), 4) * 100

        elif total_surplus_rep > total_surplus_dem: 
            efficiency_gap = round(((total_surplus_rep - total_surplus_dem) / total_votes), 4) * 100
        #num_seats
        if efficiency_gap > EFFICIENCY_GAP_LIMIT:
            num_seats = efficiency_gap / (100 / num_districts)
            print(f"Gerrymandering in {state_input} favoring {winner} worth {num_seats:0.2f} congressional seats.")
        else:
            print(f"No evidence of gerrymandering in {state_input}.")
        
    else:
        print("Gerrymandering computation only valid when more than {MIN_NUM_DISTRICTS} districts.")
    
   
    
main()