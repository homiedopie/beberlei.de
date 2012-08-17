Building an Object Model: No setters allowed
============================================

If you are using an object relational mapper or any other database
abstraction technology that is object-oriented, then you will probably
use setter methods or properties (C#) to encapsulate object properties.

Take `a look
<https://github.com/FriendsOfSymfony/FOSUserBundle/blob/master/Model/User.php>`_
at the default ``User`` entity from the Symfony2 FOSUserBundle plugin for
example: A collosus of getter/setter methods with nearly no real business
logic. This is how most of our persistence related objects look like in PHP.
A Rails ActiceRecord such as `Redmines "Issue"
<https://github.com/redmine/redmine/blob/master/app/models/issue.rb>`_ avoids
the explicit getter/setters, however generates accessors magically for you.
Nevertheless you have to add considerable amound of code to configure all the
properties.

Why do we use getters/setters so much?

- Tools generate objects from a database, adding getters and setters
  automatically.
- Frameworks make them automatically available for database records/rows.
- IDEs can magically create getter/setter pairs for fields.
- We want the flexibility to change every field whenever we want.
- It became natural in OOP to have write access to every field.

However, you should realize: Getters/setters `violate the open/closed principle
<http://en.wikipedia.org/wiki/Open/closed_principle>`_ and are `considered evil
<http://stackoverflow.com/questions/565095/are-getters-and-setters-evil>`_
(`Long version
<http://www.javaworld.com/javaworld/jw-09-2003/jw-0905-toolbox.html>`_). Yet
we keep creating these methods in the hundrets and thousands.

Getting rid of setters
----------------------

One way to avoid writing setters is a task based approach to your model. Think
of every task that is performed in your application and add a method that
changes all the affected fields at once.

.. code-block:: php

    <?php
    class Post
    {
        public function compose($headline, $text, array $tags)
        {
            // check invariants, business logic, filters

            $this->headline = $headline;
            $this->text     = $text;
            $this->tags     = $tags;
        }

        public function publish(\DateTime $onDate = null)
        {
            // check invariants, business logic, filters

            $this->state       = "published";
            $this->publishDate = $onDate ?: new \DateTime("now");
        }
    }

This ``Post`` is now much more protected from outside destruction and
is actually much better to read and understand. You can clearly see
the behaviors that exist on this object. In the future you might even
be able to change the behavior without breaking client code.

You could even call this code domain driven, but actually its just applying
the SOLID principles to your entities.

Tackling getters
----------------

Now you still need getters to access the information, either if you display
your models directly in the view or for testing purposes. There is another way
to get rid of all the getters that you don't need ecplitly in your domain
model, using the visitor pattern in combination with view models:

.. code-block:: php

    <?php
    class Post
    {
        public function render(PostView $view)
        {
            $view->id          = $this->id;
            $view->publishDate = $this->publishDate;
            $view->headline    = $this->headline;
            $view->text        = $this->text;
            $view->author      = $this->author->render(new AuthorView);

            return $view;
        }
    }

    class PostView
    {
        public $id;
        //... more public properties
    }

There are drawbacks with this approach though:

- Why use the Post model in memory, when you are only passing ``PostView``
  instances to the controllers and views only anyways? Its much more efficient
  to have your database map to the view objects directly.
- You have to write additional classes for every entity (Data transfer objects)
  instead of passing the entities directly to the view. But if you want to
  cleanly seperate your model from the application/framework, you don't get
  around view model/data transfer objects anyways.
- It looks awkard in tests at first, but you can write some custom assertions
  to get your sanity back for this task.

What about the automagic form handling?
---------------------------------------

Some form frameworks like the `Symfony2 <http://www.symfony.com>`_ or `Zend
Framework 2 <http://framework.zend.com>`_ ones map forms directly to objects
and back. Without getters/setters this is not possible anymore obviously.
However if you are decoupling your model from your framework, then using this
kind of form framework on your entities is a huge no go anyways.

Think back to the tasks we are performing on our ``Post`` entity:

- Edit (title, body, tags)
- Publish (publishDate)

Both tasks allow only a subset of the properties to be modified. For each of
these tasks we need a custom form "model". Think of these models as command
objects:

.. code-block:: php

    class EditPostCommand
    {
        private $title;
        private $body;
        private $tags;
        // and their associated getters/setters, or just use public properties
    }

In our application we could attach these form models to our form framework and
then pass these as commands into our "real model" through a service layer,
`message bus <http://www.eaipatterns.com/MessageBus.html>`_ or something equivalent:

.. code-block:: php

    class PostController
    {
        public function editAction(Request $request)
        {
            $editPostCommand = new EditPostCommand();

            // here be the form framework handling...
            $form = $this->createForm(new EditPostType(), $editPostCommand);
            $form->bind($request);

            if ($form->isValid()) {
                $this->postService->edit($editPostCommand);
            }
        }
    }

This way we seperated the business model from the application framework nice
and clean.

A word about RAD
----------------

Rapid-application development or rapid prototyping is a usual approach in web
development. My explicit approach seems to be completly against this kind of
development and much slower as well. But I think you don't loose much time:

- Those simple command objects can be code-generated or generated by your IDE
  in a matter of seconds. You could even extend your ORMs code generation
  capabilities to generate these dummy objects for you. Since you don't need
  ORM mapping information for these objects, you don't need to spend much
  thinking about their creation. 
- Rapid prototypes can get hard to maintain quickly. That does not mean they
  are unmaintainable, but you might run into troubles when a big database
  refactoring is necessary or you skip the refactoring and try to complete the
  application with an ill-fit model.
- Explicit models are much simpler to unit-test. You spend lots of time not
  waiting for your slow tests through the application. That is if you test at
  all.

I am very interested in your opinions on getter/setters and my attempt to avoid them,
aswell your experiences with other approaches.

.. author:: default
.. categories:: none
.. tags:: none
.. comments::
