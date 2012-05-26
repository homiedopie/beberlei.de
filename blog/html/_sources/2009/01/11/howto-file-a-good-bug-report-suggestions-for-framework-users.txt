Howto file a good bug report: Suggestions for framework users
=============================================================

I have fixed quite a number of bugs for the ZF lately, which lead me to
this post about how to file a good bug report. There are many annoying
bug reports out there, where the reporter of the bug withholds important
information to the bugfixer unintended. This advice applies bug reports
in general of course.

What are the benefits of a good bug report? The bug generally gets fixed
faster, when the developer has more information at hand. Additionally
other developers might come to rescue since they can understand the
issue faster. These benefits are good for both parties. If you take no
time for a good bug report, your issue might risk to end up getting old
or closed unfixed.

-  **Post the whole Exception Stack Trace**: If the library throws an
   Exception into your application that is unexpected and may indicate
   an bug: Do not post the Message or Exception name only. The exception
   may be thrown in many different places or due to different reasons.
   The PHP exception class offers the method **getTraceAsString()**,
   which offers many information to the developer what the cause of the
   exception might be. Please use it!
-  **Post codefixes in a patch format**: When you find a bug in the
   framework, it is quite possible that you can offer a fix directly.
   Writing "Replace x in line y with z" does not help very often. The
   component might be in flux and the line positions change more often
   than you think. Please create a diff file of this changes that
   indicate the precise position of the change. This diff also includes
   2 lines above and below the patched code for direction of the
   developer. SVN Diffs are even more useful since they include the
   revision where you fixed the bug in.
-  **Post reproducible cases as PHPUnit Test**: If you find a bug and
   can show how to reproduce it: Write a unittest to prove it. It is ZF
   policy to create a unittest for each bugfix showing that the bug was
   indeed fixed and previous functionality remains the same, so this
   unit-test has to be written anyways. Many show-offs rely on massive
   **echo** statements or **var\_dump**, which render them almost
   useless for the developer.
-  **Attach a unit-test to a submitted patch**: This is related to the
   previous point. If you add a unit test your patch will get more
   attention. It will prove that you have thought about the patch, its
   consequences and that you might have checked it does not break
   backwards compatibility. This is worth a lot.
-  **Run the test suite with your patch**: If you want to provide a
   patch. Run the testsuite of the Zend Framework. It might break
   expected behaviour. When you post a patch that will break BC, it will
   be recognized. Your bug report might be closed, which helps nobody.

When you find a bug you have probably thought about it and how to fix
it. This is valuable information. Disregarding one of this points will
lead to missing information on part of the developer that he has to
"learn" again. This takes time, which may make your bug last longer than
it should.

.. categories:: none
.. tags:: none
.. comments::
.. author:: beberlei <kontakt@beberlei.de>