just another settings
~~~~~~~~~~~~~~~~~~~~~

Just a code I use in a few Bottle/Flask-based and a few other projects.

.. code:: python

    from just_another_settings import EnvSelector, EnvField

    class BaseSettings(object):
        DEBUG = True
        # EnvField looks for the variable and fetches it, otherwise use value from default parameter
        MONGOLAB_URL = EnvField('MONGO_URL')
        HOST = EnvField('HOST', default='localhost')


    class ProdSettings(BaseSettings):
        DEBUG = False
        HOST = 'example.com'


    class DevSettings(BaseSettings):
        pass


    # env selector - selects settings base on env values
    env_selector = EnvSelector('APP_MODE', 'dev', dev=DevSettings(), prod=ProdSettings())

    # value selector - selects settings base on passed(to the `choose` method) value
    by_value_selector = ValueSelector(dev=DevSettings(), prod=ProdSettings())

    # somewhere in main file:
    # env
    application.config.from_object(env_selector.choose())
    # by value
    application.config.from_object(by_value_selector.choose('dev'))