.. categories:: none
.. tags:: none
.. comments::
.. author:: beberlei <kontakt@beberlei.de>

Multidimensional Array via SPL
==============================

Per default any implementation of ArrayObject does not allow to use the
object as multidimensional array. This snippet here implements the
support:
    ::

        class ArrayMultiObject extends ArrayObject
        {
            function __construct($array, $flags = 0, $iterator_class = "ArrayIterator")
            {
                $objects = array();
                foreach($array AS $key => $value) {
                    if(is_array($value)) {
                        $objects[$key] = new ArrayMultiObject($value, $flags, $iterator_class);
                    } else {
                        $objects[$key] = $value;
                    }
                }

                parent::__construct($objects, $flags, $iterator_class);
            }

            public function offsetSet($name, $value)
            {
                if(is_array($value)) {
                    $value = new ArrayMultiObject($value);
                }

                return parent::offsetSet($name, $value);
            }
        }

