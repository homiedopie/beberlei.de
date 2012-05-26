.. categories:: none
.. tags:: none
.. comments::
.. author:: beberlei <kontakt@beberlei.de>

My 2 cents on Zend_Search_Lucene Update Problems
================================================

`Zend\_Search\_Lucene <http://framework.zend.com>`_ (or Lucene in
general) does not support an update statement, therefore we must check
via find() if a specific article that should be updated already exists.

Numerous solutions exist for this problem (`for example this PDF
Tutorial by a Zend
Programmer <http://devzone.zend.com/content/zendcon_07_slides/Evron_Shahar_Indexing_With_Zend_Search_Lucene-ZendCon07.pdf>`_).
Mine looks as follows. The first thing is to Set an Analyzer other from
the default one. The Default Analyzer only looks at letters, not at
numbers.

    ::

        Zend_Search_Lucene_Analysis_Analyzer::setDefault(new
            Zend_Search_Lucene_Analysis_Analyzer_Common_Utf8Num_CaseInsensitive()
        );
        $index = Zend_Search_Lucene::open('/path/to/index/directory');

We can now save an identifier containing letters and numbers, for
example the md5 string of the Article Database ID.

    ::

        $doc = new Zend_Search_Lucene_Document();
        $field = Zend_Search_Lucene_Field::Keyword('id', md5($data['id']));
        $doc->addField($field);
        $index->addDocument($doc);

Before updating an entry you have to delete any entry that has been
indexed before:

    ::

        $hits = $index->find('id:'.md5($articleID));
        foreach($hits AS $hit) {
            $index->delete($hit->id);
        }

The `Tutorial Talk on Search
Lucene <http://devzone.zend.com/content/zendcon_07_slides/Evron_Shahar_Indexing_With_Zend_Search_Lucene-ZendCon07.pdf>`_
(given abote) uses an extended version of this delete routine snippet
that also checks if an article is up to date and does not have to be
reindexed and deletes multiple entries of one article.
