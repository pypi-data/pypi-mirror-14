class Query(object):

    def __init__(self, table, query):
        self.table = table
        self.rows = query

    def check(self):
        try:
            count = self.rows.count()
        except OperationalError as e:
            return False
        return True

    def grep(self, pattern, case_sensitive):
        # functions.concat would be neater, but doesn't seem to translate
        # correctly on sqlite
        parts = ''
        for idx, column in enumerate(self.table.columns):
            if idx > 0:
                parts = parts + ' // '
            part = functions.coalesce(expression.cast(column,
                                                      types.Unicode),
                                      '')
            parts = parts + part
        if case_sensitive:
            self.rows = self.rows.filter(parts.contains(sequence))
        else:
            self.rows = self.rows.filter(parts.ilike('%%' + sequence + '%%'))

    def order(self):
        primary_key = self.table.primary_key
        if len(primary_key) >= 1:
            self.rows = self.rows.order_by(*primary_key)
        elif len(self.table.c) >= 1:
            self.rows = self.rows.order_by(*table.c)

    def filters(self, row_filters):
        for filter in row_filter:
            self.rows = self.rows.filter(text(filter))

    def limit(self, ct):
        self.rows = self.rows.limit(ct)
