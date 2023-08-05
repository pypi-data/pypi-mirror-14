"""Volatility class is to get daily/overnight volatility
"""
# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import pandas as pd
import warnings

from config import *
from historicaldata import DBConn
from pandas.io.sql import read_sql
from copy import deepcopy
from pandas.tseries.offsets import BDay
from matplotlib import cm as CM
from matplotlib import patheffects
from statsmodels.graphics.tsaplots import *

warnings.filterwarnings('ignore')  # Hide all warnings in ipython
pd.set_option("display.precision", 4)

# predefined styles
STYLES = ['r', 'g', 'b', 'm', 'y', 'k', 'c'] * 10
STYLES1 = map(lambda x: x + 'o-', STYLES)
STYLES2 = map(lambda x: x + 'o-.', STYLES)
STYLES3 = map(lambda x: x + 'o', STYLES)

# predefined figure size
FIGURE_SIZE = (14, 3)
FIGURE_SIZE2 = (14, 6)


def next_business_day(d, num=1):
  """d - str
  """
  d = datetime.strptime(d, '%Y-%m-%d') + BDay(num)
  s = str(d.date())
  if s in map(str, yml_holiday['us']['full']):
    return next_business_day(s, 1)
  return s


def prev_business_day(d, num=1):
  """d - str
  """
  d = datetime.strptime(d, '%Y-%m-%d') - BDay(num)
  s = str(d.date())
  if s in map(str, yml_holiday['us']['full']):
    return prev_business_day(s, 1)
  return s


def week_day(d):
  return datetime.strptime(d, '%Y-%m-%d').weekday()


def week_day_str(d):
  s = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
  return s[week_day(d)]


class Volatility(object):
  sql_cache = {}

  def __init__(self, src='MySQL', filename=None):

    if src == 'MySQL':
      self.dbconn = DBConn().get_connection()
      self.dtcond = "and dt>'2014-10'"
      self.tbl = "bar1d"
      self.dat = None

    if src == 'CSV':
      self.dat = pd.read_csv(filename, index_col='dt', parse_dates=True)

  def cached_query(self, sql):
    if Volatility.sql_cache.has_key(sql):
      return Volatility.sql_cache[sql]
    tmp = read_sql(sql, self.dbconn, index_col='dt')
    Volatility.sql_cache[sql] = tmp
    return tmp

  def set_date_condition(self, cond, tbl):
    self.dtcond = cond
    self.tbl = tbl

  def set_symbols(self, syms):
    self.syms = syms

  def get_range(self):
    """Get daily price range"""
    self.dat = None
    for s in self.syms:
      sql = "SELECT dt,h-l AS '{}' FROM {} WHERE s='{}' {} ORDER BY dt".format(
          s, self.tbl, s, self.dtcond)
      # print sql
      if self.dat is not None:
        tmp = self.cached_query(sql)
        self.dat = self.dat.join(tmp)
      else:
        self.dat = self.cached_query(sql)
    return self.dat

  def get_log_range(self):
    """Get logrithm daily price range"""
    self.dat = np.log(self.get_range())
    self.dat = self.dat.replace([np.inf, -np.inf], np.nan)
    return self.dat

  def get_volume(self):
    self.dat = None
    for s in self.syms:
      sql = "SELECT dt,v AS '{}' FROM {} WHERE s='{}' {} ORDER BY dt".format(
          s, self.tbl, s, self.dtcond)
      if self.dat is not None:
        tmp = self.cached_query(sql)
        self.dat = self.dat.join(tmp)
      else:
        self.dat = self.cached_query(sql)
    return self.dat

  def get_bc(self):
    self.dat = None
    for s in self.syms:
      sql = "SELECT dt,bc AS '{}' FROM {} WHERE s='{}' {} ORDER BY dt".format(
          s, self.tbl, s, self.dtcond)
      if self.dat is not None:
        tmp = self.cached_query(sql)
        self.dat = self.dat.join(tmp)
      else:
        self.dat = self.cached_query(sql)
    return self.dat

  def get_wap(self):
    self.dat = None
    for s in self.syms:
      sql = "SELECT dt,w AS '{}' FROM {} WHERE s='{}' {} ORDER BY dt".format(
          s, self.tbl, s, self.dtcond)
      if self.dat is not None:
        tmp = self.cached_query(sql)
        self.dat = self.dat.join(tmp)
      else:
        self.dat = self.cached_query(sql)
    return self.dat

  def get_overnight_volatility(self):
    """overnight volatility"""
    tmp = self.get_signed_overnight_volatility()
    self.dat = abs(tmp)
    return self.dat

  def get_signed_overnight_volatility(self):
    """singed overnight volatility"""
    self.dat = None
    for s in self.syms:
      oname = '{}Open'.format(s)
      cname = '{}Close'.format(s)
      sql = "SELECT dt,o AS {},c as {} FROM {} WHERE s='{}' {} ORDER BY dt".format(
          oname, cname, self.tbl, s, self.dtcond)
      tmp = self.cached_query(sql)

      OL = tmp[oname][1:]
      CL = tmp[cname][0:(tmp[cname].size - 1)]
      idx = OL.index
      x = OL.tolist()
      y = CL.tolist()
      onvol = [x[i] - y[i] for i in xrange(len(x))]  # overnight volatility
      tmp = pd.DataFrame(onvol, columns=[s], index=idx)
      if self.dat is not None:
        self.dat = self.dat.join(tmp)
      else:
        self.dat = tmp
    return self.dat

  def get_signed_daily_volatility(self):
    """daily volatility"""
    self.dat = None
    for s in self.syms:
      sql = "SELECT dt,c-o as {} FROM {} WHERE s='{}' {} ORDER BY dt".format(
          s, self.tbl, s, self.dtcond)
      tmp = self.cached_query(sql)
      if self.dat is not None:
        self.dat = self.dat.join(tmp)
      else:
        self.dat = tmp
    return self.dat

  def get_cashflow(self):
    """Get cash flow, where CF = trading volume * weight average price"""
    self.dat = None
    for s in self.syms:
      sql = "SELECT dt,v*w AS '{}' FROM {} WHERE s='{}' {} ORDER BY dt".format(
          s, self.tbl, s, self.dtcond)
      if self.dat is not None:
        tmp = self.cached_query(sql)
        self.dat = self.dat.join(tmp)
      else:
        self.dat = self.cached_query(sql)
    return self.dat

  def get_seasonality_matrix(self):
    d2 = deepcopy(self.dat)
    d2['wd'] = d2.index.map(lambda x: x.weekday())
    # add a new column wd into the dataframe
    # print dd.head()
    ddgroup = d2.groupby('wd')  # volatility by weekday
    ddmean = ddgroup.mean()
    # p0=ddmean.plot(subplots=True, figsize=(25,3), layout=(1, 6),
    #                       style=['r^-.','go-.','bo-.','mo-.','ko-.','ro-.'],
    #                       sharex=True,kind='area',alpha=0.5)
    # print ddmean
    ddmm = ddmean.mean()
    self.smatrix = (ddmean - ddmm) / ddmm + 1
    return self.smatrix

  def get_next_day(self, d, n=1, s='SPY'):
    """nd=v.getNextDay('2014-12-11'); print type(nd[0])"""
    sql = "SELECT dt FROM {} WHERE s='{}' and dt>'{}' limit {}".format(
        self.tbl, s, d, n)
    return read_sql(sql, self.dbconn)['dt']

  def to_csv(sel, fld, FCdt=None):
    if FCdt is None:
      FCdt = YMD
    sel.dat.to_csv(fld + 'vol_{}.csv'.format(FCdt))


