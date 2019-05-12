# -*- coding: utf-8 -*-
"""
Created on Sat Oct 13 10:22:36 2018

@author: Eric


Ce module implémente un objet permettant de mesure le temps entre deux jalons.
"""

import datetime as dt
import pandas as pd
import logging as log

from pytools.time.timetools import diff_times


class Chrono:
    FIRST_MARK = 'first'
    LAST_MARK = 'last'

    UNIT_DAY = 'day'
    UNIT_HOUR = 'hour'
    UNIT_MINUTE = 'minute'
    UNIT_SECOND = 'second'

    def __init__(self):
        self._marks_ = {}

    def add_mark(self, name:str=None, value:dt.datetime=None) -> None:
        if name is None:
            if len(self._marks_) == 0:
                name = self.FIRST_MARK
            else:
                name = self.LAST_MARK
        if value is None:
            self._marks_[name] = dt.datetime.today()
        elif isinstance(value, float):
            self._marks_[name] = dt.datetime.fromtimestamp(value)
        elif isinstance(value, (dt.datetime, dt.date, dt.time)):
            self._marks_[name] = value
        else:
            raise TypeError(type(value))

    def delta(self, first_mark=FIRST_MARK, last_mark=LAST_MARK, unit=UNIT_SECOND):
        if first_mark not in self:
            if self.FIRST_MARK not in self:
                self.add_mark(self.FIRST_MARK)
            first_mark = self.FIRST_MARK

        if last_mark not in self:
            if self.LAST_MARK not in self:
                self.add_mark(self.LAST_MARK)
            last_mark = self.LAST_MARK

        return diff_times(self[first_mark], self[last_mark], unit=unit)

    def report_to_panda(self, unit=UNIT_SECOND):
        report = pd.DataFrame(columns=['marker', 'date', 'delay'])
        pred_key = None
        for i, key in enumerate(sorted(self._marks_.keys(),
                                       key=lambda t: self[t])):
            if i == 0:
                report = report.append({
                            'marker': key,
                            'date': self[key],
                            'delay': None
                            }, ignore_index=True)
            else:
                report = report.append({
                            'marker': key,
                            'date': self[key],
                            'delay': self.delta(pred_key, key, unit=unit)
                            }, ignore_index=True)
            pred_key = key
        return report

# =============================================================================
# Special method
# =============================================================================
    def __getitem__(self, value):
        if value in self._marks_.keys():
            return self._marks_[value]
        else:
            log.warning("{classname}.__getitem__ : mark {mark} unknow".format(
                    classname=self.__class__,
                    mark=value
                    )
            )
            return None

    def __len__(self):
        return len(self._marks_)

    def __contains__(self, value):
        return value in self._marks_

