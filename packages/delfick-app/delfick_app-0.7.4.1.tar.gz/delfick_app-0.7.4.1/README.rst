Delfick App
===========

A framework to simplify and remove duplication when creating a new application.
It is opinionated in nature and aims to be declarative.

Getting Started
---------------

The most basic example of usage would look something like:

.. code-block:: python

    #!/usr/bin/env python
    from delfick_app import App

    class MyApp(object):
        def start(self, cli_args):
            print "hello world"

    class Main(App):
        def execute(self, args, extra_args, cli_args, logging_handler):
            """Start your app!"""
            MyApp().start(cli_args)

    main = Main.main
    if __name__ == "__main__":
        main()

This will give you a usage that looks like:

    $ ./app.py [--verbose|--silent|--debug]

Where --verbose and --debug show more logs and --silent silences all the logs.

Your logs will be colourful and your mainline will catch and print any
DelfickError exceptions nicely to the terminal.

Advanced Usage
--------------

.. code-block:: python

    from my_app import MyApp, VERSION

    from delfick_app import App
    import logging

    class Main(App):

        # Setting both VERSION and boto_useragent_name
        # Will change boto's useragent to include {name}/{VERSION}
        # Not setting them means boto's useragent is unchanged
        VERSION = VERSION
        boto_useragent_name = "myapp"

        # Cli options for configuration special cli options
        cli_categories = ['app']
        cli_description = "My amazing app"
        cli_environment_defaults = {"CONFIG_LOCATION": ("--config", './config.yml')}
        cli_positional_replacements = [('--task', 'list_tasks'), '--environment']

        def execute(self, args, extra_args, cli_args, logging_handler):
            # Optionally set the logging theme between 'light' and 'dark'
            self.setup_logging_theme(logging_handler, colors="dark")

            # Do what is necessary to start the app
            app = MyApp()
            app.start(cli_args)

        def setup_other_logging(self, args, verbose=False, silent=False, debug=False):
            logging.getLogger("boto").setLevel([logging.CRITICAL, logging.ERROR][verbose or debug])

        def specify_other_args(self, parser, defaults):
            parser.add_argument("--task"
                , help = "The task to execute"
                , **defaults['--task']
                )

            parser.add_argument("--environment"
                , help = "the environment to use"
                , **defaults["--environment"]
                )

            parser.add_argument("--config"
                , help = "The configuration to use"
                , **defaults["--config"]
                )

    main = Main.main
    if __name__ == '__main__':
        main()

With the above configuration, the following three usages are equivalent::

    $ ./app.py some_task dev --config ./config.yml

    $ ./app.py --task some_task --environment dev --config ./config.yml

    $ APP_CONFIG=./config.yml ./app.py some_task dev

Installation
------------

Just use pip::

    $ pip install delfick_app

Tests
-----

Run the following::

    $ mkvirtualenv delfick_app
    $ workon delfick_app
    $ pip install -e .
    $ pip install -e ".[tests]"

To install delfick_app and it's dependencies.

Then to run the tests::

    $ ./test.sh

