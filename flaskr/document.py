'''
    ファイルを検索して表示するためのブループリント
    
    t.odaka

'''
#from lib2to3.pytree import _Results
from curses.ascii import isdigit
import os
import urllib
import datetime, re
from dateutil.relativedelta import relativedelta
from pickle import DICT, FALSE
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, current_app, make_response
)
from werkzeug.exceptions import abort
import logging

from flaskr.auth import login_required
from flaskr.db import get_db

from io import StringIO
import csv

bp = Blueprint('document', __name__)

##
#  ファイル属性を取得する。
#
##
def get_file_attr(file_path):
    _r = dict()
    _r["path"] = file_path
    _r["size"] = "{:.1f}".format(os.path.getsize(file_path)/1000.0)
    _r["mtime"] = datetime.datetime.fromtimestamp(os.path.getmtime(file_path)).strftime('%Y-%m-%d %H:%M:%S')
    _r["ctime"] = datetime.datetime.fromtimestamp(os.path.getctime(file_path)).strftime('%Y-%m-%d %H:%M:%S')
    _r["link"] = "download/" + urllib.parse.quote(file_path)
    return _r

##
#  入力された日付フォーマットのチェック（なんちゃってロジック）
#
##
def date_format_check(date_fmt):
    date_pattern = re.compile('(20\d{2})(\d{2})(\d{2})')
    result = date_pattern.search(date_fmt)
    if result:
        y, m, d = result.groups()
#        current_app.logger.debug(y)
        if y < "2021":
            return False
        if m > "12":
            return False
        if d > "31":
            return False
        
        _dt = y+m+d
        if len(_dt) > 8:
            return False
    
        return _dt
    else:
        return False

##
#  ファイル名から金額を抜き出す
# 
##
def get_amount(filename):
    a_pattern = re.compile('\d*')
    results = a_pattern.findall(filename)
#    current_app.logger.debug(results)

    for _r in results:
        if len(_r) > 0 and not date_format_check(_r):
            return str(_r)
    
    return False


##
#  処理日の何ヶ月か前の１日目を取得する
#
##
def get_firstday_month(_mbefore):
    today = datetime.datetime.today()
    thismonth = datetime.datetime(today.year, today.month, 1)
    targetmonth = thismonth - relativedelta(months=int(_mbefore))
    return targetmonth.strftime('%Y%m%d')

##
#  データリストの作成
#
##
def create_datalist(word, sdate, edate, samount, eamount):
    _l = list()
    for _t in current_app.config["DOC_PATH"]:
        # https://www.curict.com/item/48/4807c14.html
        for root, dirs, files in os.walk(top=_t, followlinks=True):
            for file in files:
                if not file.startswith(('.')) \
                    and file.endswith(tuple(current_app.config["DOC_FORMAT"])) \
                    and (current_app.config["DOC_KEY"] in file):

                    # ファイル名から日付と金額を抽出
                    _fd = False
                    _fa = False
                    if date_format_check(file):
                        _fd = date_format_check(file)
                    if get_amount(file):
                        _fa = get_amount(file)

                    # 日付と金額がともに抽出できなければ対象外
                    _er = True
                    if not _fd or not _fa:
                        _er = False

                    # 期間開始日以降のファイル
#                   current_app.logger.debug(date_format_check(file))
                    if _er:
                        current_app.logger.debug(file)
                        current_app.logger.debug(_fa)
                        current_app.logger.debug(samount)
                        if _fd >= sdate:
                            # 期間終了日が指定された場合
                            if len(edate) > 0:
                                if _fd <= edate:
                                    if int(_fa) >= int(samount):
                                        # 金額範囲（上限）が指定されている場合
                                        if len(eamount) > 0:
                                            if int(_fa) <= int(eamount):
                                                # フリーワードが指定された場合
                                                _r = None
                                                if not word is None:
                                                    if word in file:
                                                        file_path = os.path.join(root, file)
                                                        _r = get_file_attr(file_path)
                                                    else:
                                                        pass
                                                else:
                                                    file_path = os.path.join(root, file)
                                                    _r = get_file_attr(file_path)

                                                if _r is not None:
                                                    _l.append( _r )

                                        # 金額範囲（上限）が指定されない場合
                                        else:
                                            # フリーワードが指定された場合
                                            _r = None
                                            if not word is None:
                                                if word in file:
                                                    file_path = os.path.join(root, file)
                                                    _r = get_file_attr(file_path)
                                                else:
                                                    pass
                                            else:
                                                file_path = os.path.join(root, file)
                                                _r = get_file_attr(file_path)

                                            if _r is not None:
                                                _l.append( _r )

                            # 期間終了日が指定されない場合
                            else:
                                if int(_fa) >= int(samount):
                                    # 金額範囲（上限）が指定されている場合
                                    if len(eamount) > 0:
                                        if int(_fa) <= int(eamount):
                                            # フリーワードが指定された場合
                                            _r = None
                                            if not word is None:
                                                if word in file:
                                                    file_path = os.path.join(root, file)
                                                    _r = get_file_attr(file_path)
                                                else:
                                                    pass
                                            else:
                                                file_path = os.path.join(root, file)
                                                _r = get_file_attr(file_path)

                                            if _r is not None:
                                                _l.append( _r )

                                    # 金額範囲（上限）が指定されない場合
                                    else:
                                        # フリーワードが指定された場合
                                        _r = None
                                        if not word is None:
                                            if word in file:
                                                file_path = os.path.join(root, file)
                                                _r = get_file_attr(file_path)
                                            else:
                                                pass
                                        else:
                                            file_path = os.path.join(root, file)
                                            _r = get_file_attr(file_path)

                                        if _r is not None:
                                            _l.append( _r )
    
    return _l


