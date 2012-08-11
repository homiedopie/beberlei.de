Bounded Contexts
================

I regularly fall into the same trap with applications, when thinking of the one
model that unifies all the use-cases and allows to solve every problem. This is
a natural human trait to find the one puzzle piece that connects everything.
However in software design there is a case to be made for the seperation of
different contexts. Eric Evans described this in detail in his `"Bounded
Context" <http://domaindrivendesign.org/node/91/>`_ pattern in Domain Driven
Design. I read somewhere that he actually considers this the most important
pattern in the whole book.

The essence of this architectural pattern is, that it often makes sense to
complete seperate different parts of an application and develop different
models for overlapping concepts. The goal is to simplify the different parts
and release us from the burden of finding that one model that fits all use
cases.

We should remeber this pattern more often when doing application design.
It is much less akward to have some parts of the model reimplemented for
different purposes, than creating a God object that tries to unify everything.

This is especially important when seperating the CRUD parts from the really
complicated and interesting parts that benefit from domain driven design.

At the `SoCraTes conference <http://www.socrates-conference.de/>`_ at the
beginning of august I took part in a DDD architecture game that focussed on
bounded context. We were given a very simple domain concept "Customer" and
assigned different roles in the business.  Everyone described their perfect
customer very differently, imagining the Customer object that fits all these
requirements was quite an eye opener. And even if there is no such single
software that operates a business, going to the extreme and defining 10
different angles for a single concept made me clear, that sometimes different
overlaping implementations are not such a bad thing.

You should read up on Bounded Context from other sources. There is obviously
the chapter in the Domain Driven Design book, but there are also many sources
online. Many of them describe much better than me, what the benefits of bounded
contexts are.

.. author:: default
.. categories:: none
.. tags:: none
.. comments::
