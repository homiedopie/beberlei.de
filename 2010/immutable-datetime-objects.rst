:author: beberlei <kontakt@beberlei.de>
:date: 2010-01-08

Immutable DateTime Objects
==========================

One serious drawback of `PHPs DateTime
extension <http://de.php.net/DateTime>`_ is the mutability of its
instances. It can lead to serious bugs if a DateTime instance is passed
between different functions and is modified at unexpected places.
Additionally this possibly rules out several optimizations for scripts
that make very heavy use of dates and could share references to equal
timestamps.

**Warning:** All the code assumes that you work with one timezone only!

The following code is an immutable version of PHP's DateTime. All setter
methods throw an exception and add(),sub() and modify() clone the
current instance, apply the operation and return the new instance.

.. code-block:: php

        <?php
        namespace Whitewashing\DateTime;

        class DateTime extends \DateTime
        {
            /**
             * To prevent infinite recursions
             *
             * @var bool
             */
            private static $_immutable = true;

            public function add($interval)
            {
                if (self::$_immutable) {
                    self::$_immutable = false;
                    $newDate = clone $this;
                    $newDate->add($interval);
                    self::$_immutable = true;
                    return $newDate;
                } else {
                    return parent::add($interval);
                }
            }

            public function modify($modify)
            {
                if (self::$_immutable) {
                    self::$_immutable = false;
                    $newDate = clone $this;
                    $newDate->modify($modify);
                    self::$_immutable = true;
                    return $newDate;
                } else {
                    return parent::modify($modify);
                }
            }

            public function sub($interval)
            {
                if (self::$_immutable) {
                    self::$_immutable = false;
                    $newDate = clone $this;
                    $newDate->sub($interval);
                    self::$_immutable = true;
                    return $newDate;
                } else {
                    return parent::sub($interval);
                }
            }

            public function setDate($year, $month, $day) {
                throw new ImmutableException();
            }
            public function setISODate($year, $week, $day=null) {
                throw new ImmutableException();
            }
            public function setTime($hour, $minute, $second=null) {
                throw new ImmutableException();
            }
            public function setTimestamp($timestamp) {
                throw new ImmutableException();
            }
            public function setTimezone($timezone) {
                throw new ImmutableException();
            }
        }
        class ImmutableException extends \Exception
        {
            public function __construct()
            {
                parent::__construct("Cannot modify Whitewashing\DateTime\DateTime instance, its immutable!");
            }
        }

Its not the prettiest code, but it works.

A next optimization would be a **DateFactory** that manages DateTime
instances by returning already existing instances for specific dates.
This is not a perfect solution, since you won't be able to enforce a
single instance when you are using the relative descriptive dates or
when calculating with dates using add(), sub() and modify(), however for
lots of dates created from a database or other external source it might
be quite a powerful optimization depending on your use-case:

.. code-block:: php

        namespace Whitewashing\DateTime;

        class DateFactory
        {
            static private $_dates = array();

            static public function create($hour, $minute, $second, $month, $day, $year)
            {
                $ts = mktime($hour, $minute, $second, $month, $day, $year);
                if (!isset(self::$_dates[$ts])) {
                    self::$_dates[$ts] = new DateTime('@'.$ts);
                }
                return self::$_dates[$ts];
            }

            static public function createFromMysqlDate($mysqlDate)
            {
                list($date, $time) = explode(" ", $mysqlDate);
                if($time == null) {
                    $hour = $minute = $second = 0;
                } else {
                    list($hour, $minute, $second) = explode(":", $time);
                }
                list($year, $month, $day) = explode("-", $mysqlDate);
                return self::create($hour, $minute, $second, $month, $day, $year);
            }
        }

This includes some date time calculations and date creation with
mktime() and DateTimes unix timestamp capabilities to be able to work.
Otherwise the sharing of instances could not be implemented. If you need
to create shareable instances from other formats you could just create
another creation method for it and convert the format for create() to be
used.
