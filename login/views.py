from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User

from django.contrib import messages

    #  id:
    #    Тип: AutoField (автоинкрементное целое число)
    #    Описание: Уникальный первичный ключ для каждой записи пользователя.
    
    #  password:
    #    Тип: CharField
    #    Описание: Хэшированный пароль пользователя. Django всегда хранит пароли в зашифрованном виде.
    
    #  last_login:
    #    Тип: DateTimeField (с blank=True, null=True)
    #    Описание: Дата и время последнего входа пользователя в систему. Используется для отслеживания активности.
    
    #  is_superuser:
    #    Тип: BooleanField (с default=False)
    #    Описание: Флаг, указывающий, является ли пользователь суперпользователем. Суперпользователи имеют полный доступ ко всем функциям и административному интерфейсу Django.
    
    #  username:  
    #    Тип: CharField
    #    Описание: Уникальное имя пользователя. Это поле обязательно для входа в систему по умолчанию.
    #    Ограничения: Максимальная длина, уникальность.
    
    #  first_name:
    #    Тип: CharField
    #    Описание: Имя пользователя.
    #    Ограничения: Максимальная длина.
    
    #  last_name:
    #    Тип: CharField
    #    Описание: Фамилия пользователя.
    #    Ограничения: Максимальная длина.
   
    #  email:
    #    Тип: EmailField
    #    Описание: Адрес электронной почты пользователя.
    #    Ограничения: Максимальная длина, опционально может быть уникальным (unique=True).
    
    #  is_staff:
    #    Тип: BooleanField (с default=False)
    #    Описание: Флаг, указывающий, является ли пользователь сотрудником (т.е. имеет ли доступ к административному сайту Django, но не обязательно является суперпользователем).
    
    #  is_active:
    #    Тип: BooleanField (с default=True)
    #    Описание: Флаг, указывающий, является ли учетная запись пользователя активной. Неактивные пользователи не могут войти в систему.
   
    #  date_joined:
    #    Тип: DateTimeField (с default=timezone.now)
    #    Описание: Дата и время регистрации пользователя.


# Create your views here.

def Login(request):     
    context = {
        'title': "Вход в личный кабинет",
    }

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        print("Введённый логин:", username,"\nВведённый пароль:", password)

        #user = authenticate(request, username=username, password=password)
        user = User.objects.filter(username=username).exists()

        if user:
            password_cor = authenticate(request, username=username, password=password)
            print("Correct Password: ", password_cor)

            if password_cor:
                if password_cor is not False:
                    print("User Login: ", username)

                    login(request, password_cor)
                    print("\n\nВход в аккаунт по логину ", username, " выполнен успешно!\n\n")
                    return redirect('../')
                
                else:
                    messages.error(request, 'Неправильный логин или пароль')
                    return render(request, 'login/login.html', context)
            else:
                messages.error(request, 'Неправильный логин или пароль')
                return render(request, 'login/login.html', context)
        else:
            return render(request, 'login/login.html', context)
    else:
        return render(request, 'login/login.html', context)

def signup(request):
    return render(request, 'login/signup.html')

def create_user(request):
    context = {
        'title': "Регистрация пользователя",
    }

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        password_confirmation = request.POST.get('password_confirmation')

        if password != password_confirmation:
            messages.error(request, 'Пароли не совпадают')
            return render(request, 'login/signup.html', context)
        
        try:
            user = User.objects.filter(username=username).exists()
            if user:
               messages.error(request, 'Пользователь с таким именем уже существует.')
               return render(request, 'login/signup.html', context)
            
            user = User.objects.create_user(username, "", password)
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return redirect('/')
            else:
                messages.error(request, "Не удалось войти после регистрации, повторите попытку")
                return render(request, 'login/signup.html', context)
        
        except Exception as e:
            messages.error(request, f'Ошибка валидации {e}')
            return render(request, 'login/signup.html', context)
    else:
        return render(request, 'login/signup.html', context)