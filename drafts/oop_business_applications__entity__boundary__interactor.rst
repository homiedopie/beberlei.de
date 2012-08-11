OOP Business Applications: Entity, Boundary, Interactor
=======================================================

Continuing the series, I will talk about Entity, Boundary and Interactor (EBI). I
first heard about it in a keynote video of `Uncle Bob
<https://sites.google.com/site/unclebobconsultingllc/>`_ on Ruby Midwest called
`"The lost years of architecture"
<http://www.confreaks.com/videos/759-rubymidwest2011-keynote-architecture-the-lost-years>`_.
This is also described as `Hexagonal architecture
<http://alistair.cockburn.us/Hexagonal+architecture>`_ or "Ports and Adapters"
by Alistair Cockburn. I would call EBI a design pattern as it is clearly not an
architecture on its own.

In this pattern any client of the system talks to the model using a model
request object and receives data from the model in form of model responses objects.
Additionally when your model talks to any kind of persistence or subsystem it
should go through an adapter that is replacable. For a model architecture
designed this way, you can replace any part of the UI oder lower layers by
writing new adapters and plug them in.

Terminology
-----------

To iterate the terminology:

**Entities** are objects that represent the system data of the application. They don't contain
much logic except rules that are set in stone and are never going to change
(based on physic or mathematical laws or something).

**Interactors** are use-case objects, they contain the business logic that is valid
in the current use-case and works with entities to fullfil their task.

The **boundary** is responsible for translating model request/response into a
format that the UI or actor can understand. They also mediate between model
and lower levels, for example to manage database transactions.

An example
----------

Lets start with an example in PHP code. We will keep using a common example
throughout all blog posts, the usual Bank Account/Money Transfer. The use case
is the money transfer from one bank account (source) to another one
(destination).

We start by implementing the entity ``BankAccount``:

.. code-block:: php

    <?php
    class BankAccount 
    {
        private $balance;

        public function __construct()
        {
            $this->balance = new Money(0);
        }

        public function withdraw(Money $money)
        {
            $this->balance = $this->balance->subtract($money);
        }

        public function deposit(Money $money)
        {
            $this->balance = $this->balance->add($money);
        }
    }

It is straightforward to implement the ``withdraw` and ``deposit``
functionality. The Money object implementation is omitted here.

The Interactor handles the use-case of transfering money from the
source to the destination account:

.. code-block::

    <?php
    class MoneyTransferRequest
    {
        public $sourceId;
        public $destinationId;
        public $amount;
    }
    class MoneyTransferResponse
    {
    }

    class MoneyTransfer
    {
        private $accountDao; // ctor omitted

        public function transferMoney(MoneyTransferRequest $transfer)
        {
            $source      = $this->accountDao->find($transfer->sourceId);
            $destination = $this->accountDao->find($transfer->destinationId);
            $money       = new Money($transfer->amount);

            $source->withdraw($money);
            $destination->deposit($money);

            return new MoneyTransferResponse();
        }
    }

The ``MoneyTransferRequest`` and ``MoneyTransferResponse`` objects are dumb
value objects or data-transfer objects as they are commonly called.

You can see in the example that we use a Data Access object to retrieve the
source and destination account entities from some storage subsystem. To follow the EBI
design pattern, we have to decouple this data access object from the model,
by offering a port (Interface):

.. code-block:: php

    interface AccountDaoInterface
    {
        public function find($accountId);
    }

This way our business logic is storage independent.

An example for a boundary would be the requirement for a transaction in
the bank account sample. We need to wrap the whole MoneyTransfer use-case in
a transaction. Lets say the invocation of our Use-Case is controlled through
some kind of application boundary object:

.. code-block:: php

    class BankApplicationBoundary
    {
        private $applicationFactory;

        public function transferMoney(MoneyTransferRequest $request)
        {
            $unitOfWork = $this->applicationFactory->createUnitOfWork();
            return $unitOfWork->work(function($factory) use ($request) {
                $useCase = new MoneyTransfer($factory->createAccountDao());
                return $useCase->transferMoney($request);
            });
        }
    }

This is a very elaborate way to describe that calling the transfer money
use-case is wrapped in a UnitOfWork, another port for the storage system to
manage transactions in this case. The code here is very explicit about
the actual task. In a real application you would probably find a more
generic approach to getting this job done.

Pros and Cons
-------------

This design pattern very closely resembles the **Service Layer** pattern that
is described in Martin Fowlers PoEAA, going a bit more into detail by naming
individual parts of the pattern more explicit. Without more
restrictions using this pattern will drive you towards many of the problems
described in my previous post. Entities are still a meaningless getter/setter
storage and use-cases interact with these to modify the state of the system.

Clean seperation from frameworks is achieved, however at a significant cost.
Manually implementing this seperation without stepping back and thinking
about further abstractions is leading to lots of code being manually written.

One particular annoyance are the data-transfer objects. You need to invest
quite some work to get a mapping working from entities to transfer objects and
back. In the process you will loose the convenience of "Open Entity Manager in
the View" anti-pattern, where you can lazy load any data you want to access in
the view. This is quite a painful step, because you are loosing lots of
flexibility. Much more annoying is the need to update entities from
data-transfer objects, requiring sophisticated code for merging of partial object
graphs. As we will see in future blog posts one particular problem that EBI
does not specifically address is the reuse of data-transfer-objects for read
and write scenarios.

What this design pattern improves is the testability of code and also the
execution of tests is MUCH better, when you don't have to go through the whole
application stack to test something.

Implementing behavior into the use-cases also avoids lots of lasagna code
compared to a fully domain driven design. You get a very good overview of
what is actually happening just by looking at the Model Request and Interactor
classes.

In conclusion I can recommend using the EBI pattern, however you have to be
careful to find abstraction layers that keep your code DRY and SOLID, something
which does not come naturally with this pattern. Additionally you should be
careful to avoid lots of DTO <-> Entity Mapping code by using some
code-generation for example to do parts of this job for you.  The worst outcome
with this pattern is you having to manually code layers for HTTP Request/Form
=> DTO => Entity mapping and the other way around.

.. author:: default
.. categories:: none
.. tags:: none
.. comments::
