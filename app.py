from datetime import datetime
from flask import Flask, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Info(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    age = db.Column(db.Integer, default=0)
    job_title = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
# with app.app_context():
#     db.create_all()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        job_title = request.form['job_title']

        new_info = Info(name=name, age=age, job_title=job_title)

        try:
            db.session.add(new_info)
            db.session.commit()
            return redirect('/')
        except:
            return "There was an issue adding your information"

    infos = Info.query.order_by(Info.date_created).all()
    return render_template('index.html', infos=infos)

if __name__ == "__main__":
    app.run(debug=True)
