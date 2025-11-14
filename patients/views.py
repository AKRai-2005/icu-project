from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Patient

# Serializer for the Patient model, best kept in the same app
class PatientSerializer(serializers.ModelSerializer):
    attending_physician = serializers.StringRelatedField()
    admitted_by = serializers.StringRelatedField()

    class Meta:
        model = Patient
        fields = '__all__' # Exposes all fields from your Patient model

@api_view(['GET', 'POST'])
def list_create_patients(request):
    """
    GET /api/patients/: Retrieves a list of all patients.
    POST /api/patients/: Creates a new patient record.
    """
    if request.method == 'GET':
        try:
            patients = Patient.objects.all().order_by('-admission_date')
            serializer = PatientSerializer(patients, many=True)
            return Response({'status': 'success', 'data': serializer.data})
        except Exception as e:
            return Response({'status': 'error', 'message': str(e)}, status=500)
    
    if request.method == 'POST':
        serializer = PatientSerializer(data=request.data)
        if serializer.is_valid():
            if request.user and request.user.is_authenticated:
                serializer.save(admitted_by=request.user)
            else:
                serializer.save()
            return Response({'status': 'success', 'message': 'Patient created', 'data': serializer.data}, status=201)
        return Response({'status': 'error', 'message': 'Invalid data', 'errors': serializer.errors}, status=400)

@api_view(['GET', 'PUT', 'DELETE'])
def patient_detail_view(request, patient_id):
    """
    Handles GET, PUT, DELETE for a single patient at /api/patients/{id}/.
    """
    try:
        patient = Patient.objects.get(id=patient_id)
    except Patient.DoesNotExist:
        return Response({'status': 'error', 'message': 'Patient not found'}, status=404)

    if request.method == 'GET':
        serializer = PatientSerializer(patient)
        return Response({'status': 'success', 'data': serializer.data})

    elif request.method == 'PUT':
        serializer = PatientSerializer(patient, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'status': 'success', 'message': 'Patient updated', 'data': serializer.data})
        return Response({'status': 'error', 'errors': serializer.errors}, status=400)

    elif request.method == 'DELETE':
        patient.delete()
        return Response({'status': 'success', 'message': 'Patient deleted'}, status=204)
