# CS1210: HW1
######################################################################
# Complete the signed() function, certifying that:
#  1) the code below is entirely your own work, and
#  2) it has not been shared with anyone outside the intructional team.
#
def signed():
    return(["cjdittmer"])

######################################################################
# In this homework, you will be implementing a spelling bee game,
# inspired by the that appears in the New York Times. The purpose of
# the game is to find as many possible words from a display of 7
# letters, where each word must meet the following criteria:
#   1. it must consist of four or more letters; and
#   2. it must contain the central letter of the display.
# So, for example, if the display looks like:
#    T Y
#   B I L
#    M A
# where I is the "central letter," the words "limit" and "tail" are
# legal, but "balmy," "bit," and "iltbma" are not.
#
# We'll approach the construction of our system is a step-by-step
# fashion; for this homework, I'll provide specs and function
# signatures to help you get started. If you stick to these specs and
# signatures, you should soon have a working system.
#
# First, we'll need a few functions from the random module. Read up on
# these at docs.python.org.
from random import choice, randint, sample

######################################################################
# fingerprint(W) takes a word, W, and returns a fingerprint of W
# consisting of an ordered set of the unique character constituents of
# the word. You have already encountered fingerprint(W) so I will
# provide the reference solution here for you to use elsewhere.
def fingerprint(W):
    return(''.join(sorted(set(W))))
######################################################################
# score(W) takes a word, W, and returns how many points the word is
# worth. The scoring rules here are straightforward:
#   1. four letter words are worth 1 point;
#   2. each additional letter adds 1 point up to a max of 9; and
#   3. pangrams (use all 7 letters in display) are worth 10 points.
# So, for example:
#      A L
#     O B Y
#      N E
#   >>> score('ball')
#   1
#   >>> score('balloon')
#   4
#   >>> score('baloney')
#   10     # Pangram!
#
def score(W):
    score = 0
    if len(W) >= 4:
        if len(W) == 4:
            score = 1
        elif len(W) == 5:
            score = 2
        elif len(W) == 6:
            score = 3
        elif len(W) == 7:
            if len(fingerprint(W)) == 7:
                score = 10
            else:
                score = 4
    return(score)
######################################################################
# jumble(S, i) takes a string, S, having exactly 7 characters and an
# integer index i where 0<=i<len(S). The string describes a puzzle,
# while i represents the index of S corresponding to the "central"
# character in the puzzle. This function doesn't return anything, but
# rather prints out a randomized representation of the puzzle, with
# S[i] at the center and the remaining characters randomly arrayed
# around S[i]. So, for example:
#    >>> jumble('abelnoy', 1)
#     A L
#    O B Y
#     N E
#    >>> jumble('abelnoy', 1)
#     N Y
#    L B A
#     E O
#
def jumble(S, i):
    SNotI = [x for x in S if x != S[i]]     #initialize the word without the center value
    randomString = []
    for x in range(0,7, 1):     # loop to organize the word into the format it will be printed
        if x != 3:  #as long as the code is not at the center value
            randomInt = randint(0, len(SNotI)-1)    #takes a random integer to use for taking a random value from the SNotI list
            randomString.append(SNotI[randomInt])   #adds letter to the randomstring
            SNotI.remove(SNotI[randomInt])  #removes letter from list so it is not reused
        else:
            randomString.append(S[i])   #once the code reaches the center value it adds the value with position i to the string
    
    print('', randomString[0].capitalize(), randomString[1].capitalize()) 
    print(randomString[2].capitalize(), randomString[3].capitalize(), randomString[4].capitalize()) #Print statment to create the wanted look for the game
    print('', randomString[5].capitalize(), randomString[6].capitalize())  
######################################################################
# readwords(filename) takes the name of a file containing a dictionary
# of English words and returns two values, a dictionary of legal words
# (those having 4 or more characters and fingerprints of 7 of fewer
# characters), with fingerprints as keys and values consisting of sets
# of words with that fingerprint, as well as a list, consisting of all
# of the unique keys of the dictionary having exactly 7 characters (in
# no particular order).
#
# Your function should provide some user feedback. So, for example:
#    >>> D,S=readwords('words.txt')
#    113809 words read: 82625 usable; 33830 unique fingerprints.
#    >>> len(S)
#    13333
#    >>> S[0]
#    'abemort'
#    >>> D[S[0]]
#    {'barometer', 'bromate'}
#
def readwords(filename):
    
    readFile = open(filename)   #creates a variable that reads the list
    legalWords = []     #List for the legal words in the game
    allFingerPrints = []    #all the finger prints in the game
    uniqueFingerprints = []     #all finger prints with length 7
    wordCounter = 0     #counter to count how many words are read from the text file
    wordDictionary = dict()     #dictionary that will be returned in the function 
    for line in readFile:
        wordCounter = wordCounter + 1
        if len(line) >= 5 and len(fingerprint(line))<= 8:   #is word legal? (value greater than expected do to hidden /n in each word)
            legalWords.append(line)
            if fingerprint(line) not in allFingerPrints:    #makes sure repeat finger prints are not re added to list
                allFingerPrints.append(fingerprint(line))      
        if len(fingerprint(line)) == 8:     #is fingerprint = 7? (value greater than expected do to hidden /n in each word)
            if fingerprint(line[:-1]) not in uniqueFingerprints:
                uniqueFingerprints.append(fingerprint(line[:-1]))   # the[:-1] makes sure that the /n is not included in the list
    for x in legalWords:
        wordDictionary[fingerprint(x[:-1])] = x[:-1]    # the[:-1] makes sure that the /n is not included in the list
    print(wordCounter, 'words read:', len(legalWords), 'usable;', len(allFingerPrints), 'unique fingerprints.')
    return(wordDictionary,uniqueFingerprints)   
       
