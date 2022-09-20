import os

from flask import Flask, current_app
from werkzeug.serving import WSGIRequestHandler
from werkzeug.urls import uri_to_iri

import json
import logging

#
#   werkzeugのロガーのカスタマイズ
#   https://qiita.com/fetaro/items/bfa65b9b4cb5527d51a8
#
# werkzeugロガーの取得
werkzeug_logger = logging.getLogger("werkzeug")
# レベルの変更
#werkzeug_logger.setLevel(logging.INFO)
werkzeug_logger.setLevel(logging.ERROR)
def custom_log_request(self, code="-", size="-"):
    try:
        path = uri_to_iri(self.path)
        msg = "%s %s %s" % (self.command, path, self.request_version)
    except AttributeError:
        msg = self.requestline
    code = str(code)
    werkzeug_logger.info('"%s" %s %s' % (msg, code, size))

# 関数の置き換え
WSGIRequestHandler.log_request = custom_log_request

#
#   Flask appの定義
#
# https://msiz07-flask-docs-ja.readthedocs.io/ja/latest/tutorial/factory.html
def create_app(test_config=None):
    # flaskのロガー
    logging.basicConfig(level=logging.WARNING)
#    logging.basicConfig(level=logging.DEBUG)

    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'dencho.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_json('dencho_config.json', silent=False)
    else:
        # load the test config if passed in
        app.config.from_json(test_config, silent=False)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    # db.init_appをインスタンスに登録
    from . import db
    db.init_app(app)

    # auth blue printをインスタンスに登録
    from . import auth
    app.register_blueprint(auth.bp)

    # document blue printをインスタンスに登録
    from . import document
    app.register_blueprint(document.bp)
    app.add_url_rule('/', endpoint='index')

    return app