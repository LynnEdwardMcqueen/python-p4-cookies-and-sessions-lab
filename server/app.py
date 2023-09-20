#!/usr/bin/env python3

from flask import Flask, make_response, jsonify, session
from flask_migrate import Migrate



from models import db, Article, User

app = Flask(__name__)
app.secret_key = b'Y\xf1Xz\x00\xad|eQ\x80t \xca\x1a\x10K'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

foo_count = ["Razmataz"]
@app.route('/clear')
def clear_session():
    session['page_views'] = 0
    return {'message': '200: Successfully cleared session data.'}, 200

@app.route('/articles')
def index_articles():

    pass

@app.route('/articles/<int:id>')
def show_article(id):
    print("Made it into show_article")
    article = Article.query.filter(Article.id == id).first().to_dict()

    if (session.get("page_views") == None):
        print("page_views == None")
        foo_count.append("None")
    else:
        froo = session.get("page_views")
        print (f"page_views init = {froo}")
        foo_count.append(froo)
    
    
    # Since the initial request will not have a returning cookie, treat that special case.  Since we
    # desire for the initial value to be 0, initialize it to -1 and then every case works with the increment
    # that comes next.
    session["page_views"] =  session.get("page_views") + 1  if (session.get("page_views") != None) else 0

    foo_count.append(session.get("page_views"))


#    session["page_views"] = session.get("page_views") + 1


    if (session.get("page_views") < 3):
        response = make_response (
            article,
            200
        )
    else:
        response = make_response (
            {'message': 'Maximum pageview limit reached'},
            401
        )

    return response

if __name__ == '__main__':
    app.run(port=5555)
