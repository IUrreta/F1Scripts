import sqlite3
import random



def run_script(option=""):
    conn = sqlite3.connect("scripts/result/main.db")
    cursor = conn.cursor()

    text = option.lower()
    params = text.split()


    driver = params[1].capitalize()
    #gets the driver id of the driver you want to transfer
    multiple_drivers = ["Perez", "Raikkonen", "Hulkenberg", "Toth", "Stanek", "Villagomez", "Bolukbasi", "Marti"]
    for i in range(len(multiple_drivers)):
        if(driver == multiple_drivers[i]):
            driver = driver + "1"
    if(driver == "Aleclerc"):
        driver_id = (132,)  
    elif(driver == "Devries"):
        driver_id = (76,)        
    else:
        driver_id = cursor.execute('SELECT StaffID FROM Staff_CommonData WHERE StaffType = 0 AND LastName = "[StaffName_Surname_' + str(driver) + ']"').fetchone()

    if(params[0] == "fire"):
        cursor.execute("DELETE FROM Staff_Contracts WHERE StaffID = " + str(driver_id[0]))     #deletes the driver you're replacing current contract
        cursor.execute("UPDATE Staff_DriverData SET AssignedCarNumber = NULL WHERE StaffID = " + str(driver_id[0]))        #takes him out of his car
        engineer_id = cursor.execute("SELECT RaceEngineerID FROM Staff_RaceEngineerDriverAssignments WHERE DriverID = " + str(driver_id[0])).fetchone()
        cursor.execute("UPDATE Staff_RaceEngineerDriverAssignments SET IsCurrentAssignment = 0 WHERE RaceEngineerID = " + str(engineer_id[0]) + " AND DriverID = " + str(driver_id[0]))
    elif(params[0] == "hire"):
        new_team = params[2].capitalize()
        car_in_team = params[3]
        salary = params[4]
        starting_bonus = params[5]
        race_bonus = params[6]
        race_bonus_pos = params[7]
        year_end = params[8]   

        #default values for some arguments
        if(starting_bonus == "none"):
            starting_bonus = "0"

        if(race_bonus == "none"):
            race_bonus = "0"
            race_bonus_pos = "10"

        day = cursor.execute("SELECT Day FROM Player_State").fetchone()

        #gets the id of the team you want to move in the driver
        if "Ferrari" in new_team: new_team_id = 1
        elif "Mclaren" in new_team: new_team_id = 2
        elif "Red bull" in new_team or "Redbull" in new_team or "Rb" in new_team: new_team_id = 3
        elif "Merc" in new_team or "Mercedes" in new_team: new_team_id = 4
        elif "Alpine" in new_team: new_team_id = 5
        elif "Williams" in new_team: new_team_id = 6
        elif "Haas" in new_team: new_team_id = 7
        elif "Alphatauri" in new_team or "Alpha tauri" in new_team or "At" in new_team: new_team_id = 8
        elif "Alfa" in new_team or "Romeo" in new_team: new_team_id = 9
        elif "Aston" in new_team or "Martin" in new_team: new_team_id = 10
        else: new_team_id = -1

        cursor.execute("INSERT INTO Staff_Contracts VALUES (" + str(driver_id[0]) + ", 0, 1," + str(day[0]) + ", 1, " + str(new_team_id) + ", " +  str(car_in_team) + ", 1, '[OPINION_STRING_NEUTRAL]', " + str(day[0]) + ", " + year_end + ", 1, '[OPINION_STRING_NEUTRAL]', " + salary + ", 1, '[OPINION_STRING_NEUTRAL]', " + starting_bonus + ", 1, '[OPINION_STRING_NEUTRAL]', " + race_bonus + ", 1, '[OPINION_STRING_NEUTRAL]', " + race_bonus_pos + ", 1, '[OPINION_STRING_NEUTRAL]')")
        cursor.execute("UPDATE Staff_DriverData SET AssignedCarNumber = " + str(car_in_team) + " WHERE StaffID = " + str(driver_id[0]))

        #checks if the driver was in the standings and if it wasn't it updates the standings
        position_in_standings = cursor.execute("SELECT MAX(Position) FROM Races_DriverStandings WHERE SeasonID = " + str(year[0])).fetchone()
        points_driver_in_standings = cursor.execute("SELECT Points FROM Races_DriverStandings WHERE DriverID = " + str(driver_id[0]) + " AND SeasonID = " + str(year[0])).fetchone()
        
        if(points_driver_in_standings == None):
            points_driver_in_standings = (0,)
        
        cursor.execute("INSERT INTO Races_DriverStandings VALUES (" + str(year[0]) + ", " + str(driver_id[0]) + ", " + str(points_driver_in_standings[0])+ ", " + str(position_in_standings[0] + 1) + ", 0, 0)")








 
    year =  cursor.execute("SELECT CurrentSeason FROM Player_State").fetchone()

    #
    if(driver_exists == None):      #if the driver does not have a contract
        cursor.execute("DELETE FROM Staff_Contracts WHERE StaffID = " + str(driver_replaced_id[0])) #deletes the driver you're replacing current contract
        
        #inserts the new driver contract
        
    elif(old_team_id[0] > 10):  #if the driver has a contract with an f2/3 team

        
        cursor.execute("UPDATE Staff_DriverData SET AssignedCarNumber = NULL WHERE StaffID = " + str(driver_replaced_id[0]))         #takes him out of his car
        #updates the new driver's contract to be with his new team
        cursor.execute("UPDATE Staff_Contracts SET TeamID = " + str(new_team_id) + ", ContractType = 0, Accepted = 1, \
        OfferDay = " + str(day[0]) + ", PatienceWhenOffered = 1, PosInTeam = " + str(car_in_team) + ", PosInTeamOpinion = 1, \
        PosInTeamOpinionStr = '[OPINION_STRING_NEUTRAL]', StartDay = " + str(day[0]) + ", EndSeason = " + year_end + ", \
        LengthOpinion = 1, LengthOpinionStr = '[OPINION_STRING_NEUTRAL]', \
        Salary =  " + salary + ", SalaryOpinion = 1, SalaryOpinionStr = '[OPINION_STRING_NEUTRAL]', \
        StartingBonus = " + starting_bonus +  ", StartingBonusOpinion = 1, StartingBonusOpinionStr = '[OPINION_STRING_NEUTRAL]', \
        RaceBonus = " + race_bonus + ", RaceBonusOpinion = 1, RaceBonusOpinionStr = '[OPINION_STRING_NEUTRAL]', \
        RaceBonusTargetPos = " + race_bonus_pos + ", RaceBonusTargetPosOpinion = 1, RaceBonusTargetPosOpinionStr = '[OPINION_STRING_NEUTRAL]' \
        WHERE StaffID = " + str(driver_id[0]))
    else:       #if the driver already has a contract with an f1 team
        #swaps their cars in the team you are movig out a driver
        old_driver_pos = cursor.execute("SELECT PosInTeam FROM Staff_Contracts WHERE  StaffID = " + str(driver_id[0])).fetchone()
        cursor.execute("UPDATE Staff_Contracts SET TeamID = " + str(old_team_id[0]) + ", PosInTeam = " + str(old_driver_pos[0]) + " WHERE StaffID = " + str(driver_replaced_id[0]))
        cursor.execute("UPDATE Staff_DriverData SET AssignedCarNumber = " + str(old_driver_pos[0]) + " WHERE StaffID = " + str(driver_replaced_id[0]))
        #updates the new driver's contract to be with his new team
        cursor.execute("UPDATE Staff_Contracts SET TeamID = " + str(new_team_id) + ", ContractType = 0, Accepted = 1, \
        OfferDay = " + str(day[0]) + ", PatienceWhenOffered = 1, PosInTeam = " + str(car_in_team) + ", PosInTeamOpinion = 1, \
        PosInTeamOpinionStr = '[OPINION_STRING_NEUTRAL]', StartDay = " + str(day[0]) + ", EndSeason = " + year_end + ", \
        LengthOpinion = 1, LengthOpinionStr = '[OPINION_STRING_NEUTRAL]', \
        Salary =  " + salary + ", SalaryOpinion = 1, SalaryOpinionStr = '[OPINION_STRING_NEUTRAL]', \
        StartingBonus = " + starting_bonus +  ", StartingBonusOpinion = 1, StartingBonusOpinionStr = '[OPINION_STRING_NEUTRAL]', \
        RaceBonus = " + race_bonus + ", RaceBonusOpinion = 1, RaceBonusOpinionStr = '[OPINION_STRING_NEUTRAL]', \
        RaceBonusTargetPos = " + race_bonus_pos + ", RaceBonusTargetPosOpinion = 1, RaceBonusTargetPosOpinionStr = '[OPINION_STRING_NEUTRAL]' \
        WHERE StaffID = " + str(driver_id[0]))

    #updates the car in the team you are moving in a driver




    #updates driver-enginer pairings
    engineer_id_new = cursor.execute("SELECT RaceEngineerID FROM Staff_RaceEngineerDriverAssignments WHERE DriverID = " + str(driver_id[0])).fetchone()
    if(engineer_id_new != None):
        cursor.execute("UPDATE Staff_RaceEngineerDriverAssignments SET IsCurrentAssignment = 0 WHERE RaceEngineerID = " + str(engineer_id_new[0]) + " AND DriverID = " + str(driver_id[0]))
    
    pair_exists = cursor.execute("SELECT DaysTogether FROM Staff_RaceEngineerDriverAssignments WHERE RaceEngineerID = " + str(engineer_id_old[0]) + " AND DriverID = " + str(driver_id[0])).fetchone()
    
    if(pair_exists != None):
        cursor.execute("UPDATE Staff_RaceEngineerDriverAssignments SET IsCurrentAssignment = 1 WHERE RaceEngineerID = " + str(engineer_id_old[0]) + " AND DriverID = " + str(driver_id[0]))
    else:
        cursor.execute("INSERT INTO Staff_RaceEngineerDriverAssignments VALUES (" + str(engineer_id_old[0]) + ", " + str(driver_id[0]) +  ", 0, 0, 1)")

    #gives new numbers to newcommers in f1
    driver_has_number = cursor.execute("SELECT Number FROM Staff_DriverNumbers WHERE CurrentHolder = " + str(driver_id[0])).fetchone()
    if(driver_has_number == None):
        free_numbers = cursor.execute("SELECT Number FROM Staff_DriverNumbers WHERE CurrentHolder IS NULL AND Number != 0").fetchall()
        rand_index = random.randrange(len(free_numbers))
        new_num = free_numbers[rand_index]
        cursor.execute("UPDATE Staff_DriverNumbers SET CurrentHolder = " + str(driver_id[0]) + " WHERE Number = " + str(new_num[0]))





    conn.commit()
    conn.close()


def get_description():
    return "Allows you to transfer driver between teams. Please read the readme before use. \n More info on how to use in the stats_readme.txt  \nAuthor: u/ignaciourreta"

if __name__ == '__main__':
    run_script()