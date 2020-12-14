#!/user/bin/python
# _*_ coding:utf-8 _*_
__author__ = "super.gyk"

import sqlite3

import click
from flask import current_app, g
from flask.cli import with_appcontext


# 创建数据库连接
def get_db():
    """
    g 是一个特殊对象，独立于每一个请求。在处理请求过程中，
    它可以用于储存 可能多个函数都会用到的数据。把连接储存于其中，
    可以多次使用，而不用在同一个 请求中每次调用 get_db 时都创建一个新的连接。
    :return:
    """
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


# 关闭数据库连接
def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()


# 初始化数据库
def init_db():
    """
    open_resource() 打开一个文件，该文件名是相对于 flaskr 包的；
    get_db 返回一个数据库连接，用于执行文件中的命令。
    :return:
    """
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))


@click.command('init-db')  # click.command()定义一个名为 init-db 命令行，它调用 init_db 函数，并为用户显示一个成功的消息
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')


def init_app(app):
    """
    close_db 和 init_db_command 函数需要在应用实例中注册，否则无法使用;
    然而，既然我们使用了工厂函数，那么在写函数的时候应用实例还无法使用。
    代替地， 我们写一个函数，把应用作为参数，在函数中进行注册。
    """
    app.teardown_appcontext(close_db)  # 告诉 Flask 在返回响应后进行清理的时候调用此函数。
    app.cli.add_command(init_db_command)  # 添加一个新的 可以与 flask 一起工作的命令。

# 运行 init-db 命令：flask init-db
