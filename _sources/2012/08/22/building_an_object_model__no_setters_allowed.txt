Building an Object Model: No setters allowed
============================================

If you are using an object relational mapper or any other database
abstraction technology that converts rows to objects, then you will probably
use getter/setter methods or properties (C#) to encapsulate object properties.

Take `a look
<https://github.com/FriendsOfSymfony/FOSUserBundle/blob/master/Model/User.php>`_
at the default ``User`` entity from the Symfony2 FOSUserBundle plugin for
example: A collosus of getter/setter methods with nearly no real business
logic. This is how most of our persistence related objects look like in PHP.
A Rails ActiceRecord such as `Redmines "Issue"
<https://github.com/redmine/redmine/blob/master/app/models/issue.rb>`_ avoids
the explicit getter/setters, however generates accessors magically for you.
Nevertheless you have to add considerable amound of code to configure all the
properties. And code using these active records becomes ambiguous as well.

Why do we use getters/setters so much?

- Tools generate objects from a database, adding getters and setters
  automatically.
- Frameworks make them automatically available for database records/rows.
- IDEs can magically create getter/setter pairs for fields.
- We want the flexibility to change every field whenever we want.
- It became natural in OOP to have write access to every field.

However Getters/setters `violate the open/closed principle
<http://en.wikipedia.org/wiki/Open/closed_principle>`_, prevent information
hiding and are `should be considered evil
<http://stackoverflow.com/questions/565095/are-getters-and-setters-evil>`_
(`Long version
<http://www.javaworld.com/javaworld/jw-09-2003/jw-0905-toolbox.html>`_). Using
getters and setters allows to *decouples* the business logic for setting values from the
actual storage. Something that object-orientation was suppose to avoid.

Getting rid of setters
----------------------

Avoiding setters is much simpler than getters, so lets start with them.

One way to avoid writing setters is a task based approach to the model. Think
of every task that is performed in an application and add a method that
changes all the affected fields at once, to perform this task. In the famous
blog example the ``Post`` object may look like:

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

The ``Post`` class is now much more protected from the outside and
is actually much better to read and understand. You can clearly see
the behaviors that exist on this object. In the future you might even
be able to change the state of this object without breaking client code.

You could even call this code domain driven, but actually its just applying
the SOLID principles to entities.

Tackling getters
----------------

Avoiding getters is a bit more cumbersome and given no setters, maybe
not worth the trouble anymore.

You still need getters to access the object state, either if you display
models directly in the view or for testing purposes. There is another way
to get rid of all the getters that you don't need explicitly in a domain
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
  to have the database map to the view objects directly. This is what CQRS
  postulates as seperation of read- and write model.
- You have to write additional classes for every entity (Data transfer objects)
  instead of passing the entities directly to the view. But if you want to
  cleanly seperate the model from the application/framework, you don't get
  around view model/data transfer objects anyways.
- It looks awkard in tests at first, but you can write some custom assertions
  to get your sanity back for this task.

What about the automagic form mapping?
--------------------------------------

Some form frameworks like the `Symfony2 <http://www.symfony.com>`_ or `Zend
Framework 2 <http://framework.zend.com>`_ ones map forms directly to objects
and back. Without getters/setters this is obviously not possible anymore.
However if you are decoupling the model from the framework, then using this
kind of form framework on entities is a huge no go anyways.

Think back to the tasks we are performing on our ``Post`` entity:

- Edit (title, body, tags)
- Publish (publishDate)

Both tasks allow only a subset of the properties to be modified. For each of
these tasks we need a custom form "model". Think of these models as command
objects:

.. code-block:: php

    <?php
    class EditPostCommand
    {
        public $id;
        public $headline;
        public $text;
        public $tags = array();
    }

In our application we could attach these form models to our form framework and
then pass these as commands into our "real model" through a service layer,
`message bus <http://www.eaipatterns.com/MessageBus.html>`_ or something equivalent:

.. code-block:: php

    <?php
    class PostController
    {
        public function editAction(Request $request)
        {
            $post = $this->findPostViewModel($request->get('id'));

            // This could need some more automation/generic code
            $editPostCommand           = new EditPostCommand();
            $editPostCommand->id       = $request->get('id');
            $editPostCommand->headline = $post->headline;
            $editPostCommand->text     = $post->text;
            $editPostCommand->tags     = $post->tags;

            // here be the form framework handling...
            $form = $this->createForm(new EditPostType(), $editPostCommand);
            $form->bind($request);

            if (!$form->isValid()) {
                // invalid, show errors
            }

            // here we invoke the model, finally, through the service layer
            $this->postService->edit($editPostCommand);
        }
    }

    class PostService
    {
        public function edit(EditPostCommand $command)
        {
            $post = $this->postRepository->find($command->id);
            $post->compose($command->headline, $command->text, $command->tags);
        }
    }

This way we seperated the business model from the application framework.

A word about RAD
----------------

Rapid-application development or rapid prototyping is a wide-spread approach in web
development. My explicit approach seems to be completly against this kind of
development and much slower as well. But I think you don't loose much time
in the long run:

- Simple command objects can be code-generated or generated by IDEs
  in a matter of seconds. Or you could even extend ORMs code generation
  capabilities to generate these dummy objects for you. Since you don't need
  ORM mapping information for these objects or think about performance
  implications in context with the ORM, you don't need to spend much
  thinking about their creation. 
- Explicit models are much simpler to unit-test and those tests run much faster
  than tests through the UI that RAD prototypes need.
- Generated Rapid prototypes can get hard to maintain quickly. That does not mean they
  are unmaintainable, but they seem to favour reimplementation instead of
  refactoring, something that leads to problems given the low code coverage
  that these prototypes normally have.

Conclusion
----------

If we take a step back from all our tools suggesting to generate getter/setters
we find that there is a simple way to avoid using setters when focussing on the
tasks that objects perform. This actually makes our code much more readable and
is one building block towards clean object oriented code and domain driven design.

I am very interested in your opinions on this topic and my attempt to avoid them,
please leave comments when leaving this website :-)

.. author:: default
.. categories:: none
.. tags:: none
.. comments::
