from django.shortcuts import render, redirect
from core.forms import SignUpForm, LoginForm, AdminSignUpForm, UpdateForm
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .models import User
from django.http import HttpResponse, JsonResponse
from .serializers import UserListSerializer, UserSerializer
from json import loads
from django.db.models import Q


def index(request):
    """
    Returns dashboard for an authenticated useer, else, it returns the index page
    """
    if request.user.is_authenticated():
        user = request.user
        serialized_user = UserSerializer(user, context={"request": request})
        return render(request, 'dashboard.html', {'user': serialized_user.data, 'title': "Dashboard"})
    else:
        return render(request, 'index.html', {'title': 'Index'})


@login_required
def admin_dashboard(request):
    """
    returns the admin page for admin users only
    """
    return render(request, 'admin_dashboard.html', {'title': 'Admin Dashboard'})


@login_required
def user_list(request):
    """
    Api endpoint view for return all users
    """
    users = User.objects.all()
    serialized_users = UserListSerializer(users, many=True, context={'request': request})
    return JsonResponse(serialized_users.data, safe=False)


@login_required
def user_detail(request, pk):
    try:
        user = User.objects.get(id=pk)
    except User.DoesNotExist:
        return HttpResponse(status=404)
    serialized_user = UserSerializer(user, context={'request': request})
    return JsonResponse(serialized_user.data, safe=False)


@csrf_exempt
@login_required
def update_profile(request):
    """
    Update profile
    """
    if request.method == 'POST':
        if request.POST.get("_method") == "PUT":
            user = request.user
            update_form = UpdateForm(request.POST, request.FILES, instance=user)
            if update_form.is_valid():
                user = update_form.save(commit=False)
                user.skills = loads(request.POST.get('skills'))
                user.interest = loads(request.POST.get('interest'))
                user.save()
                return redirect(index)
            else:
                # return the form object with validation errors
                return render(request, 'update_profile.html', {'title': 'Update', 'update_form': update_form})
    elif request.method == 'GET':
        user = request.user
        update_form = UpdateForm(instance=user)
        serialized_user = UserSerializer(user, context={'request': request})
        return render(request, 'update_profile.html', {'user': serialized_user.data, 'title': 'Update', 'update_form': update_form})
    else:
        return HttpResponse(status=404)


def select_role(request):
    return render(request, 'select_role.html', {'title': "Roles"})


@csrf_exempt
def signup(request, role):
    if request.method == "POST":
        if role == 'admin':
            userform = AdminSignUpForm(request.POST)
        else:
            userform = SignUpForm(request.POST)
        if userform.is_valid():
            user = userform.save()
            user = authenticate(password=userform.cleaned_data.get('password1'), username=userform.cleaned_data.get('username'))
            login(request, user)
            return redirect(index)
        else:
            return render(request, 'signup.html', {'userform': userform})
    else:
        if role == 'admin':
            userform = AdminSignUpForm()
        else:
            userform = SignUpForm()
        return render(request, 'signup.html', {'userform': userform})


@csrf_exempt
def auth(request):
    if request.method == "POST":
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data.get('username')
            password = login_form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                nxt = request.GET.get('next')
                if nxt:
                    return redirect(nxt)
                else:
                    return redirect(index)
            else:
                return redirect(auth)
        else:
            return render(request, 'login.html', {'login_form': login_form})
    else:
        login_form = LoginForm()
        return render(request, 'login.html', {'login_form': login_form})


def logout_user(request):
    logout(request)
    return redirect(auth)


@login_required
def search(request):
    """
    Q encapsulates a SQL expression in a Python object that can be used in database-related operations.
    In general, Q() objects make it possible to define and reuse conditions. This permits the construction
    of complex database queries using | (OR) and & (AND) operators; in particular, it is not otherwise possible to use OR in QuerySets
    """

    q = request.GET.get('q')
    queryset = User.objects.filter(Q(first_name__icontains=q) | Q(last_name__icontains=q) |\
                                   Q(username__icontains=q) | Q(position__icontains=q) | Q(email__icontains=q) | Q(mobile_number__icontains=q))
    serialized_users = UserListSerializer(queryset, many=True, context={'request': request})
    return JsonResponse(serialized_users.data, safe=False)
