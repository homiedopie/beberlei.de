Explicit Code requires no comments - Only bad code does
=======================================================

Following the recent discussion on commenting source code by `Brandon
Savage <http://www.brandonsavage.net/on-code-commenting-and-technical-debt/>`_
and `Marco
Tabini <http://mtabini.blogspot.com/2009/04/myth-of-myth-of-self-commenting-code.html>`_,
I wanted to add upon Marcos code example to show that it not even needs
any inline comments and can be greatly enhanced in readability with
taking 2-5 minutes of time and refactoring the code. The original code
sample was:

    ::

        function __construct(array $pathInfo) {
            $section = $pathInfo[0];
            $file = $pathInfo[1];

            // Assume that the location of this file is inside the main trunk, and that pathInfo has already been filtered.

            $path = dirname(__FILE__) . '/../../' . $section . '/xml/static/' . $file . '.xml';

            if (!file_exists($path)) {
                Controller::singleton()->doError(404);
            }

            parent::__construct('main/xsl/template.xsl', $path);
        }

This sample is somehow related to the response and view rendering of an
application and its pretty understandable. For me there are some squirks
though that would make me have to scroll to other classes to see how
they interact. For example the path information falls from heaven. Why
is it an array of 2 values and are these sections set the same all the
time? And what exactly happens when the front controller does the 404
error? Is there a die() or exit in the **doError()**

The Agile movement postulates the phase of refactoring for a finished
piece of code. Rebuilding the hacked solutions that did it to make them
more understandable. I applied this to Marcos code snippet. The
refactoring produces about double the code, but its done entirely by
using NetBeans nice Rename variable and copy paste on extracting
methods, which takes not more than 5 minutes.

    ::

        class StaticXmlXsltRendererImpl extends AbstractXsltView
        {
            function render(array $filteredPathInfo) {
                $templateValuesXmlPath = $this->getTemplateValuesXmlFile($filteredPathInfo);

                if(!$this->templateExists($templateValuesXmlPath)) {
                    Controller::singleton()->doError(404);
                } else {
                    parent::render('main/xsl/template.xsl', $templateValuesXmlPath);
                }
            }

            private function getTemplateValuesXmlFile($filteredPathInfo) {
                $section = $this->getSection($filteredPathInfo);
                $file = $this->getFile($filteredPathInfo);

                // Assume that the location of this file is inside the main trunk
                return dirname(__FILE__) . '/../../' . $section . '/xml/static/' . $file . '.xml';
            }


            private function getSection($pathInfo) {
                return $pathInfo[0];
            }

            private function getFile($pathInfo) {
                return $pathInfo[1];
            }

            private function templateExists($path) {
                return file_exists($path);
            }
        }

In this code snippet the class name, variable names and methods clearly
communicate what is done, which wasn't the case in the previous example.
The only change for the clients is the change of using the constructor
to using the **render()** method, which communicates the intend more.
Also the render method now clearly communicates that either the error or
the parent rendering is executed and leaves no doubt about it.

The **getTemplateValuesXmlFile()** method still uses the comment to show
the assumption about relative paths, but this is only the case because
application configuration is made implicit into the code. This has to be
extracted to be an explicit configuration constant and the comment can
go.

    ::

            private function getTemplateValuesXmlFile($filteredPathInfo) {
                $section = $this->getSection($filteredPathInfo);
                $file = $this->getFile($filteredPathInfo);

                return APPLICATION_ROOT . '/' . $section . '/xml/static/' . $file . '.xml';
            }

    In my opinion commenting code is necessary only for non-refactored
    code that has been hacked into existence and is hard to understand.
    Either the programmer has to get it done and has no chance to
    clearly communicate the intend. Or what is even worse the to be
    changed legacy code is hard to understand but you can't take the
    chances to refactor it because its also already in production and
    has no tests. Now from the second point it is obvious that upon ugly
    code you put only more and more ugly code to fix the problems. This
    is what leads to the legacy maintenance problems that pretty much
    every programmer faces. And then commenting comes into play: You
    have to add a new feature X and it has to be done fast. You don't
    really understand the code or how it works together but you know you
    can put the new code for the feature into existence but its really
    unintuitive. So you begin to comment it excessively, because its the
    only way to clearly show its intend.

    There are two mindestting factors that help to write code that is
    understandable without having to excessively comment it:

    -  From the beginning, do not write code for the computer but for
       developers. Changing this attitude really helps to write
       understandable code like the one above.
    -  Only leave code better than it was before, never worse.

    There are five technical practices that - when followed - allow to
    write clearly communicating code from the beginning:

    #. Giving classes, variables and methods good names. This is a
       no-brainer but few people seem to follow it anyways.
    #. Following the object-oriented **Single Responsibility Principle**
       by never giving a class more than one responsibility. Macros
       example seems to follow this one.
    #. Methods should never switch in the level of detail. Micro-work at
       the datastructure level should never be mixed with macro level
       delegation to executing large chunks of code. Macros code
       violates this by mixing the path building micro-level work with
       the macro-level work of rendering the XSLT template. The path
       building code can be hidden behind a method to communicate intend
       more clearly.
    #. Exchange if conditions with private methods that explain the
       condition being checked for. In Marcos example this is not really
       necessary, because file\_exists already is quite a good
       description to the condition. But in cases of logical
       combinations of conditions the method extracting is a superior
       way to explain the conditions intend without having to write a
       comment.
    #. **Seperate Query and Command**: A method never should do a query
       which returns the state of an object and a command which executes
       a set of rules on the state.

    These practices sum up to one guideline: Make code explicit. This
    obviously requires less commenting since a comment of explicit code
    would be duplication and duplication is bad. What if you have a
    project that does not follow this guidelines? Then of course
    comments should be used to explain code, but in the long run this
    should be refactored to self-explaining code. Additionally every new
    feature should be programmed explicitly to follow the "leave code
    better than before" principle.

    In my opinion two refactoring tools are missing that would greatly
    help PHP programmers write nice to read code: Extract method and
    Replace magic value with constant. Can someone integrate them into
    NetBeans please?

    **Update:** Fixed a creepy copy-paste code bug, thanks to azeroth
    for pointing out. Moved methods around a bit to be more reading
    friendly.

.. categories:: none
.. tags:: none
.. comments::
.. author:: beberlei <kontakt@beberlei.de>