def histogram2(data, ax=None):
  """A histogram function for list and pandas time series"""
  BINNUM = 100
  try:
    d = data.replace([np.inf, -np.inf], np.nan)
    low = d.min()
    high = d.max()
    d.hist(bins=np.arange(low, high, (high - low) / BINNUM),
           color='b', alpha=0.4, figsize=FIGURE_SIZE, ax=ax)
    # plt.legend(d.columns)
  except:
    low = min(d)
    high = max(d)
    plt.hist(d, bins=np.arange(
        low, high, (high - low) / BINNUM), color='b', alpha=0.4)


def ts2list(ts, remove_nan=True):
  """pandas series to list"""
  y = ts.tolist()
  if remove_nan:
    return [i for i in y if str(i) != 'nan']
  return y


def heatmap(df):
  """http://stackoverflow.com/questions/20520246/create-heatmap-using-pandas-timeseries"""
  dflen = len(df.index)
  dflen2 = len(df.columns)
  # print dflen, dflen2
  figsize = (1.6 * dflen, .6 * dflen2)
  fig = plt.figure(figsize=figsize)
  ax = fig.add_subplot(111)
  # use dir(matplotlib.cm) to get a list of the installed colormaps
  # the "_r" means "reversed" and accounts for why zero values are plotted
  # as white
  cmap = CM.get_cmap('YlOrRd', 50)
  # http://matplotlib.org/examples/color/colormaps_reference.html
  ax.imshow(df, interpolation="nearest", cmap=cmap)

  # ax.invert_yaxis()
  # ax.xaxis.tick_top()

  v = df.columns.tolist()
  v2 = df.index.tolist()
  ax.set_xticks(np.arange(dflen) + 0., minor=False)
  ax.set_yticks(np.arange(dflen2) + 0., minor=False)
  ax.set_xticklabels(v)
  ax.set_yticklabels(v2)
  ax.grid(True)
  path_effects = [patheffects.withSimplePatchShadow(shadow_rgbFace=(1, 1, 1))]
  for i in range(dflen):
    for j in range(dflen2):
      ax.text(j, i, '{:.2f}'.format(df.iget_value(i, j)),
              size='medium', ha='center', va='center', path_effects=path_effects)
  plt.show()


