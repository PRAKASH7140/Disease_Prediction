from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import pandas as pd

@csrf_exempt
def suggest_medicine_precautions(request):
    if request.method == 'POST':
        try:
            # Parse the request body as JSON
            data = json.loads(request.body)
            disease = data.get('disease')

            if not disease:
                return JsonResponse({'success': False, 'error': 'Disease not provided.'})

            # Fetch medicine and precautions
            medicine_precautions = get_medicine_and_precautions(disease)

            if medicine_precautions:
                return JsonResponse({
                    'success': True,
                    'medicine_precautions': medicine_precautions
                })
            else:
                return JsonResponse({
                    'success': False,
                    'error': 'No data found for the predicted disease.'
                })
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'error': 'Invalid JSON data.'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False, 'error': 'Invalid request method.'})

def get_medicine_and_precautions(disease):
    try:
        # Load the CSV files
        precautions_df = pd.read_csv('./main_app/precautions_df.csv')  # Corrected file name
        medication_df = pd.read_csv('./main_app/medications.csv')     # Corrected file name

        # Fetch precautions
        precautions = precautions_df[precautions_df['Disease'] == disease]
        if not precautions.empty:
            precautions_list = [
                precautions['Precaution_1'].values[0],
                precautions['Precaution_2'].values[0],
                precautions['Precaution_3'].values[0],
                precautions['Precaution_4'].values[0]
            ]
            precautions_str = ", ".join(filter(lambda x: isinstance(x, str), precautions_list))
        else:
            precautions_str = "No precautions available."

        # Fetch medication
        medication = medication_df[medication_df['Disease'] == disease]
        if not medication.empty:
            medication_str = medication['Medication'].values[0]
        else:
            medication_str = "No medication available."

        # Combine precautions and medication
        result = f"Precautions: {precautions_str}\nMedication: {medication_str}"
        return result
    except Exception as e:
        return f"Error fetching data: {str(e)}"