Benchmark and Optimize Zend Framework Performance
=================================================

In the fall of `Rasmus presentation (Simple is
Hard) <http://talks.php.net/show/froscon08>`_ on
`FrOSCon <http://www.froscon.org>`_ I tried to optimize `Zend
Frameworks <http://framework.zend.com>`_ performance a little bit. There
has also been a little discussion on the Zend Framework Mailing List on
this topic.

I haven't changed great parts of the code or anything, I just
benchmarked how different global include strategies affect the overall
performance of my blog software written with help of the ZF. The
following include strategies were tested (I've used the Zend Framework
1.6 RC2 package for all of them):

#. Zend\_Loader Autoload, Default PHP Include Path
#. Zend\_Loader Autoload, Swapped Include Path
#. ZF 1.6 RC2 stripped from all **"require\_once"** dependencies,
   Zend\_Loader Autoload, Swapped Include Path
#. ZF 1.6 RC2 stripped from all **"require\_once"** dependencies, no
   autoload, used `inclued <http://pecl.php.net/package/inclued>`_ to
   find file dependencies and require (not \_once) them all on startup.

To strip all the require\_once from the Zend Framework source code, i
built a little script to do that for me. For the last test I wrote a
little script that used the **inclued\_get\_data()** function to built a
correct dependency tree for all includes. I have put each configuration
of my Zend Framework install 30 seconds under siege with 5 concurrent
requests. I have rerun all tests with APC and without APC.

Results without APC
^^^^^^^^^^^^^^^^^^^

+----------------------------------+-----------------+-------------+-----------------+
| Include Strategy                 | Response time   | Trans/sec   | Performance %   |
+----------------------------------+-----------------+-------------+-----------------+
| Autoload, default include path   | 0.20            | 24.65       | 100%            |
+----------------------------------+-----------------+-------------+-----------------+
| Autoload, swapped include path   | 0.19            | 26.83       | 95%             |
+----------------------------------+-----------------+-------------+-----------------+
| Autoload, ZF w/o require\_once   | 0.17            | 29.27       | 85%             |
+----------------------------------+-----------------+-------------+-----------------+
| No-Autoload, require up front    | 0.16            | 31.82       | 80%             |
+----------------------------------+-----------------+-------------+-----------------+

You can see that each step makes a ZF application run faster and that
the full optimization with requiring all scripts up front is about 20%
faster than the default configuration.

Results with APC
^^^^^^^^^^^^^^^^

+----------------------------------+-----------------+-------------+-----------------+
| Include Strategy                 | Response time   | Trans/sec   | Performance %   |
+----------------------------------+-----------------+-------------+-----------------+
| Autoload, default include path   | 0.11            | 45.76       | 100%            |
+----------------------------------+-----------------+-------------+-----------------+
| Autoload, swapped include path   | 0.09            | 53.05       | 81,81%          |
+----------------------------------+-----------------+-------------+-----------------+
| Autoload, ZF w/o require\_once   | 0.08            | 60.90       | 72,72%          |
+----------------------------------+-----------------+-------------+-----------------+
| No-Autoload, require up front    | 0.07            | 73.99       | 63,63%          |
+----------------------------------+-----------------+-------------+-----------------+

Turning APC on gives a boost of about 50% to your application no matter
what include strategy you are following (so there is excuse not using
APC). But switching between different include strategies still makes a
huge difference in performance. Percentage-wise this is a larger
difference than without APC. Requiring all dependent scripts up front
takes only about 63% of the default configuration time, which can make a
major difference on any production server.

In an application knowing which includes of the Zend Framework will be
needed on each request is difficult, since different helpers and classes
might be needed based on which url is requested. It maybe a good
practice to just include all the classes that might be needed. If this
is a job to hard to do you can still get lots of performance gain out of
your application by fixing the include path, using Zend Loaders Autoload
and stripping all require\_once calls from all of the Zend Framework
files.

.. categories:: none
.. tags:: none
.. comments::
.. author:: beberlei <kontakt@beberlei.de>