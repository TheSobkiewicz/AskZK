from forms.models import Form, Question, PossibleValue, Answer
# Create example data
def create_example_data():
    # Create a form
    form = Form.objects.create()

    # Create questions for the form
    question1 = Question.objects.create(form=form, value='What is your age?', order=1)
    question2 = Question.objects.create(form=form, value='What is your gender?', order=2)

    # Create possible values for questions
    possible_value1_q1 = PossibleValue.objects.create(question=question1, value='Under 18')
    possible_value2_q1 = PossibleValue.objects.create(question=question1, value='18-25')
    possible_value3_q1 = PossibleValue.objects.create(question=question1, value='26-35')

    possible_value1_q2 = PossibleValue.objects.create(question=question2, value='Male')
    possible_value2_q2 = PossibleValue.objects.create(question=question2, value='Female')
    possible_value3_q2 = PossibleValue.objects.create(question=question2, value='Other')

    # Create answers
    Answer.objects.create(possible_value=possible_value2_q1)
    Answer.objects.create(possible_value=possible_value1_q2)
    Answer.objects.create(possible_value=possible_value3_q2)
    Answer.objects.create(possible_value=possible_value1_q1)
    Answer.objects.create(possible_value=possible_value2_q2)
    Answer.objects.create(possible_value=possible_value3_q1)
    Answer.objects.create(possible_value=possible_value3_q2)

# Call the function to create example data
create_example_data()
