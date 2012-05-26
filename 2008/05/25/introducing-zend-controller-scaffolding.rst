.. categories:: none
.. tags:: none
.. comments::
.. author:: beberlei <kontakt@beberlei.de>

Introducing: Zend Controller Scaffolding
========================================

In the last couple of weeks I `came across the
idea <http://codecaine.co.za/posts/form-generation-with-zend-form-part-2/>`_
of building a little component for scaffolding in Zend Framework. After
playing around with this idea a little I came up with an
Zend\_Controller\_Scaffolding object, which extends the
Zend\_Controller\_Action object.

It takes any Zend\_Db\_Table\_Abstract object and generates create and
update forms using Zend\_Form and displays them in the Controller. The
component is very easy to use, as this example shows:

    ::

        class SomeController extends WW_Controller_Scaffolding {
            public function init() {
                $this->setScaffolding(new ZendDbTableModel(), $options);
            }
        }

You now have access to the following actions of the controller:
some/create some/edit some/delete and some/index (some/list). They
handle all your model editing dreams.

All you have to own is the WW\_Controller\_Scaffolding Library Class and
a folder of scaffolding view templates both of which are `bundled in an
archive you can
download <http://www.beberlei.de/sources/zend_controller_scaffolding-0.5.5.tar.gz>`_.

**Download**

-  `Download Version
   0.5.5 <http://www.beberlei.de/sources/zend_controller_scaffolding-0.5.5.tar.gz>`_

**Changes**

-  0.5.5: Put Component into own Namespace (WW = Whitewashing). Make it
   possible to hide fields in the list via the options. Allow to specify
   scaffolding view scripts folder via options.

**Install & Usage**

    ::

        Untar the two folders include/ and views/ into your
        Zend Framework project application directory.

        Make sure the include folder is in your Zend_Loader
        include path or move the Scaffolding.php so that it
        is placed in your library include path.

        Define each Controller that should be a Scaffolding Interface
        as:

        class SomeController extends WW_Controller_Scaffolding {
            public function init() {
                $this->setScaffolding(new ZendDbTableModel(), $options);
            }
        }

        Where $options is an array or Zend_Config object with any of the following keys:

          'allow_edit_primary_key' True/false - Wheater the form allows you to set the
                                  Primary Key fields or not

         'field_names' an Array of the Database Tables field names mapped to Label Names

         'hide_list_fields' Array of database table field names that should not be displayed in the list overview.

         'checkbox' an Array of Database Table field names that should be represented
                    as Checkbox. Useful for TINYINT(1) fields that represent boolean decisions.

         'view_folder' Sometimes you want to use different views for scaffolding in one project. Use
                       this variable and copy the scaffolding folder for each component you want to
                       change the view basics for.

**Todos & Problems:**

-  Many To Many Relationsships are not implemented yet (Using
   MultiSelec).
-  Compound Keys are probably not working correctly
-  Relationsships on non-primary key fields probably don't work as
   expected
-  Relationsships with lots of data are not scaled down for easy
   administration.

Please report any bugs and feature requests or recommodations to
**kontakt at beberlei dot de**.
