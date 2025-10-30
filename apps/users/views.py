from django.shortcuts import redirect, render
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator


class LoginView(View):
    template_name = 'users/login.html'
    
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('tasks:task_list')
        return render(request, self.template_name)
    
    def post(self, request):
        try:
            email = request.POST.get('email', '').strip()
            password = request.POST.get('password', '')
            
            if not email or not password:
                messages.error(request, 'Por favor completa todos los campos')
                return render(request, self.template_name)
            
            user = authenticate(request, email=email, password=password)
            
            if user is not None:
                if not user.is_active:
                    messages.error(request, 'Tu cuenta está inactiva')
                    return render(request, self.template_name)
                    
                login(request, user)
                next_url = request.GET.get('next', 'tasks:task_list')
                return redirect(next_url)
            else:
                messages.error(request, 'Credenciales inválidas')
                return render(request, self.template_name)
        
        except Exception:
            messages.error(request, 'Error al procesar el inicio de sesión')
            return render(request, self.template_name)


@method_decorator(csrf_exempt, name='dispatch')
class LogoutView(View):
    """Vista de logout que acepta GET y POST sin requerir CSRF token."""
    
    def post(self, request):
        try:
            logout(request)
        except Exception:
            pass
        return redirect('users:login')
    
    def get(self, request):
        try:
            logout(request)
        except Exception:
            pass
        return redirect('users:login')