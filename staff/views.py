from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth import authenticate
from django.db import connection
from .models import CustomUser

# Serializer for the CustomUser model
class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'role']

@api_view(['POST'])
def login_user(request):
    """POST /api/login/ - Authenticates a user."""
    print("\n--- LOGIN ATTEMPT ---")
    print(f"Received data: {request.data}")
    try:
        username = request.data.get('username')
        password = request.data.get('password')
        role = request.data.get('role')
        
        if not all([username, password, role]):
            print("DEBUG: Missing username, password, or role.")
            return Response({'status': 'error', 'message': 'All fields are required'}, status=400)
        
        user = authenticate(username=username, password=password)
        print(f"Authenticate() result: {user}")
        
        if user is None:
            print("DEBUG: Invalid credentials. 'authenticate' returned None.")
            return Response({'status': 'error', 'message': 'Invalid username or password'}, status=401)
        
        if user.role.upper() != role.upper():
            print(f"DEBUG: Role mismatch. DB role: {user.role.upper()}, Request role: {role.upper()}")
            return Response({'status': 'error', 'message': 'Role mismatch'}, status=401)
        
        if not user.is_active:
            print("DEBUG: User account is inactive.")
            return Response({'status': 'error', 'message': 'User account is inactive'}, status=401)
        
        print("--- LOGIN SUCCESSFUL ---\n")
        serializer = CustomUserSerializer(user)
        return Response({'status': 'success', 'message': 'Login successful', 'data': serializer.data})
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return Response({'status': 'error', 'message': str(e)}, status=500)

@api_view(['GET'])
def health_check(request):
    """GET /api/health/ - Checks API and database connectivity."""
    try:
        connection.cursor().execute("SELECT 1")
        return Response({'status': 'success', 'message': 'API is running and DB is connected'})
    except Exception as e:
        return Response({'status': 'error', 'message': str(e)}, status=503)

@api_view(['GET'])
def list_doctors(request):
    """GET /api/doctors/ - Returns a list of DOCTORs."""
    doctors = CustomUser.objects.filter(role='DOCTOR')
    serializer = CustomUserSerializer(doctors, many=True)
    return Response({'status': 'success', 'data': serializer.data})

@api_view(['GET'])
def list_nurses(request):
    """GET /api/nurses/ - Returns a list of NURSEs."""
    nurses = CustomUser.objects.filter(role='NURSE')
    serializer = CustomUserSerializer(nurses, many=True)
    return Response({'status': 'success', 'data': serializer.data})
