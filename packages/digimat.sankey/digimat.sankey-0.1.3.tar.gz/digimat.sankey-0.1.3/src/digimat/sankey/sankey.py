# -*- coding: utf-8 -*-

import textwrap
import StringIO
from datetime import datetime, timedelta

import pandas as pd
# from pandas import Series
# from pandas import DataFrame

import numpy as np

# use non interactive mode
import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
# http://matplotlib.org/api/sankey_api.html
import matplotlib.sankey as sankey
from matplotlib.table import Table

# require Pillow
from PIL import Image

# sudo pip install py_expression_eval
from py_expression_eval import Parser

import pprint
# import sys
# import traceback


class Consumer(object):
    def __init__(self, c, dtFrom=None, dtTo=None):
        self._c=c
        self._items={}
        if dtFrom is None:
            dtFrom=datetime.now()-timedelta(days=365*10)
        self._dtFrom=dtFrom
        if dtTo is None:
            dtTo=datetime.now()
        self._dtTo=dtTo

    @property
    def dtFrom(self):
        return self._dtFrom

    @property
    def dtTo(self):
        return self._dtTo

    def stampStr(self):
        stamp='%s..%s' % (self.dtFrom.strftime('%d-%m-%Y'), self.dtTo.strftime('%d-%m-%Y'))
        return stamp

    def clean(self):
        self._items={}

    def dtstr(self, dt):
        return dt.strftime("%Y-%m-%d")

    def dbretrieve(self, key):
        df = pd.read_sql("""
            SELECT records.stamp, records.value
            FROM records
            INNER JOIN `keys` ON `keys`.id=records.idkey
            WHERE `keys`.`key`='%s'
            ORDER BY stamp
            """ % key,
            self._c,
            parse_dates='stamp',
            index_col='stamp')

        return df

    def resample(self, s, rule, how='min'):
        if rule:
            return s.resample(rule, how=how, closed='left', label='left')
        return s

    # resample period
    # http://pandas-docs.github.io/pandas-docs-travis/timeseries.html#offset-aliases
    # see also anchory offsets for resample period (i.e. W-MON) :
    # http://pandas-docs.github.io/pandas-docs-travis/timeseries.html#anchored-offsets
    def load(self, key, resample=None, resampleHow='min', reject=0.0):
        try:
            df=self._items[key]
        except:
            df=self.dbretrieve(key)
            self._items[key]=df

        s=df['value']
        s.name=key
        rs=self.resample(s, resample, how=resampleHow)
        rs2=self.reject_outliers(rs, reject)

        rs2.fillna(method='pad', inplace=True)
        # rs2.interpolate(inplace=True)

        return rs2

    def loadDaily(self, key, resampleHow='min', reject=0.0):
        return self.load(key, 'D', resampleHow, reject=reject)

    def loadWeekly(self, key, resampleHow='min', reject=0.0):
        return self.load(key, 'W-MON', resampleHow, reject=reject)

    def loadMonthly(self, key, resampleHow='min', reject=0.0):
        return self.load(key, 'MS', resampleHow, reject=reject)

    def loadYearly(self, key, resampleHow='min', reject=0.0):
        return self.load(key, 'AS', resampleHow, reject=reject)

    # def pruneOutOfDateRecords(self, s):
        # data=s[self._dtFrom:self._dtTo]
        # return data

    def conso(self, key, factor=1.0, resample='d', reject=0.0):
        try:
            s=self.load(key, resample, reject=reject)
            data=s[self._dtFrom:self._dtTo]
            return (data[-1]-data[0])*factor
        except:
            pass
        return 0.0

    def reject_outliers(self, data, m=2.):
        if m<=0:
            return data
        return data[abs(data)<=m]
        d = np.abs(data - np.median(data))
        mdev = np.median(d)
        s = d/mdev if mdev else 0.
        print "--------REJECTED", data[s>=m]
        return data[s<m]


class FlowStream(object):
    def __init__(self, index, name, value, factor=1.0, orientation=0):
        self._index=index
        self._name=name
        self._value=value
        self._factor=factor
        self._orientation=orientation

    @property
    def index(self):
        return self._index

    @property
    def name(self):
        return self._name

    @property
    def value(self):
        return self.calcValue()

    @property
    def orientation(self):
        return self._orientation

    def calcValue(self):
        if self._value is not None:
            return self._value*self._factor
        return 0.0

    def normalizedValue(self, total):
        return self.value()/total

    def isInput(self):
        return None

    def isOutput(self):
        if self.isInput() is None:
            return None
        return not self.isInput()


class FlowStreamInput(FlowStream):
    def isInput(self):
        return True


class FlowStreamOutput(FlowStream):
    def isInput(self):
        return False


