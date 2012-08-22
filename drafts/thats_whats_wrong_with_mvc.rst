This is whats wrong with MVC
============================

`MVC is dead, MOVE on <http://cirw.in/blog/time-to-move-on>`_ raved on Hackernews today.
Its a very short blog post that proposes an improvement of the MVC pattern. His
reasons:

    I'm certainly not the first person to notice this, but the problem with MVC as
    given is that you end up stuffing too much code into your controllers, because
    you don't know where else to put it.

I did notice this and there is a simple way to show what is wrong with MVC
in web-applications. Its the tangling of business logic to controller methods,
such as form-handling, redirection, session/flash handling, routing.

Any medium sized controller action easily ends up having multiple "exit" points
with completly different semantic meaning: A form request for example can lead to 
redirects or re-displaying of the form with errors.

And its not easy to decouple your business logic from this necessary controller
code.

See this PHP and Symfony2 example:

    public function editAction(User $user, Request $request)
    {
        $form = $this->createType(new UserType(), $user);

        if ($request->getMethod() === 'POST') {
            $form->bindRequest($request);

            if ($form->isValid()) {
                $this->get('doctrine.orm.default_entity_manager')->flush();

                $this->get('session')->setFlash('notice', 'User was successfully updated');

                return $this->redirect($this->generateUrl('show_user', array(
                    'id' => $user->getId()
                )));
            }
        }

        return array('user' => $user, 'form' => $form);
    }

And the similar code in Ruby on Rails:

    class UserController < ApplicationController
      def edit
        @user = User.find(params[:id])
           
        if request.isPost?
          if @user.update_attributes(params[:user])
            @user.save()
            redirect_to(@user, :notice => 'User was successfully updated.') 
          end
        end
      end
    end

These code blocks are sufficently simple, but once you add logic to the validation
failed or passed parts, you start mixing business logic and controller. Ask yourself
the quetion. Can I "easily" re-use that code in a non-web context? You can't.

Every line in the two examples are glue code around your model. And there are too
many variants of them to build reusable code-blocks that allow seperation of model
and controller.

And for framework authors its simple to stop at this point in the documentation. You
are regularly told to seperate model and controller.

That coupling of model and controller is wrong with MVC in web applications. Trying
a simple abstraction of both through a service layer makes your apps much more complicated
though and kills the RAD. In my experience, only a well-thought translation layer between both can
help you keep the RAD necessary for web-development and seperate model from controllers.
The MOVE pattern is one good way, but there is also Entity-Boundary-Interactor or
Data-Context-Interaction.

.. author:: default
.. categories:: none
.. tags:: none
.. comments::
