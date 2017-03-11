Generate Proxy code using a stream wrapper
==========================================

This blog-post is about an experiment and I am curios what others have to say about it. For Doctrine 2 we need to generate Proxy classes for the mapped objects to implement the Lazy Loading pattern. This is currently done with a console command or during runtime (for development). For Doctrine 2.1 we were thinking about using eval() as a third option for shared hosting or development environments. One annoyance of having to generate proxy code is that you have to regenerate it every time you change the original file. Additionally this makes deployment a little more complicated.

Today I got the idea to use stream wrappers to solve this problem. You can use stream-wrappers in combination with include/require and if you are using APC the generated php code can even be cached. That means you only have to generate the code once and after that everything is served from APCs opcode cache. Additionally by using the return values of ``stat()`` for the original file you can automatically regenerate your proxy code in APC when the original file changes.

I haven't found a good way to pass state into a stream wrapper, that is why I put the data into $GLOBALS before calling ``include()``. The client code looks like this:

.. code-block:: php
    
    <?php
    stream_wrapper_register("dc2proxy", "Doctrine\ORM\Proxy\ProxyStreamWrapper");

    $proxyDir = "dc2proxy:///proxies";
    $GLOBALS['DOCTRINE2_PSW_EM'] = $em;
    $GLOBALS['DOCTRINE2_PSW_ENTITYNAME'] = $className;
    $GLOBALS['DOCTRINE2_PSW_PROXYCLASS'] = $proxyClass;

    require $proxyDir. "/".str_replace("\\", "", $proxyClass) . ".php";

    unset($GLOBALS['DOCTRINE2_PSW_EM'], $GLOBALS['DOCTRINE2_PSW_ENTITYNAME'], $GLOBALS['DOCTRINE2_PSW_PROXYCLASS']);

Not the nicest code, but it works. I can generate PHP code and have APC cache it for me until the original code changes.
The stream wrapper to make this work looks like this:

.. code-block:: php

    <?php
    namespace Doctrine\ORM\Proxy;

    class ProxyStreamWrapper
    {
        private $proxyCode;

        function stream_open($path, $mode, $options, &$opened_path)
        {
            $this->position = 0;
            $this->proxyCode = $GLOBALS['DOCTRINE2_PSW_EM']
                    ->getProxyFactory()
                    ->getProxyClassCode($GLOBALS['DOCTRINE2_PSW_ENTITYNAME'], $GLOBALS['DOCTRINE2_PSW_PROXYCLASS']);

            return true;
        }

        public function stream_stat()
        {
            $reflClass = new \ReflectionClass($GLOBALS['DOCTRINE2_PSW_ENTITYNAME']);
            $stat = stat($reflClass->getFileName());
            $stat[0] *= -1;
            $stat["ino"] *= -1;
            return $stat;
        }

        public function url_stat()
        {
            $reflClass = new \ReflectionClass($GLOBALS['DOCTRINE2_PSW_ENTITYNAME']);
            $stat = stat($reflClass->getFileName());
            $stat[0] *= -1;
            $stat["ino"] *= -1;
            return $stat;
        }

        function stream_read($count)
        {
            $ret = substr($this->proxyCode, $this->position, $count);
            $this->position += strlen($ret);
            return $ret;
        }

        function stream_write($data)
        {
            $left = substr($this->proxyCode, 0, $this->position);
            $right = substr($this->proxyCode, $this->position + strlen($data));
            $this->proxyCode = $left . $data . $right;
            $this->position += strlen($data);
            return strlen($data);
        }

        function stream_tell()
        {
            return $this->position;
        }

        function stream_eof()
        {
            return $this->position >= strlen($this->proxyCode);
        }

        function stream_seek($offset, $whence)
        {
            switch ($whence) {
                case SEEK_SET:
                    if ($offset < strlen($this->proxyCode) && $offset >= 0) {
                         $this->position = $offset;
                         return true;
                    } else {
                         return false;
                    }
                    break;

                case SEEK_CUR:
                    if ($offset >= 0) {
                         $this->position += $offset;
                         return true;
                    } else {
                         return false;
                    }
                    break;

                case SEEK_END:
                    if (strlen($this->proxyCode) + $offset >= 0) {
                         $this->position = strlen($this->proxyCode) + $offset;
                         return true;
                    } else {
                         return false;
                    }
                    break;

                default:
                    return false;
            }
        }
    }

What do you think about this approach? Are there any potential problems I am not seeing?

.. categories:: none
.. tags:: PHPMagic
.. comments::
