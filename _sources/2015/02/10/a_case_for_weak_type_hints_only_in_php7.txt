A case for weak type hints only in PHP7
=======================================

TL;DR: I was one voice for having strict type hints until I tried the current
patch. From both a library and application developer POV they don't bring much
to the table. I think PHP would be more consistent with weak type hints only.

These last weeks there have been tons of discussions about `scalar type
hints <https://wiki.php.net/rfc/scalar_type_hints>`_
in PHP following `Andrea Faulds <https://twitter.com/andreafaulds>`_ RFC
that is currently in voting. Most of them were limited to PHP Internals
mailinglist but since the voting started some days ago much has also been said
on Twitter and blogs.

This post is my completly subjective opinion on the issue.

I would have preferred strict type hints, however after trying the patch, I
think that strict type hints

- will cause considerable problems for application developers, forcing them to
  "replicate weak type hinting" by manually casting everywhere.
- are useless for library developers, because they have to assume the user
  is in weak type mode.
- are useless within a library because I already know the types at the public
  API, weak mode would suffice for all the lower layers of my library.

Neither group of developers gets a considerable benefit from the current RFCs strict mode.

The simple reason for this, request, console inputs and many databases provide
us with strings, casting has to happen somewhere. Having strict type hints
would not save us from this, type juggling and casting has to happen and
PHP's current approach is one of the main benefits of the language.

## Real World Weak vs Strict Code Example

Lets look at an example of everyday framework code `Full
Code <https://gist.github.com/beberlei/8b23160dd0b4466fe1c5>`_ to
support my case:

.. code-block:: php

    <?php

    class UserController
    {
        public function listAction(Request $request)
        {
            $status = $request->get('status'); // this is a string

            return [
                'users' => $this->service->fetchUsers($status),
                'total' => $this->service->fetchTotalCount($status)
            ];
        }
    }

    class UserService
    {
        const STATUS_INACTIVE = 1;
        const STATUS_WAITING = 2;
        const STATUS_APPROVED = 3;

        private $connection;

        public function fetchUsers(int $status): array
        {
            $sql = 'SELECT u.id, u.username FROM users u WHERE u.status = ? LIMIT 10';

            return $this->connection->fetchAll($sql, [$status]);
        }

        public function fetchTotalCount(int $status): int
        {
            $sql = 'SELECT count(*) FROM users u WHERE u.status = ?';

            return $this->connection->fetchColumn($sql, [$status]); // returns a string
        }
    }

See how the code on ``UserService`` is guarded by scalar typehints to enforce
having the right types inside the service:

- ``$status`` is a flag to filter the result by and it is one of the integer constants, the type hint coerces an integer from the request string.
- ``fetchTotalCount()`` returns an integer of total number of users matching the query, the type hint coerces an integer from the database string.

This code example *only* works with weak typehinting mode as described in the RFC.

Now lets enable strict type hinting to see how the code fails:

- Passing the string status from the request to UserSerice methods is rejected, we need to cast status to integer.
- Returning the integer from ``fetchTotalCount`` fails because the database returns a string number. We need to cast to integer.

::

    Catchable fatal error: Argument 1 passed to UserService::fetchUsers() must
    be of the type integer, string given, called in /tmp/hints.php on line 22
    and defined in /tmp/hints.php on line 37

    Catchable fatal error: Return value of UserService::fetchTotalCount() must
    be of the type integer, string returned in /tmp/hints.php on line 48

The fix everybody would go for is casting to ``(int)`` manually:

.. code-block:: php

    public function listAction(Request $request)
    {
        $status = (int)$request->get('status'); // this is a string

        return [
            'users' => $this->service->fetchUsers($status),
            'total' => $this->service->fetchTotalCount($status)
        ];
    }

and:

.. code-block:: php

    public function fetchTotalCount(int $status): int
    {
        $sql = 'SELECT count(*) FROM users u WHERE u.status = ?';

        return (int)$this->connection->fetchColumn($sql, [$status]);
    }

It feels to me that enabling strict mode completly defeats the purpose, because
now we are forced to convert manually, reimplementing weak type hinting in our
own code.

