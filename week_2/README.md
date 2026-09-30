# Week 2 — The Sandbox

## Question 1. Why does the swap grid start as a copy of the current state, rather than being filled with zeros? What would happen to a grain that does not move if G′ started empty?

In the code, new starts as a copy of old. Most cells don't move on any given tick. A grain resting on the floor, a water drop, a wall: none of them do anything. The code never writes anything for them. It only writes to new when something moves.

So if new started empty, every grain that stays put would simply vanish. Nothing would ever copy it over. Walls would disappear too, since the loop skips them completely. Starting with a copy means "everything stays where it is unless told otherwise." A moving grain then only has to write itself into the new spot and clear its old spot.

## Question 2. Remove the randomised column order and replace it with a fixed left-to-right scan. Run the simulation for a few hundred ticks. What happens to the shape of a sand pile? Why?

The pile leans in one direction instead of forming a neat, symmetric triangle. Usually, when a grain is blocked below, it slides diagonally into whichever side is free. With a fixed left-to-right order, the grains on the left are always processed first. They get first pick of the free spots, and the pattern of who moves, and when, is the same every tick. That builds in a steady bias toward one side.

Random order gives left and right an equal chance on average, so the bias cancels out and the pile comes out symmetric.
