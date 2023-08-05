class OverflowDate(object):
    def __init__(self, **info):
        self.info = info

    def isocalendar(self):
        if 'isocalendar' in self.info:
            return self.info['isocalendar']
