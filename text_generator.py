# markov chain text generator
# very basic sequence modeling

import sys
import numpy
from os import path

#use dictionary as a model
memory = {}

#list of all possible symbols
alphabet = []

default_input_url = "https://raw.githubusercontent.com/jraleman/42_get_next_line/master/tests/hhgttg.txt"

#parse args
def parse(arg, args):
	for a in range(len(args)):
		if args[a] == arg and (a+1) < len(args):
			return args[a+1]
	return False

def download(url):
	import wget
	return wget.download(url)

	
url = parse("-u", sys.argv)
if url == False:
	filename = parse("-f", sys.argv)
n_chars = int(parse("-c", sys.argv))
n_generate = int(parse("-g", sys.argv))
n_warmup = int(parse("-w", sys.argv))
epochs = int(parse("-e", sys.argv))

wanthelp = "-h" in sys.argv

if wanthelp:
	print("\nUsage")
	print("-u input url [Default hitchhiker's guide to the galaxy]")
	print("-f input file")
	print("-c number prev chars [Default 8]")
	print("-g number of chars to generate [Default 1050]")
	print("-w number of chars to generate warmup [Default 1035]")
	print("-e number of training epochs [Default 1]")
	quit()

#set default hyperparameters
if url == False:
	filename = default_input_url.split("/")[-1]
	if not path.exists(filename):
		filename = download(default_input_url)
else:
	filename = download(url)

if not n_chars:
	n_chars = 8
if not n_generate:
	n_generate = 1050
if not n_warmup:
	n_warmup = 1035
if not epochs:
	epochs = 1


# open file
print("\nReading file \"{}\"...".format(filename))

with open(filename, "r") as f:
	# reads all lines and removes non alphabet words
	book = f.read()

length = len(book)
i = 0

#parse all characters of book into alphabet
for l in list(book):
	i += 1

	#display progress
	if i % 10 == 0:
		print("\r{}%".format(1+int(100*(i/length))),end="")

	#add only unique symbols
	if l not in alphabet:
		alphabet.append(l)

length = len(book)

#alphabet in order
alphabet.sort()
print("\nAlphabet size:", len(alphabet))

i = n_chars
read = [book[i] for i in range(n_chars)]

print("Learning text...")

#learning text for n_epochs
for i in range(epochs):
	print("\nEpoch {}...".format(i))

	while i < len(book)-1:
		letter = book[i+1]
		string = ''.join(read)

		#read state
		if string in memory:
			#if state exists, increment next symbol probability
			tmp = memory[string]
			tmp[alphabet.index(letter)] = tmp[alphabet.index(letter)] + 1.0
		else:
			#add new state if never seen
			#create vector of zeros
			dist = [0.0 for _ in range(len(alphabet))]
			dist[alphabet.index(letter)] = 1.0
			memory[string] = dist

		#remove old letter from read buffer
		read.pop(0)
		#add next letter to read buffer
		read.append(letter)

		#increment letter counter
		i+=1
		if i > len(book)-1:
			i = 0

		print("\r{}/{}".format(i, length),end="")

#initial state text - first n_chars of book
read = [book[i] for i in range(n_chars)]
print("\r Ready! Press return to generate {} chars (q to exit)".format(n_generate))


def predict():
	#get book state
	book = ''.join(read)
	#get frequencies
	dist_o = numpy.array(memory[book])
	dist = []
	#get probability distribution for state
	for d in dist_o:
		dist.append(d/dist_o.sum())

	#sample letter from distribution
	letter = numpy.random.choice(alphabet, p=dist)

	#print letter, update read buffer
	print(letter, end="")
	read.pop(0)
	read.append(letter)

def warmup(c):
	letter = read.pop(0)
	read.append(book[c])
	print(letter, end="")

c = n_chars

while True:
	query = input().lower()

	if(query == "q" or query == "quit" or query == "exit"):
		quit()

	#predict text
	for i in range(n_generate):
		if c == n_warmup:
			print(" <start> ")
		if c > n_warmup:
			predict()
		else:
			warmup(c)
			c+=1
