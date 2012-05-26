.. categories:: none
.. tags:: none
.. comments::
.. author:: beberlei <kontakt@beberlei.de>

ZF: Caching Pages via Front Controller Plugin
=============================================

Today I implemented caching using a front controller plugin (`see
Matthews post on Zend Devzone <http://devzone.zend.com/article/3372>`_)
into the Whitewashing blog software via Zend\_Cache and the Filesystem
Backend. I ran some superficial Apache Benachmark tests to have a look
at the gain change in performance.

First of all i used the complete Plugin from `Matthews article on Zend
Devzone <http://devzone.zend.com/article/3372>`_ and a missing function
getCache() in the code fragment:

    ::

        public function getCache()
        {
            if( ($response = $this->cache->load($this->key)) != false) {
                return $response;
            }
            return false;
        }

I loaded the Plugin into the front controller and initialized it with a
Zend\_Config\_Ini object. This all works very smoothly and caching is
ready to begin.

Testing came to the result that with 1000 requests, 10 of them concurent
(ab -n 1000 -c 10), which I know is a rather unrealistic assumption for
this blog, the request time dropped by half, from six to three seconds
(still lot of time, but this isn't the best webserver).

Results without caching
^^^^^^^^^^^^^^^^^^^^^^^

::

    Requests per second:    1.49 [#/sec] (mean)
    Time per request:       6695.213 [ms] (mean)

    Connection Times (ms)
                  min  mean[+/-sd] median   max
    Connect:       26   30   4.0     30      43
    Processing:  1556 6452 3372.1   5511   14768
    Waiting:     1436 6129 3174.1   5145   14595
    Total:       1583 6483 3373.2   5538   14810

Results with caching
^^^^^^^^^^^^^^^^^^^^

::

    Requests per second:    3.03 [#/sec] (mean)
    Time per request:       3304.534 [ms] (mean)

    Connection Times (ms)
                  min  mean[+/-sd] median   max
    Connect:       26   31   6.3     30      73
    Processing:   781 3214 1757.7   3103    7445
    Waiting:      650 3055 1731.4   2928    7190
    Total:        809 3245 1757.8   3135    7475

As said before this testing is superficial, but its gives a broad sense
of what perfomance gain is possible with just some lines of code and a
temporary directory. Using memcache will probably speed up the process
another good amount.

Later I realized that complete page caching (rather than block element
caching) sucks when you inject admin area linkes into the navigation,
which would allow non-logged in users to see parts of the admin area so
I had to disable caching totally. You never know in the first place (you
should though). I have to rework my admin area or extend my
authentication or the caching plugin somehow. This will probably be the
topic another time.