##
#   ファイルリストの検索と表示
#
##
@bp.route('/', methods=('GET', 'POST'))
@login_required
def index():
    word = None
    _em = ''
    _l = list()

    # 入力チェック
    edate = ''
    eamount = ''
    word = ''
    if request.method == 'POST':
        word = request.form['word']
        sdate = request.form['sdate']
        edate = request.form['edate']
        samount = request.form['samount']
        eamount = request.form['eamount']
        if len(sdate) > 0:
            if not date_format_check(sdate):
                _em = "検索開始日が正しくありません"
        if len(_em) == 0:
            if len(edate) > 0:
                if not date_format_check(edate):
                    _em = "検索終了日が正しくありません"
        if len(_em) == 0:
            if len(edate) > 0 and edate < sdate:
                _em = "検索終了日は開始日以降にしてください"
        if len(_em) == 0:
            if len(samount) > 0:
                if not samount.isdecimal():
                    _em = "金額蘭には数字を入力してください"
        if len(_em) == 0:
            if len(eamount) > 0:
                if not eamount.isdecimal():
                    _em = "金額蘭には数字を入力してください"
        if len(_em) == 0:
            if len(samount) > 0 and len(eamount) > 0:
                if samount > eamount:
                    _em = "金額範囲の指定が正しくありません"

    else:
        # GETの場合には絞り込み開始日の初期値をセット。（初回照会時）
        sdate = get_firstday_month(2)
        samount = '0'
#        dt_now = datetime.datetime.now()
#        sdate = dt_now.strftime('%Y%m%d')
#        current_app.logger.debug(sdate)

    if len(_em) == 0:
        # データリストの作成
        _l = create_datalist(word, sdate, edate, samount, eamount)


    return render_template('document/index.html', paths=_l, emsg=_em, sdate=sdate, samount=samount)


##
#   ファイルのダウンロード
#
##
# https://qiita.com/5zm/items/760000cf63b176be544c
@bp.route('/download/<path:file_path>', methods=['GET'])
@login_required
def download(file_path):
    _f = urllib.parse.unquote(file_path)
    current_app.logger.debug(_f)

    if not _f.startswith(('/')):
        _f = '/' + _f
    _res = make_response()
    _res.data = open(_f, "rb").read()
    _fn = file_path.split('/')[-1]

    _res.headers['Content-Disposition'] = 'attachment; filename=' + _fn
    _res.mimetype = 'application/octet-stream'

    return _res


##
#   検索結果のCSVダウンロード
#
##
@bp.route('/csv', methods=['POST'])
@login_required
def dlcsv():
    _em = ''
    _l = list()

    # 入力チェック
    word = request.form['word']
    sdate = request.form['sdate']
    edate = request.form['edate']
    samount = request.form['samount']
    eamount = request.form['eamount']
    if len(sdate) > 0:
        if not date_format_check(sdate):
            _em = "検索開始日が正しくありません"
    if len(_em) == 0:
        if len(edate) > 0:
            if not date_format_check(edate):
                _em = "検索終了日が正しくありません"
    if len(_em) == 0:
        if len(edate) > 0 and edate < sdate:
            _em = "検索終了日は開始日以降にしてください"
    if len(_em) == 0:
        if len(samount) > 0:
            if not samount.isdecimal():
                _em = "金額蘭には数字を入力してください"
    if len(_em) == 0:
        if len(eamount) > 0:
            if not eamount.isdecimal():
                _em = "金額蘭には数字を入力してください"
    if len(_em) == 0:
        if len(samount) > 0 and len(eamount) > 0:
            if samount > eamount:
                _em = "金額範囲の指定が正しくありません"

    if len(_em) > 0:
        return render_template('document/index.html', paths=_l, emsg=_em)

    else:
        # データリストの作成
        _l = create_datalist(word, sdate, edate, samount, eamount)

        # csvデータの作成
#       https://teratail.com/questions/59915
#       Shift-jisに変換するので面倒臭い感じになっている。        
        _sio = StringIO()
        _w = csv.writer(_sio)
        _w.writerow( ["ファイル", "サイズ", "最終更新日時"] )
        for _d in _l:
            _w.writerow( [_d['path'], _d['size']+'KiB', _d['mtime']] )

        _fn = "filenames_{}.csv".format(datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S'))
        _res = make_response()
        _res.data = _sio.getvalue().encode('cp932')
        _res.headers['Content-Disposition'] = 'attachment; filename=' + _fn
        _res.mimetype = 'text/csv'        


        return _res


##
#   config.jsonの内容を表示する
#
## 
@bp.route('/config-info')
@login_required
def config_info():
    _f = dict()
    _f["doc_path"] = current_app.config["DOC_PATH"]
    _f["doc_key"] = current_app.config["DOC_KEY"]
    _f["doc_format"] = current_app.config["DOC_FORMAT"]

    return render_template('document/config_info.html', parms=_f)

