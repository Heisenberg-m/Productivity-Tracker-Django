from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from .models import Goal,LogEntry
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import timedelta
from django.http import JsonResponse
import json

def landing(request):
    return render(request, 'tracker/landing.html') 

def register(request):
    if request.method == 'POST':

        try:
            fname = request.POST.get('fname', '').strip()
            lname = request.POST.get('lname', '').strip()
            username = request.POST.get('username', '').strip()
            email = request.POST.get('email', '').strip()
            pass1 = request.POST.get('pass1', '').strip()
            pass2 = request.POST.get('pass2', '').strip()


            context = {
                'fname': fname,
                'lname': lname,
                'username': username,
                'email': email,
            }

            if not fname or not lname or not username or not email or not pass1 or not pass2:
                messages.error(request, "Please fill all fields.")
                return render(request, 'tracker/register.html', context)

            if pass1 != pass2:
                messages.error(request, 'Passwords do not match!')
                return render(request, 'tracker/register.html', context)

            
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username already taken!')
                return render(request, 'tracker/register.html', context)

            
            if User.objects.filter(email=email).exists():
                messages.error(request, 'An account with that email already exists!')
                return render(request, 'tracker/register.html', context)

    
            try:
                new_user = User.objects.create_user(
                    username=username,
                    first_name=fname,
                    last_name=lname,
                    email=email,
                    password=pass1
                )

            except Exception as e:

                messages.error(request, "An error occurred while creating your account. Please try again.")
                return render(request, 'tracker/register.html', context)

            messages.success(request, 'Account created successfully! Please login.')
            return redirect('login_view')

        except Exception as e:

            messages.error(request, "Something went wrong. Please try again.")
            return render(request, 'tracker/register.html')

    return render(request, 'tracker/register.html')


def login_view(request):
    if request.method == 'POST':
        uname = request.POST.get('username')
        passw = request.POST.get('pass1')
        
        user = authenticate(request, username=uname, password=passw)

        if user is not None:
            login(request, user)

            return redirect('home')
        
        else:
            messages.error(request, 'Invalid username or password.')
            return redirect('login_view')

    return render(request, 'tracker/login.html')


def logout_view(request):
    logout(request)
    return redirect('login_view')


@login_required
def home(request):
    if Goal.objects.filter(user=request.user).exists():
        return redirect('dashboard')

    if request.method == 'POST':
        try:
            monday = float(request.POST.get('Monday') or 0)
            tuesday = float(request.POST.get('Tuesday') or 0)
            wednesday = float(request.POST.get('Wednesday') or 0)
            thursday = float(request.POST.get('Thursday') or 0)
            friday = float(request.POST.get('Friday') or 0)
            saturday = float(request.POST.get('Saturday') or 0)
            sunday = float(request.POST.get('Sunday') or 0)
             
            Goal.objects.create(
                user=request.user,
                Monday=monday,
                Tuesday=tuesday,
                Wednesday=wednesday,
                Thursday=thursday,
                Friday=friday,
                Saturday=saturday,
                Sunday=sunday
                )
            messages.success(request, 'Your weekly goals have been set!')

            return redirect('dashboard')

        except ValueError:
            messages.error(request, 'Please enter valid numbers for your goals.')
            return redirect('home')

    return render(request, 'tracker/home.html')

@login_required
def edit_goal(request):
    goal = Goal.objects.filter(user=request.user).first()
    if not goal:
        return redirect('home')  

    if request.method == 'POST':
        try:
            goal.Monday = float(request.POST.get('Monday') or 0)
            goal.Tuesday = float(request.POST.get('Tuesday') or 0)
            goal.Wednesday = float(request.POST.get('Wednesday') or 0)
            goal.Thursday = float(request.POST.get('Thursday') or 0)
            goal.Friday = float(request.POST.get('Friday') or 0)
            goal.Saturday = float(request.POST.get('Saturday') or 0)
            goal.Sunday = float(request.POST.get('Sunday') or 0)
            goal.save()
            messages.success(request, 'Your weekly goals have been updated!')
            return redirect('dashboard')
        except ValueError:
            messages.error(request, 'Please enter valid numbers.')
            return redirect('edit_goal')

    return render(request, 'tracker/home.html', {"goal": goal})


@login_required
def dashboard(request):
    today = timezone.now().date()
    user = request.user

    
    if request.method == 'POST':
        try:
            hours_to_add = float(request.POST.get('hours') or 0)

            log_entry, created = LogEntry.objects.get_or_create(
                user=user,
                date=today,
                defaults={'hours': 0}
            )

            log_entry.hours += hours_to_add
            log_entry.save()

            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({
                    'status': 'success',
                    'message': 'Timer hours logged successfully!'
                })

            messages.success(request, 'Hours logged successfully!')
            return redirect('dashboard')

        except ValueError:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({
                    'status': 'error',
                    'message': 'Invalid number of hours.'
                }, status=400)

            messages.error(request, 'Please enter a valid number of hours.')

    
    today_log = LogEntry.objects.filter(user=user, date=today).first()
    today_hours = today_log.hours if today_log else 0


    weekly_goal = Goal.objects.filter(user=user).first()

    if weekly_goal:
        total_target_week = (
            weekly_goal.Monday +
            weekly_goal.Tuesday +
            weekly_goal.Wednesday +
            weekly_goal.Thursday +
            weekly_goal.Friday +
            weekly_goal.Saturday +
            weekly_goal.Sunday
        )

        day_name = today.strftime("%A")
        goal_today = getattr(weekly_goal, day_name, 0)
    else:
        total_target_week = 0
        goal_today = 0

    week_start = today - timedelta(days=today.weekday())
    week_end = week_start + timedelta(days=6)

    week_logs = LogEntry.objects.filter(
        user=user,
        date__range=[week_start, week_end]
    )
    total_completed_week = sum(log.hours for log in week_logs)


    month_logs = LogEntry.objects.filter(
        user=user,
        date__month=today.month,
        date__year=today.year
    )
    total_completed_month = sum(log.hours for log in month_logs)

    total_target_month = total_target_week * 4

    
    all_logs = LogEntry.objects.filter(user=user)
    total_completed_all = sum(log.hours for log in all_logs)

    total_target_all = total_target_week * 52

    
    streak = 0
    day_pointer = today

    while LogEntry.objects.filter(user=user, date=day_pointer).exists():
        streak += 1
        day_pointer -= timedelta(days=1)

    context = {
        'today_date': today.strftime('%A, %b %d, %Y'),
        'today_hours': today_hours,
        'goal_today': goal_today,
        'total_target_week': total_target_week,
        'total_completed_week': total_completed_week,
        'total_target_month': total_target_month,
        'total_completed_month': total_completed_month,
        'total_target_all': total_target_all,
        'total_completed_all': total_completed_all,
        'streak': streak,
    }

    return render(request, 'tracker/dashboard.html', context)


def timer(request):
    return render(request, 'tracker/timer.html')