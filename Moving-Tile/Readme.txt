TCSS 435 Programming Assignment 1 - Moving tile problem
Ethan Cheatham

Note to instructor: this program uses the numpy library, and is parsed via linux commandline,
hopefully the input is read the same as windows

Usage: python3 ./FifteenProblem "123456789ABC DFE" BFS

Problem one: "123456789EACDB F"
BFS: 5, 75, 33, 42
DFS: Does not finish
DLS(Depth = 5): 5, 43, 19, 6
A-STAR H1: 5, 243, 77, 166
A-STAR H2: 5, 17, 6, 11
GBFS H1: 5, 243, 77, 166
GBFS H2: 5, 17, 6, 11


Problem two: "51246A379 C8DEBF"
BFS: 11, 11630, 5750, 5800
DFS: Does not finish
DLS(Depth = 15): 15, 126406, 60145, 23
A-STAR H1: 11, 36, 12, 24
A-STAR H2: 11, 34, 11, 23
GBFS H1: 11, 36, 12, 24
GBFS H2: 11, 34, 11 ,23



Time Complexity:
BFS:
DFS:
DLS:
A-STAR:
GBFS: