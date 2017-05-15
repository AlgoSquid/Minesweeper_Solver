# Minesweeper_Solver
Programming challenge  from Codewars.com (Kata 1) to solve minesweeper. Solved in Python 3.4.

Description from codewars (https://www.codewars.com/kata/57ff9d3b8f7dda23130015fa):

Have you ever played Minesweeper? It's a WINDOWS own game, It mainly tests the player's ability to think logically.

Here is some rules of game, maybe helpful to someone who haven't played Minesweeper:

The goal of the game is to uncover all the squares that do not contain mines without being "blown up" by clicking on a square with a mine underneath. The location of the mines is discovered by a process of logic. Clicking on the game board will reveal what is hidden underneath the chosen square or squares (a large number of blank squares may be revealed in one go if they are adjacent to each other). Some squares are blank but some contain numbers (1 to 8), each number being the number of mines adjacent to the uncovered square. To help avoid hitting a mine, the location of a suspected mine can be marked by flagging it with the right mouse button. The game is won once all blank squares have been uncovered without hitting a mine, any remaining mines not identified by flags being automatically flagged by the computer. However, in the event that a game is lost and the player mistakenly flags a safe square, that square will either appear with a red X covering the mine (denoting it as safe), or just a red X (also denoting it as safe).
Task

In this kata, I'll give you a string map as a game map, and a number n means the total number of mines. like this:

map =
? ? ? ? ? ?
? ? ? ? ? ?
? ? ? 0 ? ?
? ? ? ? ? ?
? ? ? ? ? ?
0 0 0 ? ? ?

n = 6

Yes, you always get a matrix with some question marks, except for some 0(because I think you need a place to start your logical reasoning.).

Digit 0 means that no mine around here, so you can safely open the grids around 0. How to open the grid? I've preload a method open, usage is open(row,column) (for Java users: Game.open(int x, int y)). It will return a number that is how many mines around this grid. If there is an error in your logical reasoning, when you use the open method to open a grid, but there is a mine hidden in this grid, then the test will fail. Please note, method open only return a number, but did not modify the map, you should modify the map by yourself.

You opening more and more grids.. Until all safe grids are opened and all mines grids are marked by 'x'. then return the result like this:

1 x 1 1 x 1
2 2 2 1 2 2
2 x 2 0 1 x
2 x 2 1 2 2
1 1 1 1 x 1
0 0 0 1 1 1

If the game can not got a valid result, should return "?". See following:

 map =
 0 ? ?
 0 ? ?
 n = 1

 First you open two middle grids(get them using method 
 `open(0,1)` and `open(1,1)`), then got:

 map =
 0 1 ?
 0 1 ?

 Now, there is only one mine left, but there are two `?` left.
 The mine can be hidden in any of them. 

 So you should return "?" as the result.
