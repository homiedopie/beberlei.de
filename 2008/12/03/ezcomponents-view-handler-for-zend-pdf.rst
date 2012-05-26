
ezComponents View Handler for Zend_Pdf
======================================

`My previous posting <http://www.whitewashing.de/blog/article/93>`_
discussed different view handlers based on routing information. One
example was the PDF View which was implemented rather hackish through
overwriting the **createResponseBody()** function of **ezcMvcView**.
`Derick <http://www.derickrethans.nl/>`_ told me the way to go would be
writing my own PDF view handler. Since this is a rather lengthy topic I
created this new post that only discusses using
`Zend\_Pdf <http://framework.zend.com/manual/en/zend.pdf.html>`_ as a
View Handler in the new `ezComponents
MvcTools <http://www.ezcomponents.org>`_.

The code for the View Handler would look like the following:

    ::

        abstract class myPdfViewHandler implements ezcMvcViewHandler
        {
            /**
             * Contains the zone name
             *
             * @var string
             */
            protected $zoneName;

            /**
             * Contains the variables that will be available in the template.
             *
             * @var array(mixed)
             */
            protected $variables = array();

            /**
             * Pdf object to be rendered.
             *
             * @var Zend_Pdf
             */
            protected $pdf;

            /**
             * Creates a new view handler, where $zoneName is the name of the block and
             * $templateLocation the location of a view template.
             *
             * @var string $zoneName
             * @var string $templateLocation
             */
            public function __construct( $zoneName, $templateLocation = null )
            {
                $this->zoneName = $zoneName;
            }

            /**
             * Adds a variable to the template, which can then be used for rendering
             * the view.
             *
             * @param string $name
             * @param mixed $value
             */
            public function send( $name, $value )
            {
                $this->variables[$name] = $value;
            }

            /**
             * Processes the template with the variables added by the send() method.
             * The result of this action should be retrievable through the getResult() method.
             */
            public function process( $last )
            {
                // template method
            }

            /**
             * Returns the value of the property $name.
             *
             * @throws ezcBasePropertyNotFoundException if the property does not exist.
             * @param string $name
             * @ignore
             */
            public function __get( $name )
            {
                return $this->variables[$name];
            }

            /**
             * Returns true if the property $name is set, otherwise false.
             *
             * @param string $name
             * @return bool
             * @ignore
             */
            public function __isset( $name )
            {
                return array_key_exists( $name, $this->variables );
            }

            /**
             * Returns the name of the template, as set in the constructor.
             *
             * @return string
             */
            public function getName()
            {
                return $this->zoneName;
            }

            /**
             * Returns the result of the process() method.
             *
             * @return mixed
             */
            public function getResult()
            {
                if($this->pdf instanceof Zend_Pdf) {
                    return $this->pdf->render();
                } else {
                    throw new Exception("Could not render PDF.");
                }
            }
        }

Now you would implement a concrete PDF view handler by extending
myPdfViewHandler.

    ::

        class myConcretePdfViewHandler extends myPdfViewHandler {
            public function process( $last ) 
            {
                $pdf = new Zend_Pdf();
                // do concrete PDF drawing stuff here

                // save PDF here, will be rendered in getResult()
                $this->pdf = $pdf;
            }
        }

And your **ezcMvcView** implementation will make of **createZones()**
and look like the following:

    ::

        class myPdfView extends ezcMvcView {
            function createZones( $layout )
            {
                $zones = array(); 
                // A decision which concrete Pdf Handler should be used would be decided on here.
                $zones[] = new myConcretePdfViewHandler( 'concreteA' );
                return $zones;
            }
        }

There you go!

.. categories:: none
.. tags:: none
.. comments::
.. author:: beberlei <kontakt@beberlei.de>