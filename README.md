# give-a-dollar

I love math puzzles and such. Every once in a while, one really gets my attention for some reason. In this case, the reason is how counter-intuitive the results are.

The scenario is fairly simple: You have 45 people in a room and give each of them $45. For each "round of play", each person who has money has to give $1 to some other person at random.

What would you expect the results to look like after, say, 5,000 rounds?

Most people will say they would expect things to be somewhat random, for fairly evenly distributed. Surprisingly, that is not the case at all.

## The Results

We'll start wit the results. If you run this, you will find that the distribution curve is not remotely even and slopes significantly upward for a few lucky people who end up with a lot of money. The graph below shows the results of a sample run with the values unsorted:

![Unsorted Results](https://github.com/w4jbm/give-a-dollar/raw/main/Images/plrs5000.png)

Just how counter-intuitive the results are especially jump out if we sort them so we can get a better idea of the distribution:

![Sorted Results](https://github.com/w4jbm/give-a-dollar/raw/main/Images/sort5000.png)

Just what is going on? Heck if I know... :smile:

There is actually an indepth look at this in an [academic paper found here](http://www2.physics.umd.edu/~yakovenk/papers/EPJB-17-723-2000.pdf). The short answer is that in a closed system where money is neither created nor loss, things move towards a Boltzmann-Gibbs distribution.

## The Program

I found JS and R programs for looking at this, but could not find anything in Python. So I rolled my own and here it is. There are bits and pieces of a lot of things that went into this, but it will create a plot for each "round" (initially one for the raw results and the other sorted to show the distribution, then these two are combined into a single image). Once we do that for all of the rounds, it creates a GIF from the individual images.

The results depend on the actual random sequence, so they are different every time. But you should end up with something that looks similar to this:

![Results as GIF](https://raw.githubusercontent.com/w4jbm/give-a-dollar/main/Images/resized.gif)

This has been resized and only shows every tenth frame to save space, but it still gives you a good idea of what to expect. On the terminal screen, you will also see progress as things are processed along with some statistical details of the final state.

![Screenshot](https://raw.githubusercontent.com/w4jbm/give-a-dollar/main/Images/Screenshot.png)

## Areas for Future Work

There is logic that stops someone from "giving" when they run out of money. One area to explore is the impact of the ability to "borrow".

## The fine print...

To the extent applicable, all code and other material in this repository is:

Copyright 2022 by James McClanahan and made available under the terms of The MIT License.

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