D,S = readwords('words.txt')
######################################################################
# round(D, S) takes two arguments, corresponding to the values
# returned by readwords(), randomly selects a puzzle seed from the
# list S and a central letter from within S. It then shows the puzzle
# and enters a loop where the user can:
#    1. enter a new word for scoring;
#    2. enter / to rescramble and reprint the puzzle;
#    3. enter + for a new puzzle; or
#    4. enter . to end the game.
# When a word is entered, it is checked for length (must be longer
# than 4 characters and its fingerprint must be contained within the
# puzzle seed). The word is then checked against D, and if found, is
# scored and added to the list of words.
#
# Here is a sample interactive transcript of round() in action:
#    >>> D,S = readwords('words.txt')
#    >>> round(D,S)
#     E H
#    R P U
#     O S
#    Input words, or: '/'=scramble; ':'=show; '+'=new puzzle; '.'=quit
#    sb> pose
#    Bravo! +1
#    sb> repose
#    Bravo! +3
#    sb> house
#    Word must include 'p'
#    sb> :
#    2 words found so far:
#      pose
#      repose
#    sb> /
#     H R
#    O P E
#     S U
#    sb> prose
#    Bravo! +2
#    sb> +
#    You found 3 of 415 possible words: you scored 6 points.
#    True
#
def round(D, S):
    randomFingerprintint = randint(0, len(S)-1)     #takes a random value to find a random word in the fingerprint List
    randomFingerprint = S[randomFingerprintint]     #set the found word as the word for the game     
    centerLetter = randint(0, len(randomFingerprint)-1)     #take random number to set as the center letter value
    jumble(randomFingerprint, centerLetter)     #calls jumble function to print out word in format for the game
    loopBreak = 0   #value to break while loop when the game is finished
    listOfWords = []    #List of used words(gets refreshed if user wants new puzzle)
    totalScore = 0      #List of current score(gets refreshed if user wants new puzzle)
    potentialWords = 0  #Number of potential words for puzzle
    for x in D:     #Loop to find number of potential words
        possibleWord = x    #takes a word from the dictionary
        wordChecker = 0
        for y in possibleWord:  #Loop to check if the word can be made from the puzzle word 
            if y in randomFingerprint:
                wordChecker = wordChecker + 1   
        if wordChecker == len(possibleWord):    #If word can be made by puzzle 1 is added to number of possible words  
            potentialWords = potentialWords + 1                     
    while loopBreak == 0:   #will continue until user inputs . to change loopBreak to 1             
        userInput = (input("Input words, or: '/'=scramble; ':'=show; '+'=new puzzle; '.'=quit\n")).lower()  #Asks user for input and stores as userInput
        if userInput == '/':    #scramble current word
            jumble(randomFingerprint, centerLetter)
        elif userInput == ':':  #check amount of words found and what they are
            print('Words found so far', len(listOfWords))
            for word in listOfWords:    #Loop to print all words found
                print(word)
        elif userInput == '+':  #Reinitializes values from before the while loop to reset game
            print('You found', len(listOfWords), 'of', potentialWords, 'possible words: you scored', totalScore, 'points.' )
            randomFingerprintint = randint(0, len(S)-1)
            randomFingerprint = S[randomFingerprintint]
            centerLetter = randint(0, len(randomFingerprint)-1)
            jumble(randomFingerprint, centerLetter) 
            listOfWords = []
            totalScore = 0
            potentialWords = 0
            for x in D: #same loop as on 195 since the values are reset
                possibleWord = x
                wordChecker = 0
                for y in possibleWord:  
                    if y in randomFingerprint:
                        wordChecker = wordChecker + 1   
                if wordChecker == len(possibleWord):
                    potentialWords = potentialWords + 1   
        elif userInput == '.':  #Ends game
            loopBreak = 1
            print('You found', len(listOfWords), 'of', potentialWords, 'possible words: you scored', totalScore, 'points.', 'Goodbye!' ) #End message
        else:
            print(userInput)
            wordLength = len(userInput)
            if wordLength > 3:  #Is word 4 or more letters?
                userList = list(userInput)
                testcase = 0
                for x in userList:  #Is the word in the puzzle word?
                    if x in randomFingerprint:
                        testcase = testcase + 1   
                if testcase == len(userInput): 
                    if userInput not in listOfWords:    #Has the word been used before?
                        try:    #checks if the user inputed a word who has a dictionary value
                            D[fingerprint(userInput)]
                            totalScore = totalScore + score(userInput)  #calculate value of word
                            listOfWords.append(userInput)   #add to list of words
                            print('Nice Word! You get', score(userInput),'points')  #print to user score given 
                        except: #output if word not found in dictionary
                            print("not valid word")
                else:
                    print("not valid word")
            else:
                print("not valid word")                
round(D,S)


######################################################################
# play(filename='words.txt') takes a single optional argument filename
# (defaults to 'words.txt') that gives the name of the file containing
# the dictionary of legal words. After invoking readwords(), it
# repeatedly invokes rounds() until it obtains a False, indicating the
# game is over.
#
def play(filename='words.txt'):
    D,S = readwords(filename)   #call readwords function to create dictionary and finger prints list from text file
    round(D,S)  #play round using dictionary and finger print list found from text file

