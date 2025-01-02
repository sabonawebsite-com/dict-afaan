from flask import Flask, render_template, request, redirect, flash  
from flask_sqlalchemy import SQLAlchemy  

app = Flask(__name__)  
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///father_dictionary.db'  
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  
app.secret_key = 'your_secret_key'  # Replace with a real secret key  
db = SQLAlchemy(app)  

# Database Model  
class Father(db.Model):  
    term = db.Column(db.String, primary_key=True)  
    definition = db.Column(db.String)  

# Initialize the database  
with app.app_context():  
    db.create_all()  

@app.route('/')  
def index():  
    all_terms = Father.query.all()  
    return render_template('index.html', terms=all_terms)  

@app.route('/search', methods=['POST'])  
def search():  
    term = request.form.get('term', '').strip().lower()  
    result = Father.query.filter_by(term=term).first()  
    if result:  
        flash(f'Definition: {result.definition}', 'success')  
    else:  
        flash('Not found in the database.', 'warning')  
    return redirect('/')  

@app.route('/add', methods=['POST'])  
def add_record():  
    term = request.form.get('new_term', '').strip()  
    definition = request.form.get('new_definition', '').strip()  
    if term and definition:  
        new_entry = Father(term=term, definition=definition)  
        try:  
            db.session.add(new_entry)  
            db.session.commit()  
            flash('Record added successfully.', 'success')  
        except:  
            flash('Term already exists.', 'warning')  
        finally:  
            return redirect('/')  
    flash('Both fields are required to add a record.', 'warning')  
    return redirect('/')  

@app.route('/delete/<term>', methods=['POST'])  
def delete_record(term):  
    entry = Father.query.filter_by(term=term).first()  
    if entry:  
        db.session.delete(entry)  
        db.session.commit()  
        flash(f'Record "{term}" deleted successfully.', 'success')  
    return redirect('/')  

if __name__ == '__main__':  
    app.run(debug=True)