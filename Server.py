import rpyc
import random


suits = ["♥", "♠", "♦", "♣"]
ranks = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
val_map = {"A":1,"2":2,"3":3,"4":4,"5":5,"6":6,"7":7,"8":8,"9":9,"10":10,"J":10,"Q":10,"K":10}  # 先默认A为1


# exposed_开头的方法可被客户端调用
class MyService(rpyc.Service):
    def __init__(self):
        self.cards = [[rank, suit] for rank in ranks for suit in suits]
        self.dealer_hole_card = []
        self.dealer_card = []
        self.player_card = []
        self.is_start = False
        self.dealer_turn = False
        self.dealer_possible_val = []
        self.player_possible_val = []

    def shuffle(self):
        self.cards = [[rank, suit] for rank in ranks for suit in suits]
        random.shuffle(self.cards)
        self.dealer_hole_card = []
        self.dealer_card = []
        self.player_card = []
        self.is_start = False
        self.dealer_turn = False
        self.dealer_possible_val = []
        self.player_possible_val = []
    def exposed_show_card(self):
        hole_card = self.dealer_hole_card if self.dealer_turn else [["*","*"]]
        dealer_card = hole_card +self.dealer_card
        card_str = f'Dealer:{dealer_card}\nPlayer:{self.player_card}'
        print(card_str)
        return card_str
    def update_val(self, who="player"):
        card_list = self.player_card
        if who == "dealer":
            card_list = self.dealer_card + self.dealer_hole_card
        sum_val = 0
        for card in card_list:
            sum_val += val_map[card[0]]
        possible_val = [sum_val, sum_val+10] \
            if any(card[0]=="A" for card in card_list) else [sum_val, 0]
        if who == "dealer":
            self.dealer_possible_val = possible_val
        else:
            self.player_possible_val = possible_val

    def exposed_get_max_val(self, who="player"):
        if who == "dealer":
            return max(self.dealer_possible_val[0], self.dealer_possible_val[1]) \
            if self.dealer_possible_val[1] <= 21 else self.dealer_possible_val[0]
        return max(self.player_possible_val[0], self.player_possible_val[1]) \
            if self.player_possible_val[1] <= 21 else self.player_possible_val[0]

    def is_bust(self, who="player"):
        sum_val = self.player_possible_val
        if who == "dealer":
            sum_val = self.dealer_possible_val
        return True if sum_val[0]>21 else False
    def exposed_dealer_is_bust(self):
        return self.is_bust("dealer")
    def exposed_player_is_bust(self):
        return self.is_bust("player")
    def get_one_card(self):
        card = random.choice(self.cards)
        self.cards.remove(card)
        return card
    def exposed_dealer_get_card(self):
        self.dealer_card.append(self.get_one_card())
        self.update_val(who="dealer")
    def exposed_player_get_card(self):
        self.player_card.append(self.get_one_card())
        self.update_val(who="player")
    def dealer_get_hole_card(self):
        self.dealer_hole_card.append(self.get_one_card())
        self.update_val(who="dealer")
    def exposed_start(self):
        print('---------------------[New Game]---------------------')
        self.shuffle()
        if self.is_start:
            return
        self.dealer_get_hole_card()
        self.exposed_dealer_get_card()
        self.exposed_player_get_card()
        self.exposed_player_get_card()
        self.is_start = True
    def exposed_dealer_turn(self):
        self.dealer_turn = True



server = rpyc.ThreadedServer(MyService(), port=18861) # protocol_config={"allow_public_attrs": True, } 访问built-in 属性
server.start()