class Flow(object):
    def __init__(self, sankey, name, color, rotation):
        self._sankey=sankey
        self._name=name
        self._index=len(sankey.flows())
        self._color=color
        self._rotation=rotation
        self._inputs=[]
        self._outputs=[]
        self._prior=None
        self._priorConnect=None

    @property
    def sankey(self):
        return self._sankey

    @property
    def name(self):
        return self._name

    @property
    def consumer(self):
        return self.sankey.consumer

    @property
    def index(self):
        return self._index

    @property
    def color(self):
        return self._color

    @property
    def rotation(self):
        return self._rotation

    def inputStreamByName(self, name):
        for stream in self._inputs:
            if stream.name==name:
                return stream

    def outputStreamByName(self, name):
        for stream in self._outputs:
            if stream.name==name:
                return stream

    def inflate(self, name, value, orientation=0):
        if value is None:
            value=0
        value=abs(value)
        stream=FlowStreamInput(len(self._inputs), name, value, 1.0, orientation)
        print "(%s:%.02f)--%d-->[%s]" % (stream.name, stream.value, stream.index, self.name)
        self._inputs.append(stream)
        return stream

    def inflateLeft(self, name, value):
        return self.inflate(name, value, -1)

    def inflateRight(self, name, value):
        return self.inflate(name, value, 1)

    def inflateWith(self, flow, streamName, orientation=0):
        rstream=flow.outputStreamByName(streamName)
        if rstream:
            lstream=self.inflate(rstream.name, rstream.value, orientation)
            self._prior=flow.index
            self._priorConnect=(len(flow._inputs)+rstream.index, lstream.index)
            return lstream

    def inflateLeftWith(self, flow, streamName):
        return self.inflateWith(flow, streamName, -1)

    def inflateRightWith(self, flow, streamName):
        return self.inflateWith(flow, streamName, 1)

    def deflate(self, name, value, orientation=0):
        if value is None:
            value=0
        value=abs(value)
        stream=FlowStreamOutput(len(self._outputs), name, value, 1.0, orientation)
        print "[%s]--%d-->(%s:%.02f)" % (self.name, stream.index, stream.name, stream.value)
        self._outputs.append(stream)
        return stream

    def deflateRight(self, name, value):
        return self.deflate(name, value, 1)

    def deflateLeft(self, name, value):
        return self.deflate(name, value, -1)

    def totalIn(self):
        value=0
        for stream in self._inputs:
            value+=stream.value
        return value

    def totalOut(self):
        value=0
        for stream in self._outputs:
            value+=stream.value
        return value

    def total(self):
        return max(self.totalIn(), self.totalOut())

    def missing(self):
        return abs(self.totalIn()-self.totalOut())

    def missingOutput(self):
        if self.totalOut()<self.totalIn():
            return self.missing()
        return 0.0

    def missingInput(self):
        if self.totalIn()<self.totalOut():
            return self.missing()
        return 0.0

    def distributeMissingOnOutputs(self):
        missing=self.missing()
        if missing:
            total=self.totalOut()
            for stream in self._outputs:
                stream._value+=(stream._value/stream._factor/total)*missing

    def distributeMissingOnInputs(self):
        missing=self.missing()
        if missing:
            total=self.totalIn()
            for stream in self._inputs:
                stream._value+=(stream._value/stream._factor/total)*missing

    def completeMissingStream(self, name=None, orientation=0):
        missing=self.missing()
        if missing:
            if not name:
                name='%s:?' % self.name
                if self.totalIn()>self.totalOut():
                    self.deflate(name, missing, orientation)
                else:
                    self.inflate(name, missing, orientation)

    def completeLeftMissingStream(self, name=None):
        return self.completeMissingStream(name, -1)

    def completeRightMissingStream(self, name):
        return self.completeMissingStream(name, 1)

    def sankeyData(self):
        flows=[]
        labels=[]
        orientations=[]

        for stream in self._inputs:
            value=stream.value
            label=stream.name
            flows.append(value)

            if self.total()>0:
                ratio=value/self.total()
                if ratio>=0.001:
                    label='%s %.01f%%' % (label, ratio*100.0)

            labels.append(label)
            orientations.append(stream.orientation)

        for stream in self._outputs:
            value=stream.value
            label=stream.name
            value=stream.value
            if value>0:
                flows.append(-value)
            else:
                flows.append(0.0)

            if self.total()>0:
                ratio=value/self.total()
                if ratio>=0.001:
                    label='%s %.01f%%' % (label, ratio*100.0)

            labels.append(label)
            orientations.append(stream.orientation)

        return (flows, labels, orientations)


