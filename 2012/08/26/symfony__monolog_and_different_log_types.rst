Symfony, Monolog and different log types
========================================

Symfony uses the excellent Monolog library for logging everything related
to the symfony application stack. But sometimes you need a different logger
that responds differently to the log error levels. Ideally you don't want
to reuse the application log mechanism to avoid messing with the 
fingers crossed listener of Monolog, that keeps the application log files small
in case no errors occur.

This can be easily done with Symfonys MonologBundle with a feature called
channel. Every log handler, such as file, syslog, mail or
fingers crossed is attached to the default logger called "app". This is
referenced by the dependency injection service called ``monolog.logger``.

If you want to create a different logger service that is responsible for a
different type of your application stack, just define it using the ``channels``
option:

.. code-block:: yaml

    monolog:
        handlers:
            myfile:
                type: stream
                path: %kernel.logs_dir%/myfile.log
                channels: mychannel

To actually write to ``mychannel`` you have to tag all the services that use
``mychannel`` with the following tag:

.. code-block:: xml

    <service id="my_service" class="MyService">
        <tag name="monolog.logger" channel="mychannel" />
        <argument type="service" id="logger" />
    </service>

With this approach you are now as flexible as with the default channel ``app``
regarding to logging in development, testing and production environments for
example. Once there is a channel created through the DIC tag, you can actually
fetch it from the DIC with ``monolog.logger.mychannel`` in our example.
I don't like this approach too much, because it misuses tags for modifying
arguments, where tags are actually for the services themselves. However it is
usable and works.

This feature is included starting with Symfony 2.1. It is `documented in a
cookbook entry
<http://symfony.com/doc/master/cookbook/logging/channels_handlers.html>`_,
however some insights of this blog post are still inside a pending Pull
Request.

.. author:: default
.. categories:: none
.. tags:: none
.. comments::
