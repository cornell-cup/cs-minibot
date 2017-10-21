class Singleton(type):
    """ A metaclass for describing a singleton class. """

    __instances = None

    def __call__(cls, *args, **kwargs):
        if cls.__instances is None:
            cls.__instances = super(Singleton, cls).__call__(*args, **kwargs)
        return cls.__instances
