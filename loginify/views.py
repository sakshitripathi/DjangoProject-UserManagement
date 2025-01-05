from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import UserDetails
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth import login as django_login
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
def print_hello_world(request):
    return HttpResponse("hello from backend")
def hello_from_template(request):
    return render(request, 'login_app/home.html')
@csrf_exempt
def signup(request):
    if request.method == "POST":
        user_name = request.POST.get("user_name")
        email = request.POST.get("email")
        password = request.POST.get("password")
        
        if UserDetails.objects.filter(email=email).exists():
            messages.error(request, "Email is already registered")
            return redirect("signup")
        user = UserDetails(user_name=user_name, email=email, password=password)
        user.save()
        
        messages.success(request, "Signup successful")
        return redirect("login")
    
    return render(request, 'login_app/signup.html')
@csrf_exempt
def user_login(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        
        try:
            user = UserDetails.objects.get(email=email)
            if user.password == password:
                django_login(request, user)  
                messages.success(request, "Login successful")
                return redirect("success")
            else:
                messages.error(request, "Invalid credentials")
        except UserDetails.DoesNotExist:
            messages.error(request, "Email is not registered")
    
    return render(request, "login_app/userlogin.html")

def success(request):
    return render(request, "login_app/success.html")   
@csrf_exempt     
def get_all_users(request):
    users = UserDetails.objects.all()
    user_data = [{"user_name": user.user_name, "email": user.email} for user in users]
    return JsonResponse({"users": user_data})
def get_user_by_email(request, email):
    try:
        user = UserDetails.objects.get(email=email)
        user_data = {"user_name": user.user_name, "email": user.email}
        return JsonResponse(user_data)
    except UserDetails.DoesNotExist:
        return JsonResponse({"error": "User not found"}, status=404)
@csrf_exempt
def update_user(request, user_name):
    if request.method == "POST":
        try:
            # Retrieve the user based on the unique user_name
            user = UserDetails.objects.get(user_name=user_name)
            
            # Get the new email and password from the request
            new_email = request.POST.get("email")
            new_password = request.POST.get("password")
            
            print(f"Received email: {new_email}, password: {new_password}")
            
            # Check if the email is provided and different from the existing one
            if new_email and new_email != user.email:
                user.email = new_email
            
            # Check if the password is provided and different from the existing one
            if new_password:
                user.password = new_password

            # Save the updated user object
            user.save()

            return JsonResponse({"message": "User updated successfully"})
        
        except UserDetails.DoesNotExist:
            return JsonResponse({"error": "User not found"}, status=404)
    
    return JsonResponse({"error": "Invalid request method"}, status=400)
@csrf_exempt
def delete_user(request, email):
    try:
        user = UserDetails.objects.get(email=email)
        user.delete()
        return JsonResponse({"message": "User deleted successfully"})
    except UserDetails.DoesNotExist:
        return JsonResponse({"error": "User not found"}, status=404)