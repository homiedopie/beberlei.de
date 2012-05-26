:author: beberlei <kontakt@beberlei.de>
:date: 2010-05-02

Testing Database Locks with PHPUnit and Gearman
===============================================

For the Beta 2 release of `Doctrine
2 <http://www.doctrine-project.org>`_ we plan to integrate pessimistic
Database-level locks across all the supported vendors (MySQL, Oracle,
PostgreSql, IBM DB2 so far). This means row-level locking as defined in
the ANSI SQL Standard using "SELECT .. FOR UPDATE" will be available
optionally in DQL Queries and Finder methods. The Implementation of this
extension to SELECT statements is rather trivial, however functional
testing of this feature is not.

A general approach would look like this:

#. Run Query 1 and 2 with FOR UPDATE into the background
#. Have both queries lock the row for a specified time x (using sleep)
#. Verify that one of the two processes/threads runs approximately 2\*x
   the lock time.

Since PHP does not support process forking or threads naturally you run
into a serious problem. How do you execute two database queries in
parallel and verify that indeed one query is locking read access for the
second one?

Side note: There are some drawbacks to this testing approach. It could
be that one background threads finishes the lock sleep already when the
second just starts. The locking would work in these cases, however the
lock time would not nearly be 2\*x seconds, producing a test-failure. We
are talking about a functional test though and I will accept a failure
from time to time just to be 99% sure that locking works.

Solving this problem with Gearman provides a pretty nice "real-world"
example for the Job-Server that I wanted to share. This blog post
contains a stripped down code-example from the Doctrine 2 testsuite. If
you are interested, you can see the complete Gearman Locking Tests in
`on
GitHub <http://github.com/beberlei/doctrine2/tree/lock-support/tests/Doctrine/Tests/ORM/Functional/Locking/>`_.

Gearman allows to register worker processes with the job-server and
offers clients to execute jobs on those workers in parallel. After
installing the Gearman job-server and PHP pecl/gearman extension
(`Rasmus Lerdorf has a post on
installation <http://toys.lerdorf.com/archives/51-Playing-with-Gearman.html>`_)
we can go on writing our locking tests with Gearman.

The first bit is the worker, a PHP script that tries to acquire a
database lock and then sleeps for a second. The return value of this
script is the total time required for acquiring the lock and sleeping.

.. code-block:: php

        class LockAgentWorker
        {
            public function findWithLock($job)
            {
                $fixture = $this->processWorkload($job); // setup doctrine in here

                $s = microtime(true);
                $this->em->beginTransaction();

                $entity = $this->em->find($fixture['entityName'], $fixture['entityId'], $fixture['lockMode']);

                sleep(1);
                $this->em->rollback(); // clean up doctrine

                return (microtime(true) - $s);
            }
        }

The glue-code for the worker script contains of the registering of the
worker method with the job-server and a simple infinite loop:

.. code-block:: php

        $lockAgent = new LockAgentWorker();

        $worker = new \GearmanWorker();
        $worker->addServer();
        $worker->addFunction("findWithLock", array($lockAgent, "findWithLock"));

        while($worker->work()) {
            if ($worker->returnCode() != GEARMAN_SUCCESS) {
                break;
            }
        }

We need two running workers for this to work, since one worker only
processes one task at a time. Just open up two terminals and launch the
php scripts. They will wait for their first task to process.

Now we need to write our PHPUnit TestCase, which will contain a
GearmanClient to execute two of the "findWithLock" in parallel. Our
locking assertion will work like this:

#. Register two tasks for the "findWithLock" method that access the same
   database row.
#. Register a completed callback using
   "GearmanClient::setCompleteCallback()" that collects the run-time of
   the individual workers.
#. Execute this tasks in parallel using "GearmanClient::runTasks()".
#. Assert that the maximum run-time is around 2 seconds (since each
   worker sleeps 1 second)

The code for this steps could look like:

.. code-block:: php

        class GearmanLockTest extends \Doctrine\Tests\OrmFunctionalTestCase
        {
            private $gearman = null;
            private $maxRunTime = 0;
            private $articleId;

            public function testLockIsAquired()
            {
                // .. write fixture data into the database

                $gearman = new \GearmanClient();
                $gearman->addServer();
                $gearman->setCompleteCallback(array($this, "gearmanTaskCompleted"));

                $workload = array(); // necessary workload data to configure workers
                $gearman->addTask("findWithLock", serialize($workload));
                $gearman->addTask("findWithLock", serialize($workload));

                $gearman->runTasks();

                $this->assertTrue($this->maxRunTime >= 2);
            }

            public function gearmanTaskCompleted($task)
            {
                $this->maxRunTime = max($this->maxRunTime, $task->data());
            }
        }

Now if both workers are waiting for processing the task we can run this
test and get a green bar for a working lock support.
