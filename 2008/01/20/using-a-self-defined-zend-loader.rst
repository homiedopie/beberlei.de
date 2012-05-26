.. categories:: none
.. tags:: none
.. comments::
.. author:: beberlei <kontakt@beberlei.de>

Using a self defined Zend_Loader
================================

When you start writing with a Framework like Zend like I did in the last
weeks, you probably are still haunted by all the bad habits of pseudo
object orientated PHP design, using lots of require and include's.
Zend\_Loader doesn't seem to help at first, its just another command
(Zend\_Loader::loadClass or ::loadFile). It sucks to register lots of
autoload paths too.

I wrote my own Zend\_Loader child class. It grabs all include paths from
a config File using the Zend\_Config class, and completly frees you of
thinking about includes.

    ::

        class WWLoader extends Zend_Loader
        {
            private static $dirs = NULL;
            
            public static function loadClass($class)
            {       
                if(self::$dirs===NULL) {
                    //
                    // Include directories of this application are saved in a configuration file. If it has not been
                    // loaded before do so now and safe everything to the private static variable $dirs which will
                    // then be used in further loadings
                    //
                    $dirs = array();
                    $conf_app_path = new Zend_Config_Ini(sprintf('%s%s', constant('ZEND_CONFIG_PATH'), 'application.ini'), 'appincludepath');
                    self::extractPaths($conf_app_path->toArray(), $dirs);
                    self::$dirs = $dirs;
                }
                
                parent::loadClass($class, self::$dirs, true);
            }

            public static function autoload($class)
            {
                try {
                    self::loadClass($class);
                    return $class;
                } catch (Exception $e) {
                    return false;
                }
            }
            
            /**
             * Given an array with subkeys of include paths this function unifies this array to
             * a single one and returns the result in the second argument $dirs which is given 
             * by reference.
             *
             * @param Array $array
             * @param Array $dirs
             */
            public static function extractPaths($array, &$dirs)
            {
                foreach($array AS $k => $v) {
                    if(is_array($v)) {
                        self::extractPaths($v, $dirs);
                    } else {
                        $dirs[] = $v;
                    }
                }
            }
        }

ZEND\_CONFIG\_PATH is the only constant I use in my application. I
initialize the following at the beginning of my bootstrap file:

    ::

        define('ZEND_CONFIG_PATH', dirname(__FILE__)."/../application/config/");

        require_once 'Zend/Loader.php';
        require_once dirname(__FILE__).'/../application/include/WWLoader.php';
        Zend_Loader::registerAutoload();
        Zend_Loader::registerAutoload('WWLoader');

After that, its just Objects.
