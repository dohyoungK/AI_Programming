'''201624419/KimDoHyoung'''

startingWord = "NAISNIENLGELTETWEORRSD"
crossedOutLetters = ""
remainingLetters = ""

for i in range(0, len(startingWord)):
    if (i%2) == 0:
        crossedOutLetters += startingWord[i] + " "
    else:
        remainingLetters += startingWord[i] + " "

print("Starting word:", startingWord)
print("Crossed out letters:", crossedOutLetters)
print("Remaining letters:", remainingLetters)