class Figure(object):
    def __init__(self, nrows=1, ncols=1, **kwargs):
        self._nrows=nrows
        self._ncols=ncols
        self._plots={}

        # Make the graphs a bit prettier, and bigger
        # deprecated: pd.set_option('display.mpl_style', 'default')

        matplotlib.style.use('ggplot')
        # print matplotlib.style.available

        # fix default white background
        kwargs.setdefault('facecolor', 'white')

        # print kwargs
        self._fig=plt.figure(**kwargs)

    def plot(self, name):
        try:
            return self._plots[name]
        except:
            pass

    def addplot(self, name='main', row=0, col=0, vspan=1, hspan=1, **kwargs):
        plot=self.plot(name)
        if plot:
            return plot

        ax=plt.subplot2grid((self._nrows, self._ncols), (row, col), colspan=hspan, rowspan=vspan, **kwargs)
        plot=Plot(ax)
        return plot

    @property
    def fig(self):
        return self._fig

    def render(self):
        pass

    def image(self):
        self.render()

        buf = StringIO.StringIO()
        plt.savefig(buf,
                format='png',
                bbox_inches='tight',
                frameon=False,
                pad_inches=0.6,
                # transparent=False,
                facecolor=self._fig.get_facecolor(),
                edgecolor='none')
        buf.seek(0)
        image = Image.open(buf)
        # open don't load data until it is used, so load it before closing buffer !
        image.load()
        buf.close()

        return image

    def save(self, fpath):
        image=self.image()
        image.save(fpath)
        self.close()

    def close(self):
        self.fig.clf()
        plt.close(self.fig)

    def text(self, x, y, label, *args, **kwargs):
        # http://matplotlib.org/api/figure_api.html
        self.fig.text(x, y, label, *args, **kwargs)

    def addPageNumber(self, page, of=None):
        label='page %d' % page
        if of:
            label += '/%d' % of
        self.fig.text(0.95, 0.05, label, {'horizontalalignment': 'right'})

    def addFooter(self, label, **kwargs):
        kwargs.setdefault('horizontalalignment', 'left')
        self.fig.text(0.05, 0.05, label, **kwargs)

    def addHeader(self, label, **kwargs):
        kwargs.setdefault('horizontalalignment', 'left')
        self.fig.text(0.05, 0.95, label, **kwargs)

    def addHeaderRight(self, label, **kwargs):
        kwargs.setdefault('horizontalalignment', 'right')
        self.fig.text(0.95, 0.95, label, **kwargs)


class Plot(object):
    def __init__(self, ax):
        self._ax=ax

    @property
    def ax(self):
        return self._ax

    @property
    def figure(self):
        return self.ax.figure

    def setTitle(self, title, size=12, loc=None):
        if title:
            self.ax.set_title(title, size=size)

    def setUnit(self, unit):
        if unit:
            self.ax.set_title(unit, size=12, loc='left')

    def setSecondaryUnit(self, unit):
        if unit:
            self.ax.set_title(unit, size=12, loc='right')

    def setYLabel(self, label, size=12):
        if label:
            self.ax.set_ylabel(label, size=size)

    def table(self, **kwargs):
        table=Table(self.ax, **kwargs)
        self.ax.set_axis_off()
        return table

    def ylabels(self):
        return self.ax.get_yticklabels()

    def setColorYLabels(self, color):
        [i.set_color(color) for i in self.ylabels()]


class SimplePlot(object):
    def __init__(self, s, width=17, height=11, title=None, ylabel=None, unit=None):
        self._s=s
        self._title=title
        self._ylabel=ylabel
        self._unit=unit
        self._figure=Figure(1, 1, figsize=(width, height), frameon=False)
        # self._figure.fig.patch.set_facecolor('white')

    @property
    def s(self):
        return self._s

    def onPlot(self, plot):
        self._s.plot(ax=plot.ax, drawstyle='steps-post')
        plot.ax.set_xlabel('')

    def render(self):
        plot=self._figure.addplot('main', 0, 0)
        plot.setTitle(self._title)
        plot.setUnit(self._unit)
        plot.setYLabel(self._ylabel)
        self.onPlot(plot)

    def image(self):
        self.render()
        return self._figure.image()

    def save(self, fpath):
        self.render()
        return self._figure.save(fpath)

    def close(self):
        self._figure.close()


class SimpleScatter(object):
    def __init__(self, x, y, colors=None, width=20, height=10, title=None, ylabel=None, xlabel=None, unit=None):
        self._x=x
        self._y=y
        self._colors=colors
        self._title=title
        self._ylabel=ylabel
        self._unit=unit
        self._figure=Figure(1, 1, figsize=(width, height), frameon=False)
        # self._figure.figpatch.set_facecolor('white')

    def render(self):
        plot=self._figure.addplot('main', 0, 0)
        plot.setTitle(self._title)
        plot.setUnit(self._unit)
        plot.setYLabel(self._ylabel)
        plot.ax.scatter(x=self._x, y=self._y, c=self._colors)

    def image(self):
        self.render()
        return self._figure.image()

    def save(self, fpath):
        self.render()
        return self._figure.save(fpath)


