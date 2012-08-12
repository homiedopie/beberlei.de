OOP Business Applications: Command-Query-Responsibility-Seggregation (CQRS)
===========================================================================

The last pattern for desigining your business logic is called
"Command-Query-Responsiblity-Seggregation" or short CQRS. It has its roots in
the `"Command Query Seperation"
<http://en.wikipedia.org/wiki/Command-query_separation>`_ principle that was
put forward by Bertrand Meyer.

Wikipedia has a very good summary about what this principle is about:

::

    Command-Query-Seperation states that every method should either be a
    command that performs an action, or a query that returns data to the
    caller, but not both. In other words, asking a question should not change
    the answer. More formally, methods should return a value only if they are
    referentially transparent and hence possess no side effects. 

CQRS is an OOP design pattern building on that imperative principle. As
I tried to understand this pattern I found that there are many different
variations of it that all have their place. This however makes it hard to write an
introduction blog post, without confusing the reader or selling CQRS as a
complexity nightmare, which is not always the case.

The first obvious requirement: Our write service methods are not allowed to
return data anymore. This may increase the complexity at first, especially when
you work with MySQL that only generates IDs during the INSERT operation,
however a strict adherence to this principle allows us to turn every command
from synchroneous to asynchroneous processing later without much problems.
This solves one problem of my list of annoyances in a clean way ("Never return
data from your commands"). Although services are not allowed to return
something, they are allowed to throw exceptions and refuse the execution. This
is one way of direct feedback about command failures to the user. If you are
speculating with asynchroneous processing of the tasks however, you loose that
channel.

At its heart there is obviously the seperation of Read and Write methods. This
can be easily achieved by just having two different service layer classes
instead of one. This insight alone is not really helpful, its just moving
methods around. Coupled to this change however is the notion, that read and
write models don't have to be the same. Let me clarify what problems of my list
occur, just because of using the same models and DTOs for reading and writing:

- Getter/Setter Madness. In write models we don't need setters, as we can have
  methods that handle each command explicitly. Additionally in write scenarios
  we don't need all that bidirectional associations that make the use of an ORM
  much more difficult. In Read-only models we don't actually need
  getters/setters. They could just use public properties or even be arrays.
- ORM Performance, Lazy Loading and Query Restrictions: In a write scenario we
  mostly need queries by primary key, changing only a few set of objects. In
  read scenarios we often need complex joins and aggregations. Using just one
  model mapped with one ORM may lead to both read and write scenarios to affect
  each other negatively.
- Reading a DTO, modifying it on the client then writing its full
  representation back to the server leads to very tricky problems with
  validation and state-machines. If you pass the whole DTO for updating, the
  model actually never knows what the intent of the change was. This requires
  complex mapping of all property and association changes from the DTO to the
  entity object. This approach has lead to a class of security problems called
  "mass-assignment-vulnerability", where in a mass assignment from DTO to
  entity object, the client can change fields he is not allowed to.

As the first step, why not transform SQL directly to a view model in a highly
optimized way? There is no actual need to pass through boundary, service layer, data
access objects and translate back and forth just to read some data. This is a
simple concept, but it has huge implications. For a modelling purist that I
want to be, it gives me absolution that I don't have to come up with the one
model that fits all use-cases. Read and write operations are so fundamentally
different, that we shouldn't reject to use different models for
them mentally and in code.

One drawback is obviously a naive implementation doubles the amount of classes
and services to write. But there are simple shortcuts to avoid having to write
a full blown read-model:

- Mapping SQL to PHP arrays and stdClass objects through a simple gateway is
  very simple. You can easily generialize this to a simple object that gives
  efficent access to all your data.
- If the write model fits the read use-cases, does not have performance
  requirements and is not the central object of your domain, but rather just a
  sidekick: Just reuse it
- In Doctrine ORM for example you could re-use the model, but hydrate it only
  as arrays - saving the costly transformation to an object model. 
- You could actually use the entities from the model, not to loose the "Open
  Entity Manager in view" benefits for RAD. But be warned, this leads to the
  Doctrine ORM Entity model being the read model and your write model should be
  managed in a different way.

The important thing to take away from this seperation is, that the read part of
your application isn't the part where the business value is generated. Putting
that code into a different part of your applications allows you to work with
the underyling data-source much more directly, without need for much
abstractions.

Compared to the previous posts this was lots of introduction, but that is
in my opinion, because CQRS comes with lots of structure and concepts that
actually guide and constrain you while implementing. Having a techincal
architecture constraining the "how its going to be done" is useful to keep
a consistent code-base.

One thing that CQRS puts forward is the concept of Commands, Command Handlers
and Command Bus and how they interact. Commands are simple objects that
contain all the data necessary to execute an operation. Each command is
processed by exactly one command handler. The Command Bus is responsible to
route a command to its apporpriate command handler.

Example
-------

Here is the most simple implementation of the Command Bus, just holds a hash map
mapping command class names to command handlers:

.. code-block:: php

    <?php
    class TransferMoneyCommand
    {
        public $sourceId;
        public $destinationId;
        public $money;
    }
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
bus is a central entry point to any write operation. This is what in EBI would
be called the boundary, however here its actually a central concept. You can
wrap commands in transactions here, add logging or whatever you think is
necessary. Additionally we can guard the code agaisnt any return values passed
back to the system from handlers by accident. With this we can rewrite the
TransferMoney service:

.. code-block:: php

    <?php
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

There is also a benefit from the mental model of commands vs the "generic" term
of model requests in EBI. Your model becomes a much more task oriented focus,
compared to generic CRUD based updating of entities.

Now this is an advanced step, but we could seperate use-cases even more, trying
to make our code more DRY and SOLID. We might want to call additional commands
from a command handler. I haven't seen a direct example for this in any of the CQRS
blogs or examples, but it makes perfect sense: Since we require command
handlers to not return state, we can actually process commands sequentially,
even if they are called nested in each other. Suppose I have a command to
upload a new picture to my gallery, which calls another command to actually
start the resizing of pictures. Using a stack of commands inside the
CommandBus, we could linearize the execution of commands, freeing us from
having to think about nested transactions inside commands. We just drop all the
child commands from the stack when the transaction of the parent command fails. 
This allows us to have many small transactions on a resource instead of one big
one and through customization of the command bus allows asynchroneous
processing with ZeroMQ, Gearman or any other message queue.

Pros and Cons
-------------

I really like CQRS for multiple reasons. It offers a common "framework" how to
solve tasks and does so by posing restrictions on how to do this tasks. This is very
helpful, because the code-base is based on conventions that are simple to
understand by everyone on the team. It frees you from the curse of choice.

It also open ups to the reality that read and write operations are very
different and might require different models to efficently function. Although
this may also be a negative point, if you end up with lots of additional code
that is required to be maintained. However it also frees developers from having
to keep so much code in mind. In general working on the read side of the model
means that you cannot affect anything breaking on the write side (and vice
versa).

With different read and write models you also don't run into so many problems
with your ORM any more. You design the entities to be optimized for the write
model only, loose the bidirectional associations and avoid all the optmizations
here and there for read performance.

Compared to EBI, where we had to maintain a mapping between DTOs and entities,
CQRS explicitly uses the command based approach to avoid the complexity of
these mappings. You will still have to map between command and entity, however
doing so in the context of a use-case simplifies the code considerably compared
to a generic mapping solution.

With the command in command execution, it is even possible to divide the tasks
into many small isolated parts, which makes it much simpler to create DRY and
SOLID code.

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
.. categories:: none
.. tags:: none
.. comments::
