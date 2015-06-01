import signal

from tornado.options import define, options

from .core import Reactor


def define_options():
    define(
        'config',
        default=Reactor.defaults['config'],
        help='Path to an configuration file')

    config_formats = '/'.join(sorted(Reactor.parsers))
    define(
        'config_format',
        help=("Config file format if it can't be determinated from file name "
              "({})".format(config_formats)))

    define(
        'pidfile',
        default=Reactor.defaults['pidfile'],
        help='Set pid file')

    define(
        'graphite_url',
        default=Reactor.defaults['graphite_url'],
        help='Graphite URL')


def run():
    define_options()
    options.parse_command_line()

    r = Reactor(**options.as_dict())

    signal.signal(signal.SIGTERM, r.stop)
    signal.signal(signal.SIGINT, r.stop)
    signal.signal(signal.SIGHUP, r.reinit)

    r.start()

if __name__ == '__main__':
    run()