class DOWSignature(object):
    def __init__(self, s):
        self._s=s
        self._valid=False

    def colors(self, n=7):
        # todo:
        colors=['#363f15',
            '#89732e',
            '#4ab03b',
            '#8e3db6',
            '#551c31',
            '#345b9c',
            '#ae3a48']
        return colors

    def calc(self):
        self._x=[]
        self._y=[]
        self._color=[]

        colors=self.colors(7)

        for i in range(len(self._s)):
            stamp=self._s.index[i]
            yvalue=self._s[i]
            try:
                xvalue=stamp.weekday()
                self._x.append(xvalue)
                self._y.append(yvalue)
                self._color.append(colors[xvalue])
            except:
                pass

        self._valid=True

    def draw(self, plot):
        if not self._valid:
            self.calc()
        plot.ax.scatter(x=self._x, y=self._y, c=self._color)


class Signature(object):
    def __init__(self, sx, sy, colormode='dow'):
        self._sx=sx
        self._sy=sy
        self._colormode=colormode
        self._valid=False

    def color(self, n):
        colors=['#363f15',
            '#89732e',
            '#4ab03b',
            '#8e3db6',
            '#551c31',
            '#345b9c',
            '#ae3a48']

        try:
            return colors[n]
        except:
            return '#ff0000'

    def calc(self):
        self._x=[]
        self._y=[]
        self._color=[]

        for i in range(len(self._sy)):
            stamp=self._sy.index[i]
            yvalue=self._sy[i]
            try:
                xvalue=self._sx[stamp]
                self._x.append(xvalue)
                self._y.append(yvalue)
                if self._colormode=='year':
                    self._color.append(self.color(stamp.year % 7))
                elif self._colormode=='month':
                    self._color.append(self.color(stamp.month-1))
                else:
                    self._color.append(self.color(stamp.weekday()))
            except:
                pass

        self._valid=True

    def draw(self, plot):
        if not self._valid:
            self.calc()
        plot.ax.scatter(x=self._x, y=self._y, c=self._color)


class TSignature(object):
    def __init__(self, c, sy, tkey='r_9100_2_mtogvetre200d0_0_0'):
        self._c=c
        sx=c.loadDaily(tkey)
        super(TSignature, self).__init__(sx, sy)


