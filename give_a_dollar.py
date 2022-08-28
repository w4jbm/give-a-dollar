#!/usr/bin/python3
#
# give_a_dollar.py
#
# A Python tool to studying an interesting scenario by Jim McClanahan W4JBM
#
# The Scenario:
#
# 45 people are each given $45. For 5,000 rounds, each person who has money
# must give $1 to another random person (who is, obviously, not themselves).
#
# The question is what does the distribution of money look like over a long
# period of time. Most people (even those familar with statistics and probability)
# tend to guess that the amount each person has will remain relatively flat.
#
# Surprisingly, this is not what happens...
#
# Results are in the format of a GIF. To resize the GIF, you can use the command:
#
# $ gifsicle --resize 320x480 --colors 16 gad.gif > resized.gif
#
# Originally in R from dggoldst at:
# https://gist.github.com/dggoldst/e77cacae87a9b88de52f7868936899c5#file-give_a_dollar-r
#
# Translating R to Python was more difficult than it was worth (since I know
# virtually nothing about R), but some of the variable names survived. :-)
#
# Details on building a gif included info from Thiago Carvalho at:
# https://towardsdatascience.com/basics-of-gifs-with-pythons-matplotlib-54dd544b6f30
#
# Info on merging two images from radarhere at:
# https://stackoverflow.com/questions/53876007/how-to-vertically-merge-two-images
#
# Note: Running under a fairly fresh copy of MX Linux, I would get errors on
# exit after larger runs along the lines of:
#
# ICE default IO error handler doing an exit(), pid=xxx, errno = 32
#
# When I removed the version of matplotlib installed using pip and instead used
# one installated with apt install, the problem went away.

import os
import numpy as np
import matplotlib.pyplot as plt
import random
import imageio.v2 as imageio
from PIL import Image
from tqdm.auto import tqdm

NUMPLAYERS = 45
INITWEALTH = 45
ROUNDS = 5000
GRAPH_MAX = 200

BANK_MIN = INITWEALTH
BANK_MAX = INITWEALTH

filenames = []
filemerge = []

#initialize the bank
#columns wealths of the NUMPLAYERS players
#rows show wealths of each of the ROUNDS ticks of the clocks
bank = np.empty(NUMPLAYERS)
bank.fill(INITWEALTH)

# print(bank)

# This function takes a "player number" as its input and then
# returns a random player number that is not equal to itself.
#
# This is used so that i can give $1 to j.
def give_to(i):
    j = random.choice(list(set([x for x in range(0, NUMPLAYERS)]) - set([i])))
    return(j)

print("Running itterations and creating frames...")

for current_round in tqdm(range(0, ROUNDS+1)):
    for player in range(0, NUMPLAYERS):

        # For Round #1, let's plot the initial state
        if current_round == 0:
            continue ;

        # Does this player have any money left?
        if bank[player] == 0:
            continue ;

        # If so, give someone a dollars
        bank[player] -= 1
        bank[give_to(player)] += 1

    # Capture Min and Max for round
    BANK_MIN = min(np.amin(bank),BANK_MIN)
    BANK_MAX = max(np.amax(bank),BANK_MAX)

    # The following is used for times when I don't need a graph
    # each individual round--% 10 will cut the size of the file
    # and the run time significantly by only graphing 1 in 10
    # rounds

    if (current_round % 1) == 0:

        # Plot the results by Player
        plt.title("Unsorted by Player")
        plt.bar(range(0,NUMPLAYERS), bank, color='b')
        plt.ylim(0,GRAPH_MAX)

        filename = 'plrs' + str(current_round) + '.png'
        filenames.append(filename)

        plt.savefig(filename)
        plt.close()

        # Plot the results Sorted (low to high)
        plt.title("Sorted Distribution")
        plt.bar(range(0,NUMPLAYERS), np.sort(bank), color='r')
        plt.ylim(0,GRAPH_MAX)
        plt.figtext (0.01,0.01,"https://www.github.com/w4jbm/give-a-dollar",horizontalalignment='left')
        plt.figtext (0.99,0.01,current_round,fontfamily="monospace",horizontalalignment='right')


        filename = 'sort' + str(current_round) + '.png'
        filenames.append(filename)

        plt.savefig(filename)
        plt.close()

        # Now merge the two images
        filename = 'merg' + str(current_round) + '.png'
        imgs = [Image.open(i) for i in filenames]

        min_img_width = min(i.width for i in imgs)

        total_height = 0
        for i, img in enumerate(imgs):
            # If the image is larger than the minimum width, resize it
            if img.width > min_img_width:
                imgs[i] = img.resize((min_img_width, int(img.height / img.width * min_img_width)), Image.ANTIALIAS)
            total_height += imgs[i].height

        img_merge = Image.new(imgs[0].mode, (min_img_width, total_height))
        y = 0
        for img in imgs:
            img_merge.paste(img, (0, y))
            y += img.height
        img_merge.save(filename)
        img_merge.close()

        # Now get rid of the two files we had prior to merging things
        # except save the final results
        if current_round != ROUNDS:
            for f in filenames:
                os.remove(f)

        # Save to list of images to go in GIF
        filemerge.append(filename)

        # Clear the working list
        filenames = []

print("Merging frames to create GIF...")

# We have all the files created, so now me merge them!
with imageio.get_writer('gad.gif', mode='I') as writer:
    for f in tqdm(filemerge):
        image = imageio.imread(f)
        writer.append_data(image)
    writer.close()

# Remove files
for f in filemerge:
    os.remove(f)

print()
print("RESULTS SUMMARY:")
print("Over all runs, values ranged from Minimum of",BANK_MIN,"to Maximum of", BANK_MAX)
print()
print("Final values ranged from a Minimum of",np.amin(bank),"to a Maximum of",np.amax(bank))
print("Final Mean was",np.mean(bank),"with a Standard Deviation of",np.std(bank))
print("Final values have a Median of",np.median(bank))

exit()
