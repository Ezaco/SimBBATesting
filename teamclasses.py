class ImportDTO:
    def __init__(self, r):
        self.Results = r

class MatchResults:
    def __init__(self, t1, t2, r1, r2, game_id):
        self.TeamOne = t1
        self.TeamTwo = t2
        self.RosterOne = r1
        self.RosterTwo = r2
        self.GameID = game_id

class Team:
    def __init__(self, t):
        self.TeamName = t['TeamName']
        self.Mascot = t['Mascot']
        self.Abbr = t['Abbr']
        self.Conference = t['Conference']
        self.Coach = t['Coach']
        self.ID = t['ID']
        self.Stats = TeamStats()

class TeamStats:
    def __init__(self):
        self.Points = 0
        self.Possessions = 0
        self.FGM = 0
        self.FGA = 0
        self.FGPercent = 0
        self.ThreePointsMade = 0
        self.ThreePointAttempts = 0
        self.ThreePointPercent = 0
        self.FTM = 0
        self.FTA = 0
        self.FTPercent = 0
        self.Rebounds = 0
        self.OffRebounds = 0
        self.DefRebounds = 0
        self.Assists = 0
        self.Steals = 0
        self.Blocks = 0
        self.TotalTurnovers = 0
        self.LargestLead = 0
        self.FirstHalfScore = 0
        self.SecondHalfScore = 0
        self.OvertimeScore = 0
        self.Fouls = 0

    def AddPoints(self, pts, poss, ht, is_ot):
        self.Points += pts
        if poss <= ht:
            self.FirstHalfScore += pts
        elif is_ot == False:
            self.SecondHalfScore += pts  
        else:
            self.OvertimeScore += pts
    def CalculateLead(self, pts, diff):
        if self.LargestLead < diff:
            self.LargestLead += pts
    def AddFieldGoal(self, made_shot):
        self.FGA += 1
        if made_shot == True:
            self.FGM += 1
        self.FGPercent = self.FGM / self.FGA
    def AddThreePointShot(self, made_shot):
        self.ThreePointAttempts += 1
        if made_shot == True:
            self.ThreePointsMade += 1
        self.ThreePointPercent = self.ThreePointsMade / self.ThreePointAttempts
    def AddFreeThrow(self, made_shot):
        self.FTA += 1
        if made_shot == True:
            self.FTM += 1
        self.FTPercent = self.FTM / self.FTA
    def AddRebound(self, is_offense):
        self.Rebounds += 1
        if is_offense == True:
            self.OffRebounds += 1
        else:
            self.DefRebounds += 1
    def AddAssist(self):
        self.Assists += 1
    def AddSteal(self):
        self.Steals += 1
    def AddBlocks(self):
        self.Blocks += 1
    def AddTurnover(self):
        self.TotalTurnovers += 1
    def AddPossession(self):
        self.Possessions += 1
    def AddFoul(self):
        self.Fouls += 1

class Roster:
    def __init__(self, r):
        self.roster = r

class CollegePlayer:
    def __init__(self, cp):
        self.ID = cp['ID']
        self.FirstName = cp['FirstName']
        self.LastName = cp['LastName']
        self.TeamID = cp['TeamID']
        self.TeamAbbr = cp['TeamAbbr']
        self.IsRedshirt = cp['IsRedshirt']
        self.IsRedshirting = cp['IsRedshirting']
        self.Position = cp['Position']
        self.Age = cp['Age']
        self.Stars = cp['Stars']
        self.Height = cp['Height']
        self.Shooting2 = cp['Shooting2']
        self.Shooting3 = cp['Shooting3']
        self.Finishing = cp['Finishing']
        self.Ballwork = cp['Ballwork']
        self.Rebounding = cp['Rebounding']
        self.Defense = cp['Defense']
        self.Stamina = cp['Stamina']
        self.Minutes = cp['Minutes']
        self.Overall = cp['Overall']
        self.Stats = CollegePlayerStats(cp)
        self.Shooting = 0
        self.AdjShooting = 0
        self.AdjFinishing = 0
        self.AdjBallwork = 0
        self.AdjRebounding = 0
        self.AdjDefense = 0
        self.ReboundingPer = 0
        self.DefensePer = 0
        self.AssistPer = 0
        self.Usage = 0
        
    def get_advanced_stats(self, totalrebounding, totalDefense, totalAssist):
        self.Shooting = ((self.Shooting2 + self.Shooting3) / 2)
        self.AdjShooting = self.Shooting * self.Minutes
        self.AdjFinishing = self.Finishing * self.Minutes
        self.AdjBallwork = self.Ballwork * self.Minutes
        self.AdjRebounding = self.Rebounding * self.Minutes
        self.AdjDefense = self.Defense * self.Minutes
        self.ReboundingPer = self.AdjRebounding / totalrebounding
        self.DefensePer = self.AdjDefense / totalDefense
        self.AssistPer = self.AdjBallwork / totalAssist
        self.Usage = self.Minutes / 20

class CollegePlayerStats:
    def __init__(self, cp):
        self.CollegePlayerID = cp['ID']
        self.Minutes = cp['Minutes']
        self.Possessions = 0
        self.FGM = 0
        self.FGA = 0
        self.FGPercent = 0
        self.ThreePointsMade = 0
        self.ThreePointAttempts = 0
        self.ThreePointPercent = 0
        self.FTM = 0
        self.FTA = 0
        self.FTPercent = 0
        self.Points = 0
        self.TotalRebounds = 0
        self.OffRebounds = 0
        self.DefRebounds = 0
        self.Assists = 0
        self.Steals = 0
        self.Blocks = 0
        self.Turnovers = 0
        self.Fouls = 0

    def AddPossession(self):
        self.Possessions += 1

    def AddFieldGoal(self, made_shot, pts = 0):
        self.Possessions += 1
        self.FGA += 1
        if (made_shot):
            self.FGM += 1
            self.Points += pts
        self.FGPercent = self.FGM / self.FGA
        if pts == 3:
            self.AddThreePoint(made_shot)
        

    def AddThreePoint(self, made_shot):
        self.ThreePointAttempts += 1
        if made_shot:
            self.ThreePointsMade += 1
        self.ThreePointPercent = self.ThreePointsMade / self.ThreePointAttempts

    def AddFTAttempt(self):
        self.FTA += 1
        self.FTPercent = self.FTM / self.FTA

    def AddFTMade(self):
        self.FTA += 1
        self.FTM += 1
        self.FTPercent = self.FTM / self.FTA
        self.Points += 1

    def AddAssist(self):
        self.Assists += 1

    def AddSteal(self):
        self.Steals += 1

    def AddBlock(self):
        self.Blocks += 1

    def AddRebound(self, is_offense):
        self.TotalRebounds += 1
        if is_offense == True:
            self.OffRebounds += 1
        else:
            self.DefRebounds += 1

    def AddTurnover(self):
        self.Turnovers += 1

    def AddFoul(self):
        self.Fouls += 1