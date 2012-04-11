this is a genetic algorithm that composes melodies. 

initial population:
it builds a markov model to spawn the initial population to a) slightly reduce the search space,
and b) act as an influencer. the user has the ability to select <i>x</i> different artists, <i>y</i> different songs, and/or <i>z</i> different genres, where each 
of these items is a midi file. i have written a midi parser, which extracts the melody(pitch, duration) from the midi file(s) and stores it into a text file, which
is then processed by the markov model.

fitness:
for the time being, i am leaving this as an interactive fitness function (i.e. the user has to rate the each song), but i have added some witchcraft to 
reduce the amount of work the user needs to do. i also have plans for adding a neural network to act as an auto-rater. the current rating system uses 
jquery to add interaction to the listening part of the application. the user can move the pitches around to modify the melody to his/her liking. the euclidean distance is used to calculate the fitness value.

selection:
rates are adjustable by the user on the front-end
in addition to roulette wheel and tournament selection, i have added gender based-selection, which mimics rules of human society for mating. i have plans
on adding grouping for clustering purposes where groups are friends and family.

crossover:
n-point crossover. rates are adjustable by the user on the front-end.

mutation:
rates are adjustable by the user on the front-end.

termination:
rates are adjustable by the user on the front-end.

technology:
python
	web.py
html/css/jquery
sql

if you have any questions and/or comments please feel free to contact me.
