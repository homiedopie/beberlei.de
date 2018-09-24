Proofing the Pythagorean theorem and what this means for Domain-Driven Design
=============================================================================

According to Wikipedia the `Pythagoraen theorem
<https://en.wikipedia.org/wiki/Pythagorean_theorem#Other_proofs_of_the_theorem>`_
is the theorem with the highest number of known proofs, citing a book
containing over 370 of them.

What does this mean for modelling under the Domain-Driven Design paradigm?

In discussions with other developers I often hear the opinion, that you should
develop the model of a software entirely disconnected from technical decisions
as long as possible and fully abstracted from the choices. 

I held this opinion myself for a long time.

Discussing this with a colleague today I found a nice analogy to describe my
growing pain with this approach, something I wasn't able to formulate before.

Maybe the analogy is a bit of a stretch.

The Pythagoraen theorem shows that you can find an entirely different solution
for the same problem by using a different toolbox. Finding one or more proofs
for the theorem depends on your knowledge of different fields of mathematics.
And depending on the toolbox, the solution is simple and elegant, or complex
and theoretical.

The reverse conclusion could be, that if you develop a model (theorem) entirely
abstracted from the future implementation and toolbox, then it must increase in
generality and complexity to take into account the potential implementation
with any kind of toolbox. Or the problem space is simple like the Pythagoraen
theorem that its description allows many implementations.

Consequently, if you make technical decisions and restrict yourself to fewer
approaches/toolboxes before building the model, then the resulting model can be
simpler under the assumption that you only need it to be solved under the given
technical constraints.

For example, take Redis as a choice of database. Its built in support for more
complex data-types allows to implement extremely simple abstractions directly
on top of Redis. If you know you use Redis up front for a problem that can be
solved with lists, sets or maps, then the model and code describing this domain
logic could be extremely simplified compared a solution that makes no
assumptions about the data storage.

.. author:: default
.. categories:: none
.. tags:: none
.. comments::
