from flask import Flask,render_template,url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql.expression import func
from random import shuffle
import ast

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

app.app_context().push()

questions_tracker = []
class Questions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(100), unique=True, nullable=False)
    correct_answer = db.Column(db.String(50), unique=True, nullable=False)
    wrong_answer = db.Column(db.String(50), unique=True, nullable=False)
    subject = db.Column(db.String(50), unique=False, nullable=False)
    
    def repr(self):
        return '<Questions %r>' % self.id
    
    # def getquestion(request):
    #     return 


@app.route("/")
def home():
    return render_template('homepage.html')

message = []
@app.route("/questions", methods=['GET', 'POST'])
def questions():
    if request.method == 'POST': 
        global results_tracker
        option = request.form['option']
        question = Questions.query.get(request.form['q_a_id'])
        q_a = Questions.query.get(question.id)
        questions_tracker.append(question.id)
        
        if option == question.correct_answer:
            message.append('Correct')
        else:
            message.append('Incorrect')
            
        temp_length = len(message)
            
        if temp_length != 1:
            results_tracker += 1
        else:
            results_tracker = 0
            
        return redirect(url_for('.answers', message = ' '.join(message), q_a= q_a.id, results_tracker = results_tracker, questions_tracker = questions_tracker))
    else:
        q_a = Questions.query.filter(~Questions.id.in_(questions_tracker)).order_by(func.random()).first()
        options = [q_a.correct_answer, q_a.wrong_answer]
        shuffle(options)
        return render_template('quiz_page.html', q_a=q_a.question, q_a_id=q_a.id, option1 = options[0], option2=options[1])

@app.route("/instructions")
def instructions():
    message.clear()
    questions_tracker.clear()
    return render_template('instructions.html')

# had a logical error since i cannot pass list in the url https://www.programiz.com/python-programming/methods/string/join
# I need to convert it back into a list after recieveing it
# we need to get POST
# make a list to keep track of the questions to later so the answers
@app.route("/answers/<message>/<int:q_a>/<int:results_tracker>/<questions_tracker>")
def answers(message,q_a,results_tracker,questions_tracker):
    message = message.split()
    q_a = Questions.query.get(q_a)
    if ((results_tracker) == 0):
        return render_template('answers.html', message = message, q_a = q_a, results_tracker = results_tracker, questions_tracker = questions_tracker)
    elif (results_tracker < 5):
        return render_template('answers.html', message = message, q_a = q_a, results_tracker = results_tracker, questions_tracker = questions_tracker)
    else:
        #https://www.geeksforgeeks.org/python-program-to-convert-list-of-integer-to-list-of-string/
        return redirect(url_for('.results', questions_tracker = list(map(str, questions_tracker)), message = ' '.join(message)))

@app.route("/results/<questions_tracker>/<message>")
def results(questions_tracker, message):
    message = message.split()
    indexes = ast.literal_eval("".join(message))
    score = indexes.count('Correct')
    temp_length = len(indexes)
    #query the questions so that we can get the whole row
    #https://stackoverflow.com/questions/866465/order-by-the-in-value-list // we can use the in_() function
    #https://stackoverflow.com/questions/16158809/sqlalchemy-filter-in-operator
    #eval the list we pass down https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/eval
    questions_tracker = eval(questions_tracker)
    five_questions = Questions.query.filter(Questions.id.in_(questions_tracker)).all()
    return render_template('results.html', questions_tracker = five_questions, message = indexes, score = score, total = temp_length)

if __name__ == "__main__":
    app.run(debug=True)