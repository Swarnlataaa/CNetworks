from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///configurations.db'
db = SQLAlchemy(app)

class Configuration(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    device_name = db.Column(db.String(50), nullable=False)
    config_text = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

@app.route('/')
def index():
    configurations = Configuration.query.all()
    return render_template('index.html', configurations=configurations)

@app.route('/add', methods=['GET', 'POST'])
def add_configuration():
    if request.method == 'POST':
        device_name = request.form['device_name']
        config_text = request.form['config_text']

        new_config = Configuration(device_name=device_name, config_text=config_text)
        db.session.add(new_config)
        db.session.commit()

        return redirect(url_for('index'))

    return render_template('add.html')

@app.route('/rollback/<int:config_id>')
def rollback_configuration(config_id):
    config_to_rollback = Configuration.query.get_or_404(config_id)

    new_config = Configuration(
        device_name=config_to_rollback.device_name,
        config_text=config_to_rollback.config_text
    )

    db.session.add(new_config)
    db.session.commit()

    return redirect(url_for('index'))

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
