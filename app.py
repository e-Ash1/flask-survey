
from flask import Flask,request,render_template,redirect

#Imports Survey variables from surveys.py
from surveys import satisfaction_survey 

app = Flask(__name__)

responses=[]
#Instantiate Root Directory:
@app.route('/')
def index():
    title = satisfaction_survey.title
    instructions = satisfaction_survey.instructions
    return render_template('index.html', survey_title=title, survey_instructions=instructions)

#Dynamic instantiation of URL, based on question #
@app.route('/questions/<int:qid>')
def show_question(qid):
    # Check if the user is trying to access questions out of order:
    if qid != len(responses):
        # Redirect to the correct question
        return redirect(f"/questions/{len(responses)}")

    question = satisfaction_survey.questions[qid]
    return render_template('question.html', question=question, qid=qid)

#Handles server-side response back to client:
@app.route('/answer', methods=["POST"])
def handle_answer():
    # Get the user's answer
    answer = request.form['answer']

    # Append the answer to the responses list
    responses.append(answer)

    if len(responses) == len(satisfaction_survey.questions):
        # All questions answered, redirect to thank you page
        return redirect('/thankyou')

    # Redirect to the next question
    return redirect(f'/questions/{len(responses)}')

#Handles Completion of Survey:
@app.route('/thankyou')
def thank_you():
    return '<h1>Thank You for completing the survey!</h1>'



if __name__ == "__main":
    app.run(debug=True)