class EnergyDiagram(object):
    def __init__(self, data, key, keyTRef='r_9100_2_mtogvetre200d0_0_0', width=11, height=17, title=None, unit=None, ymax=None):
        self._data=data
        self._key=key
        self._keyTRef=keyTRef
        self._title=title
        self._unit=unit
        self._ymax=ymax
        self._figure=Figure(4, 2, figsize=(width, height), frameon=False)
        # self._figure.fig.patch.set_facecolor('white')
        if title:
            title=textwrap.wrap(title, 110)
            title='\n'.join(title)
            self._figure.fig.suptitle(title, fontsize=12)
        # plt.subplots_adjust(left=0, bottom=0.2, right=1, top=0.9, wspace=0.15, hspace=0.3)
        plt.subplots_adjust(left=0.15, bottom=0.15, right=0.9, top=0.85, wspace=0.15, hspace=0.3)

    @property
    def data(self):
        return self._data

    def addPageNumber(self, page, of=None):
        self._figure.addPageNumber(page, of)

    def addFooter(self, label, **kwargs):
        self._figure.addFooter(label, **kwargs)

    def addHeader(self, label, **kwargs):
        self._figure.addHeader(label, **kwargs)

    def addHeaderRight(self, label, **kwargs):
        self._figure.addHeaderRight(label, **kwargs)

    def loadDaily(self, key, conso=False):
        p=Parser()
        e=p.parse(key)
        variables={}
        for v in e.variables():
            sv=self.data.loadDaily(v)
            sv[sv==0] = np.nan
            if sv is None or len(sv)<1:
                print "UNKNOWN VARIABLE", v
                return None
            sv2=sv
            if conso:
                sv2=sv.shift(-1)-sv
                sv2[sv2<0]=np.nan
                if self._ymax:
                    sv2[sv2>=self._ymax]=np.nan
            sv2.interpolate(inplace=True)
            variables[v]=sv2

        s=e.evaluate(variables)
        return s

    def loadMonthly(self, key, conso=False):
        p=Parser()
        e=p.parse(key)
        variables={}
        for v in e.variables():
            sv=self.data.loadMonthly(v)
            sv[sv==0] = np.nan
            if sv is None or len(sv)<1:
                print "UNKNOWN VARIABLE", v
                return None
            sv2=sv
            if conso:
                sv2=sv.shift(-1)-sv
                sv2[sv2<0]=np.nan
                if self._ymax:
                    sv2[sv2>=self._ymax]=np.nan
            sv2.interpolate(inplace=True)
            variables[v]=sv2

        s=e.evaluate(variables)
        return s

    def renderProfile(self):
        plot=self._figure.addplot('profile', 0, 0)
        s=self.loadDaily(self._key)

        dt=datetime.now()
        data=s[dt-timedelta(days=365*10):]
        try:
            data.plot(ax=plot.ax, drawstyle='steps-post', linewidth=2.0, color='green')
        except:
            pass
        plot.ax.set_xlabel('')
        plot.setTitle('index compteur')
        # plot.ax.patch.set_facecolor('white')
        if self._unit:
            plot.setUnit('%s' % self._unit)

    def renderConso(self):
        plot=self._figure.addplot('conso', 0, 1)
        # plot.ax.patch.set_facecolor('white')
        stref=self.data.loadDaily(self._keyTRef, resampleHow='mean')
        s=self.loadDaily(self._key, True)

        dt=datetime.now()
        dtFrom=dt-timedelta(days=5*365)
        data=s[dtFrom:]

        try:
            data.plot(ax=plot.ax, drawstyle='steps-post',
                    linewidth=2.0,
                    color='green', label='conso')
        except:
            pass

        ax2=plot.ax.twinx()

        stref2=stref[dtFrom:]
        stref2.plot(ax=ax2, drawstyle='steps-post', color='red', label='Tmoy', alpha=0.7)
        [i.set_color('red') for i in ax2.get_yticklabels()]

        plot.ax.set_xlabel('')
        plot.setTitle(u'conso journaliere')
        if self._unit:
            plot.setUnit('%s/mois' % self._unit)
        plot.setSecondaryUnit(u'°C')

    def renderYear(self):
        plot=self._figure.addplot('yearconso', 1, 0, hspan=2)
        # plot.ax.patch.set_facecolor('white')
        s=self.loadDaily(self._key, True)

        dt=datetime.now()
        data=s[dt-timedelta(days=365*2):]

        try:
            data.plot(ax=plot.ax, linewidth=2.0,
                    color='green', drawstyle='steps-post')
        except:
            pass

        # ax.fill_between(s.index, s.values)
        plot.ax.set_xlabel('')
        plot.setTitle(u'conso journaliere')
        if self._unit:
            plot.setUnit('%s/mois' % self._unit)

    def renderSignature(self):
        plot=self._figure.addplot('signature', 2, 0, hspan=1, vspan=2)
        # plot.ax.patch.set_facecolor('white')

        stref=self.data.loadDaily(self._keyTRef)
        s=self.loadDaily(self._key, True)
        if self._ymax:
            s[s>=self._ymax]=np.nan

        dt=datetime.now()
        data=s[dt-timedelta(days=365*3):]

        sig=Signature(sy=data, sx=stref, colormode='year')

        plot.setTitle(u'signature conso journalière')
        plot.ax.set_xlabel('Tmoy journaliere')
        sig.draw(plot)
        if self._unit:
            plot.setUnit('%s/jour' % self._unit)

    def renderData(self):
        plot=self._figure.addplot('values', 2, 1, hspan=1, vspan=2)
        table=plot.table()

        s=self.loadMonthly(self._key, True)

        y0=datetime.now().year
        history=3

        widthLabel=0.25
        widthCell=(1.0-widthLabel)/float(history)
        colorCellTitle='#dddddd'
        # sformat='%%.02f %s' % self._unit

        labels=[None,
                'JANVIER', 'FEVRIER', 'MARS', 'AVRIL',
                'MAI', 'JUIN', 'JUILLET', 'AOUT', 'SEPTEMBRE',
                'OCTOBRE', 'NOVEMBRE', 'DECEMBRE',
                'TOTAL']

        heightCell=(1.0)/len(labels)

        row=0
        for label in labels:
            if label:
                table.add_cell(row+1, history, widthLabel, heightCell,
                        text=label, loc='left',
                        facecolor=colorCellTitle)
                row+=1

        for n in range(0, history):
            year=y0-n
            table.add_cell(0, n, widthCell, heightCell,
                    text=str(year), loc='right',
                    facecolor=colorCellTitle)

            try:
                total=0
                data=s[str(year)]
                row=1
                for m in range(0, 12):
                    value=0
                    try:
                        value=data[m]
                        if np.isnan(value):
                            svalue='--'
                        else:
                            svalue='%.1f %s' % (value, self._unit)
                    except:
                        svalue='--'

                    table.add_cell(row, n, widthCell, heightCell,
                            text=svalue,
                            loc='right')
                    row+=1
                total=data.sum()
            except:
                pass

            table.add_cell(row, n, widthCell, heightCell,
                    text='%.1f %s' % (total, self._unit),
                    loc='right',
                    facecolor=colorCellTitle)

            properties=table.properties()
        for cell in properties['child_artists']:
            cell.set_fontsize(10)

        plot.ax.add_table(table)

    def render(self):
        self.renderProfile()
        self.renderConso()
        self.renderYear()
        self.renderData()
        self.renderSignature()

    def image(self):
        self.render()
        return self._figure.image()

    def save(self, fpath):
        self.render()
        return self._figure.save(fpath)

    def close(self):
        self._figure.close()


