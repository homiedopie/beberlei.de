Enums in PHP
============

`A colleague of mine <http://blog.tobias-olry.de>`_ complained about the
missing support for Enums in PHP and how one often wants to have a
variable that is constant and has one of several specific values. We
came up with an elegant solution that we want to share, maybe its even
helpful to you.
If you want to implement Enum behaviour with a simple string or int
value you end up with having to validate the values at several different
locations in the code rather than being able to strictly enforce the
Enum structure by using typehints.

We discussed several approaches to this problem that all seemed a bit
ugly in one or another way. For example the **SplEnum** class is a step
in the right direction, however you can only use a type hint for
"SplEnum" or add another inheritance layer. Also you have to implement
different classes for each enum type, which requires you to implement a
factory method for your enum to help with creation of the different
types.

We came up with a very simple Enum concept. It uses reflection in the
constructor to check if the given value is a valid Enum value by
checking it against all the defined constants of the implementing class
and throws an Exception if it is not. The \_\_toString() magic method is
implemented to allow for simple checks of the enums value. Strict
type-checks are not possible with this construct, however in our opinion
it is a very elegant solution to enforce a limited set of specific
values throughout your code-base.

Here is the code plus a small example:

    ::

        abstract class MyEnum
        {
            final public function __construct($value)
            {
                $c = new ReflectionClass($this);
                if(!in_array($value, $c->getConstants())) {
                    throw IllegalArgumentException();
                }
                $this->value = $value;
            }

            final public function __toString()
            {
                return $this->value;
            }
        }

        class Foo extends MyEnum
        {
            const FOO = "foo";
            const BAR = "bar";
        }

        $a = new Foo(Foo::FOO);
        $b = new Foo(Foo::BAR);
        $c = new Foo(Foo::BAR);

        if($a == Foo::FOO) {
            echo "My value is Foo::FOO\n";
        } else {
            echo "I dont match!\n";
        }

        if($a == $b) {
            echo "a value equals b value!\n";
        }
        if($b == $c) {
            echo "b value equals c value!\n";
        }

Now you could nice things such as:

    ::

        function doStuff(Foo $foo) {
            switch($foo) {
                case Foo::FOO:
                    echo "do more here!\n";
                    break;
                case Foo::BAR;
                    echo "evil stop!\n";
                    break;
            }
        }

        doStuff($a);

What are your thoughts?

.. categories:: none
.. tags:: ApplicationDesign, PHP
.. comments::
