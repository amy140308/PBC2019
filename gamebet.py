#這個需要在class team與class bet之下
class gamebet():
    """
    def odds 需要輸入雙方隊伍名字
    return 賠率清單，單元數固定
    [['單雙', '單', 1.75, '雙', 1.75],
     ['大小(總分)', '大於X分', 1.75, '小於X分', 1.75],
     ['不讓分', 'A隊名', A賠率, 'B隊名', B賠率]]
    """
    def odds(self, team_name_A, team_name_B):
        print("***calculating odds...")
        data_list = []
        
        #獲得雙方隊伍勝率與平均得分
        print("getting team", team_name_A, "stats...")
        teamA = Team(team_name_A)
        teamA.get_info() #勝率是int(teamA.info[4])
        self.win_oddsA = (float(teamA.info[4][:(len(teamA.info[4])-1)]) / 100)
        teamA.get_game() #平均得分是teamA.game[(len(teamA.game) - 1)]
        self.score_A = teamA.game[(len(teamA.game) - 1)]
        
        print("getting team", team_name_B, "stats...")        
        teamB = Team(team_name_B)
        teamB.get_info() #勝率B是int(teamB.info[4])
        self.win_oddsB = (float(teamB.info[4][:(len(teamB.info[4])-1)]) / 100)
        teamB.get_game() #平均得分是teamB.game[(len(teamB.game) - 1)]
        self.score_B = teamB.game[(len(teamB.game) - 1)]
        
        """
        賠率公式：
        1. 單雙：雙方賠率都是1.75
        2. 大小(總分)：
        3. 不讓分：需判斷勝率/平均總分，決定賠率
        簡易版本：勝率對應好壞狀態，若A好B壞，則A贏；反之則B贏。若A好B好，A壞B壞，則判斷平均得分。
        若平均得分相差小於9分，則判定勝率各半。
        勝率倒數為賠率，Cap最高是3.75倍，最低是1.15倍
        """
        
        #單雙
        data_list.append(['單雙', '單', 1.75, '雙', 1.75])
        
        #大小
        scoresum = teamA.game[(len(teamA.game) - 1)] + teamB.game[(len(teamB.game) - 1)]
        scoresum = int(scoresum) + 0.5 #確保大小是以.5結尾
        data_list.append(['大小(總分)', ('大於' + str(scoresum) + '分'), 1.75,
                          ('小於' + str(scoresum) + '分'), 1.75])
        
        #不讓分
        teamA_odds = self.win_oddsA * (1 - self.win_oddsB)
        teamB_odds = self.win_oddsB * (1 - self.win_oddsA)
        
        if abs(self.score_A - self.score_B) <= 9:
            teamA_odds += ((1 - teamA_odds) - teamB_odds) / 2
            teamB_odds += ((1 - teamA_odds) - teamB_odds) / 2 

        elif self.score_A > self.score_B:
            teamA_odds += (1 - teamA_odds - teamB_odds)

        elif self.score_A < self.score_B:
            teamB_odds += (1 - teamA_odds - teamB_odds)
        
        print('win odds:', teamA_odds, teamB_odds)

        if teamA_odds != 0 and teamB_odds != 0: #判斷Cap
            teamA_odds = round((1 / teamA_odds), 2)
            teamB_odds = round((1 / teamB_odds), 2)
            
            teamA_odds = 3.75 if (teamA_odds > 3.75) else teamA_odds
            teamA_odds = 1.15 if (teamA_odds < 1.15) else teamA_odds
            teamB_odds = 3.75 if (teamB_odds > 3.75) else teamB_odds
            teamB_odds = 1.15 if (teamB_odds < 1.15) else teamB_odds
    
        else: #如果有一方勝率為0時，則直接給上下Cap最大賠率
            if teamA_odds == 0:
                teamA_odds = 3.75
                teamB_odds = 1.15
                
            elif teamB_odds == 0:
                teamA_odds = 1.15
                teamB_odds = 3.75
        
        print('bet odds for 不讓分:', teamA_odds, teamB_odds)
        
        data_list.append(['不讓分', team_name_A, teamA_odds, team_name_B, teamB_odds])
        
        return data_list