class VolumeDiagram(object):
    def __init__(self, data, key, width=11, height=17, title=None, unit=None, ymax=None):
        self._data=data
        self._key=key
        self._title=title
        self._unit=unit
        self._ymax=ymax
        self._figure=Figure(4, 2, figsize=(width, height), frameon=False)
        # self._figure.fig.patch.set_facecolor('white')
        if title:
            title=textwrap.wrap(title, 110)
            title='\n'.join(title)
            self._figure.fig.suptitle(title, fontsize=12)
        plt.subplots_adjust(left=0.15, bottom=0.15, right=0.9, top=0.85, wspace=0.15, hspace=0.3)

    @property
    def data(self):
        return self._data

    def addPageNumber(self, page, of=None):
        self._figure.addPageNumber(page, of)

    def addFooter(self, label, **kwargs):
        self._figure.addFooter(label, **kwargs)

    def addHeader(self, label, **kwargs):
        self._figure.addHeader(label, **kwargs)

    def addHeaderRight(self, label, **kwargs):
        self._figure.addHeaderRight(label, **kwargs)

    def loadDaily(self, key, conso=False):
        p=Parser()
        e=p.parse(key)
        variables={}
        for v in e.variables():
            sv=self.data.loadDaily(v)
            sv[sv==0] = np.nan
            if sv is None or len(sv)<1:
                print "UNKNOWN VARIABLE", v
                return None
            sv2=sv
            if conso:
                sv2=sv.shift(-1)-sv
                sv2[sv2<0]=np.nan
                if self._ymax:
                    sv2[sv2>=self._ymax]=np.nan

            # todo: check if really welcomed :)
            sv2.interpolate(inplace=True)
            variables[v]=sv2

        s=e.evaluate(variables)
        return s

    def loadMonthly(self, key, conso=False):
        p=Parser()
        e=p.parse(key)
        variables={}
        for v in e.variables():
            sv=self.data.loadMonthly(v)
            sv[sv==0] = np.nan
            if sv is None or len(sv)<1:
                print "UNKNOWN VARIABLE", v
                return None
            sv2=sv
            if conso:
                sv2=sv.shift(-1)-sv
                sv2[sv2<0]=np.nan
                if self._ymax:
                    sv2[sv2>=self._ymax]=np.nan

            # todo: check if really welcomed :)
            sv2.interpolate(inplace=True)
            variables[v]=sv2

        s=e.evaluate(variables)
        return s

    def renderProfile(self):
        plot=self._figure.addplot('profile', 0, 0)
        s=self.loadDaily(self._key)

        # todo: check if really welcomed ;)
        s.interpolate(inplace=True)

        dt=datetime.now()
        data=s[dt-timedelta(days=365*10):]
        try:
            data.plot(ax=plot.ax, drawstyle='steps-post', linewidth=2.0, color='blue')
        except:
            pass
        plot.ax.set_xlabel('')
        plot.setTitle('index compteur')
        # plot.ax.patch.set_facecolor('white')
        if self._unit:
            plot.setUnit('%s' % self._unit)

    def renderConso(self):
        plot=self._figure.addplot('conso', 0, 1)
        # plot.ax.patch.set_facecolor('white')
        s=self.loadMonthly(self._key, True)

        dt=datetime.now()
        dtFrom=dt-timedelta(days=5*365)
        data=s[dtFrom:]

        try:
            data.plot(ax=plot.ax, drawstyle='steps-post',
                    linewidth=2.0,
                    color='blue', label='conso')
        except:
            pass

        plot.ax.set_xlabel('')
        plot.setTitle(u'conso mensuelle')
        if self._unit:
            plot.setUnit('%s/mois' % self._unit)

    def renderYear(self):
        plot=self._figure.addplot('yearconso', 1, 0, hspan=2)
        # plot.ax.patch.set_facecolor('white')
        s=self.loadMonthly(self._key, True)

        dt=datetime.now()
        data=s[dt-timedelta(days=365*2):]

        try:
            data.plot(ax=plot.ax, linewidth=2.0,
                    color='blue', drawstyle='steps-post')
        except:
            pass

        # ax.fill_between(s.index, s.values)
        plot.ax.set_xlabel('')
        plot.setTitle(u'conso mensuelle')
        if self._unit:
            plot.setUnit('%s/mois' % self._unit)

    def renderSignature(self):
        plot=self._figure.addplot('signature', 2, 0, hspan=1, vspan=2)
        # plot.ax.patch.set_facecolor('white')

        s=self.loadDaily(self._key, True)

        dt=datetime.now()
        data=s[dt-timedelta(days=365*3):]

        sig=DOWSignature(s=data)

        plot.setTitle(u'signature conso journalière')
        plot.ax.set_xlabel('jour semaine (0=DI, 1=LU, ...)')
        sig.draw(plot)
        if self._unit:
            plot.setUnit('%s/jour' % self._unit)

    def renderData(self):
        plot=self._figure.addplot('values', 2, 1, hspan=1, vspan=2)
        table=plot.table()

        s=self.loadMonthly(self._key, True)

        y0=datetime.now().year
        history=3

        widthLabel=0.25
        widthCell=(1.0-widthLabel)/float(history)
        colorCellTitle='#dddddd'
        # sformat='%%.02f %s' % self._unit

        labels=[None,
                'JANVIER', 'FEVRIER', 'MARS', 'AVRIL',
                'MAI', 'JUIN', 'JUILLET', 'AOUT', 'SEPTEMBRE',
                'OCTOBRE', 'NOVEMBRE', 'DECEMBRE',
                'TOTAL'
                ]

        heightCell=(1.0)/len(labels)

        row=0
        for label in labels:
            if label:
                table.add_cell(row, history, widthLabel, heightCell,
                        text=label, loc='left',
                        facecolor=colorCellTitle)
            row+=1

        for n in range(0, history):
            year=y0-n
            table.add_cell(0, n, widthCell, heightCell,
                    text=str(year), loc='right',
                    facecolor=colorCellTitle)

            try:
                total=0
                data=s[str(year)]
                row=1
                for m in range(0, 12):
                    value=0
                    try:
                        value=data[m]
                        if np.isnan(value):
                            svalue='--'
                        else:
                            svalue='%.1f %s' % (value, self._unit)
                    except:
                        svalue='--'

                    table.add_cell(row, n, widthCell, heightCell,
                            text=svalue,
                            loc='right')
                    row+=1
                total=data.sum()
            except:
                pass

            table.add_cell(row, n, widthCell, heightCell,
                    text='%.1f %s' % (total, self._unit),
                    loc='right',
                    facecolor=colorCellTitle)

        properties=table.properties()
        for cell in properties['child_artists']:
            cell.set_fontsize(10)

        plot.ax.add_table(table)

    def render(self):
        self.renderProfile()
        self.renderConso()
        self.renderYear()
        self.renderData()
        self.renderSignature()

    def image(self):
        self.render()
        return self._figure.image()

    def save(self, fpath):
        self.render()
        return self._figure.save(fpath)

    def close(self):
        self._figure.close()


