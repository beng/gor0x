Status

I use Trello for project management. I have made the board public so you can view my progress/see what I'm currently working on.

http://trello.com/board/thesis/503a21fa486d9e635310bcd8

---

Description

This is a genetic algorithm that composes melodies and allows the user to play an integral part of the composition process without requiring any previous music theory knowledge. This is only possible because of how I designed the fitness function -- the user actually acts as as composer and is allowed to make a specific number of changes to the current individual. This is a unique interactive fitness function that adds a new level of user engagement and reduces user boredom.

---

Genetic Algorithm Overview

Initial Population:
it builds a markov model to spawn the initial population to a) slightly reduce the search space,
and b) act as an influencer. the user has the ability to select <i>x</i> different artists, <i>y</i> different songs, and/or <i>z</i> different genres, where each 
of these items is a midi file. i have written a midi parser, which extracts the melody(pitch, duration) from the midi file(s) and stores it into a text file, which
is then processed by the markov model.

Fitness:
for the time being, i am leaving this as an interactive fitness function (i.e. the user has to rate the each song), but i have added some witchcraft to 
reduce the amount of work the user needs to do. i also have plans for adding a neural network to act as an auto-rater. the current rating system uses 
jquery to add interaction to the listening part of the application. the user can move the pitches around to modify the melody to his/her liking. the euclidean distance is used to calculate the fitness value.

Selection:
rates are adjustable by the user on the front-end
in addition to roulette wheel and tournament selection, i have added gender based-selection, which mimics rules of human society for mating. i have plans
on adding grouping for clustering purposes where groups are friends and family.

Crossover:
n-point crossover. rates are adjustable by the user on the front-end.

Mutation:
rates are adjustable by the user on the front-end.

Termination:
rates are adjustable by the user on the front-end.

Technology:
python, web.py, music21, html/css/jquery

