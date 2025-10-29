from email import message
from django.shortcuts import redirect, render
from django.views import View
from django.contrib.auth import authenticate, login, logout

class LoginView(View):
    template_name = 'users/login.html'
    
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('tasks:task_list')
        return render(request, self.template_name)
    
    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        if not email or not password:
            message.error(request, 'Porfavor completa todos los campos')
            return render(request, self.template_name)
        
        user = authenticate(request, email=email, password=password)
        
        if user is not None:
            login(request, user)
            next_url = request.GET.get('next', 'tasks:task_list')
            return redirect(next_url)
        else:
            message.error(request, 'Credenciales inválidas')
            return render(request, self.template_name)
        
        
class LogoutView(View):
    def post(self, request):
        logout(request)
        return redirect('users:login')
    
    def get(self, request):
        logout(request)
        return redirect('users:login')