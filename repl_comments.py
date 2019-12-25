#Program To Print Previous comments entered. Secured with Password.

from hashlib import sha256

def create_hash(password):
    pw_bytestring = password.encode()
    return sha256(pw_bytestring).hexdigest()
def printComments():
    print("Previously entered comments:")
    for i,cmnd in enumerate(comments):
        print(i+1,'.',cmnd)

comments = list()
pw_hash = "55f96f7d175068fba8700315b5849c1ffbb1d037e64bccb69abc81e8baf64416"

while True:
    comment = input('Enter Your Comment [Press q to leave ] ')
    if comment == 'q' or comment == 'Q':
        break
    pw_confirmation = create_hash(input('Enter Your Password: '))
    if pw_hash != pw_confirmation:
        print("I a sorry I can’t let you do that.")
        continue
    else:
        comments.append(comment)
        printComments()
    

print("Program Terminated Succesfuly ")
