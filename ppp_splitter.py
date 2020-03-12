#!/usr/bin/python
import sys

# input:   each players profit and losses
# output:  each players rake earned
#
# Rule: Player that loses the most gets the rake
# until they are equal with the second biggest loser,
# then they share the rake until they tie the third
# and so on...
def rake_calculator(player_pl):
    rake = -1 * sum(player_pl)
    if (rake < 0):
        raise Exception("Negative Rake.")
    player_pl_with_rake = player_pl[:]
    rake_total = [0]*len(player_pl)
    
    # We distribute rake to the players 
    # that have lost the most until 
    # they tie the next person.
    while(rake > 0):
        
        # Find who deserves rake.
        lowest = min(player_pl_with_rake)
        player_indices_earning_rake = []
        for i in range(len(player_pl)):
            if (player_pl_with_rake[i] == lowest):
                player_indices_earning_rake.append(i)
                
        # Find the second biggest loser, 
        # the one not getting rake.
        second_lowest = 0
        for i in range(len(player_pl)):
            if (player_pl_with_rake[i] > lowest):
                if (player_pl_with_rake[i] < second_lowest):
                    second_lowest = player_pl_with_rake[i]
                    
        # How much rake we are giving out this round.
        # Either enough so we tie the second biggest loser
        # or the rest of the rake.
        giving_cap = (second_lowest-lowest) * len(player_indices_earning_rake)
        amt_to_give = min(giving_cap, rake)
        
        # Give the rake
        amt_per_player = amt_to_give / len(player_indices_earning_rake)
        for i in player_indices_earning_rake:
            rake_total[i] += amt_per_player
            player_pl_with_rake[i] += amt_per_player
        rake -= amt_to_give
        
    return rake_total
      

# input format: [name1,PL1,name2,PL2,...]
def main(argv):
    # Parse the input.
    if (len(argv) % 2 == 1):
        print("Player and PL do not match up.")
        return
    number_of_players = len(argv) // 2
    player_names = []
    player_pl = []
    for i in range(number_of_players):
        player_names.append(argv[2*i])
        player_pl.append(float(argv[2*i+1]))
    
    # Give out rake.
    player_rake = rake_calculator(player_pl)
    for i in range(number_of_players):
        player_pl[i] += player_rake[i]
    print("Rake Earned:")
    for i in range(number_of_players):
        if (player_rake[i] > 0):
            print("{0}: {1:.2f}".format(player_names[i],player_rake[i]))
    print(" ")
    
    # Collect the transactions 
    output = []
    
    # Every iteration of the loop makes a new transaction.
    # The biggest winner pays the biggest loser until one 
    # of them is break even. Then repeat.
    while(max(player_pl) > .001):
        
        # Find the biggest winner and loser
        biggest_winner_amt = max(player_pl)
        biggest_loser_amt = min(player_pl)
        biggest_winner_index = -1
        biggest_loser_index = -1
        for i in range(number_of_players):
            if (player_pl[i] == biggest_winner_amt):
                biggest_winner_index = i
            if (player_pl[i] == biggest_loser_amt):
                biggest_loser_index = i 
        assert(biggest_winner_index != -1)
        assert(biggest_loser_index  != -1)
        
        # Make the payment
        if (biggest_winner_amt > -1*biggest_loser_amt):
            output.append("{0:<10} pays {1:<10} {2:>8.2f}".format(
                                                player_names[biggest_loser_index],
                                                player_names[biggest_winner_index],
                                                -1*biggest_loser_amt))
            player_pl[biggest_winner_index] += biggest_loser_amt
            player_pl[biggest_loser_index]  -= biggest_loser_amt  
        else:
            output.append("{0:<10} pays {1:<10} {2:>8.2f}".format(
                                                player_names[biggest_loser_index],
                                                player_names[biggest_winner_index],
                                                biggest_winner_amt))
            player_pl[biggest_winner_index] -= biggest_winner_amt
            player_pl[biggest_loser_index]  += biggest_winner_amt
    
    # Print out the payments.
    # Sorting organizes by payer.
    output.sort()
    for i in output:
        print(i)
    return
        
if __name__ == "__main__":
   main(sys.argv[1:])
