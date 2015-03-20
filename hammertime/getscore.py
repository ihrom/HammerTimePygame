


def get_high_score():
    high_score = 0
    try:
        high_score_file = open('hammertime\\high_score.txt','r')
        high_score = int(high_score_file.read())
        high_score_file.close()
    except IOError:
        print('There is no high score yet...')
    return high_score

def save_high_score(new_high_score):
    try:
        high_score_file = open('hammertime\\high_score.txt','w')
        high_score_file.write(str(new_high_score))
        high_score_file.close()
    except IOError:
        print('Unable to save the high score.')
        