def Forecast1Day(ss=('BITA', 'SOHU'),
                 Dfrom='2014-01-01', Dto='2014-12-09',
                 useSMatrix=True):
  v = Volatility()
  v.set_symbols(syms=ss)
  v.set_date_condition(" and dt>'{}' and dt<='{}'".format(Dfrom, Dto), "bar1d")
  dd = v.get_log_range()
  vf = v.forecast()
  nd = next_business_day(Dto)
  # print nd

  m = v.get_seasonality_matrix()
  mByWD = m.iloc[[week_day(nd)]]
  if useSMatrix:
    pass
  else:
    mByWD.ix[:, :] = 1
  adjustedVol = vf.values * mByWD

  ############################################################
  v2 = Volatility()
  v2.set_symbols(syms=ss)
  v2.set_date_condition(" and dt='{}'".format(nd), "bar1d")
  realizedVol = v2.get_log_range()
  if len(realizedVol.index) == 0:
    return (None, None, None)

  ############################################################
  adjustedVol = adjustedVol.set_index(realizedVol.index)
  forecastError = (adjustedVol - realizedVol)
  return (forecastError, realizedVol, adjustedVol)


def backtest(ss,
             training_head='2014-08-01',
             training_tail="2014-10-01",
             useSMatrix=True):
  fe = None
  d0 = None
  vf = None
  for i in xrange(100):
    (fe_, d0_, vf_) = Forecast1Day(ss,
                                   Dfrom=training_head,
                                   Dto=training_tail,
                                   useSMatrix=useSMatrix)
    if fe_ is None:
      break
    if fe is not None:
      fe = pd.concat([fe, fe_])
      d0 = pd.concat([d0, d0_])
      vf = pd.concat([vf, vf_])
    else:
      fe = fe_
      d0 = d0_
      vf = vf_
    training_tail = next_business_day(training_tail)
  return (fe, d0, vf)


def acfpacf(mydata, t, FIGURE_SIZE=FIGURE_SIZE):
  fig = plt.figure(figsize=FIGURE_SIZE)
  ax1 = fig.add_subplot(121)
  fig = plot_acf(mydata, ax=ax1)
  p = plt.title('{} (ACF)'.format(t))
  plt.grid(True)
  ax2 = fig.add_subplot(122)
  fig = plot_pacf(mydata, lags=40, ax=ax2)
  plt.grid(True)
  p = plt.title('{} (PACF)'.format(t))


def VolWithWD(ddgroup, s):
  # cs='rybgmk' # red -Monday, yellow- Tuesday ...
  for n, g in ddgroup:  # print n, g
    # g[s].plot(figsize=FIGURE_SIZE,kind='line',style=STYLES3[n],alpha=0.8, legend=False, markersize=8).legend(
    #        ['Mon','Tue','Wed','Thu','Fri'],loc='center left', bbox_to_anchor=(1, 0.5))
    g[s].plot(figsize=FIGURE_SIZE, kind='kde', style=STYLES[n]).legend(
        ['Mon', 'Tue', 'Wed', 'Thu', 'Fri'], loc='center left', bbox_to_anchor=(1, 0.5))
    # plt.axvline(x=g[s].mean(), ymin=0, ymax=1.2, color=STYLES[n])
  for n, g in ddgroup:  # print n, g
    plt.axvline(x=g[s].mean(), ymin=0, ymax=1.2,
                color=STYLES[n], alpha=1, lw=1)
    # for n, g in ddgroup:#print n, g
    #    plt.axvline(x=g[s].median(), ymin=0, ymax=1.2, color=STYLES[n],alpha=1, lw=1)


def VolLineWithWD(ddgroup, s):
  for n, g in ddgroup:  # print n, g
    g[s][-15:].plot(figsize=FIGURE_SIZE, kind='line', style=STYLES1[n], alpha=0.8, legend=False, markersize=8).legend(
        ['Mon', 'Tue', 'Wed', 'Thu', 'Fri'], loc='center left', bbox_to_anchor=(1, 0.5))


def FridayEffect(d2, sym):
  fig = plt.figure(figsize=FIGURE_SIZE)

  xy = d2[[sym, 'wd']]
  p = xy[sym].plot(kind='line', alpha=0.8, legend=True)
  for i in range(5):
    x = xy.index[xy['wd'] == i]
    y = xy[xy['wd'] == i][sym].values

    plt.plot(x, y, STYLES[i] + 'o', markersize=12, alpha=0.5)


