
A knight's tour solver in pascal
================================

My professor has a task on the current problem set of my pascal
programming course to program, demanding a recursive program finding a
solution to the `knights tour
problem <http://en.wikipedia.org/wiki/Knight's_tour>`_ on a chess board
of size n>=3 given a starting position. I used a backtracking algorithm
(at least that is what wikipedia tells me it is), by trying all possible
combinations and setting steps back, when they do not lead to a
solution.

Beginning with n = 7 my algorithmus gets very slow, caused by the
backtracking algorithm which is not very efficient. I found some
interesting articles regarding this problem using graph theory to solve
it. Some pretty big minds have thought about the problem, I guess its
not for me to find such an solution for a little task of the weekly
problem set.

`Wolfram MathWorld: Knights
Tour <http://mathworld.wolfram.com/KnightsTour.html>`_
 `Presentation Knights Tour (German
Language) <http://www.zaik.uni-koeln.de/AFS/teachings/ss07/InfoSeminar/handout/leonid_torgovitski_nknighttours.pdf>`_

.. categories:: none
.. tags:: none
.. comments::
.. author:: beberlei <kontakt@beberlei.de>