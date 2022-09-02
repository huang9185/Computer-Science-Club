from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from .models import *

import re
import json

def index(request):
    return render(request, 'diet/index.html')

@login_required
def profile(request):
       
    # Get the profile page
    if request.method == "GET":

        records = Record.objects.filter(user_id=request.user.id).order_by('time').reverse()

        if Record.objects.filter(user_id=request.user.id).count() > 0:

            # Check if type exist
            if request.GET.get('type'):
                search_type = request.GET.get('type')
                search_input = request.GET.get('searchInput')
                if search_type == 'date':
                    records = records.filter(time__day=search_input)
                elif search_type == 'month':
                    records = records.filter(time__month=search_input)
                elif search_type == 'year':
                    records = records.filter(time__year=search_input)
                else:
                    return render(request, 'diet/profile.html', {
                        "message": "No matching records"
                    })
            else:
                search_type = False

            if not records.count() > 0:
                return render(request, 'diet/profile.html', {
                    "message": "No matching records"
                })

            # Implement pagination
            paginator = Paginator(records, 15)
            page_obj = paginator.get_page(request.GET.get('page'))

            # Create a list including page numbers
            pre_nums = []
            try:
                page_number = int(request.GET.get('page'))
            except:
                page_number = 1
            for num in range(page_number - 2, page_number):
                pre_nums.append(num)

            nex_nums = []
            for num in range(page_number + 1, page_number + 3):
                nex_nums.append(num)

            index_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]

            if not page_obj.has_previous():
                previous_page_number = False
            else:
                previous_page_number = page_obj.previous_page_number()
            if not page_obj.has_next():
                next_page_number = False
            else:
                next_page_number = page_obj.next_page_number()

            if search_type:
                return render(request, 'diet/profile.html', {
                    "message": "User records collected",
                    "page_obj": record_serialize(page_obj),
                    "pre": pre_nums,
                    "nex": nex_nums,
                    "type": search_type,
                    "searchInput": search_input,
                    "next_page_number": next_page_number,
                    "has_next": page_obj.has_next(),
                    "number": page_obj.number,
                    "previous_page_number": previous_page_number,
                    "has_previous": page_obj.has_previous()
                })
            return render(request, 'diet/profile.html', {
                "message": "User records collected",
                "page_obj": record_serialize(page_obj),
                "pre": pre_nums,
                "nex": nex_nums,
                "next_page_number": next_page_number,
                "has_next": page_obj.has_next(),
                "number": page_obj.number,
                "previous_page_number": previous_page_number,
                "has_previous": page_obj.has_previous()
            })
        else:
            return render(request, 'diet/profile.html', {
                "message": "No records yet"
            })
    
    # Record only for POST request
    elif request.method == 'POST':
        
        # Load data
        vf = request.POST.get("vf")
        other = request.POST.get("other")
        liquid = request.POST.get("liquid")
        grain = request.POST.get("grain")
        protein = request.POST.get("protein")
        # Create object
        record = Record(
            user_id=request.user.id,
            vf_amt=vf,
            protein_amt=protein,
            grain_amt=grain,
            other_amt=other,
            liquid_amt=liquid
        )
        record.save()

        return render(request, 'diet/index.html', {
            "message": "Data recorded"
        })

def record_serialize(records, num=15):
    rec= []
    for record, index in zip(records, range(1, 16)):
        new = {
            "index": index,
            "time": record.time,
            "vf_amt": record.vf_amt,
            "protein_amt": record.protein_amt,
            "grain_amt": record.grain_amt,
            "liquid_amt": record.liquid_amt,
            "other_amt": record.other_amt,
            "id": record.pk
        }
        rec.append(new)
    return rec

