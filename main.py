import random
import math
import pandas as pd
from pandas import DataFrame
from dbconn import *
from baseprobabilities import *

def neutralInput():
    while True:
        Neutral = input("Neutral court? (yes/no): ")
        if Neutral not in ('yes', 'no', 'y', 'n'):
            print("Not an appropriate choice.")
        else:
            return(Neutral)

def rungame():
    Home = input("Enter home team: ")
    Away = input("Enter away team: ")
    Neutral = neutralInput()
    
    t1 = Home
    t2 = Away
    if Neutral == "no" or Neutral == "n":
        HCA = -0.01
        HCAAdj = round(-0.01/-3,12)
    elif Neutral == "yes" or Neutral == "y":
        HCA = 0
        HCAAdj = 0
        
    t1TipChance = 0.5
    t1TipChance = 0.5
    
    t1rosterRawquery = "SELECT 2shooting, 3shooting, finishing, ballwork, rebounding, defense, stamina, minutes, rebounding*minutes AS 'reboundingrate', defense*minutes AS 'defenserate', ballwork*minutes AS 'assistrate' FROM players WHERE school = '%s'" % t1    
    t1rosterRaw_df = pd.read_sql(t1rosterRawquery,dbconn)
    
    t1Rebounding = round(t1rosterRaw_df['reboundingrate'].sum())
    t1StealBlock = round(t1rosterRaw_df['defenserate'].sum())
    t1Ballwork = round(t1rosterRaw_df['assistrate'].sum())
    
    t1rosterquery = "SELECT pid, ((2shooting+3shooting)/2)+finishing+ballwork+rebounding+defense AS 'ovr', fname, lname, home_city, home_state, stars, 2shooting, 3shooting, ((2shooting+3shooting)/2) AS 'shooting', finishing, ballwork, rebounding, defense, stamina, minutes, minutes/200 AS 'usage', ((2shooting+3shooting)/2)*minutes AS 'adjshooting', finishing*minutes AS 'adjfinishing', ballwork*minutes AS 'adjballwork', rebounding*minutes AS 'adjrebounding', defense*minutes AS 'adjdefense', rebounding*minutes AS 'reboundingrate', defense*minutes AS 'defenserate', ballwork*minutes AS 'assistrate', (rebounding*minutes)/%s AS 'reboundingper', (defense*minutes)/%s AS 'defenseper', (ballwork*minutes)/%s AS 'assistper' FROM players WHERE school = '%s'" % (t1Rebounding, t1StealBlock, t1Ballwork, t1)
    t1roster_df = pd.read_sql(t1rosterquery,dbconn)
    
    t1teamquery = "SELECT * FROM schools WHERE abbrev = '%s'" % t1
    t1team_df = pd.read_sql(t1teamquery,dbconn)
    
    t2rosterRawquery = "SELECT 2shooting, 3shooting, finishing, ballwork, rebounding, defense, stamina, minutes, rebounding*minutes AS 'reboundingrate', defense*minutes AS 'defenserate', ballwork*minutes AS 'assistrate' FROM players WHERE school = '%s'" % t2    
    t2rosterRaw_df = pd.read_sql(t2rosterRawquery,dbconn)
    
    t2Rebounding = round(t2rosterRaw_df['reboundingrate'].sum())
    t2StealBlock = round(t2rosterRaw_df['defenserate'].sum())
    t2Ballwork = round(t2rosterRaw_df['assistrate'].sum())
    
    t2rosterquery = "SELECT pid, ((2shooting+3shooting)/2)+finishing+ballwork+rebounding+defense AS 'ovr', fname, lname, home_city, home_state, stars, 2shooting, 3shooting, ((2shooting+3shooting)/2) AS 'shooting', finishing, ballwork, rebounding, defense, stamina, minutes, minutes/200 AS 'usage', ((2shooting+3shooting)/2)*minutes AS 'adjshooting', finishing*minutes AS 'adjfinishing', ballwork*minutes AS 'adjballwork', rebounding*minutes AS 'adjrebounding', defense*minutes AS 'adjdefense', rebounding*minutes AS 'reboundingrate', defense*minutes AS 'defenserate', ballwork*minutes AS 'assistrate', (rebounding*minutes)/%s AS 'reboundingper', (defense*minutes)/%s AS 'defenseper', (ballwork*minutes)/%s AS 'assistper' FROM players WHERE school = '%s'" % (t2Rebounding, t2StealBlock, t2Ballwork, t2)
    t2roster_df = pd.read_sql(t2rosterquery,dbconn)
    
    t2teamquery = "SELECT * FROM schools WHERE abbrev = '%s'" % t2
    t2team_df = pd.read_sql(t2teamquery,dbconn)
    
    t1Offense = round((t1roster_df['adjshooting'].sum() + t1roster_df['adjfinishing'].sum() + t1roster_df['adjballwork'].sum())/3)
    t1RebDiff = round(t1roster_df['adjrebounding'].sum() - t2roster_df['adjrebounding'].sum())
    t1BallDef = round(t1roster_df['adjballwork'].sum() - t2roster_df['adjdefense'].sum())
    t1OffensiveRebound = round((0.00003*t1RebDiff)+0.28,6)
    t1StealsAdj = round(-0.000008*t1BallDef,6)
    t1OtherTO = round(-0.000005*t1BallDef,6)
    t1StealsAdjNeg = t1StealsAdj/(-3)
    t1OtherTOAdjNeg = t1OtherTO/(-3)
    t1threeptAttemptGPAdj = (0.81*(t1team_df['3ptpro'].item()/100))-threeptAttemptProbability
    t1twoptJumperGPAdj = (0.81*(t1team_df['2jumppro'].item()/100))-twoptJumperProbability
    t1twoptInsideGPAdj = (0.81*(t1team_df['2inspro'].item()/100))-twoptInsideProbability
    t1BaseCutoff = 0
    t1StealCutoff = stealProbability + t1StealsAdj + t1BaseCutoff
    t1OtherTOCutoff = otherTurnoverProbability + HCA + t1OtherTO + t1StealCutoff
    t1threeptAttemptCutoff = round(threeptAttemptProbability + HCAAdj + t1StealsAdjNeg + t1OtherTOAdjNeg + t1threeptAttemptGPAdj + t1OtherTOCutoff,5)
    t1twoJumperCutoff = round(twoptJumperProbability + HCAAdj + t1StealsAdjNeg + t1OtherTOAdjNeg + t1twoptJumperGPAdj + t1threeptAttemptCutoff,5)
    t1twoInsideCutoff = round(twoptInsideProbability + HCAAdj + t1StealsAdjNeg + t1OtherTOAdjNeg + t1twoptInsideGPAdj + t1twoJumperCutoff)
    
    t2Offense = round((t2roster_df['adjshooting'].sum() + t2roster_df['adjfinishing'].sum() + t2roster_df['adjballwork'].sum())/3)
    t2RebDiff = round(t2roster_df['adjrebounding'].sum() - t1roster_df['adjrebounding'].sum())
    t2BallDef = round(t2roster_df['adjballwork'].sum() - t1roster_df['adjdefense'].sum())
    t2OffensiveRebound = round((0.00003*t2RebDiff)+0.28,6)
    t2StealsAdj = round(-0.000008*t2BallDef,6)
    t2OtherTO = round(-0.000005*t2BallDef,6)
    t2StealsAdjNeg = round(t2StealsAdj/-3,12)
    t2OtherTOAdjNeg = round(t2OtherTO/-3,12)
    t2threeptAttemptGPAdj = round((0.81*(t2team_df['3ptpro'].item()/100))-threeptAttemptProbability,5)
    t2twoptJumperGPAdj = round((0.81*(t2team_df['2jumppro'].item()/100))-twoptJumperProbability,6)
    t2twoptInsideGPAdj = round((0.81*(t2team_df['2inspro'].item()/100))-twoptInsideProbability,6)
    t2BaseCutoff = 0
    t2StealCutoff = stealProbability + t2StealsAdj + t2BaseCutoff
    t2OtherTOCutoff = otherTurnoverProbability + t2OtherTO + t2StealCutoff
    t2threeptAttemptCutoff = round(threeptAttemptProbability + t2StealsAdjNeg + t2OtherTOAdjNeg + t2threeptAttemptGPAdj + t2OtherTOCutoff,5)
    t2twoJumperCutoff = round(twoptJumperProbability + t2StealsAdjNeg + t2OtherTOAdjNeg + t2twoptJumperGPAdj + t2threeptAttemptCutoff,5)
    t2twoInsideCutoff = round(twoptInsideProbability + t2StealsAdjNeg + t2OtherTOAdjNeg + t2twoptInsideGPAdj + t2twoJumperCutoff)    

    
    if t1team_df['pace'].item() == 'Very Fast':
        t1pace = random.randint(80,85)
    elif t1team_df['pace'].item() == 'Fast':
        t1pace = random.randint(75,80)
    elif t1team_df['pace'].item() == 'Balanced':
        t1pace = random.randint(70,75)
    elif t1team_df['pace'].item() == 'Slow':
        t1pace = random.randint(65,70)
    elif t1team_df['pace'].item() == 'Very Slow':
        t1pace = random.randint(60,65)
        
    if t2team_df['pace'].item() == 'Very Fast':
        t2pace = random.randint(80,85)
    elif t2team_df['pace'].item() == 'Fast':
        t2pace = random.randint(75,80)
    elif t2team_df['pace'].item() == 'Balanced':
        t2pace = random.randint(70,75)
    elif t2team_df['pace'].item() == 'Slow':
        t2pace = random.randint(65,70)
    elif t2team_df['pace'].item() == 'Very Slow':
        t2pace = random.randint(60,65)

    print(str(t1team_df['abbrev'].item()) + " Offense: " + str(t1Offense))
    print(str(t1team_df['abbrev'].item()) + " Rebounding Difference: "+ str (t1RebDiff))
    print(str(t1team_df['abbrev'].item()) + " Ballwork-Defense: " + str(t1BallDef))
    print(str(t1team_df['abbrev'].item()) + " Offensive Rebound Value: " + str(t1OffensiveRebound))
    print(str(t1team_df['abbrev'].item()) + " Steals Adjustment: " + str(t1StealsAdj))
    print(str(t1team_df['abbrev'].item()) + " Other Turnovers: " + str(t1OtherTO))
    print(str(t1team_df['abbrev'].item()) + " 3pt Proportion: " + str(t1team_df['3ptpro'].item()))
    print(str(t1team_df['abbrev'].item()) + " 2pt Jumper Proportion: " + str(t1team_df['2jumppro'].item()))
    print(str(t1team_df['abbrev'].item()) + " 2pt Inside Proportion: " + str(t1team_df['2inspro'].item()))
    print(str(t1team_df['abbrev'].item()) + " Pace: " + str(t1pace))
    print("\n")
    print(str(t2team_df['abbrev'].item()) + " Offense: " + str(t2Offense))
    print(str(t2team_df['abbrev'].item()) + " Rebounding Difference: " + str(t2RebDiff))
    print(str(t2team_df['abbrev'].item()) + " Ballwork-Defense: " + str(t2BallDef))
    print(str(t2team_df['abbrev'].item()) + " Offensive Rebound Value: " + str(t2OffensiveRebound))
    print(str(t2team_df['abbrev'].item()) + " Steals Adjustment: " + str(t2StealsAdj))
    print(str(t2team_df['abbrev'].item()) + " Other Turnovers: " + str(t2OtherTO))
    print(str(t2team_df['abbrev'].item()) + " 3pt Proportion: " + str(t2team_df['3ptpro'].item()))
    print(str(t2team_df['abbrev'].item()) + " 2pt Jumper Proportion: " + str(t2team_df['2jumppro'].item()))
    print(str(t2team_df['abbrev'].item()) + " 2pt Inside Proportion: " + str(t2team_df['2inspro'].item()))
    print(str(t2team_df['abbrev'].item()) + " Pace: " + str(t2pace))
    
    print("\n")
    print("\n")
    
    possessionNum = 0
    
    t1pts = 0
    t2pts = 0
    
    gett1Players = t1roster_df['pid']
    gett2Players = t2roster_df['pid']
    
    while possessionNum < (t1pace+t2pace):
        if possessionNum == 0:
            tipOff = random.random()
            if tipOff < t1TipChance:
                possession = t2
                print(t2 + " wins the tip")
            else:
                possession = t1
                print(t1 + " wins the tip")
                
        if Neutral == "no" or Neutral == "n":
            HCA = 0.025
        elif Neutral == "yes" or Neutral == "y":
            HCA = 0
        
        possessionNum += 1
            
        possrand = random.random()
        
        if possession == t1:
            if possrand < t1StealCutoff:
                pickPlayer = random.choices(gett2Players,weights=t2roster_df['defenseper'],k=1)
                stealPlayer = t2roster_df[t2roster_df['pid'] == pickPlayer[0]]
                printShooter = stealPlayer['fname'].item() + " " + stealPlayer['lname'].item()
                print(str(possessionNum) + " " + possession + ": " + printShooter  + " steals the ball for " + t2 + "!")
                possession = t2
            elif possrand < t1OtherTOCutoff:
                otherTO = random.random()
                pickPlayer = random.choices(gett1Players,weights=t1roster_df['usage'],k=1)
                toPlayer = t1roster_df[t1roster_df['pid'] == pickPlayer[0]]
                printShooter = toPlayer['fname'].item() + " " + toPlayer['lname'].item()
                if otherTO < 0.582:
                    print(str(possessionNum) + " " + possession + ": " + printShooter + " lost the ball out of bounds.")
                elif otherTO < 0.64:
                    print(str(possessionNum) + " " + possession + ": Shot clock violation on " + printShooter + ".")
                elif otherTO < 1:
                    print(str(possessionNum) + " " + possession + ": Offensive foul on " + printShooter + ".")
                possession = t2
            elif possrand < t1threeptAttemptCutoff:
                pickPlayer = random.choices(gett1Players,weights=t1roster_df['usage'],k=1)
                shooter = t1roster_df[t1roster_df['pid'] == pickPlayer[0]]
                printShooter = shooter['fname'].item() + " " + shooter['lname'].item()
                blockAdj = (0.00001*t2roster_df['defenserate'].sum())-0.0153
                made3nf = (0.015*shooter['3shooting'].item())+0.185+HCA
                madeDiff = made3nf-0.335
                missed3nf = 0.635-madeDiff-blockAdj
                made3foul = 0.005
                missed3foul = 0.015
                blocked = 0.01+blockAdj
                base3Cutoff = 0
                made3Cutoff = base3Cutoff+made3nf
                missed3Cutoff = made3Cutoff+missed3nf
                blocked3Cutoff = missed3Cutoff+blocked
                missed3foulCutoff = blocked3Cutoff+missed3foul
                made3foulCutoff = missed3foulCutoff+made3foul
                eventOutcome = random.random()
                if eventOutcome < made3Cutoff:
                    print(str(possessionNum) + " " + possession + ": " + printShooter + " 3-point attempt...Score!")
                    t1pts+=3
                    assistRand = random.random()
                    if assistRand > 0.173:
                        pickAssister = random.choices(gett1Players,weights=t1roster_df['assistper'],k=1)
                        assister = t1roster_df[t1roster_df['pid'] == pickAssister[0]]
                        printAssister = assister['fname'].item() + " " + assister['lname'].item()
                        print("       Assisted by: "+ printAssister)
                    possession = t2
                elif eventOutcome < missed3Cutoff:
                    print(str(possessionNum) + " " + possession + ": " + printShooter + " 3-point attempt...Missed!")
                    rebrand = random.random()
                    if rebrand < t1OffensiveRebound:
                        pickt1Rebounder = random.choices(gett1Players,weights=t1roster_df['reboundingper'],k=1)
                        t1rebounder = t1roster_df[t1roster_df['pid'] == pickt1Rebounder[0]]
                        printt1Rebounder = t1rebounder['fname'].item() + " " + t1rebounder['lname'].item()
                        print("       Rebounded by " + printt1Rebounder + ".")
                        possession = t1
                    else:
                        pickt2Rebounder = random.choices(gett2Players,weights=t2roster_df['reboundingper'],k=1)
                        t2rebounder = t2roster_df[t2roster_df['pid'] == pickt2Rebounder[0]]
                        printt2Rebounder = t2rebounder['fname'].item() + " " + t2rebounder['lname'].item()
                        print("       Rebounded by " + printt2Rebounder + ".")
                        possession = t2
                elif eventOutcome < blocked3Cutoff:
                    pickBlocker = random.choices(gett2Players,weights=t2roster_df['defenseper'],k=1)
                    blocker = t2roster_df[t2roster_df['pid'] == pickBlocker[0]]
                    printBlocker = blocker['fname'].item() + " " + blocker['lname'].item()
                    print(str(possessionNum) + " " + possession + ": " + printShooter + " 3-point attempt...BLOCKED by " + printBlocker + ".")
                    rebrand = random.random()
                    if rebrand < 0.43:
                        pickt1Rebounder = random.choices(gett1Players,weights=t1roster_df['reboundingper'],k=1)
                        t1rebounder = t1roster_df[t1roster_df['pid'] == pickt1Rebounder[0]]
                        printt1Rebounder = t1rebounder['fname'].item() + " " + t1rebounder['lname'].item()
                        print("       Rebounded by " + printt1Rebounder + ".")
                        possession = t1
                    else:
                        pickt2Rebounder = random.choices(gett2Players,weights=t2roster_df['reboundingper'],k=1)
                        t2rebounder = t2roster_df[t2roster_df['pid'] == pickt2Rebounder[0]]
                        printt2Rebounder = t2rebounder['fname'].item() + " " + t2rebounder['lname'].item()
                        print("       Rebounded by " + printt2Rebounder + ".")
                        possession = t2
                elif eventOutcome < missed3foulCutoff:
                    print(str(possessionNum) + " " + possession + ": " + printShooter + " 3-point attempt...Missed, but fouled on the play.")
                    foulShots = 3
                    ftCutoff = (0.02*shooter['2shooting'].item())+0.5
                    while foulShots > 0:
                        if random.random() > ftCutoff:
                            print("       Free throw coming up... good!")
                            t1pts += 1
                            foulShots -= 1
                            if foulShots == 0:
                                possession = t2
                        elif random.random() < ftCutoff:
                            print("       Free throw coming up... rattled out.")
                            foulShots -= 1
                            if foulShots == 0:
                                rebrand = random.random()
                                if rebrand < t1OffensiveRebound:
                                    pickt1Rebounder = random.choices(gett1Players,weights=t1roster_df['reboundingper'],k=1)
                                    t1rebounder = t1roster_df[t1roster_df['pid'] == pickt1Rebounder[0]]
                                    printt1Rebounder = t1rebounder['fname'].item() + " " + t1rebounder['lname'].item()
                                    print("       Rebounded by " + printt1Rebounder + ".")
                                    possession = t1
                                else:
                                    pickt2Rebounder = random.choices(gett2Players,weights=t2roster_df['reboundingper'],k=1)
                                    t2rebounder = t2roster_df[t2roster_df['pid'] == pickt2Rebounder[0]]
                                    printt2Rebounder = t2rebounder['fname'].item() + " " + t2rebounder['lname'].item()
                                    print("       Rebounded by " + printt2Rebounder + ".")
                                    possession = t2
                elif eventOutcome < made3foulCutoff:
                    print(str(possessionNum) + " " + possession + ": " + printShooter + " 3-point attempt...Score! Fouled, and one!")
                    t1pts += 3
                    assistRand = random.random()
                    if assistRand > 0.173:
                        pickAssister = random.choices(gett1Players,weights=t1roster_df['assistper'],k=1)
                        assister = t1roster_df[t1roster_df['pid'] == pickAssister[0]]
                        printAssister = assister['fname'].item() + " " + assister['lname'].item()
                        print("       Assisted by: "+ printAssister)
                    foulShots = 1
                    ftCutoff = (0.02*shooter['2shooting'].item())+0.5
                    while foulShots > 0:
                        if random.random() > ftCutoff:
                            print("       Free throw coming up... good!")
                            t1pts += 1
                            foulShots -= 1
                        elif random.random() < ftCutoff:
                            print("       Free throw coming up... rattled out.")
                            foulShots -= 1
                    if foulShots == 0:
                        possession = t2                
            elif possrand < t1twoJumperCutoff:
                pickPlayer = random.choices(gett1Players,weights=t1roster_df['usage'],k=1)
                shooter = t1roster_df[t1roster_df['pid'] == pickPlayer[0]]
                printShooter = shooter['fname'].item() + " " + shooter['lname'].item()
                blockAdj = (0.00001*t2roster_df['defenserate'].sum())-0.0153
                made2jnf = (0.006*shooter['2shooting'].item())+0.185+HCA
                madeDiff = made2jnf-0.335
                missed2jnf = 0.53-madeDiff-blockAdj
                made2jfoul = 0.01
                missed2jfoul = 0.02
                blocked = 0.07+blockAdj
                base2jCutoff = 0
                made2jCutoff = base2jCutoff+made2jnf
                missed2jCutoff = made2jCutoff+missed2jnf
                blocked2jCutoff = missed2jCutoff+blocked
                missed2jfoulCutoff = blocked2jCutoff+missed2jfoul
                made2jfoulCutoff = missed2jfoulCutoff+made2jfoul
                eventOutcome = random.random()
                if eventOutcome < made2jCutoff:
                    print(str(possessionNum) + " " + possession + ": " + printShooter + " 2-point jumper...Score!")
                    t1pts+=2
                    assistRand = random.random()
                    if assistRand > 0.678:
                        pickAssister = random.choices(gett1Players,weights=t1roster_df['assistper'],k=1)
                        assister = t1roster_df[t1roster_df['pid'] == pickAssister[0]]
                        printAssister = assister['fname'].item() + " " + assister['lname'].item()
                        print("       Assisted by: "+ printAssister)
                    possession = t2
                elif eventOutcome < missed2jCutoff:
                    print(str(possessionNum) + " " + possession + ": " + printShooter + " 2-point jumper...Missed!")
                    rebrand = random.random()
                    if rebrand < t1OffensiveRebound:
                        pickt1Rebounder = random.choices(gett1Players,weights=t1roster_df['reboundingper'],k=1)
                        t1rebounder = t1roster_df[t1roster_df['pid'] == pickt1Rebounder[0]]
                        printt1Rebounder = t1rebounder['fname'].item() + " " + t1rebounder['lname'].item()
                        print("       Rebounded by " + printt1Rebounder + ".")
                        possession = t1
                    else:
                        pickt2Rebounder = random.choices(gett2Players,weights=t2roster_df['reboundingper'],k=1)
                        t2rebounder = t2roster_df[t2roster_df['pid'] == pickt2Rebounder[0]]
                        printt2Rebounder = t2rebounder['fname'].item() + " " + t2rebounder['lname'].item()
                        print("       Rebounded by " + printt2Rebounder + ".")
                        possession = t2
                elif eventOutcome < blocked2jCutoff:
                    pickBlocker = random.choices(gett2Players,weights=t2roster_df['defenseper'],k=1)
                    blocker = t2roster_df[t2roster_df['pid'] == pickBlocker[0]]
                    printBlocker = blocker['fname'].item() + " " + blocker['lname'].item()
                    print(str(possessionNum) + " " + possession + ": " + printShooter + " 2-point jumper...BLOCKED by " + printBlocker + ".")
                    rebrand = random.random()
                    if rebrand < 0.43:
                        pickt1Rebounder = random.choices(gett1Players,weights=t1roster_df['reboundingper'],k=1)
                        t1rebounder = t1roster_df[t1roster_df['pid'] == pickt1Rebounder[0]]
                        printt1Rebounder = t1rebounder['fname'].item() + " " + t1rebounder['lname'].item()
                        print("       Rebounded by " + printt1Rebounder + ".")
                        possession = t1
                    else:
                        pickt2Rebounder = random.choices(gett2Players,weights=t2roster_df['reboundingper'],k=1)
                        t2rebounder = t2roster_df[t2roster_df['pid'] == pickt2Rebounder[0]]
                        printt2Rebounder = t2rebounder['fname'].item() + " " + t2rebounder['lname'].item()
                        print("       Rebounded by " + printt2Rebounder + ".")
                        possession = t2
                elif eventOutcome < missed2jfoulCutoff:
                    print(str(possessionNum) + " " + possession + ": " + printShooter + " 2-point jumper...Missed, but fouled on the play.")
                    foulShots = 2
                    ftCutoff = (0.02*shooter['2shooting'].item())+0.5
                    while foulShots > 0:
                        if random.random() > ftCutoff:
                            print("       Free throw coming up... good!")
                            t1pts += 1
                            foulShots -= 1
                            if foulShots == 0:
                                possession = t2
                        elif random.random() < ftCutoff:
                            print("       Free throw coming up... rattled out.")
                            foulShots -= 1
                            if foulShots == 0:
                                rebrand = random.random()
                                if rebrand < t1OffensiveRebound:
                                    pickt1Rebounder = random.choices(gett1Players,weights=t1roster_df['reboundingper'],k=1)
                                    t1rebounder = t1roster_df[t1roster_df['pid'] == pickt1Rebounder[0]]
                                    printt1Rebounder = t1rebounder['fname'].item() + " " + t1rebounder['lname'].item()
                                    print("       Rebounded by " + printt1Rebounder + ".")
                                    possession = t1
                                else:
                                    pickt2Rebounder = random.choices(gett2Players,weights=t2roster_df['reboundingper'],k=1)
                                    t2rebounder = t2roster_df[t2roster_df['pid'] == pickt2Rebounder[0]]
                                    printt2Rebounder = t2rebounder['fname'].item() + " " + t2rebounder['lname'].item()
                                    print("       Rebounded by " + printt2Rebounder + ".")
                                    possession = t2
                elif eventOutcome < made2jfoulCutoff:
                    print(str(possessionNum) + " " + possession + ": " + printShooter + " 2-point jumper...Score! Fouled, and one!")
                    t1pts += 2
                    assistRand = random.random()
                    if assistRand > 0.678:
                        pickAssister = random.choices(gett1Players,weights=t1roster_df['assistper'],k=1)
                        assister = t1roster_df[t1roster_df['pid'] == pickAssister[0]]
                        printAssister = assister['fname'].item() + " " + assister['lname'].item()
                        print("       Assisted by: "+ printAssister)
                    foulShots = 1
                    ftCutoff = (0.02*shooter['2shooting'].item())+0.5
                    while foulShots > 0:
                        if random.random() > ftCutoff:
                            print("       Free throw coming up... good!")
                            t1pts += 1
                            foulShots -= 1
                            if foulShots == 0:
                                possession = t2
                        elif random.random() < ftCutoff:
                            print("       Free throw coming up... rattled out.")
                            foulShots -= 1
                            if foulShots == 0:
                                rebrand = random.random()
                                if rebrand < t1OffensiveRebound:
                                    pickt1Rebounder = random.choices(gett1Players,weights=t1roster_df['reboundingper'],k=1)
                                    t1rebounder = t1roster_df[t1roster_df['pid'] == pickt1Rebounder[0]]
                                    printt1Rebounder = t1rebounder['fname'].item() + " " + t1rebounder['lname'].item()
                                    print("       Rebounded by " + printt1Rebounder + ".")
                                    possession = t1
                                else:
                                    pickt2Rebounder = random.choices(gett2Players,weights=t2roster_df['reboundingper'],k=1)
                                    t2rebounder = t2roster_df[t2roster_df['pid'] == pickt2Rebounder[0]]
                                    printt2Rebounder = t2rebounder['fname'].item() + " " + t2rebounder['lname'].item()
                                    print("       Rebounded by " + printt2Rebounder + ".")
                                    possession = t2
            elif possrand < t1twoInsideCutoff:
                pickPlayer = random.choices(gett1Players,weights=t1roster_df['usage'],k=1)
                shooter = t1roster_df[t1roster_df['pid'] == pickPlayer[0]]
                printShooter = shooter['fname'].item() + " " + shooter['lname'].item()
                blockAdj = (0.00001*t1roster_df['defenserate'].sum())-0.0153
                made2inf = (0.005*shooter['finishing'].item())+0.513+HCA
                madeDiff = made2inf-0.563
                missed2inf = 0.147-madeDiff-blockAdj
                made2ifoul = 0.05
                missed2ifoul = 0.14
                blocked = 0.1+blockAdj
                base2iCutoff = 0
                made2iCutoff = base2iCutoff+made2inf
                missed2iCutoff = made2iCutoff+missed2inf
                blocked2iCutoff = missed2iCutoff+blocked
                missed2ifoulCutoff = blocked2iCutoff+missed2ifoul
                made2ifoulCutoff = missed2ifoulCutoff+made2ifoul
                eventOutcome = random.random()
                if eventOutcome < made2iCutoff:
                    print(str(possessionNum) + " " + possession + ": " + printShooter + " Inside shot...Score!")
                    t1pts+=2
                    assistRand = random.random()
                    if assistRand > 0.57:
                        pickAssister = random.choices(gett1Players,weights=t1roster_df['assistper'],k=1)
                        assister = t1roster_df[t1roster_df['pid'] == pickAssister[0]]
                        printAssister = assister['fname'].item() + " " + assister['lname'].item()
                        print("       Assisted by: "+ printAssister)
                    possession = t2
                elif eventOutcome < missed2iCutoff:
                    print(str(possessionNum) + " " + possession + ": " + printShooter + " Inside shot...Missed!")
                    rebrand = random.random()
                    if rebrand < t1OffensiveRebound:
                        pickt1Rebounder = random.choices(gett1Players,weights=t1roster_df['reboundingper'],k=1)
                        t1rebounder = t1roster_df[t1roster_df['pid'] == pickt1Rebounder[0]]
                        printt1Rebounder = t1rebounder['fname'].item() + " " + t1rebounder['lname'].item()
                        print("       Rebounded by " + printt1Rebounder + ".")
                        possession = t1
                    else:
                        pickt2Rebounder = random.choices(gett2Players,weights=t2roster_df['reboundingper'],k=1)
                        t2rebounder = t2roster_df[t2roster_df['pid'] == pickt2Rebounder[0]]
                        printt2Rebounder = t2rebounder['fname'].item() + " " + t2rebounder['lname'].item()
                        print("       Rebounded by " + printt2Rebounder + ".")
                        possession = t2
                elif eventOutcome < blocked2iCutoff:
                    pickBlocker = random.choices(gett2Players,weights=t2roster_df['defenseper'],k=1)
                    blocker = t2roster_df[t2roster_df['pid'] == pickBlocker[0]]
                    printBlocker = blocker['fname'].item() + " " + blocker['lname'].item()
                    print(str(possessionNum) + " " + possession + ": " + printShooter + " Inside shot...BLOCKED by " + printBlocker + ".")
                    rebrand = random.random()
                    if rebrand < 0.43:
                        pickt1Rebounder = random.choices(gett1Players,weights=t1roster_df['reboundingper'],k=1)
                        t1rebounder = t1roster_df[t1roster_df['pid'] == pickt1Rebounder[0]]
                        printt1Rebounder = t1rebounder['fname'].item() + " " + t1rebounder['lname'].item()
                        print("       Rebounded by " + printt1Rebounder + ".")
                        possession = t1
                    else:
                        pickt2Rebounder = random.choices(gett2Players,weights=t2roster_df['reboundingper'],k=1)
                        t2rebounder = t2roster_df[t2roster_df['pid'] == pickt2Rebounder[0]]
                        printt2Rebounder = t2rebounder['fname'].item() + " " + t2rebounder['lname'].item()
                        print("       Rebounded by " + printt2Rebounder + ".")
                        possession = t2
                elif eventOutcome < missed2ifoulCutoff:
                    print(str(possessionNum) + " " + possession + ": " + printShooter + " Inside shot...Missed, but fouled on the play.")
                    foulShots = 2
                    ftCutoff = (0.02*shooter['2shooting'].item())+0.5
                    while foulShots > 0:
                        if random.random() > ftCutoff:
                            print("       Free throw coming up... good!")
                            t1pts += 1
                            foulShots -= 1
                            if foulShots == 0:
                                possession = t2
                        elif random.random() < ftCutoff:
                            print("       Free throw coming up... rattled out.")
                            foulShots -= 1
                            if foulShots == 0:
                                rebrand = random.random()
                                if rebrand < t1OffensiveRebound:
                                    pickt1Rebounder = random.choices(gett1Players,weights=t1roster_df['reboundingper'],k=1)
                                    t1rebounder = t1roster_df[t1roster_df['pid'] == pickt1Rebounder[0]]
                                    printt1Rebounder = t1rebounder['fname'].item() + " " + t1rebounder['lname'].item()
                                    print("       Rebounded by " + printt1Rebounder + ".")
                                    possession = t1
                                else:
                                    pickt2Rebounder = random.choices(gett2Players,weights=t2roster_df['reboundingper'],k=1)
                                    t2rebounder = t2roster_df[t2roster_df['pid'] == pickt2Rebounder[0]]
                                    printt2Rebounder = t2rebounder['fname'].item() + " " + t2rebounder['lname'].item()
                                    print("       Rebounded by " + printt2Rebounder + ".")
                                    possession = t2
                elif eventOutcome < made2ifoulCutoff:
                    print(str(possessionNum) + " " + possession + ": " + printShooter + " Inside shot...Score! Fouled, and one!")
                    t1pts += 2
                    assistRand = random.random()
                    if assistRand > 0.57:
                        pickAssister = random.choices(gett1Players,weights=t1roster_df['assistper'],k=1)
                        assister = t1roster_df[t1roster_df['pid'] == pickAssister[0]]
                        printAssister = assister['fname'].item() + " " + assister['lname'].item()
                        print("       Assisted by: "+ printAssister)
                    foulShots = 1
                    ftCutoff = (0.02*shooter['2shooting'].item())+0.5
                    while foulShots > 0:
                        if random.random() > ftCutoff:
                            print("       Free throw coming up... good!")
                            t1pts += 1
                            foulShots -= 1
                            if foulShots == 0:
                                possession = t2
                        elif random.random() < ftCutoff:
                            print("       Free throw coming up... rattled out.")
                            foulShots -= 1
                            if foulShots == 0:
                                rebrand = random.random()
                                if rebrand < t1OffensiveRebound:
                                    pickt1Rebounder = random.choices(gett1Players,weights=t1roster_df['reboundingper'],k=1)
                                    t1rebounder = t1roster_df[t1roster_df['pid'] == pickt1Rebounder[0]]
                                    printt1Rebounder = t1rebounder['fname'].item() + " " + t1rebounder['lname'].item()
                                    print("       Rebounded by " + printt1Rebounder + ".")
                                    possession = t1
                                else:
                                    pickt2Rebounder = random.choices(gett2Players,weights=t2roster_df['reboundingper'],k=1)
                                    t2rebounder = t2roster_df[t2roster_df['pid'] == pickt2Rebounder[0]]
                                    printt2Rebounder = t2rebounder['fname'].item() + " " + t2rebounder['lname'].item()
                                    print("       Rebounded by " + printt2Rebounder + ".")
                                    possession = t2
        elif possession == t2:
            if possrand < t2StealCutoff:
                pickPlayer = random.choices(gett1Players,weights=t1roster_df['defenseper'],k=1)
                stealPlayer = t1roster_df[t1roster_df['pid'] == pickPlayer[0]]
                printShooter = stealPlayer['fname'].item() + " " + stealPlayer['lname'].item()
                print(str(possessionNum) + " " + possession + ": " + printShooter  + " steals the ball for " + t1 + "!")
                possession = t1
            elif possrand < t2OtherTOCutoff:
                otherTO = random.random()
                pickPlayer = random.choices(gett2Players,weights=t2roster_df['usage'],k=1)
                toPlayer = t2roster_df[t2roster_df['pid'] == pickPlayer[0]]
                printShooter = toPlayer['fname'].item() + " " + toPlayer['lname'].item()
                if otherTO < 0.582:
                    print(str(possessionNum) + " " + possession + ": " + printShooter + " lost the ball out of bounds.")
                elif otherTO < 0.64:
                    print(str(possessionNum) + " " + possession + ": Shot clock violation on " + printShooter + ".")
                elif otherTO < 1:
                    print(str(possessionNum) + " " + possession + ": Offensive foul on " + printShooter + ".")
                possession = t1
            elif possrand < t2threeptAttemptCutoff:
                pickPlayer = random.choices(gett2Players,weights=t2roster_df['usage'],k=1)
                shooter = t2roster_df[t2roster_df['pid'] == pickPlayer[0]]
                printShooter = shooter['fname'].item() + " " + shooter['lname'].item()
                blockAdj = (0.00001*t1roster_df['defenserate'].sum())-0.0153
                made3nf = (0.015*shooter['3shooting'].item())+0.185
                madeDiff = made3nf-0.335
                missed3nf = 0.635-madeDiff-blockAdj
                made3foul = 0.005
                missed3foul = 0.015
                blocked = 0.01+blockAdj
                base3Cutoff = 0
                made3Cutoff = base3Cutoff+made3nf
                missed3Cutoff = made3Cutoff+missed3nf
                blocked3Cutoff = missed3Cutoff+blocked
                missed3foulCutoff = blocked3Cutoff+missed3foul
                made3foulCutoff = missed3foulCutoff+made3foul
                eventOutcome = random.random()
                if eventOutcome < made3Cutoff:
                    print(str(possessionNum) + " " + possession + ": " + printShooter + " 3-point attempt...Score!")
                    t2pts+=3
                    assistRand = random.random()
                    if assistRand > 0.173:
                        pickAssister = random.choices(gett2Players,weights=t2roster_df['assistper'],k=1)
                        assister = t2roster_df[t2roster_df['pid'] == pickAssister[0]]
                        printAssister = assister['fname'].item() + " " + assister['lname'].item()
                        print("       Assisted by: "+ printAssister)
                    possession = t1
                elif eventOutcome < missed3Cutoff:
                    print(str(possessionNum) + " " + possession + ": " + printShooter + " 3-point attempt...Missed!")
                    rebrand = random.random()
                    if rebrand < t2OffensiveRebound:
                        pickt2Rebounder = random.choices(gett2Players,weights=t2roster_df['reboundingper'],k=1)
                        t2rebounder = t2roster_df[t2roster_df['pid'] == pickt2Rebounder[0]]
                        printt2Rebounder = t2rebounder['fname'].item() + " " + t2rebounder['lname'].item()
                        print("       Rebounded by " + printt2Rebounder + ".")
                        possession = t2
                    else:
                        pickt1Rebounder = random.choices(gett1Players,weights=t1roster_df['reboundingper'],k=1)
                        t1rebounder = t1roster_df[t1roster_df['pid'] == pickt1Rebounder[0]]
                        printt1Rebounder = t1rebounder['fname'].item() + " " + t1rebounder['lname'].item()
                        print("       Rebounded by " + printt1Rebounder + ".")
                        possession = t1
                elif eventOutcome < blocked3Cutoff:
                    pickBlocker = random.choices(gett1Players,weights=t1roster_df['defenseper'],k=1)
                    blocker = t1roster_df[t1roster_df['pid'] == pickBlocker[0]]
                    printBlocker = blocker['fname'].item() + " " + blocker['lname'].item()
                    print(str(possessionNum) + " " + possession + ": " + printShooter + " 3-point attempt...BLOCKED by " + printBlocker + ".")
                    rebrand = random.random()
                    if rebrand < 0.43:
                        pickt2Rebounder = random.choices(gett2Players,weights=t2roster_df['reboundingper'],k=1)
                        t2rebounder = t2roster_df[t2roster_df['pid'] == pickt2Rebounder[0]]
                        printt2Rebounder = t2rebounder['fname'].item() + " " + t2rebounder['lname'].item()
                        print("       Rebounded by " + printt2Rebounder + ".")
                        possession = t2
                    else:
                        pickt1Rebounder = random.choices(gett1Players,weights=t1roster_df['reboundingper'],k=1)
                        t1rebounder = t1roster_df[t1roster_df['pid'] == pickt1Rebounder[0]]
                        printt1Rebounder = t1rebounder['fname'].item() + " " + t1rebounder['lname'].item()
                        print("       Rebounded by " + printt1Rebounder + ".")
                        possession = t1
                elif eventOutcome < missed3foulCutoff:
                    print(str(possessionNum) + " " + possession + ": " + printShooter + " 3-point attempt...Missed, but fouled on the play.")
                    foulShots = 3
                    ftCutoff = (0.02*shooter['2shooting'].item())+0.5
                    while foulShots > 0:
                        if random.random() > ftCutoff:
                            print("       Free throw coming up... good!")
                            t2pts += 1
                            foulShots -= 1
                            if foulShots == 0:
                                possession = t1
                        elif random.random() < ftCutoff:
                            print("       Free throw coming up... rattled out.")
                            foulShots -= 1
                            if foulShots == 0:
                                rebrand = random.random()
                                if rebrand < t2OffensiveRebound:
                                    pickt2Rebounder = random.choices(gett2Players,weights=t2roster_df['reboundingper'],k=1)
                                    t2rebounder = t2roster_df[t2roster_df['pid'] == pickt2Rebounder[0]]
                                    printt2Rebounder = t2rebounder['fname'].item() + " " + t2rebounder['lname'].item()
                                    print("       Rebounded by " + printt2Rebounder + ".")
                                    possession = t2
                                else:
                                    pickt1Rebounder = random.choices(gett1Players,weights=t1roster_df['reboundingper'],k=1)
                                    t1rebounder = t1roster_df[t1roster_df['pid'] == pickt1Rebounder[0]]
                                    printt1Rebounder = t1rebounder['fname'].item() + " " + t1rebounder['lname'].item()
                                    print("       Rebounded by " + printt1Rebounder + ".")
                                    possession = t1
                elif eventOutcome < made3foulCutoff:
                    print(str(possessionNum) + " " + possession + ": " + printShooter + " 3-point attempt...Score! Fouled, and one!")
                    t2pts += 3
                    assistRand = random.random()
                    if assistRand > 0.173:
                        pickAssister = random.choices(gett2Players,weights=t2roster_df['assistper'],k=1)
                        assister = t2roster_df[t2roster_df['pid'] == pickAssister[0]]
                        printAssister = assister['fname'].item() + " " + assister['lname'].item()
                        print("       Assisted by: "+ printAssister)
                    foulShots = 1
                    ftCutoff = (0.02*shooter['2shooting'].item())+0.5
                    while foulShots > 0:
                        if random.random() > ftCutoff:
                            print("       Free throw coming up... good!")
                            t2pts += 1
                            foulShots -= 1
                            if foulShots == 0:
                                possession = t1
                        elif random.random() < ftCutoff:
                            print("       Free throw coming up... rattled out.")
                            foulShots -= 1
                            if foulShots == 0:
                                rebrand = random.random()
                                if rebrand < t2OffensiveRebound:
                                    pickt2Rebounder = random.choices(gett2Players,weights=t2roster_df['reboundingper'],k=1)
                                    t2rebounder = t2roster_df[t2roster_df['pid'] == pickt2Rebounder[0]]
                                    printt2Rebounder = t2rebounder['fname'].item() + " " + t2rebounder['lname'].item()
                                    print("       Rebounded by " + printt2Rebounder + ".")
                                    possession = t2
                                else:
                                    pickt1Rebounder = random.choices(gett1Players,weights=t1roster_df['reboundingper'],k=1)
                                    t1rebounder = t1roster_df[t1roster_df['pid'] == pickt1Rebounder[0]]
                                    printt1Rebounder = t1rebounder['fname'].item() + " " + t1rebounder['lname'].item()
                                    print("       Rebounded by " + printt1Rebounder + ".")
                                    possession = t1
            elif possrand < t2twoJumperCutoff:
                pickPlayer = random.choices(gett2Players,weights=t2roster_df['usage'],k=1)
                shooter = t2roster_df[t2roster_df['pid'] == pickPlayer[0]]
                printShooter = shooter['fname'].item() + " " + shooter['lname'].item()
                blockAdj = (0.00001*t1roster_df['defenserate'].sum())-0.0153
                made2jnf = (0.006*shooter['2shooting'].item())+0.185
                madeDiff = made2jnf-0.335
                missed2jnf = 0.53-madeDiff-blockAdj
                made2jfoul = 0.01
                missed2jfoul = 0.02
                blocked = 0.07+blockAdj
                base2jCutoff = 0
                made2jCutoff = base2jCutoff+made2jnf
                missed2jCutoff = made2jCutoff+missed2jnf
                blocked2jCutoff = missed2jCutoff+blocked
                missed2jfoulCutoff = blocked2jCutoff+missed2jfoul
                made2jfoulCutoff = missed2jfoulCutoff+made2jfoul
                eventOutcome = random.random()
                if eventOutcome < made2jCutoff:
                    print(str(possessionNum) + " " + possession + ": " + printShooter + " 2-point jumper...Score!")
                    t2pts+=2
                    assistRand = random.random()
                    if assistRand > 0.678:
                        pickAssister = random.choices(gett2Players,weights=t2roster_df['assistper'],k=1)
                        assister = t2roster_df[t2roster_df['pid'] == pickAssister[0]]
                        printAssister = assister['fname'].item() + " " + assister['lname'].item()
                        print("       Assisted by: "+ printAssister)
                    possession = t1
                elif eventOutcome < missed2jCutoff:
                    print(str(possessionNum) + " " + possession + ": " + printShooter + " 2-point jumper...Missed!")
                    rebrand = random.random()
                    if rebrand < t2OffensiveRebound:
                        pickt2Rebounder = random.choices(gett2Players,weights=t2roster_df['reboundingper'],k=1)
                        t2rebounder = t2roster_df[t2roster_df['pid'] == pickt2Rebounder[0]]
                        printt2Rebounder = t2rebounder['fname'].item() + " " + t2rebounder['lname'].item()
                        print("       Rebounded by " + printt2Rebounder + ".")
                        possession = t2
                    else:
                        pickt1Rebounder = random.choices(gett1Players,weights=t1roster_df['reboundingper'],k=1)
                        t1rebounder = t1roster_df[t1roster_df['pid'] == pickt1Rebounder[0]]
                        printt1Rebounder = t1rebounder['fname'].item() + " " + t1rebounder['lname'].item()
                        print("       Rebounded by " + printt1Rebounder + ".")
                        possession = t1
                elif eventOutcome < blocked2jCutoff:
                    pickBlocker = random.choices(gett1Players,weights=t1roster_df['defenseper'],k=1)
                    blocker = t1roster_df[t1roster_df['pid'] == pickBlocker[0]]
                    printBlocker = blocker['fname'].item() + " " + blocker['lname'].item()
                    print(str(possessionNum) + " " + possession + ": " + printShooter + " 2-point jumper...BLOCKED by " + printBlocker + ".")
                    rebrand = random.random()
                    if rebrand < 0.43:
                        pickt2Rebounder = random.choices(gett2Players,weights=t2roster_df['reboundingper'],k=1)
                        t2rebounder = t2roster_df[t2roster_df['pid'] == pickt2Rebounder[0]]
                        printt2Rebounder = t2rebounder['fname'].item() + " " + t2rebounder['lname'].item()
                        print("       Rebounded by " + printt2Rebounder + ".")
                        possession = t2
                    else:
                        pickt1Rebounder = random.choices(gett1Players,weights=t1roster_df['reboundingper'],k=1)
                        t1rebounder = t1roster_df[t1roster_df['pid'] == pickt1Rebounder[0]]
                        printt1Rebounder = t1rebounder['fname'].item() + " " + t1rebounder['lname'].item()
                        print("       Rebounded by " + printt1Rebounder + ".")
                        possession = t1
                elif eventOutcome < missed2jfoulCutoff:
                    print(str(possessionNum) + " " + possession + ": " + printShooter + " 2-point jumper...Missed, but fouled on the play.")
                    foulShots = 2
                    ftCutoff = (0.02*shooter['2shooting'].item())+0.5
                    while foulShots > 0:
                        if random.random() > ftCutoff:
                            print("       Free throw coming up... good!")
                            t2pts += 1
                            foulShots -= 1
                            if foulShots == 0:
                                possession = t1
                        elif random.random() < ftCutoff:
                            print("       Free throw coming up... rattled out.")
                            foulShots -= 1
                            if foulShots == 0:
                                rebrand = random.random()
                                if rebrand < t2OffensiveRebound:
                                    pickt2Rebounder = random.choices(gett2Players,weights=t2roster_df['reboundingper'],k=1)
                                    t2rebounder = t2roster_df[t2roster_df['pid'] == pickt2Rebounder[0]]
                                    printt2Rebounder = t2rebounder['fname'].item() + " " + t2rebounder['lname'].item()
                                    print("       Rebounded by " + printt2Rebounder + ".")
                                    possession = t2
                                else:
                                    pickt1Rebounder = random.choices(gett1Players,weights=t1roster_df['reboundingper'],k=1)
                                    t1rebounder = t1roster_df[t1roster_df['pid'] == pickt1Rebounder[0]]
                                    printt1Rebounder = t1rebounder['fname'].item() + " " + t1rebounder['lname'].item()
                                    print("       Rebounded by " + printt1Rebounder + ".")
                                    possession = t1
                elif eventOutcome < made2jfoulCutoff:
                    print(str(possessionNum) + " " + possession + ": " + printShooter + " 2-point jumper...Score! Fouled, and one!")
                    t2pts += 2
                    assistRand = random.random()
                    if assistRand > 0.678:
                        pickAssister = random.choices(gett2Players,weights=t2roster_df['assistper'],k=1)
                        assister = t2roster_df[t2roster_df['pid'] == pickAssister[0]]
                        printAssister = assister['fname'].item() + " " + assister['lname'].item()
                        print("       Assisted by: "+ printAssister)
                    foulShots = 1
                    ftCutoff = (0.02*shooter['2shooting'].item())+0.5
                    while foulShots > 0:
                        if random.random() > ftCutoff:
                            print("       Free throw coming up... good!")
                            t2pts += 1
                            foulShots -= 1
                            if foulShots == 0:
                                possession = t1
                        elif random.random() < ftCutoff:
                            print("       Free throw coming up... rattled out.")
                            foulShots -= 1
                            if foulShots == 0:
                                rebrand = random.random()
                                if rebrand < t2OffensiveRebound:
                                    pickt2Rebounder = random.choices(gett2Players,weights=t2roster_df['reboundingper'],k=1)
                                    t2rebounder = t2roster_df[t2roster_df['pid'] == pickt2Rebounder[0]]
                                    printt2Rebounder = t2rebounder['fname'].item() + " " + t2rebounder['lname'].item()
                                    print("       Rebounded by " + printt2Rebounder + ".")
                                    possession = t2
                                else:
                                    pickt1Rebounder = random.choices(gett1Players,weights=t1roster_df['reboundingper'],k=1)
                                    t1rebounder = t1roster_df[t1roster_df['pid'] == pickt1Rebounder[0]]
                                    printt1Rebounder = t1rebounder['fname'].item() + " " + t1rebounder['lname'].item()
                                    print("       Rebounded by " + printt1Rebounder + ".")
                                    possession = t1
            elif possrand < t2twoInsideCutoff:
                pickPlayer = random.choices(gett2Players,weights=t2roster_df['usage'],k=1)
                shooter = t2roster_df[t2roster_df['pid'] == pickPlayer[0]]
                printShooter = shooter['fname'].item() + " " + shooter['lname'].item()
                blockAdj = (0.00001*t2roster_df['defenserate'].sum())-0.0153
                made2inf = (0.005*shooter['finishing'].item())+0.513
                madeDiff = made2inf-0.563
                missed2inf = 0.147-madeDiff-blockAdj
                made2ifoul = 0.05
                missed2ifoul = 0.14
                blocked = 0.1+blockAdj
                base2iCutoff = 0
                made2iCutoff = base2iCutoff+made2inf
                missed2iCutoff = made2iCutoff+missed2inf
                blocked2iCutoff = missed2iCutoff+blocked
                missed2ifoulCutoff = blocked2iCutoff+missed2ifoul
                made2ifoulCutoff = missed2ifoulCutoff+made2ifoul
                eventOutcome = random.random()
                if eventOutcome < made2iCutoff:
                    print(str(possessionNum) + " " + possession + ": " + printShooter + " Inside shot...Score!")
                    t2pts+=2
                    assistRand = random.random()
                    if assistRand > 0.57:
                        pickAssister = random.choices(gett2Players,weights=t2roster_df['assistper'],k=1)
                        assister = t2roster_df[t2roster_df['pid'] == pickAssister[0]]
                        printAssister = assister['fname'].item() + " " + assister['lname'].item()
                        print("       Assisted by: "+ printAssister)
                    possession = t1
                elif eventOutcome < missed2iCutoff:
                    print(str(possessionNum) + " " + possession + ": " + printShooter + " Inside shot...Missed!")
                    rebrand = random.random()
                    if rebrand < t2OffensiveRebound:
                        pickt2Rebounder = random.choices(gett2Players,weights=t2roster_df['reboundingper'],k=1)
                        t2rebounder = t2roster_df[t2roster_df['pid'] == pickt2Rebounder[0]]
                        printt2Rebounder = t2rebounder['fname'].item() + " " + t2rebounder['lname'].item()
                        print("       Rebounded by " + printt2Rebounder + ".")
                        possession = t2
                    else:
                        pickt1Rebounder = random.choices(gett1Players,weights=t1roster_df['reboundingper'],k=1)
                        t1rebounder = t1roster_df[t1roster_df['pid'] == pickt1Rebounder[0]]
                        printt1Rebounder = t1rebounder['fname'].item() + " " + t1rebounder['lname'].item()
                        print("       Rebounded by " + printt1Rebounder + ".")
                        possession = t1
                elif eventOutcome < blocked2iCutoff:
                    pickBlocker = random.choices(gett1Players,weights=t1roster_df['defenseper'],k=1)
                    blocker = t1roster_df[t1roster_df['pid'] == pickBlocker[0]]
                    printBlocker = blocker['fname'].item() + " " + blocker['lname'].item()
                    print(str(possessionNum) + " " + possession + ": " + printShooter + " Inside shot...BLOCKED by " + printBlocker + ".")
                    rebrand = random.random()
                    if rebrand < 0.43:
                        pickt2Rebounder = random.choices(gett2Players,weights=t2roster_df['reboundingper'],k=1)
                        t2rebounder = t2roster_df[t2roster_df['pid'] == pickt2Rebounder[0]]
                        printt2Rebounder = t2rebounder['fname'].item() + " " + t2rebounder['lname'].item()
                        print("       Rebounded by " + printt2Rebounder + ".")
                        possession = t2
                    else:
                        pickt1Rebounder = random.choices(gett1Players,weights=t1roster_df['reboundingper'],k=1)
                        t1rebounder = t1roster_df[t1roster_df['pid'] == pickt1Rebounder[0]]
                        printt1Rebounder = t1rebounder['fname'].item() + " " + t1rebounder['lname'].item()
                        print("       Rebounded by " + printt1Rebounder + ".")
                        possession = t1
                elif eventOutcome < missed2ifoulCutoff:
                    print(str(possessionNum) + " " + possession + ": " + printShooter + " Inside shot...Missed, but fouled on the play.")
                    foulShots = 2
                    ftCutoff = (0.02*shooter['2shooting'].item())+0.5
                    while foulShots > 0:
                        if random.random() > ftCutoff:
                            print("       Free throw coming up... good!")
                            t2pts += 1
                            foulShots -= 1
                            if foulShots == 0:
                                possession = t1
                        elif random.random() < ftCutoff:
                            print("       Free throw coming up... rattled out.")
                            foulShots -= 1
                            if foulShots == 0:
                                rebrand = random.random()
                                if rebrand < t2OffensiveRebound:
                                    pickt2Rebounder = random.choices(gett2Players,weights=t2roster_df['reboundingper'],k=1)
                                    t2rebounder = t2roster_df[t2roster_df['pid'] == pickt2Rebounder[0]]
                                    printt2Rebounder = t2rebounder['fname'].item() + " " + t2rebounder['lname'].item()
                                    print("       Rebounded by " + printt2Rebounder + ".")
                                    possession = t2
                                else:
                                    pickt1Rebounder = random.choices(gett1Players,weights=t1roster_df['reboundingper'],k=1)
                                    t1rebounder = t1roster_df[t1roster_df['pid'] == pickt1Rebounder[0]]
                                    printt1Rebounder = t1rebounder['fname'].item() + " " + t1rebounder['lname'].item()
                                    print("       Rebounded by " + printt1Rebounder + ".")
                                    possession = t1
                elif eventOutcome < made2ifoulCutoff:
                    print(str(possessionNum) + " " + possession + ": " + printShooter + " Inside shot...Score! Fouled, and one!")
                    t2pts += 2
                    assistRand = random.random()
                    if assistRand > 0.57:
                        pickAssister = random.choices(gett2Players,weights=t2roster_df['assistper'],k=1)
                        assister = t2roster_df[t2roster_df['pid'] == pickAssister[0]]
                        printAssister = assister['fname'].item() + " " + assister['lname'].item()
                        print("       Assisted by: "+ printAssister)
                    foulShots = 1
                    ftCutoff = (0.02*shooter['2shooting'].item())+0.5
                    while foulShots > 0:
                        if random.random() > ftCutoff:
                            print("       Free throw coming up... good!")
                            t2pts += 1
                            foulShots -= 1
                            if foulShots == 0:
                                possession = t1
                        elif random.random() < ftCutoff:
                            print("       Free throw coming up... rattled out.")
                            foulShots -= 1
                            if foulShots == 0:
                                rebrand = random.random()
                                if rebrand < t2OffensiveRebound:
                                    pickt2Rebounder = random.choices(gett2Players,weights=t2roster_df['reboundingper'],k=1)
                                    t2rebounder = t2roster_df[t2roster_df['pid'] == pickt2Rebounder[0]]
                                    printt2Rebounder = t2rebounder['fname'].item() + " " + t2rebounder['lname'].item()
                                    print("       Rebounded by " + printt2Rebounder + ".")
                                    possession = t2
                                else:
                                    pickt1Rebounder = random.choices(gett1Players,weights=t1roster_df['reboundingper'],k=1)
                                    t1rebounder = t1roster_df[t1roster_df['pid'] == pickt1Rebounder[0]]
                                    printt1Rebounder = t1rebounder['fname'].item() + " " + t1rebounder['lname'].item()
                                    print("       Rebounded by " + printt1Rebounder + ".")
                                    possession = t1
        
                    
        if possessionNum == math.floor((t1pace+t2pace)/2):
            print("\n")
            print("-----HALFTIME!-----")
            print("Halftime score")
            print(t2 + ": " + str(t2pts))
            print(t1 + ": " + str(t1pts))
            print("\n")
    
        if possessionNum == t1pace+t2pace and t1 == t2:
            print("-----OVERTIME!-----")
            possesionNum -= math.floor((t1pace+t2pace)/8)
            
    print("\n")
    print("Final Score")
    print(t2 + ": " + str(t2pts))
    print(t1 + ": " + str(t1pts))
    print("\n")
rungame()