class EfficiencyDiagram(object):
    def __init__(self, data, key1, key2, factor=1.0, keyTRef='r_9100_2_mtogvetre200d0_0_0', width=11, height=17, title=None, unit1=None, unit2=None):
        self._data=data
        self._key1=key1
        self._key2=key2
        self._factor=factor
        self._keyTRef=keyTRef
        self._title=title
        self._unit1=unit1
        self._unit2=unit2
        self._figure=Figure(4, 2, figsize=(width, height), frameon=False)
        # self._figure.fig.patch.set_facecolor('white')
        if title:
            self._figure.fig.suptitle(title, fontsize=12)
        plt.subplots_adjust(left=0, bottom=0.2, right=1, top=0.9, wspace=0.15, hspace=0.3)

    @property
    def data(self):
        return self._data

    def loadWeekly(self, key, conso=False):
        p=Parser()
        e=p.parse(key)

        variables={}
        for v in e.variables():
            print "LOAD", v
            sv=self.data.loadWeekly(v)
            if sv is None or len(sv)<1:
                print "UNKNOWN VARIABLE", v
                return None
            sv2=sv
            if conso:
                sv2=sv.shift(-1)-sv
                sv2[sv2<0]=np.nan
            variables[v]=sv2

        print "EVAL"
        s=e.evaluate(variables)
        print "OK"
        return s

    def renderProfile1(self):
        plot=self._figure.addplot('profile1', 0, 0)
        s=self.loadWeekly(self._key1)

        dt=datetime.now()
        dtFrom=dt-timedelta(days=365*10)
        data=s[dtFrom:]
        try:
            data.plot(ax=plot.ax, drawstyle='steps-post', linewidth=2.0, color='green')
        except:
            pass

        plot.setTitle(self._key1)
        plot.ax.set_xlabel('')
        # plot.ax.patch.set_facecolor('white')
        plot.setUnit(self._unit1)

    def renderProfile2(self):
        plot=self._figure.addplot('profile2', 0, 1)
        s=self.loadWeekly(self._key2)

        dt=datetime.now()
        dtFrom=dt-timedelta(days=365*10)
        data=s[dtFrom:]
        try:
            data.plot(ax=plot.ax, drawstyle='steps-post',
                    linewidth=2.0,
                    color='green')
        except:
            pass

        plot.setTitle(self._key2)
        plot.ax.set_xlabel('')
        # plot.ax.patch.set_facecolor('white')
        plot.setUnit(self._unit2)

    def renderEfficiency(self):
        plot=self._figure.addplot('rendement hebdomadaire', 1, 0, hspan=2, vspan=2)
        # plot.ax.patch.set_facecolor('white')

        s1=self.loadWeekly(self._key1, True)
        s2=self.loadWeekly(self._key2, True)

        s=s1/(s2*self._factor)

        dt=datetime.now()
        dtFrom=dt-timedelta(days=365*5)
        data=s[dtFrom:]

        try:
            data.plot(ax=plot.ax, linewidth=2.0,
                    color='green', drawstyle='steps-post')
        except:
            pass

        plot.ax.set_ylim([0, 1.5])

        stref=self.data.loadWeekly(self._keyTRef)
        stref2=stref[dtFrom:]

        ax2=plot.ax.twinx()
        stref2.plot(ax=ax2,
                drawstyle='steps-post',
                color='red',
                label='Tmoy',
                alpha=0.4)

        [i.set_color('red') for i in ax2.get_yticklabels()]
        plot.ax.set_xlabel('')
        plot.setTitle(u'rendement')
        plot.setSecondaryUnit(u'°C')

        # signature
        plot=self._figure.addplot('signature', 3, 0, hspan=2, vspan=1)
        # plot.ax.patch.set_facecolor('white')

        sig=Signature(sy=data, sx=stref2, colormode='year')
        # sig=DOWSignature(s=data)

        plot.setTitle(u'signature rendement hebdomadaire')
        plot.ax.set_xlabel('Tmoy journaliere')
        sig.draw(plot)
        plot.setUnit('%')

    def render(self):
        self.renderProfile1()
        self.renderProfile2()
        self.renderEfficiency()

    def image(self):
        self.render()
        return self._figure.image()

    def save(self, fpath):
        self.render()
        return self._figure.save(fpath)

    def close(self):
        self._figure.close()


