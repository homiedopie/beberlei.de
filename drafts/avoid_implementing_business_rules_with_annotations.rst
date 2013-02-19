Avoid implementing business rules with Annotations
==================================================

In January I was participating at the awesome `PHP Benelux 2013
<http://conference.phpbenelux.eu/2013/schedule/>`_ conference and attended
`Raphael Dohms <http://www.rafaeldohms.com.br/>`_ talk on "PHP Annotations -
They exist!". It was a very good talk about the history, current state and
actual implementations for Annotations in PHP.

At the end of the talk there was an important question from one person in the
audiance about how to test code that is using annotations to drive the business
rules. I try to answer the question in this blog post.

Lets start by the beginning and define annotations. Annotations are metadata to
code blocks. Comparable to INI, XML or YAML they provide a way to load
configuration. In contrast to the other configuration mechanisms however,
annotations are right next to PHP code they configure. They allow you to
configure classes, properties, methods in context without having to move around
in several of configuration files. 

The Doctrine Annotations library has spawned several new libraries that allow
to configuration through annotations. Should we just use them, because they are
so convenient?

No! In my opinion it is important to differentiate between different use-cases
of annotations. Take a look at Doctrine ORM Mapping or Raphaels DMS Filter library.
Using their annotations looks like this:

.. code-block:: php

    <?php
    use Doctrine\ORM\Mapping as ORM;
    use DMS\Filter\Rules as Filter;

    /**
     * @ORM\Entity
     * @ORM\Table(name="users")
     **/
    class User
    {
        /**
         * @ORM\Id @ORM\GeneratedValue @ORM\Column(type="integer")
         **/
        private $id;

        /**
         * @ORM\Column(type="string")
         * @Filter\Trim()
         **/
        private $email;
    }

Both libraries solve problems of the infrastructure layer and not of the
business domain. Both libraries could probably also be configurable through
PHP code, XML and YAML and this would be completly fine.

The use of annotations in this case is just a substitute for XML, INI or YAML
configuration files, allowing your business model to integrate into infrastructure
libraries.

The same holds for the Serialization-, WSDL- or Routing configuration using
annotations.

Problematic Use-Cases
---------------------

There are use-cases when I am careful about the use of annotations (any kind
of configuration actually): When I am configuring how my business
objects works. The following real-world use-cases come to mind:

- Validation
- Aspects
- Dependency Injection

When libraries allow you to configure how your business objects work based on
annotations, coupled to the respective libraries way of doing things, problems
are going to appear. Depending on the implementation this can end up very
badly, with serious coupling of the library towards your business objects.

Validation
~~~~~~~~~~

Symfony Validator allows you to add assertions for validation rules on the
properties or methods of your business models.

If you think about it, validation is a cross-cutting concern. It is part of the
infastructure for simple validation rules like checking if the user input data
is valid, but it can also be used for business logic of your domain.

See this code example:

.. code-block:: php

    <?php
    use Symfony\Component\Validator\Constraints as Assert;
    use MyProject\Validator\Constraints\EmailBlacklist;

    class User
    {
        /**
         * @Assert\NotBlank
         * @Assert\Email
         * @EmailBlacklist
         **/
        private $email;
    }

We added three validation rules here, two from the Symfony core validating the
email syntax and not blank, another one from my own project, validating the
email aginst some blacklist.

Now in Symfony you can use this code either directly through the Validation
service or indirectly through the Form component:

.. code-block:: php

    <?php
    $validator = $container->get('validator');

    $user          = new User();
    $violationList = $validator->validate($user);

This sort of tangling of critical business logic to framework services is a
problem. The reason for this is that you want to be able to unit-test your
business logic. A deep integration of your business logic into the Symfony
Validation component will prevent you from actually doing this. 

To test this validation constraint, you need to:

* Call the validator service with a user object and a blacklisted email
* Call the validator service with a user object and a non-blacklisted email

In addition to testing the actual email blacklist validation, they verify
annotation parsing and the full Symfony Validator stack. In general these tests
are slow and I know this from experience, not following my own advice.

Instead you should write a completely independent E-Mail Blacklist Service:

.. code-block:: php

    <?php
    namespace MyProject\Validator;

    class EmailBlacklistService
    {
        public function isBlacklisted($email)
        {
            return true; // logic here
        }
    }

This service can be unit-tested and is part of your actual business domain,
independent of Symfony. You can now integrate this into a Symfony Validator:

    <?php

    namespace MyProject\Validator\Constraints;

    use Symfony\Component\Validator\Constraint;
    use MyProject\Validator\EmailBlacklistService;

    /**
     * @Annotation
     **/
    class EmailBlacklist extends Constraint
    {
        public $message = 'Your email %email% is on our blacklist.';
    }

    class EmailBlacklistValidator
    {
        private $blacklist;

        public function __construct(EmailBlacklistService $blacklist)
        {
            $this->blacklist = $blacklist;
        }

        public function validate($value, Constraint $constraint)
        {
            if ($this->blacklist->isBlacklisted($value)) {
                $this->context->addViolation(
                    $constraint->message,
                    array('%email%' => $value)
                );
            }
        }
    }

Now actually what we can do is write a unit-test for this Symfony validator
using mock objects. We can add a single functional tests to actually verify
the configuration is present on the ``User$email`` property, but we don't
actually need to test the validation logic through the full stack.

Inside our business model you can reuse the Blacklist Service without having to
depend on Symfony code. So instead of injecting the full validator service,
you can just inject the much more explicit blacklist service.

Validation libraries are a tricky problem when combined with validation rules
from your business domain. Be careful not to depend on them too much with
your business logic and keep it seperate.

Dependency Injection
~~~~~~~~~~~~~~~~~~~~

Using Annotations for Dependency Injection is not necessarily bad,
however the way its implemented in some frameworks may lead to
code that is unusable without the Dependency Injection container.

FLOW3 allows to inject dependencies into properties of instances:

    class BlogService
    {
        /**
         * @Inject
         **/
        private $blogRepository;
    }

This even works when you are instantiating the object yourself using ``new``.
So inside FLOW3, the call to ``new BlogService`` automatically injects the
repository.

The problem here is easy to spot. If you use framework supported Dependency
Injection with Reflection, then you don't need to write constructors or setters
anymore that actually asign the repository. This prevents you from actually
testing the code, because the classes are not easily instantiatable in a
Unit-Test anymore. Additionally you might rely on the automagic injection
in your code, so much that it is not executable without the Injection
framework being present in your unit-tests.

You can of course start providing constructors or setters, but this feature
still affects your control flow in production, using reflection instead
of the "expected" control flow.

Aspects
~~~~~~~

In FLOW3 Annotations are used to change the control flow of the applications.
As a developer you can introduce code and make it execute around arbitrary
other code. The way its implemented with code generation you can never
actually unit-test this yourself, because any test-setup requires the Aspect
Engine to run.

This is obviously a huge change of control flow, configured through
annotations. Additionally there is the code generation involved. I am very
skeptical about large scale usage of this kind of feature if it affects
the way your business logic works.

Testing this kind of feature is obviously not possible without the
AOP framework. This effectively means that its impossible to unit-test
your domain objects.

Conclusion
----------

There is a difference between using Annotations for configuration of
infrastructure services and business model interaction. The first one is
perfectly fine, its replacable by any other sort of configuration or explicit
programmatic code and doesn't hinder you writing unit-tests for your business
model. The second one makes it hard to actually do unit-testing without using
the libraries that perform the actual operations.

.. author:: default
.. categories:: PHP
.. tags:: PHP
.. comments::
