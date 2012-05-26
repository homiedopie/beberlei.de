
Zend + jQuery Enhancements: Ajax Forms, Tooltip and Autofill
============================================================

Some weeks ago `Zend Framework 1.7 <http://framework.zend.com>`_ was
released with the `jQuery <http://jquery.com>`_ support I contributed.
What is the essential advantage of using jQuery support in ZF? You can
develop forms with ajax support either by using View Helpers or directly
by the integrated Zend\_Form support. The implementation of a DatePicker
or AutoComplete functionality becomes as easy as using 2-3 lines of php
code.

Currently only support for the jQuery UI library is shipped, but you can
easily extend the jQuery support on your own and this blog post will
show you how using three very popular jQuery plugins:
`AjaxForm <http://malsup.com/jquery/form/>`_,
`Tooltip <http://bassistance.de/jquery-plugins/jquery-plugin-tooltip/>`_
and `AutoFill <http://plugins.jquery.com/project/Autofill>`_. This will
be a series of installments, beginning with the first one: AjaxForms

AjaxForm allows you to enhance any form of yours to submit the data with
ajax to the server, so no additional overhead of loading a new page is
necessary. Combining the power of Zend\_Form and jQuery's ajaxForm you
can even go so far as differentiating between successful and
non-validated form submits. We will build a Form Decorator that
integrates the AjaxForm plugin in any of your Zend\_Form's. On submit it
will send the form data to the server via ajax and clears the form
afterwards. Clients that have javascript disabled will work too, the
form is submitted to the server in a standard pre-ajax fashion and
processed that way.

First what we need is obviously the new decorator, we will call it
"My\_JQuery\_Form\_Decorator\_AjaxForm" and it will inherit from
Zend\_Form\_Decorator\_Form. What we then realize is, that this is just
using a view helper to render, so what we need additionally is a
"My\_JQuery\_View\_Helper\_AjaxForm" that extends from
"Zend\_View\_Helper\_Form". The code of the view helper will have to
look as follows to fullfil our needs:

    ::

        require_once "Zend/View/Helper/Form.php";class ZendX_JQuery_View_Helper_AjaxForm extends Zend_View_Helper_Form{  /**   * Contains reference to the jQuery view helper   *   * @var ZendX_JQuery_View_Helper_JQuery_Container   */  protected $jquery;  /**   * Set view and enable jQuery Core and UI libraries   *   * @param Zend_View_Interface $view   * @return ZendX_JQuery_View_Helper_Widget   */  public function setView(Zend_View_Interface $view)  {    parent::setView($view);    $this->jquery = $this->view->jQuery();    $this->jquery->enable()           ->uiEnable();    return $this;  }  public function ajaxForm($name, $attribs = null, $content = false, array $options=array())  {    $id = $name;    if(isset($attribs['id'])) {      $id = $attribs['id'];    }    if(!isset($options['clearForm'])) {      $options['clearForm'] = true;    }    if(count($options) > 0) {      require_once "Zend/Json.php";      $jsonOptions = Zend_Json::encode($options);      // Fix Callbacks if present      if(isset($options['beforeSubmit'])) {        $jsonOptions = str_replace('"beforeSubmit":"'.$options['beforeSubmit'].'"', '"beforeSubmit":'.$options['beforeSubmit'], $jsonOptions);      }      if(isset($options['success'])) {        $jsonOptions = str_replace('"success":"'.$options['success'].'"', '"success":'.$options['success'], $jsonOptions);      }    } else {      $jsonOptions = "{}";    }    $this->jquery->addOnLoad(sprintf(      '$("#%s").ajaxForm(%s)', $id, $jsonOptions    ));    return parent::form($name, $attribs, $content);  }}

It takes all the form-tag building of the inherited view helper for
granted and just appends the necessary jQuery code to the jQuery
onLoadActions stack. They will be outputted to the clients browser when
calling <?php $this->jQuery(); ?> in your layout or view script. Make
sure that you include the jQuery Form plugin in your code, for example
with <?php $view->jQuery()->addJavascriptFile(..); >

Programming the decorator becomes a simple trick now:

    ::

        require_once "Zend/Form/Decorator/Form.php";class My_JQuery_Form_Decorator_AjaxForm extends Zend_Form_Decorator_Form{  protected $_helper = "ajaxForm";  protected $_jQueryParams = array();  public function getOptions()  {    $options = parent::getOptions();    if(isset($options['jQueryParams'])) {      $this->_jQueryParams = $options['jQueryParams'];      unset($options['jQueryParams']);      unset($this->_options['jQueryParams']);    }    return $options;  }  /**   * Render a form   *   * Replaces $content entirely from currently set element.   *   * @param string $content   * @return string   */  public function render($content)  {    $form  = $this->getElement();    $view  = $form->getView();    if (null === $view) {      return $content;    }    $helper    = $this->getHelper();    $attribs    = $this->getOptions();    $name     = $form->getFullyQualifiedName();    $attribs['id'] = $form->getId();    return $view->$helper($name, $attribs, $content, $this->_jQueryParams);  }}

Now to use either the decorator for your form, or just the view helper
to print your form tag with jQuery code you can invoke:

    ::

        $form->addPrefixPath('My_JQuery_Form_Decorator', 'My/JQuery/Form/Decorator', 'decorator');$form->removeDecorator('Form')->addDecorator(array('AjaxForm', array(  'jQueryParams' => array(),)));$view->addHelperPath("My/JQuery/View/Helper", "My_JQuery_View_Helper");$view->ajaxForm("formId1", $attribs, $content, $options);

Now we finished up the view side of our script. Assuming that we use the
Form Decorator instead of the View Helper, we can additionally add some
fancy logic and error handling ajax fun to the action controller that is
handling the Zend\_Form instance.

    ::

        class IndexController extends Zend_Controller_Action{  public function indexAction()  {    $foo = new MyAjaxTestForm();    try {      if(!$foo->isValid($_POST)) {        throw new Exception("Form is not valid!");      } else {        // do much saving and stuff here        if($this->getRequest()->isXmlHttpRequest()) {          $this->_helper->json(array("success" => "SUCCESSMESSAGEHERE"));        }      }    } catch(Exception $e) {      if($this->getRequest()->isXmlHttpRequest()) {        $jsonErrors = array();        foreach( ( new RecursiveIteratorIterator(new RecursiveArrayIterator($form->getMessages())) ) AS $error) {          $jsonErrors[] = $error;        }        $this->_helper->json->sendJson($jsonErrors);      }    }  }}

This has to be processed by a callback function of the AjaxForm and
which may for example look like the following which uses a predefined
div box (#formMessages, dont forget to implement it) to render either
the success or the error messages.

    ::

        $form->addDecorator(array('AjaxForm', array(  'jQueryParams' => array(    'success' => "formCallback1",   ),)));$view->jQuery()->addJavascript('function formCallback1(data) {  if(data.errors) {    $("#formMessages").append("<ul>");    for each(var item in data.errors) {      $("#formMessages").append("<li>"+item+"</li>");    }    $("#formMessages").append("</ul>");  } else {    $("#formMessages").html(data.success);  }}');

This seems very complex, but you could include that javascript code into
the AjaxForm decorator and implement an Action Helper to do the action
controller side of the stuff. This will be an exercise for a future
post.

AutoFill and Tooltip extensions will be topic of the next installments
of this series, so be aware of new content soonish.

.. categories:: none
.. tags:: none
.. comments::
.. author:: beberlei <kontakt@beberlei.de>