class SankeyDiagram(object):
    def __init__(self, width=11, height=17, title=None, format='%.02f', gap=0.4, fontsize=8, textoffset=0.35, margin=0.15, unit=''):
        self._flows=[]
        self._fontsize=fontsize

        # http://matplotlib.org/api/figure_api.html#matplotlib.figure.Figure.add_subplot
        # subplot=dict(xticks=[], yticks=[])
        # self._figure=Figure(subplot_kw=subplot, figsize=(width, height), frameon=False)
        self._figure=Figure(1, 1, figsize=(width, height), frameon=False)

        plot=self._figure.addplot('sankey', xticks=[], yticks=[])
        plot.ax.patch.set_facecolor('white')

        plot.setTitle(title, 12)

        # http://matplotlib.org/api/sankey_api.html
        self._sankey=sankey.Sankey(ax=plot.ax, format=format,
                unit=unit,
                gap=gap,
                offset=textoffset,
                margin=margin)

        # self._figure.fig.patch.set_facecolor('white')

    def addPageNumber(self, page, of=None):
        self._figure.addPageNumber(page, of)

    def addFooter(self, label, **kwargs):
        self._figure.addFooter(label, **kwargs)

    def addHeader(self, label, **kwargs):
        self._figure.addHeader(label, **kwargs)

    def addHeaderRight(self, label, **kwargs):
        self._figure.addHeaderRight(label, **kwargs)

    def createFlow(self, name, color=None, rotation=0):
        try:
            self._flows[-1].completeLeftMissingStream()
        except:
            pass

        if color is None:
            color=self._flows[-1].color
        flow=Flow(self, name, color, rotation)
        self._flows.append(flow)
        return flow

    def createHorizontalFlow(self, name, color=None):
        return self.createFlow(name, color, 0)

    def createVerticalFlow(self, name, color=None):
        return self.createFlow(name, color, -90)

    def flows(self):
        return self._flows

    def flow(self, index):
        return self._flows[index]

    def render(self):
        total=0
        for flow in self._flows:
            total=max(total, flow.total())
        if total>0:
            self._sankey.scale=1.0/total
            for flow in self._flows:
                flow.completeLeftMissingStream()
                print "---RENDERING", flow.name, flow.total()
                if flow.total()>0:
                    (flows, labels, orientations)=flow.sankeyData()
                    try:
                        self._sankey.add(flows=flows, labels=labels, orientations=orientations,
                            rotation=flow.rotation,
                            facecolor=flow.color,
                            prior=flow._prior,
                            connect=flow._priorConnect)
                    except:
                        print "****** EXCEPTION!"
                        print flow.name
                        pprint.pprint(flows)
                else:
                    print "Ignoring flow %s" % flow.name

            diagrams=self._sankey.finish()
            for diagram in diagrams:
                # diagram.text.set_fontweight('bold')
                diagram.text.set_fontsize(self._fontsize)
                for text in diagram.texts:
                    text.set_fontsize(self._fontsize)
            return True

    def image(self):
        self.render()
        return self._figure.image()

    def save(self, fpath):
        self.render()
        return self._figure.save(fpath)


if __name__ == "__main__":
    pass
