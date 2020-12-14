#!/user/bin/python
# _*_ coding:utf-8 _*_
__author__ = "super.gyk"

import os
from flask import Flask


# create and configure the app
def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # init db
    from . import db
    db.init_app(app)

    # auth
    from . import auth
    app.register_blueprint(auth.bp)

    # blog
    from . import blog
    app.register_blueprint(blog.bp)
    app.add_url_rule('/', endpoint='index')
    # 关联端点名称 'index'和 / URL ，这样url_for('index')或url_for('blog.index')都会有效，会生成同样的 / URL
    return app
