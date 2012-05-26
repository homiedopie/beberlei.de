:author: beberlei <kontakt@beberlei.de>
:date: 2009-02-13

Update on Unittest and Metrics Tool
===================================

Some days ago i posted about the `PHP Unittest and Metrics
Aggregator <http://github.com/beberlei/puma/tree/master>`_ tool that i
have written on (and which I have dubbed PUMA). Discussing it with
people I came to the conclusion that the approach using
`ezcMvcTools <http://ezcomponents.org>`_ is quite problematic that it
forces to use this application, although the reporting and the
application are quite separate. This is not against ezcMvcTools: I love
it, its just the wrong type of support.

I began to split up the aggregator into some sort of importing-exporting
tool. You can specify library-, test- and output-directory of your
application and it will use the tools at hand
(`PHPUnit <http://www.phpunit.de>`_, `PDepend <http://www.pdepend.org>`_
and CodeSniffer currently) to generate their XML formatted reports. It
then parses those XML outputted files and combines their result to give
a consistent view on your application.

The Import-To-Output generator uses a three-step approach. An importer
emits signals to report observers, which will then hand over their
collected data to specific html pages that are then generated to the
disc. This is a very flexible approach that allows anyone to extend and
re-use the tool to generate project metrics, unittest overview and other
interesting details on your application.

`Have a look at the tool on
Github <http://github.com/beberlei/puma/tree/master>`_ and play with it.
I would really like to hear your thoughts.
