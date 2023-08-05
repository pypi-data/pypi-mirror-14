from __future__ import print_function
from future.builtins import *

from collections import OrderedDict
from itertools import cycle


from .FoamFrame import FoamFrame
from .plot import style as defstyle
from .plot import arangement, compose_styles, colored


import bokeh.plotting as bk


def multiframes(folder, names, reader, **kwargs):
    """ create a collection of cases for which
        only the folder is different """
    return MultiFrame([reader(f, name=n, **kwargs)
                       for (f, n) in zip(folder, names)])


class MultiFrame():
    """ Class for storage of multiple case items
        or faceted data from FoamFrame
    """

    @staticmethod
    def from_dict(input_dict, **kwargs):
        return MultiFrame(
                cases=[FoamFrame.from_dict(d, name=name, **kwargs)
                        for name, d in input_dict.items()]
                )

    def __repr__(self):
        s = "MultiFrame with {} entries:\n".format(len(self.cases))
        s += "\n".join(["{}\n{}:\n{}".format(80*"=", name, c.describe())
                        for name, c in self.cases.items()])
        return s

    def __init__(self, cases=None):
        if type(cases) == list:
            self.cases = OrderedDict([(case.properties.name, case)
                                      for case in cases])
        elif type(cases) == OrderedDict:
            self.cases = cases
        else:
            self.cases = {}

    def __getitem__(self, field):
        return [serie[field] for serie in self.cases.values()]

    def names(self):
        return [name for name in self.cases]

    def select(self, case):
        """ select a specific item """
        return self.cases[case]

    def values(self):
        for case in self.cases.values():
            yield case

    def items(self):
        for name, case in self.cases.items():
            yield name, case

    def insert(self, key, value):
        self.cases[key] = value


    def histogram(self, y, x=None, **kwargs):
        cases = list(self.cases.keys())
        fig = self.cases[cases[0]].histogram(x=x, y=y, **kwargs)
        for c in cases:
            fig = self.cases[c].histogram(x=x, y=y, figure=fig, **kwargs)
        return fig


    def show(self, y, x='Pos', z=False, overlay="Field",
             style=defstyle, filename=None, show=True, **kwargs):
        """ Display single quantity y over multiple cases
            if overlay is set all cases are plotted in to single
            graph """
        # TODO if not overlay, common part should be figure title
        style = (compose_styles(style, []) if isinstance(style, list) else style)
        dashes = cycle([[8, 4], [4, 4], [4, 2], [1, 1]])
        cases = list(self.cases.keys())
        row = self.cases[cases[0]].show(x=x, y=y, overlay=overlay,
                                        legend_prefix=cases[0], style=style,
                                        post_pone_style=True, titles=y, **kwargs)
        for c, d, col in zip(cases[1:], dashes, colored[1:]):
            row = self.cases[c].show(x=x, y=y, overlay=overlay,
                                     legend_prefix=c, style=style,
                                     row=row, post_pone_style=True,
                                     line_dash=d, titles=y, color=col, **kwargs)
        gp = bk.GridPlot(children=style(rows=arangement(list(row.values()))))
        if filename:
            bk.save(gp, filename)
        if show:
            return bk.show(gp)
        else:
            return gp

    # def show_multi(self, ys, locs, x='Pos', style=defstyle, **kwargs):
    #     bk.figure()
    #     rows=[]
    #     ys = (ys if isinstance(ys, list) else [ys])
    #     for i, y in enumerate(ys):
    #         figs = plot.plot_cases(self, y=y, x=x, order=locs,
    #                 legend=True, **kwargs)
    #         rows.append(figs)
    #     return bk.GridPlot(children=style(rows=rows))
    #

    # ----------------------------------------------------------------------
    # Filter methods

    def filter(self, name, index=None, field=None):
        for cname, case in self.cases.items():
            self.cases[cname] = case.filter(name, index, field)
        return self

    def filter_fields(self, name, lower, upper):
        """ filter based on field values

            Examples:

                .filter_fields('T', 1000, 2000)
        """
        return self.filter(name, field=lambda x: lower < x < upper)

    def filter_locations(self, index):
        """ filter based on locations

            Examples:

                .filter_location(Owls.isIn('radial'))
                .filter_location(Owls.isNotIn('radial'))

        """
        return self.filter(name='Loc', index=index)

    def filter_items(self, func):
        """ select items based on filter funtion

            Example .filter_items(lambda ff: "Foo" in ff.locations)
        """
        return MultiFrame(filter(func, self.cases.items()))

    # ----------------------------------------------------------------------
    # Selection methods

    def location(self, loc):
        return MultiFrame([c.location(loc) for _, c in self.cases.items()])

    @property
    def latest(self):
        """ Grouping delegator """
        return MultiFrame([case.latest for cname, case in self.cases.items()])

    def on(self, case, func, **kwargs):
        """
            mf.on('Exp', "location", loc='axis')
        """
        n = getattr(self.cases[case], func)(**kwargs)
        return MultiFrame([(case_ if cname != case else n)
                           for cname, case_ in self.cases.items()])

    # ----------------------------------------------------------------------
    # Grouping methods

    def by_index(self, field, func=None):
        func = (func if func else lambda x: x)
        return self.by(field, func)

    def by_field(self, field, func=None):
        func = (func if func else lambda x: x)
        return self.by(field, func)

    def by_location(self, func=None):
        func = (func if func else lambda x: x)
        return self.by("Loc", func)

    def by_time(self, func=None):
        func = (func if func else lambda x: x)
        return self.by("Time", func)

    def by(self, name, func):
        """ Grouping delegator """
        return MultiFrame([case.by(name, func)
                           for cname, case in self.cases.items()])

    def update_plot_properties(self, field, d):
        """ update plot properties of all casese """

        for _, c in self.cases.items():
                c.properties.plot_properties.insert(field, d)
        return self
