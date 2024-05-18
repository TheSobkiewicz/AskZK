from django.http import JsonResponse
from .models import Form, Question, PossibleValue
from django.db.models import Count
from django.views.decorators.http import require_GET, require_POST
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
@require_POST
def data(request):
    try:
        data = json.loads(request.body)
        form_hash = data.get('form_hash')
        if not form_hash:
            return JsonResponse({'error': 'Form hash is required.'}, status=400)
        form_instance = Form.objects.get(hash=form_hash)
        
        questions_with_answers_count = []
        for question in form_instance.questions.all():
            answers = question.possible_values.annotate(num_answers=Count('answers')).order_by('-num_answers')
            answers_data = [{'value': answer.value, 'count': answer.num_answers} for answer in answers]
            total_answers_count = sum(answer.num_answers for answer in answers)
            questions_with_answers_count.append({
                'question': question.value,
                'total_answers_count': total_answers_count,
                'answers': answers_data
            })

        form_details = {
            'form_id': str(form_instance.id),
            'form_hash': form_instance.hash,
            'questions_with_answers_count': questions_with_answers_count
        }

        return JsonResponse(form_details, json_dumps_params={'indent': 4})
    except Form.DoesNotExist:
        return JsonResponse({'error': 'Form with the provided hash does not exist.'}, status=404)

@require_GET    
def form(_, form_id):
    try:
        form_instance = Form.objects.get(id=form_id)

        questions_data = []
        for question in form_instance.questions.all():
            possible_values_data = []
            for possible_value in question.possible_values.all():
                possible_values_data.append({'value': possible_value.value})
            questions_data.append({
                'value': question.value,
                'possible_values': possible_values_data,
                'multi': question.multi
            })

        form_details = {
            'FORM': {
                'questions': questions_data
            }
        }

        return JsonResponse(form_details, json_dumps_params={'indent': 4})
    except Form.DoesNotExist:
        return JsonResponse({'error': 'Form with the provided ID does not exist.'}, status=404)
    
@csrf_exempt
@require_POST
def create(request):
    try:
        data = json.loads(request.body)
        form_data = data.get('form')

        if not isinstance(form_data, dict):
            return JsonResponse({'error': 'Invalid form data format. Expected a dictionary.'}, status=400)

        new_form = Form.objects.create()
        index = 0
        for question_key, question_data in form_data.items():
            if not isinstance(question_data, dict):
                return JsonResponse({'error': f'Invalid question data format for question "{question_key}". Expected a dictionary.'}, status=400)
            
            value = question_data.get('value')
            if not value:
                return JsonResponse({'error': f'Missing "value" key for question "{question_key}".'}, status=400)

            new_question = Question.objects.create(value=value, form=new_form, order=index)
            index += 1

            possible_values = question_data.get('possible_values', [])
            if not isinstance(possible_values, list):
                return JsonResponse({'error': f'Invalid possible values format for question "{question_key}". Expected a list.'}, status=400)

            for possible_value in possible_values:
                if not isinstance(possible_value, str):
                    return JsonResponse({'error': f'Invalid possible value format for question "{question_key}". Expected a string.'}, status=400)
                
                PossibleValue.objects.create(value=possible_value, question=new_question)

        return JsonResponse({'message': 'Form created successfully.', 'form_id': str(new_form.id)})
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON data received in the request.'}, status=400)


