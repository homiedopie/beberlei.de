OOP Business Applications: Command-Query-Responsibility-Segregation (CQRS)
==========================================================================

Other posts in this series about OOP Business Applications:

- `Trying to escape the
  mess <http://whitewashing.de/2012/08/11/oop_business_applications__trying_to_escape_the_mess.html>`_
- `Entity, Boundary, Interactor
  <http://whitewashing.de/2012/08/13/oop_business_applications_entity_boundary_interactor.html>`_
- `Data, Context, Interaction
  <http://whitewashing.de/2012/08/16/oop_business_applications__data__context__interaction.html>`_

The last pattern for designing your business logic is called
"Command-Query-Responsibility-Segregation" or short CQRS. It has its roots in
the `"Command Query Separation"
<http://en.wikipedia.org/wiki/Command-query_separation>`_ principle that was
put forward by Bertrand Meyer.

Wikipedia has a very good summary about what this principle is about:

::

    Command-Query-Separation states that every method should either be a
    command that performs an action, or a query that returns data to the
    caller, but not both. In other words, asking a question should not change
    the answer. More formally, methods should return a value only if they are
    referentially transparent and hence possess no side effects. 

CQRS is an OOP architecture design pattern building on that imperative
principle. 

.. note::

    There are many different variations of the CQRS pattern that
    all have their place. This post describes a simple variant that does
    **not**
    use Messaging, DomainEvent or EventSourcing patterns, which are commonly mentioned
    with CQRS.

At its heart is the separation of Read and Write methods. This can be easily
achieved by just having two different service layer classes instead of one.
This insight alone is not really helpful, its just moving methods around.
Coupled to this change however is the notion, that read and write models don't
necessarily have to be the same:

- Getter/Setters: We don't need setters in the write model, instead we use
  explicit methods for each write operation. Entities are also much simpler
  without bi-directional relationships that read/write models often need.
  Read-only models (ViewModel) don't need getters/setters. They could just use
  public properties or even be arrays.
- ORM Performance, Lazy Loading and Query Restrictions: In a write scenario we
  mostly need queries by primary key, changing only some objects. In
  read scenarios we need complex queries, joins and aggregations. A separation
  prevents both from affecting each other negatively.
- Mapping Data-Transfer objects becomes simple. Instead of sending the whole
  model back and forth, for the write scenario you define use-case specific
  tasks and updates. This is much simpler than generic mapping of Data Transfer
  objects to complex object graphs.
- Transforming SQL directly to a view model in a highly optimized way.
  Simple concept, but it has huge implications: A pure read-only model is simple to
  maintain and refactor for any performance requirements that come up.

Furthermore with CQRS our write service methods are not allowed to return data
anymore (With the exceptions to the rule of course). This may increase the
complexity at first, but it has benefits for scalability and decoupling.
Following this principle allows us to turn every command from synchronous to
asynchronous processing later without much problems. Services are allowed to
throw exceptions and refuse the execution. Proper validation of input data
should happen before executing write operations though.

One drawback of CQRS: A naive implementation doubles the amount of classes and
services to write. But there are simple shortcuts to avoid having to write a
full blown read-model if you don't apply CQRS religiously:

- Don't use different data-stores for both models.
- Mapping SQL to PHP arrays and stdClass objects through a simple gateway is
  very simple. You can easily generalize this to a simple object that gives
  efficient access to all your data.
- Share parts of the write and read models if you don't have to compromise
  much.

The important thing to take away from this separation is, that the read part of
your application is seldom the part where business value lies in. Moving this
code into a different part of your applications allows you to work with the
underlying data-source much more directly, without need for much abstractions.

One thing that CQRS puts forward is the concept of Commands, Command Handlers
and Command Bus and how they interact. Commands are simple objects that
contain all the data necessary to execute an operation. Each command is
processed by exactly one command handler. The Command Bus is responsible to
route a command to its appropriate command handler.

Example
-------

Here is the most simple implementation of the Command Bus, just holds a hash map
mapping command class names to command handlers:

.. code-block:: php

    <?php
    interface Handler
    {
        public function handle($command);
    }
    class CommandBus
    {
        private $handlers;
        public function register($commandClassName, Handler $handler)
        {
            $this->handlers[$commandClassName] = $handler;
        }

        public function handle($command)
        {
            $this->handlers[get_class($command)]->handle($command);
        }
    }

In your code you would always pass Commands to the bus. That way the command
bus is a central entry point to any write operation. With this we can rewrite the
TransferMoney service:

.. code-block:: php

    <?php
    class TransferMoneyCommand 
    {
        public $sourceId;
        public $destinationId;
        public $money;
    }

    class MoneyTransfer implements Handler
    {
        private $accountDao; // ctor omitted

        public function handle($command)
        {
            $source      = $this->accountDao->find($command->sourceId);
            $destination = $this->accountDao->find($command->destinationId);
            $money       = new Money($command->amount);

            $source->withdraw($money);
            $destination->deposit($money);
        }
    }

There is also a benefit from the mental model of commands compared to the
"generic" term of model requests in EBI. Your write model gets task
oriented.

Routing everything through the command bus has several benefits as well:

- Nesting handlers that take care of transactions, logging, 2 phase commits
- Order nested command calls sequentially instead of deep into each other.
- Asynchronous processing with message queue become an option

The command bus acts as the application boundary as described in the
Entity-Boundary-Interactor pattern, usage is simple:

.. code-block:: php

    <?php
    class MoneyController
    {
        public function transferAction(Request $request)
        {
            $commandBus = $this->container->get('command_bus');
            $commandBus->handle(new TransferMoneyCommand(
                $request->request->get('sourceId'),
                $request->request->get('destinationId'),
                new Money($request->request->get('amount')
            ));
        }
    }

Pros and Cons
-------------

I really like CQRS for multiple reasons. It offers explicit guidance how solve
tasks by making use of a range of different design patterns. This is very
helpful, because the code-base is based on conventions that are simple to
understand by everyone on the team. This structure liberates you from the curse
of choice and gives you a cookbook of best-practices how to solve problems.
You want this structure for all your applications, regardless of what
architectural pattern you have chosen.

Embracing the difference between read and write models is another plus of CQRS.
It is very helpful, not to try fitting both read and write into one model.  You
also don't run into so many read-related problems with an ORM any more. You
design the entities to be optimized for the write model only, loose the
bidirectional associations and avoid all the optimizations here and there for
read performance.

Compared to EBI, where we had to maintain a mapping between DTOs and entities,
CQRS explicitly uses the command based approach to avoid the complexity of
these mappings. You will still have to map between command and entity, however
doing so in the context of a use-case simplifies the code considerably compared
to a generic mapping solution.

One negative point: Its difficult to work with commands not returning any data 
in some cases. You need to find simple ways to return messages to the
user. For that you also need to validate commands on the "client" or
controller side, using the read model, so that you can prevent invalid/illegal
commands from being sent as often as possible.

Without return values from your models, you are left to using mocks as means of
testing. This might be more difficult for developers to use and understand.
This problem goes away however, if you combine CQRS with Event Sourcing. A
topic that I will discuss in the next blog post.

.. author:: default
.. categories:: PHP
.. tags:: ApplicationDesign
.. comments::
