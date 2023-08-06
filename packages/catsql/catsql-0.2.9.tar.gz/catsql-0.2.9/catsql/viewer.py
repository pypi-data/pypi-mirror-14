class Viewer(object):

    def __init__(self, url, echo=False):
        self.Base = None
        self.engine = None
        self.session = None
        self.reflected = False
        self.actual_url = None

        self.actual_url = url
        self.Base = declarative_base()
        try:
            self.engine = create_engine(url, echo=echo)
        except ImportError as e:
            print("Support library for this database not installed - {}".format(e))
            exit(1)
        except ArgumentError:
            try:
                # maybe this is a local sqlite database?
                sqlite_url = 'sqlite:///{}'.format(self.actual_url)
                self.engine = create_engine(sqlite_url, echo=echo)
                self.actual_url = sqlite_url
            except ArgumentError:
                # no joy, recreate the original problem and die.
                self.engine = create_engine(url, echo=echo)

    @property
    def url(self):
        return self.actual_url

    def validate(self):
        if not self.reflected:
            self.Base.metadata.reflect(self.engine)
            self.reflected = True
        if not self.session:
            self.session = create_session(bind=self.engine)
        return True

    @property
    def tables(self):
        self.validate()
        return self.Base.metadata.tables.items()

    def query(self, table):
        self.validate()
        return Query(table, self.session.query(table))

