# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from flask import Flask, Blueprint, render_template
from flask_dmango import Dmango

app = Flask(__name__)
dmango = Dmango(app)
dmango.register_mongodb('server1', URI='mongodb://test:test@ds061701.mlab.com:61701/pkast')

bp = Blueprint('name1', __name__)


@bp.route('/')
def index():
    print "comeon"
    try:
        db = Dmango.find_mongodb('server1')
        print db, dir(db)
        r1 = db.db['p1'].find()
        print r1.count()
        result = db["p1"].find() #발생위치
        print result
        render_template('index.html', data=result)
    except:
        import traceback
        print traceback.format_exc()

if __name__ == '__main__':
    app.run(debug=True)