@csrf_exempt
@login_required
def intake_calculator(request, calc_type):
    # Only when request is from intake form submittion
    if request.method == 'POST':

        # Load data
        foods = json.loads(request.body)["intake_amt"]
        if foods == [""]:
            return JsonResponse({
                "error": "At least one food required."
            }, status=400)

        if calc_type == 'group':
            vegfru_groups = [1, 2, 3, 8, 24]
            protein_groups = [4, 10, 13, 14, 16, 19]
            grain_groups = [5, 6]
            liquid_groups = [7, 9, 15]

        else:
            vegfru_groups = [1, 2, 3, 4, 7, 8, 10, 14, 15, 16, 18, 19, 20, 22, 23, 27, 38, 45, 75, 80, 99, 108, 117, 118]
            protein_groups = [5, 12, 21, 25, 26, 32, 37, 39, 40, 41, 42, 43, 44, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 58, 59, 72, 77, 86, 88, 112, 120]
            grain_groups = [9, 11, 24, 30, 31, 33, 66, 74, 87, 95, 104, 105, 109, 115]
            liquid_groups = [13, 17, 57, 76, 89, 94]

        vegfru_amt = 0
        protein_amt = 0
        grain_amt = 0
        liquid_amt = 0
        others_amt = 0

        group_name_list = []
        subgroup_name_list = []

        for food in foods:

            name = food["name"]
            amt = int(food["amt"])

            # Get the group of food
            group_id = Food.objects.get(name=name).group_id
            subgroup_id = Food.objects.get(name=name).subgroup_id
            group_name_list.append(Foodgroup.objects.get(pk=group_id).group_name)
            subgroup_name_list.append(Subgroup.objects.get(pk=subgroup_id).name)


            if calc_type == 'group':
                type_id = group_id
            else:
                type_id = subgroup_id

            # Organize amt according to group
            if type_id in vegfru_groups:
                vegfru_amt += amt
            elif type_id in protein_groups:
                protein_amt += amt
            elif type_id in grain_groups:
                grain_amt += amt
            elif type_id in liquid_groups:
                liquid_amt += amt
            else:
                others_amt += amt

        return JsonResponse({
            "chart_list":[vegfru_amt, protein_amt, grain_amt, others_amt],
            "liquid_amt": liquid_amt,
            "group_names": group_name_list,
            "subgroup_names": subgroup_name_list
            }, safe=False)

@login_required
def intake(request, calc_type):
    if request.method == 'GET':

        # Get a list of food names
        li = Food.objects.values_list('name', flat=True)
        return render(request, 'diet/intake.html', {
            'food_name_list': li,
            'type': calc_type
        })

# Deleted: post method, render intake html with type

@csrf_exempt
def password(request):

    # From login page
    if request.method == 'GET':
        return render(request, 'diet/password.html')

    # From password json fetch (Verify being submitted)
    elif request.method == 'POST':
        data = json.loads(request.body)
        username = data['username']
        email = data['email']

        if User.objects.filter(username=username).filter(email=email).count() > 0:
            user = User.objects.filter(username=username).get(email=email)
            return JsonResponse({
                'id': user.pk,
                'message': 'User existed'
            }, safe=False)
        else:
            return JsonResponse({
                'error': 'User does not exist'
            }, safe=False)
    
    # From password put fetch (Password being submitted)
    else:
        data = json.loads(request.body)
        user_id = data['id']
        password = data['password']
        user = User.objects.get(pk=user_id)
        user.set_password(password)
        user.save()

        return JsonResponse({
            'message': 'Password changed successfully'
        }, safe=False)

def register(request):
    # If from register form submittion
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        confirmPass = request.POST.get('passwordConfirm')
        # If username contains spaces or is empty
        if len(username) == 0:
            message = "Username is invalid"
        # If password is invalid
        elif len(password) < 8 or len(password) > 26:
            message = "Password is invalid"
        # If confirmed password is not the same
        elif confirmPass != password:
            message = "Two passwords entered are not the same"
        elif '@' not in email:
            message="Email format is not valid"
        else:
            message = False

        # Reject submittion
        if message:
            return render(request, "diet/register.html", {
                "message": message
            })
        else:
            # Attempt to create new user
            try:
                user = User.objects.create_user(username, email, password)
                user.save()
            except IntegrityError:
                return render(request, "diet/register.html", {
                    "message": "Username already taken."
                })

            login(request, user)

            return render(request, "diet/index.html")


    # If from navigation bar
    else:
        return render(request, "diet/register.html")

def login_view(request):
    # If request comes from login.html
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=str(password))
        # If user exists and password is correct
        if user is not None:
            login(request, user)
            return render(request, 'diet/index.html', {
                'message': "Logged in successfully"
            })
        else:
            return render(request, 'diet/login.html', {
                'messege': "Username or password does not exist"
            })
    # If request comes from navigation bar
    else:
        return render(request, 'diet/login.html')

@login_required
def logout_view(request):
    logout(request)
    return render(request, 'diet/index.html', {
        'message': "Logged out successfully"
    })