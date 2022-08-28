# give-a-dollar

I love math puzzles and such. Every once in a while, one really gets my attention for some reason. In this case, the reason is how counter-intuitive the results are.

The scenario is fairly simple: You have 45 people in a room and give each of them $45. For each "round of play", each person who has money has to give $1 to some other person at random.

What would you expect the results to look like after, say, 5,000 rounds?

Most people will say they would expect things to be somewhat random, for fairly evenly distributed. Surprisingly, that is not the case at all.

## The Results

We'll start wit the results. If you run this, you will find that the distribution curve is not linear and slopes significantly upward for a few lucky people who end up with a lot of money. The graph below shows the results of a sample run with the values unsorted:

!(Unsorted Results)[https://github.com/w4jbm/give-a-dollar/raw/main/Images/plrs5000.png]

Just how counter-intuitive the results are especially jump out if we sort them so we can get a better idea of the distribution:

!(Sorted Results)[../blob/main/Images/sort5000.png?raw=true]
https://github.com/w4jbm/give-a-dollar/blob/d7f005d77c437e62eacbfba317355bb31abf5e37/Images/sort5000.png

Modeling tool for a random "give a dollar" scenario in Python
