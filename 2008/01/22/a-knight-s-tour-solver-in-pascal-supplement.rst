
A knight's tour solver in pascal - supplement
=============================================

Following my `earlier post on the Knights
tour <http://www.whitewashing.de/blog/articles/6>`_: It seems it is
crucial for a backtracking algorithm what the knights starting position
is, and even more important in what order the jumps are tried. Because
there are 8 possible moves for a knight, you have to decide in which
order they should be performed. If there is not a deviation when
backtracking the algorithm gets stuck in almost the same positions very
very often.

I rewrote the order of jumps for my 7x7 board and found a solution in
seconds. Using the same order for an 8x8 board gets me stuck in endless
tries again. I see its important to implement the `Warnsdorff's
algorithm <http://en.wikipedia.org/wiki/Warnsdorff's_algorithm>`_,
perhaps I will do so.

.. categories:: none
.. tags:: none
.. comments::
.. author:: beberlei <kontakt@beberlei.de>