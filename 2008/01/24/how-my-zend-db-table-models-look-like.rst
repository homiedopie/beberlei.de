.. categories:: none
.. tags:: none
.. comments::
.. author:: beberlei <kontakt@beberlei.de>

How my Zend_Db_Table models look like
=====================================

I am not too happy with the ZF Frameworks Table access solution. Not
that I have anything against the `Table Gateway
pattern <http://martinfowler.com/eaaCatalog/tableDataGateway.html>`_,
but in most web applications you almost always have to join data some
way or another. Even this rather simple application, a blog, needs joins
for displaying articles so that category, comment count and tags can be
displayed. Therefore I use an instance of Zend\_Db\_Table\_Abstract only
for the simplest purposes and pimp it by using lots of public methods
and
`Zend\_Db\_Select <http://framework.zend.com/manual/en/zend.db.select.html>`_.
An example:
    ::

        class SomeModel extends Zend_Db_Table_Abstract
        {
          $_name = "someTable";
          $_primary = "id";

          public function getSomethingByJoin($param1, $param2)
          {
             $db = $this->getAdapter();
             $select = $db->select();
             ...[build select]
             $result = $db->query($select);

             return $result;
          }
        }

That way you still follow the MVC pattern and don't have to take one
compromise after another for getting the Table Gateway to reproduce a
result that looks like a join.