More important: We write code with casts already, the scalar type hints patch
is not necessary for that! Only a superficial level of additional safety is
gained, one additional check of something we already know is true!

Strict mode is useless for library developers, because I always have to assume
weak mode anyways.

**EDIT:** I argued before that you have to check for casting strings to 0 when
using weak typehints. That is not necessary. Passing ``fetchTotalCount("foo")``
will throw a catchable fatal error in weak mode already!

## Do we need strict mode?

In a well designed application or library, the developer can already trust the
types of his variables today, 95% of the time, without even having type hints,
using carefully designed abstractions (example Symfony Forms and Doctrine ORM): No
substantial win for her from having strict type hints.

In a badly designed application, the developer is uncertain about the types of
variables. Using strict mode in this scenario she needs to start casting
everywhere just to be sure. I cannot imagine the resulting code to look
anything but bad. Strict would actually be counterproductive here.

I also see a danger here, that writing "strict mode" code will become a best
practice and this might lead developers working on badly desigend applications
to write even crappier code just to follow best practices.

As a pro strict mode developer I could argue:

- that libraries such as Doctrine ORM and Symfony Forms already
  abstract all the nitty gritty casting from request or database today. But I
  don't think that is valid: They are two of the most sophisticated PHP libraries
  out there, maybe used by 1-5% of the userbase. I don't want to force this
  level of abstraction on all users. I can't use this level myself all the
  time. Also if libraries already abstract this for us, why need to duplicate
  the checks again if we can trust the variables types?

- that I might have complex (mathematical) algorithms that benefit from strict
  type hinting. But that is not really true: Once the variables have passed
  through the public API of my fully typehinted library I know the types and can rely
  on them on all lower levels. Weak or strict type hinting doesn't make a
  difference anymore. Well designed libraries written in PHP5 already provide
  this kind of trust using carefully designed value objects and guard clauses.

- that using strict type in my library reduce the likelihood of bugs, but that
  is not guaranteed.  Users of my library can always decide not to use strict
  type hints and that requires me as a library author to consider this use-case
  and prevent possible problems. Again using strict mode doesn't provide a
  benefit here.

- to write parts of the code in strict and parts in weak mode. But how to
  decide this? Projects usually pick only one paradigm for good reason:
  ``E_STRICT`` compatible code yes or no for example. Switching is arbitrary
  and dangerously inconsistent. As a team lead I would reject such kind of
  convention because it is impractible. Code that follows this paradigm in
  strict languages such as Java and C# has an aweful lot of converting methods
  such as ``$connection->fetchColumnAsInteger()``. I do not want to go down
  that road.

## Would we benefit from only strict mode?

Supporters of strict mode only: Make sure to understand why this will never happen!

Say the current RFC gets rejected, would we benefit from a strict type hinting
RFC? No, and the current RFC details the exact reasons why. Most notably
for BC reasons all the PHP API will not use the new strict type hinting.

This current RFC is the only chance to get any kind of strict hinting into PHP.
Yet with the limited usefullness as described before, we can agree that just
having weak mode would be more consistent and therefore better for everyone.

## Conclusion

I as PHP developer using frameworks and libraries that help me write type safe
code today, strict typing appeals to me. But put to a test in real code it
proves to be impractical for many cases, and not actually much more useful
than weak type hinting in many other cases.

Weak types provide me with much of the type safety I need: In any given method,
using only typehinted parameters and return values, I am safe from type
juggling. As a library developer I have to assume caller uses weak mode all the
time.

Having strict type hints suggests that we can somehow get rid of type juggling
all together. But that is not true, because we still have to work with user
input and databases.

The current RFC only introduced the extra strict mode because developers had a
very negative reactions towards weak type hints. Strike me from this list, weak
type hints are everything that PHP should have. I will go as far that others
strict-typers would probably agree when actually working with the patch.

I would rather prefer just having weak types for now, this is already
a big change for the language and would prove to be valuable for everyone.

I fear Strict mode will have no greater benefit than gamification of the
language, the winner is the one with the highest percentage of strict mode
code.

.. author:: default
.. categories:: PHP
.. tags:: none
.. comments::
