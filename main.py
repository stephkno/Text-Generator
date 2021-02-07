import numpy
import sys

#initialize variables
text = []

#path for input text as argument
memory = {}
alphabet = []

def parse(arg, args):
    for a in range(len(args)):
        if args[a] == arg and (a+1) < len(args):
            return args[a+1]

filenames = parse("-f", sys.argv)
n_chars = int(parse("-c", sys.argv))
n_generate = int(parse("-g", sys.argv))

print(filenames)
filenames = filenames.split(",")

for filename in filenames:
    # open file
    print("\nReading file {}...".format(filename))

    with open(filename, "r") as f:
        # reads all lines and removes non alphabet words
        book = f.read()

    length = len(book)
    i = 0

    #parse all characters of book into alphabet set
    for l in list(book):
        i += 1

        text.append(l)
        if i % 10 == 0:
            print("\r{}%".format(int(100*(i/length))),end="")

        if l not in alphabet:
            alphabet.append(l)

length = len(text)
alphabet.sort()

print("\nAlphabet size:", len(alphabet))

i = n_chars
read = [text[i] for i in range(n_chars)]
epochs = 10

print("Reading text...")

#iterate text for x epochs
for i in range(epochs):
    while i < len(text)-1:

        letter = text[i+1]
        string = ''.join(read)

        #read state
        if string in memory:
            #if state exists, increment letter probability
            tmp = memory[string]
            tmp[alphabet.index(letter)] = tmp[alphabet.index(letter)] + 1.0
        else:
            #add new state
            dist = [0.0 for _ in range(len(alphabet))]
            dist[alphabet.index(letter)] = 1.0
            memory[string] = dist

        #remove letter from read head
        read.pop(0)
        #add next letter to read head
        read.append(letter)

        #increment letter counter
        i+=1

        #print progress
        if i % 10 == 0:
            print("\r{}%".format(int(100*(i/(length*epochs)))),end="")

    print("\n")

#initial state text - first n_chars of book
read = [text[i] for i in range(n_chars)]

#write imitation text
for i in range(n_generate):

    #get text state
    text = ''.join(read)
    #get frequencies
    dist_o = numpy.array(memory[text])
    dist = []
    #get probability distribution for state
    for d in dist_o:
        dist.append(d/dist_o.sum())

    #sample letter from distribution
    letter = numpy.random.choice(alphabet, p=dist)

    #print letter, update read head
    print(letter, end="")
    read.pop(0)
    read.append(letter)
    i+=1
