Bounded Contexts
================

I regularly fall into the same trap with applications, by thinking of the one
model that unifies all the use-cases and allows to solve every problem. This is
a natural human trait to find the one puzzle piece that connects everything.
However in software design there is a case to be made for the separation of
different contexts. Eric Evans described this in detail in his `"Bounded
Context" <http://domaindrivendesign.org/node/91/>`_ pattern in Domain Driven
Design. I read somewhere that he actually considers this the most important
pattern in the whole book.

The essence of this architectural pattern is, that it often makes sense to
complete separate different parts of an application and develop different
models for overlapping concepts. The goal is to simplify the different parts
and release us from the burden of finding that one model that fits all use
cases.

We should remember this pattern more often when doing application design.
It is much less awkward to have some parts of the model reimplemented for
different purposes, than creating a God object that tries to unify everything.
This is especially important when separating the CRUD parts from the really
complicated and interesting parts that benefit from domain driven design.

At the `SoCraTes conference <http://www.socrates-conference.de/>`_ taking place
in the beginning of august I took part in a DDD architecture game that focused
on bounded context. We were given a very simple domain concept "Customer" and
assigned different roles in the business.  Everyone described their perfect
customer very differently, imagining the Customer object that fits all these
requirements was quite an eye opener. And even if there is no such single
software that operates a business, going to the extreme and defining 10
different angles for a single concept made me clear, that sometimes different
overlapping implementations are not such a bad thing.

One obvious drawback of course is duplication. Depending on how your bounded
contexts work, this is something that has to be synchronized and worked with.
Most notably `CQRS <http://martinfowler.com/bliki/CQRS.html>`_ is an
architectural pattern, that allows for Domain Driven Design AND simplifies the
synchronization with other parts of the application.

.. author:: default
.. categories:: none
.. tags:: none
.. comments::
