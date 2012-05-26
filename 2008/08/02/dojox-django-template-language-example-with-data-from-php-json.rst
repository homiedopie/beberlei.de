DojoX Django Template Language Example with Data from PHP/JSON
==============================================================

This is a simple example how you would use DojoX Django Template
Language component filled with data from a JSON GET Response:

    ::

        <script type="text/javascript" src="/development/dojo-release-1.1.1/dojo/dojo.js" djConfig="parseOnLoad:true, isDebug:true"></script>

        <script language="javascript" type="text/javascript"><!--
        dojo.require("dojox.dtl");
        dojo.require("dojox.dtl.Context");
        dojo.require("dojox.dtl.ext-dojo.NodeList");
        dojo.addOnLoad(
            dojo.xhrGet({url: "dojotest.php", handleAs: "json", handle: function(data,ioArgs){
                if(typeof data == "error"){
                    console.log("error?",data);
                } else {
                    dojo.query("#test").dtl("I am eating {{food.fruit}} and {{food.meat}}", data);
                }
            }
        }));
        --></script>

        ::

            <?php
            header('Content-type: text/json');
            $food = array('food' => array('fruit' => 'apple', 'meat' => 'chicken'));
            echo json_encode($food);
            ?>


.. categories:: none
.. tags:: none
.. comments::
.. author:: beberlei <kontakt@beberlei.de>