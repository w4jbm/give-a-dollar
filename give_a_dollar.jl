#!/usr/bin/julia
#
# give_a_dollar.jl
#
# A Julia tool to studying an interesting scenario by Jim McClanahan W4JBM
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
# Individual graphs of the progress are stored and later combined into a GIF.
# I used the Linux convert command to do this. It can be done in Julia but my
# first couple of attempts didn't work, so I fell back to this approach.
#
# I converted my Python version, but one resource I used for that is a version
# in R from dggoldst at:
# https://gist.github.com/dggoldst/e77cacae87a9b88de52f7868936899c5#file-give_a_dollar-r
#
# Translating R to Python was more difficult than it was worth (since I know
# virtually nothing about R), but some of the variable names survived. :-)

using Plots
using Glob

# Initialize Variable
num_players = 45
starting_dollars = 45
num_rounds = 5000

# Figure out number of digits for zero padding
# (I'm not sure the padding is absolutely needed, but it ensures
# the PNG files are in the right order both with the time stamp
# and when sorted by name.)
num_digits = Int(floor(log10(Float64(num_rounds)))) + 1

# Give everyone their $45
bank = fill(starting_dollars, num_players)

# Variable used to capture minimum and maximum values over the series of rounds
global player_min = starting_dollars
global player_max = starting_dollars

# A function that picks a player to give $1 to--but we can't give it
# to ourselves...
function give_to(i, num_players)
    j = rand(1:num_players-1)
    if j == i
        j += 1
    end
    return j
end

for current_round in 0:num_rounds
    for player in 1:num_players

        # If round zero, don't do anything
        # (Let's us put 'base case' in the final GIF
        if current_round == 0
            break
        end

        # Does this player have any money left?
        if bank[player] == 0
            continue
        end
        
        # If we have $1, give it to someone else
        bank[player] -= 1
        bank[give_to(player, num_players)] += 1
        
    end

    # Capture minimum over all rounds
    if (minimum(bank) < player_min)
        global player_min = minimum(bank)
    end

    # Capture maximum over all rounds    
    if (maximum(bank) > player_max)
        global player_max = maximum(bank)
    end

    # This is kind of a kludge, but if we are building a GIF
    # to share, we don't want it to be a huge file. This will
    # let you capture each round (with % 1), every tenth round
    # (with % 10) or other combinations you want.
    #
    # Every tenth for 1,000 rounds results in a GIF that is
    # 4.7 MB in size.
    #
    # NOTE: convert seems to be memory constrained and can only
    # merge a few hundred files without throwing a "resources
    # exhausted" error. Use ffmpeg if you need more frames.
    if (current_round % 25) ≠ 0
        continue
    end

    # Some of the code commented out below lets you generate
    # seperate plots for raw values and the distribution curve
    # instead of just a combined view.

    # Plot the raw values from the bank
    xs = range(1, length=num_players)
    ys = bank
#   pname = string("plot_raw", string(current_round), ".png")
    p1 = bar(xs, ys, ylims=(0,200), xlims=(0.5,45.5))
    ylabel!("Bank Balance")
    xlabel!("Player Number")
    title!("Give-a-Dollar Raw Player Data")
#   savefig(p1, pname)

    # Plot the sorted values (distribution) from the bank
#   xs = range(1, length=num_players)
    ys = sort(bank)
#   pname = string("plot_sorted", string(current_round), ".png")
    p2 = bar(xs, ys, ylims=(0,200), xlims=(0.5,45.5))
    ylabel!("Bank Balance")
    xlabel!(string("Distribution for Round ", current_round))
    title!("Give-a-Dollar Sorted Distribution")
#   savefig(p2, pname)

    pname = string("plot_merged_", lpad(current_round, num_digits, "0"), ".png")
    plot!(size=(800,800))
    final = plot(p1, p2, layout = (2,1), legend=false)
    savefig(final, pname)
    
    
end

# Use Linux commands to merge all the PNGs into a GIF
#
# Two approaches can be used, each with different tradeoffs...

# Using 'convert' gives high quality but will run out of
# buffer space after a few hundred frames and produces large
# file (because quality doesn't come without a cost).
run(`convert -delay 10 -loop 1 \*.png give_a_dollarc.gif`)

# Using 'ffmpeg' reduces the quality because of compression
# but will not overrun a buffer (because results are going to
# the disk) and produces files about half the size of 'convert'.
#run(`ffmpeg -y -framerate 10 -pattern_type glob -i '*.png' -loop -1 give_a_dollarff.gif`)

# Delete all the PNGs now that we're done with them
rm.(glob("plot*.png"))

# Print out some of the details about the run
println("Number of Rounds: ", num_rounds)
println("Minimum Dollars for a Player: ", player_min)
println("Maximum Dollars for a Player: ", player_max)
