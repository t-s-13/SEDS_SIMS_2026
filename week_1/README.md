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

With ew = 1 the peak should stay constant. In practice it usually creeps upward (or sometimes wobbles). Energy isn't being lost, but it is being made up by the numerical method.

The time-stepping method isn't exactly energy-conserving. Simple Euler stepping adds a tiny bit of energy every step, and over thousands of steps it adds up.
And the bounce is detected late. The ball has already sunk a little into the wall when the bounce is noticed. Flipping the velocity without moving the ball back out of the wall gives it a small free push each time.
