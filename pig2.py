import random
import time

class Player:
    def __init__(self,player_name):
        self.total_score = 0
        self.this_round_score = 0
        self.on_turn = False
        self.player_name = player_name
    def get_total_score(self):
        return self.total_score
    def get_this_round_score(self):
        return self.this_round_score
    def set_on_turn(self,on_turn):
        self.on_turn = on_turn
    def add_score(self,added_score):
        self.this_round_score = self.this_round_score + added_score
        if self.this_round_score + self.total_score >=100:
            self.total_score=self.this_round_score + self.total_score
            #self.this_round_score = 0
    def hold(self):
        self.total_score = self.this_round_score + self.total_score
        self.this_round_score = 0
        self.on_turn = False
    def lost_score(self):
        self.this_round_score = 0
        self.on_turn = False
    def get_player_name(self):
        return self.player_name
    def get_player_type(self):
        return self.player_name[0:0]

class ComputerPlayer(Player):
    def roll_or_hold(self):
        if self.this_round_score<min(25,100-self.total_score):
            return "r"
        else:
            return "h"

class HumanPlayer(Player):
    def roll_or_hold(self):
        return input(self.player_name + ", do you want to roll or hold (r:roll / h:hold): ")

class FactoryPlayer:
    def getPlayer(self,player_name,player_type):
        if player_type=="Human":
            return HumanPlayer(player_name)
        else:
            return ComputerPlayer(player_name)

class Die:
    def __init__(self):
        self.die_number = 0
    def roll(self):
        self.die_number = random.randint(1,6)
    def get_die_number(self):
        return self.die_number
class Proxy():
    def __init__(self):
        self.start_time = time.perf_counter()
        print("Game starts!")
    def get_elapsed_time(self):
        return time.perf_counter() - self.start_time
    def end_game(self,players):
        highest_player = players[0]
        for player in players:
            if player.get_this_round_score()+player.get_total_score()>highest_player.get_this_round_score()+highest_player.get_total_score():
                highest_player=player
        print("Game time exceed 1 minute, game over, "+highest_player.get_player_name()+" win the game with the highest score "+str(highest_player.get_this_round_score()+highest_player.get_total_score())+"!")

def main():
    game_start = 1
    number_of_players = input("Please input how many players: ")
    players =[]
    for i in range(int(number_of_players)):
        factory_player=FactoryPlayer()
        player_type=input("Please input player type of player"+str(i+1)+" (h:human / c:computer): ")
        player_name = ""
        if player_type=="h":
            player_name = "Human Player " + str(i + 1)
            player = factory_player.getPlayer(player_name,"Human")
            players.append(player)
        else:
            player_name = "Computer Player " + str(i + 1)
            player = factory_player.getPlayer(player_name, "Computer")
            players.append(player)
    proxy = Proxy()
    on_turn_index = 0
    die = Die()
    while game_start==1:
        change_turn=0
        while change_turn==0:
            decision = players[on_turn_index].roll_or_hold()
            # decision = input("Player"+str(on_turn_index+1)+", do you want to roll or hold (r:roll / h:hold): ")
            if decision=="r":
                die.roll()
                if die.get_die_number()==1:
                    players[on_turn_index].lost_score()
                    change_turn =1
                else:
                    players[on_turn_index].add_score(die.get_die_number())
                print(players[on_turn_index].get_player_name() + " rolled " + str(die.get_die_number())
                      +", total score is "+str(players[on_turn_index].get_total_score())
                      +", score in this round is "+str(players[on_turn_index].get_this_round_score()))
                if players[on_turn_index].get_total_score()>=100:
                    game_start = 0
                    change_turn =1
                    print(players[on_turn_index].get_player_name() + " win the game with a total of " + str(
                        players[on_turn_index].get_total_score()) + "!")
            else:
                players[on_turn_index].hold()
                print(players[on_turn_index].get_player_name() + " hold with a score of "+str(
                        players[on_turn_index].get_total_score()))
                change_turn=1
            if proxy.get_elapsed_time()>=60:
                proxy.end_game(players)
                game_start=0
            else:
                print("Game elapes "+str(proxy.get_elapsed_time())+" seconds")
        if on_turn_index != int(number_of_players) - 1:
            on_turn_index = on_turn_index + 1
        else:
            on_turn_index = 0


if __name__ == "__main__":
    main()