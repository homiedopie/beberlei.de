OOP Business Applications: Entity, Boundary, Interactor
=======================================================

Other posts in this series:

- [OOP Business Aplications: Trying to escape the
  mess](http://whitewashing.de/2012/08/11/oop_business_applications__trying_to_escape_the_mess.html)

Continuing the series, I will talk about Entity, Boundary and Interactor (EBI)
an architectural design pattern. I first heard about it in a keynote video of
`Uncle Bob <https://sites.google.com/site/unclebobconsultingllc/>`_ on Ruby
Midwest called `"The lost years of architecture"
<http://www.confreaks.com/videos/759-rubymidwest2011-keynote-architecture-the-lost-years>`_.
This is also described as `Hexagonal architecture
<http://alistair.cockburn.us/Hexagonal+architecture>`_ or "Ports and Adapters"
by Alistair Cockburn.

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

Boundary Abstraction
--------------------

Thinking about the boundaries I came up with a library several month ago called
[Context](https://github.com/beberlei/context). It allows you to wrap calls
to the model by some sort of proxy that transforms the request and response
and also handles transactions and such. Loosly spoken this was actually
some kind of AOP library, using the limited ways that PHP provides to implement
AOP (magic ``__call`` proxies).

With context you would do something like:

.. code-block::

    <?php
    $context = $this->getContext();

    // 1. direct invocation
    $myService = new MyService();
    $context->execute(array('service' => $myService, 'method' =>
    'doSomething', 'arguments' => $args));

    // 2. proxy wrapping
    $myService = $context->wrap(new MyService());
    $myService->doSomething($args);

The second way is obviously way more readable, but its also rather magic.

I deprecated this library because in the end it wasn't really helpful that
much. Implementing an application specific proxy for services is done in
almost no time and then it solves all your specific needs. My main problem with
the library is that it tries to magically take away the need to design the
boundary of your application yourself - in a way that is not really coherent to
other developers.

In my own current greenfield applications I quickly went away from using it,
since a custom application proxy [as shown in this
Gist](https://gist.github.com/3272909) is really much simpler to implement and
use.

Using with Symfony2
-------------------

As I am currently exclusively developing Symfony2/Silex applications, applying
EBI to Symfony2 framework based applications is very important to me. The
biggest difficulty here is the Form layer, escpecially the request data-mapping and
validation concerns, which are normally part of the model. There are two
approaches I came up with to solve this:

* Build Forms for arrays or DTOs and send them through to the boundary to the model.
  You have to validate the data again on the model, which is annoying, but in
  this case the clean way. This is not so easy to do with complex forms though
  as you need to map the request objects to your entities.
* Create a Model Request that wraps and hides the form behind a simple data
  mapping API. This way you can make it look as if you would map a DTO onto
  an object, but in this case you are using the Form API as the mapper.

.. code-block:: php

    <?php
    class MyService
    {
        public function edit(EditRequest $request)
        {
            $entity = $this->dao->find($request->id);
            $this->dataMapper->transform($request, $data);
        }
    }

The problem with this approach is, that you cant really unit-test these methods
anymore, because the complexity of the form layer mapping cannot be mocked
with this API. Additionally you have to make the DataMapper throw an exception
that you can catch in the controller, rendering the appropriate response.

Another thing that actually helped was the SensioFrameworkExtraBundle and
ParamConverters. In my project I now have the framework building the Model
Request objects by convention from the HTTP Request, so that I only need to
pass them on and can skip the actual mapping of HTTP Request to Model Request.

Pros and Cons
-------------

This design pattern very closely resembles what Fowler calls **Service Layer**
pattern in PoEAA. EBI is going a bit more into detail by naming individual
parts of the pattern more explicit. Without more restrictions however using
this pattern will drive you towards many of the problems described in my
previous post.

Clean seperation from frameworks is achieved, depending on the actual usage
however only at a significant cost.  Never forget stepping back and thinking
about further abstractions, otherwise applying EBI is leading to lots of code
being manually written. 

This already shows one particular annoyance are the data-transfer objects. You
need to invest quite some work to get a mapping working from entities to
transfer objects and back. In the process you will loose the convenience of
"Open Entity Manager in the View", where you can lazy load any
data you want to access in the view. This is quite a painful step, because you
are loosing lots of flexibility. Much more annoying is the need to update
entities from data-transfer objects, requiring sophisticated code for merging
of partial object graphs. 

What this design pattern improves is the testability of code and also the
execution of tests is MUCH better, when you don't have to go through the whole
application stack to test something.

Implementing behavior into the use-cases also avoids lots of lasagna code
compared to a messy domain driven design. You get a very good overview of
what is actually happening just by looking at the Model Request and Interactor
classes. However depending on the use-case the classes can get very big
and might need lots of collaborators, which make the problem complex again.

It is important to note that aggregating the domain logic in the use-cases
actually means going to some sort of transaction script processing, away from
domain driven design. I am pretty sure that this is not necessarily the
intention of this design pattern from a POV of Uncle Bob. However depending on
the sophistication of the applications domain logic, transaction script is
actually a very good pattern for simple to medium complex use-cases and
I like to have this as a general rule for developers ("Put behavior on the
use-case").

In conclusion I can partially recommend using the EBI pattern. You have to be
careful to find abstraction layers that keep your code DRY and SOLID however,
something which does not come naturally with this pattern. If you are not
careful you end up with all the "messy points" that I mentioned in my previoius
blog post.

You should be especially careful to avoid lots of DTO <-> Entity Mapping code
by using some code-generation for example to do parts of this job for you. The
worst outcome with this pattern is, when you manually code layers for HTTP
Request/Form => DTO => Entity mapping and the other way around. 

.. author:: default
.. categories:: none
.. tags:: none
.. comments::
