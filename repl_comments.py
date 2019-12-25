
#Simple Program To Print Previous comments entered
comments = list()

def printComments():
    for cmnd in comments:
        print(cmnd)

while True:
    comment = input('Enter Your Input [Press q to leave ] ')
    if comment == 'q' or comment == 'Q':
        break
    
    comments.append(comment)
    printComments()
    

print("Program Terminated Succesfuly ")