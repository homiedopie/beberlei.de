

Take for example Doctrine, which was managed in a single Git repository until
the late 2.0 Beta, then split into Common, DBAL and ORM and later split into
even smaller packages by splitting Common. This was only possible because
Composer exists.

However in my opinion since the splits the visibility of Pull Requests and
problems in smaller components has suffered a lot. Each Common subproject now
has its own versioning numbers, confusing even seasoned contributors on which
versions are compatible with each other. 

Symfony2 and ZendFramework2 have rejected this split into smaller packages.
Both frameworks have a lot of independent and reusable components, but are
still managed from one central repository. Technical tools are used to make
each component usable on its own from Composer/Packagist. Given my experience
from Doctrine I am glad they didn't.
