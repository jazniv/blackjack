import random

class blackjack():

    def __init__(self, dealer_hand=[], player_hand=[]):
        self.dealer_hand = []
        self.player_hand = []
        self.deck = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13] * 16

    def getHand(self, hand):

        for card in hand:
            if card == 1: print("A")
            elif card == 11: print("J")
            elif card == 12: print("Q")
            elif card == 13: print("K")
            else: print(card)
        
        print()
    
    def deal(self):
        hand = []
        for _ in range(2):
            random.shuffle(self.deck)
            hand.append(self.deck.pop())
        return hand
    
    def hit(self, hand):
        random.shuffle(self.deck)
        hand.append(self.deck.pop())
        return hand
    
    def total(self, hand):
        total = 0

        for card in hand:
            if card == 1:
                if total <= 11: total += 11
                else: total += 1
            elif card in {11, 12, 13}: total += 10
            else: total += card
        
        return total
    
    def score(self):
        player_total = self.total(self.player_hand)
        dealer_total = self.total(self.dealer_hand)

        if player_total == 21:
            if dealer_total == 21: return "Push"
            else: return "Player won"
        elif player_total < 21 and dealer_total <= 21:
            if player_total > dealer_total: return "Player won"
            elif player_total == dealer_total: return "Push"
            else: return "Dealer won"
        elif player_total < 21 and dealer_total >= 21:
            return "Player won, dealer bust"
        elif player_total > 21 and dealer_total <= 21:
            return "Dealer won, player bust"
        elif player_total > 21 and dealer_total > 21: 
            return "Push"
    
    def play(self):
        self.dealer_hand = self.deal()
        self.player_hand = self.deal()

        while True:
            print("\nPlayer's Hand:") 
            self.getHand(self.player_hand)

            print("Dealer's Card:")
            dealer_first = [self.dealer_hand[0]]
            self.getHand(dealer_first)

            choice = input("[h]it or [s]tand? ")

            while choice == "h":
                print("Player hits")
                self.player_hand = self.hit(self.player_hand)

                print("Player's Updated Cards:")
                self.getHand(self.player_hand)
                
                if self.total(self.player_hand) > 21: break

                choice = input("[h]it or [s]tand? ")
                
                if choice == "s":
                    print("Player stands")
                    break
            
            while self.total(self.dealer_hand) <= 17:
                self.dealer_hand = self.hit(self.dealer_hand)

            print("\nPlayer's Final Hand:") 
            self.getHand(self.player_hand)

            print("Dealer's Final Hand:")
            self.getHand(self.dealer_hand)            
            
            print("Total Scores:")
            print("Player: ", self.total(self.player_hand))
            print("Dealer: ", self.total(self.dealer_hand))
            print(self.score())
            
            choice = input("\n[p]lay again: ")
            if choice != "p": break
    
    def play_sim(self):
        self.dealer_hand = self.deal()
        self.player_hand = self.deal()

        choice = self.sim_choice()

        while choice == 1:
            self.player_hand = self.hit(self.player_hand)
            if self.total(self.player_hand) > 21: break
            choice = self.sim_choice()
            if choice == 0:
                break
        
        while self.total(self.dealer_hand) <= 17:
            self.dealer_hand = self.hit(self.dealer_hand)

        return self.score()
    
    # 0 = stand, 1 = hit
    def sim_choice(self):
        dealer_card = self.dealer_hand[0]
        if dealer_card in {11, 12, 13}: dealer_card = 10

        player_total = self.total(self.player_hand)

        hard_rules = {
            1 : 16,
            2 : 12,
            3 : 12,
            4 : 11,
            5 : 11,
            6 : 11,
            7 : 16,
            8 : 16,
            9 : 16,
            10: 16
        }

        soft_rules = {
            1 : 18,
            2 : 17,
            3 : 17,
            4 : 17,
            5 : 17,
            6 : 17,
            7 : 17,
            8 : 17,
            9 : 18,
            10: 18
        }

        # soft rules
        if 1 in self.player_hand:
            if player_total > soft_rules[dealer_card]: return 0
            else: return 1
        # hard rules
        else:
            if player_total > hard_rules[dealer_card]: return 0
            else: return 1

    def simulate(self):
        player_wins = 0

        for _ in range(10):
            res = self.play_sim()
            if "Player won" in res: player_wins += 1
        
        return player_wins

total_wins = 0
for _ in range(1000):
    total_wins += blackjack().simulate()

print("Player won %s percent of the time" % str(total_wins/100))