'''201624419/KimDoHyoung/010-2399-0652'''

sentence = input("Enter a sentence: ")
word = input("Enter word to replace: ")
replacementWord = input("Enter replacement word: ")

if word in sentence:
    sentence = sentence.replace(word, replacementWord)
    print(sentence)
else:
    print("There's no word in the sentence.")
