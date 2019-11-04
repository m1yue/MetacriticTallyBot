#pretty prints the scores
#input scores in ascending order
def print_tallies(sorted_scores):
    for index, num in enumerate(reversed(sorted_scores)):
        print("{:02d}".format(10-index), '-', end=" ")
        for i in range(num):
            print('|', end="")
        
        print("")
        
