from flask import Flask, request, render_template, redirect, flash, session

# Imports Survey variables from surveys.py
from surveys import satisfaction_survey 

app = Flask(__name__)
app.secret_key = 'secret_key'

# Instantiate Root Directory:
@app.route('/', methods=['GET', 'POST'])
def index():
    title = satisfaction_survey.title
    instructions = satisfaction_survey.instructions
    return render_template('index.html', survey_title=title, survey_instructions=instructions)

# Dynamic instantiation of URL, based on question #
@app.route('/questions/<int:qid>')
def show_question(qid):
    # Check if the user is trying to access questions out of order
    if qid != len(session.get('responses', [])):
        flash('Please answer the questions in order.')
        return redirect(f"/questions/{len(session.get('responses', []))}")

    question = satisfaction_survey.questions[qid]
    return render_template('question.html', question=question, qid=qid)

# Initializes the start of the survey
@app.route('/start', methods=['POST'])
def start_survey():
    session['responses'] = []
    return redirect('/questions/0')

# Handles server-side response back to client
@app.route('/answer', methods=["POST"])
def handle_answer():
    # Get the user's answer
    answer = request.form['answer']

    # Appends the answer to the responses in the session
    responses = session.get(['responses'],[])
    responses.append(answer)
    session['responses'] = responses

    if len(responses) == len(satisfaction_survey.questions):
        return redirect('/thankyou')

    return redirect(f'/questions/{len(responses)}')

# Handles Completion of Survey
@app.route('/thankyou')
def thank_you():
    return '<h1>Thank You for completing the survey!</h1>'

if __name__ == "__main__":
    app.run(debug=True)
