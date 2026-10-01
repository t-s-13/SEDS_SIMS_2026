# Week 1: Rigid Balls, Round Walls

## Question 1. A fast enough ball can end up outside the arena without the wall bounce ever being detected. Why does the detection fail, and which of ∆t, |v|, ρ, R and g decide whether it happens?

The code only checks for a wall hit at the end of each step. It never asks what happened between steps. If the ball moves so far in one step that it jumps from inside the arena to beyond the wall, the check sees "outside" and either misses the bounce or catches it far too late. This is called tunneling.

What decides it is how far the ball moves in one step compared to how thick the wall zone is (roughly the ball size ρ):

|v| and ∆t: the distance per step is about |v|·∆t. Bigger speed or bigger time step means a bigger jump.
ρ: a bigger ball is caught more easily, because it overlaps the wall zone for longer. A tiny ball can slip through.
g: gravity makes the ball speed up as it falls, so a ball that was safe at the start can become too fast later.
R: the arena size matters only for where the wall is. It doesn't change whether a jump is too big.

Roughly, it escapes when |v|·∆t is larger than about ρ.

## Question 2. Set ew = 1, so that no energy is lost at a bounce, and let the ball run for a few thousand steps. Does the peak height stay put, creep upward, or decay? Gravity and the bounce rule are the only things acting, so if it changes at all, where is that energy coming from?

Because dt is finite, the ball overshoots the wall by a small amount, and the code teleports it back inward without changing its speed. This adds a small error to the ball's energy. The longer the code runs, the more this error accumulates, until it becomes noticeable.

At larger values of dt, the energy error is noticeable much sooner. The velocities become very large and keep increasing: at higher velocities more tunneling happens, so the code has to teleport the ball back inward more often without changing its speed, which adds even more energy error.
