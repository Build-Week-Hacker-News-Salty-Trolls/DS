"""Main application for Salty HN app
"""
import pandas as pd
import numpy as np
from decouple import config
from flask import Flask, json, jsonify, request, send_file, render_template
import psycopg2
from .postgres_helper import select_query
from flask_cors import CORS, cross_origin


# Elephant DB connection info
dbname = config('ESQL_DBNAME')
user = config('ESQL_USER')
password = config('ESQL_PASSWORD')
host = config('ESQL_HOST')


def create_app():
    """Create and config routes"""
    app = Flask(__name__)
#    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#    app.config['SQLALCHEMY_DATABASE_URI'] = config('DATABASE_URL')
    app.config['ENV'] = 'debug'  # TODO change before heroku deployment
#    DB.init_app(app)
    cors = CORS(app)
    app.config['CORS_HEADERS'] = 'Content-Type'
    def saltiest_comments():
        """Query to get the text of the most salty comments.
        Returns a list of (comment, score) tuples. """
        pg_conn = psycopg2.connect(dbname=dbname, user=user,
                                   password=password, host=host)
        pg_curs = pg_conn.cursor()
        salty_comment_query = """SELECT text, salty_score
                                 FROM salt
                                 ORDER BY salty_score asc
                                 LIMIT 100;"""
        results = select_query(pg_conn, salty_comment_query)
        return results

    def saltiest_users():
        """Query to get the names of the most salty users.
        Returns a list of (user, score) tuples. """
        pg_conn = psycopg2.connect(dbname=dbname, user=user,
                                   password=password, host=host)
        # pg_curs = pg_conn.cursor()
        salty_user_query = """SELECT author, SUM(salty_score) AS total_score, ranking 
                              FROM salt
                              GROUP BY author, ranking
                              ORDER BY total_score ASC
                              LIMIT 100;"""
        results = select_query(pg_conn, salty_user_query)
        return results

    def user_comments(name="wnight"):
        """Query to get the text of a particular user and their salt scores.
        Returns a list of (comment, score) tuples. """
        pg_conn = psycopg2.connect(dbname=dbname, user=user,
                                   password=password, host=host)
        pg_curs = pg_conn.cursor()
        salty_comments_query = f"""SELECT author, text, salty_score
                              FROM salt
                              WHERE author = '{name}'
                              ORDER BY salty_score asc
                              LIMIT 10;"""
        results = select_query(pg_conn, salty_comments_query)
        return results


    def dump():
        """Query to get all data"""
        pg_conn = psycopg2.connect(dbname=dbname, user=user,
                                   password=password, host=host)
        dump_query = """SELECT * FROM salt;"""
        results = select_query(pg_conn, dump_query)
        return results
    
    def user_dump():
        """Query to get all users"""
        pg_conn = psycopg2.connect(dbname=dbname, user=user,
                                   password=password, host=host)
        user_dump_query = """SELECT author, SUM(salty_score) as total_score, ranking
                             FROM salt
                             GROUP BY author, ranking;
                           """
        results = select_query(pg_conn, user_dump_query)
        return results

    @app.route("/user-dump")
    def uset_dump_list():
        results = user_dump()
        results = results.to_json(orient = 'records')
        return results

    @app.route("/salty-users")
    def user_list():
        results = saltiest_users()
        results = results.to_json(orient = 'records')
        return results

    @app.route("/salty-comments")
    def comment_list():
        results = saltiest_comments()
        results = results.to_json(orient = 'records')
        return results

    @app.route("/user-comments/<name>", methods=['GET'])
    def user_comments_list(name):
        results = user_comments(name)
        results = results.to_json(orient = 'records')
        return results

    @app.route("/dump", methods = ['GET'])
    def dump_list():
        results = dump()
        results = results.to_json(orient = 'records')
        return results

    @app.route("/dump", methods = ['GET'])
    def dump_list():
        results = dump()
        results = results.to_json(orient = 'records')
        return results

    return app