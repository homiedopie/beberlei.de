Integrate Symfony and Webpack
=============================

Asset Management in Symfony2 is handled with the PHP based library Assetic by
default, however I have never really connected to this library and at least for
me it usually wastes more time than it saves.

I am also not a big fan of the Node.JS based stack, because it tends to fail
alot for me as well. With teams that primarily consist of PHP developers and
web-designers the transition to use Node.JS tools should be very conservative
in my opinion. Each team member should not feel overburdend by this new
technology stack.

Frontend development is really not my strong suit, so these first steps
I document here may seem obvious to some readers.

While researching about `React.JS <https://github.com/facebook/react>`_ I came across 
a tool called `Webpack <http://webpack.github.io/>`_ which you could compare
to Symfony's Assetic. It is primarily focussing on bundling Javascript modules,
but you can also ship CSS assets with it.

The real benefits for Webpack however are:

1. the builtin support for AMD or CommonJS style module loaders
2. a builtin development web-server that runs on a dedicated port, serving your
   combined assets.
3. a hot reloading plugin that automatically refreshes either the full page or
   just selected code when the assets change.
4. module loaders that allow instant translation of JSX or other languages
   with Javascript transpilers (CoffeeScript, ...)

Let's have a look at a simple example javascript application in ``app.js``
requiring jQuery. The code is part of the Symfony2 document root in ``web/``:

::

    web/
       css/
         page.css
       js/
         vendor/
           jquery.js
         app.js

Then we can use `AMD-style <https://github.com/webpack/docs/wiki/amd>`_ modules
to resolve the dependencies in our code:

.. code-block:: js

    // app.js
    define(['./vendor/jquery.js'], function($) {
        $(document).ready(function() {
            $("#content").html("Webpack Hello World!");
        });
    });

You can compare this to PHPs ``require()`` and autoloading functionality,
something that Javascript has historically been lacking and usually leads to
javascript files with many thousands lines of code. You can also use
`CommonJS-style <https://github.com/webpack/docs/wiki/commonjs>`_ module loading
if your prefer this approach.

The downside of adding this functionality is that your code **always** has to
run through Webpack to work on the browser. But Webpack solves this geniously
by including a web-server that does the translation for you in the background
all the time.  With a little help of a configuration file called ``webpack.config.js``

.. code-block:: js

    // webpack.config.js
    module.exports = {
        entry   : "./web/js/app.js",
        output: {
            filename: "bundle.js",
            path : 'web/assets/',
            publicPath : '/assets/',
        }
    }

we can start our assets development server by calling:

:: 

    $ webpack-dev-server --progress --colors --port 8090 --content-base=web/

This will start serving the combined javascript file at
``http://localhost:8090/assets/bundle.js`` as well as the asset ``page.css`` at
``http://localhost:8090/css/page.css`` by using the ``--content-base`` flag.
Every change to any of the files that are part of the result will trigger a
rebuild similar to the ``--watch`` flag of Assetic, Grunt or Gulp.

Webpack can be installed globally so it is easy to get started with. I find
this a huge benefit not having to require a ``package.json`` and Node+npm
workflow for your PHP/Symfony project.

::

    $ sudo npm install -g webpack

For integration into Symfony we make use of some Framework configuration to
change the base path used for the ``{{ asset() }}`` twig-function:

::

    # app/config/config.yml
    framework:
      templating:
        assets_base_url: "%assets_base_url%"

    # app/config/parameters.yml
    parameters:
      assets_base_url: "http://localhost:8090"

This adds a base path in front of all your assets pointing to the Webpack dev
server.

The only thing left for integration is to load the javascript file from your
twig layout file:

.. code-block:: jinja

    <html>
        <body>
            <div id="content"></div>

            {% if app.environment == "dev" %}
            <script src="{{ asset('webpack-dev-server.js') }}"></script>
            {% endif %}
            <script type="text/javascript" src="{{ asset('assets/bundle.js') }}"></script>
        </body>
    </html>

The ``webpack-dev-server.js`` file loaded only in development environment
handles the `hot module reload
<https://webpack.js.org/concepts/hot-module-replacement/>`_
exchanging, adding, or removing modules while an application is running without
a page reload whenever possible.

For production use the ``assets_base_url`` parameter has to be adjusted
to your specific needs and you use the ``webpack`` command to generate a
minified and optimized version of your javascript code.

::

    $ webpack
    Hash: 69657874504a1a1db7cf
    Version: webpack 1.6.0
    Time: 329ms
        Asset   Size  Chunks             Chunk Names
    bundle.js  30533       0  [emitted]  main
       [2] ./web/js/app.js 1608 {0} [built]
       [5] ./web/js/vendor/jquery.js 496 {0} [built]

It will be placed inside ``web/assets/bundle.js`` as specified by the output
configuration in the Webpack configuration. Getting started in production is as
easy as seting the assets base url to null and pushing the bundle.js to your
production server.

I hope this example shows you some of the benefits of using Webpack over
Assetic, Grunt or Gulp and the simplicity using it between development and
production. While the example is Symfony2 related, the concepts apply to any
kind of application.

Back to why I stumbled over Webpack in the first place: React.JS. I have been
circling around React for a while with the impression that is extremly
well-suited for frontend development. The problems I had with React where
purely operation/workflow based:

1. React encourages modular design of applications, something that you
   have to get working first using require.js for example.
2. Differentation between development (refresh on modify) and production assets
   (minified).
3. React uses a template language JSX that requires cross-compiling the
   ``*.jsx`` files they are written in into plain javascript files.

Now this blog post has already shown that Webpack solves points one and two,
but it also solves the JSX Transformation with some extra configuration
in ``webpack.config.js``:

.. code-block:: js

    // webpack.config.js
    module.exports = {
        entry: './web/js/app.jsx',
        output: {
            filename: 'bundle.js',
            path: 'web/assets/',
            publicPath: '/assets'
        },
        module: {
            loaders: [
                { test: /\.jsx$/, loader: 'jsx-loader?insertPragma=React.DOM&harmony' }
            ]
        },
        externals: {'react': 'React'},
        resolve: {extensions: ['', '.js', '.jsx']}
    }

Now it is trivally easy to use React, just create a file with the ``*.jsx``
extension and Webpack will automatically load it through Facebooks JSX
transformer before serving it as plain javascript. The only requirement is that
you have to install the NPM package ``jsx-loader``.

So far I have used webpack only for two playground projects, but I am very
confident integrating it into some of my production projects now.

.. author:: default
.. categories:: none
.. tags:: Symfony, Webpack, Javascript
.. comments::