def getwds(d2, sym):
  wds = [None] * 5
  rs = []
  for dt, row in d2.T.iteritems():
    wds[int(row['wd'])] = row[sym]
    if row['wd'] == 4:
      rs.append(list(wds))
  return rs


def compareWD(rs):
  global j
  j = 1
  fig = plt.figure(figsize=FIGURE_SIZE2)

  def __compareWD(rs, idx0, idx1):
    global j
    r0 = [(i[idx0] - i[idx1]) for i in rs if i[idx0] is not None]
    tmp = 1.0 * len([i for i in r0 if i >= 0]) / len([i for i in r0 if i < 0])
    # print "up:" + str(tmp/(1+tmp)) + " down:" + str(1/(tmp+1))
    plt.subplot(2, 2, j)
    j = j + 1
    p = plt.plot(r0, STYLES[idx0] + 'o-', markersize=6)
    plt.title('({}-{})'.format(idx0, idx1) +
              "up:{0:.2f} down:{1:.2f}".format(tmp / (1 + tmp), 1 / (tmp + 1)))
    plt.grid(True)
    p = plt.axhline(y=0)

  __compareWD(rs, 0, 1)
  __compareWD(rs, 1, 2)
  __compareWD(rs, 2, 3)
  __compareWD(rs, 3, 4)


def DrawDict(cm):
  fig = plt.figure(figsize=(12, 2))
  sr = pd.Series(data=cm.values(), index=cm.keys())
  sr.plot(style='go-.', alpha=0.8, legend=False, markersize=12)
  plt.bar(range(len(cm)), cm.values(), align='center', alpha=0.5)
  plt.xticks(range(len(cm)), cm.keys())


def VolByWD(dd, sym='SPY'):
  # http://stackoverflow.com/questions/21646710/pandas-pivot-table-using-index-data-of-dataframe
  df = dd.reset_index()
  ddp = df.pivot('dt', 'wd', sym)
  # ddp=ddp.resample('1W', how='sum')
  p0 = ddp.plot(subplots=True, figsize=[i * 1.5 for i in FIGURE_SIZE], layout=(1, 5), style=STYLES1,
                sharex=True, kind='line', alpha=1)  # .legend(loc='center left', bbox_to_anchor=(1, 0.5))
  # http://stackoverflow.com/questions/4700614/how-to-put-the-legend-out-of-the-plot
  p1 = ddp.plot(subplots=False, figsize=[i * 1.5 for i in FIGURE_SIZE], style='o-.', sharex=True, kind='line',
                alpha=1).legend(
      loc='center left', bbox_to_anchor=(1, 0.5))


if __name__ == "__main__":
  '''
  Dfrom='2014-05-01'
  Dto = '2014-12-09'
  ss=('SINA','NTES','QIHU','CTRP','ATHM', 'WB','SOHU','YY','BITA','RENN','WUBA','CYOU','QUNR','SPY','FXI','DXJ')
  (fe,d0,vf) = backtest(ss, '2014-08-01', '2014-11-21', False)'''

  Dfrom = '2014-05-01'
  Dto = '2014-12-09'

  v = Volatility()
  v.set_date_condition(" and dt>'{}' and dt<='{}'".format(Dfrom, Dto), "bar1d")
  ss = ('SINA', 'NTES', 'QIHU', 'CTRP', 'ATHM', 'WB', 'SOHU', 'YY',
        'BITA', 'RENN', 'WUBA', 'CYOU', 'QUNR', 'SPY', 'FXI', 'DXJ')
  v.set_symbols(syms=ss)

  '''
    logd=v.getLogRange()
    sov=v.getSignedOV()
    sdv=v.getSignedDV()
    m=len(sdv.columns)

    SYM='SPY'
    # We can use dd.index.map, too!!
    d2=logd
    d2['wd'] = d2.index.map(lambda x: x.weekday()) # add a new column wd into the dataframe
    FridayEffect(d2,SYM)
    rs=getwds(d2,SYM)
    compareWD(rs)'''

  ov = v.get_overnight_volatility()
  ovw = deepcopy(ov)
  ovw['wd'] = ovw.index.map(lambda x: x.weekday())
  ddgroup = ovw.groupby('wd')  # volatility by weekday
  ddmean = ddgroup.mean()
  m = len(ddmean.columns)
  # print m
  p0 = ddmean.plot(subplots=True, figsize=FIGURE_SIZE2, layout=(
      3, m / 3 + 1), style=STYLES1, kind='line', title="Weekday Effect of OV")

  SYM = 'QUNR'
  FridayEffect(ovw, SYM)
  rs = getwds(ovw, SYM)
  compareWD(rs)

  plt.show()
