from django.shortcuts import render
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
import os
from test_code import remodel_image
from style_transfer import transfer_style
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import json
from chatterbot import ChatBot
from chatterbot.response_selection import get_random_response
import logging
import sys
import os
import datetime
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from .models import RegisterUser
import re
from django.http import HttpResponse
from django.contrib.auth.hashers import check_password
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse
from django.conf import settings
from django.shortcuts import get_object_or_404
import os
import json
from .models import RegisterUser, UserDesigns

def interior_nav(request):
    return render(request, "walk_page.html")

def walktrough_page(request):
    return render(request, "walkthrough.html")

def walktrough_page2(request):
    return render(request, "walkthrough2.html")

def home_page(request):
    return render(request, "home.html")

def login_page(request):
    return render(request, "login.html")


def front_page(request):
    return render(request, "index.html")

def promte_page(request):
    return render(request, "promte.html")

def image_style_page(request):
    return render(request, "image_transfer.html")

def logout(request):
    return render(request, "home.html")

import json
from django.http import JsonResponse
import uuid  # Import for generating unique names


from django.shortcuts import render
from .models import UserDesigns

from django.http import JsonResponse
from .models import UserDesigns
from django.shortcuts import redirect
def user_designs(request):
    user_id = request.session.get('user_id')  # Get logged-in user ID
    if not user_id:
        return redirect('login')  # Redirect if user not logged in

    user_designs = UserDesigns.objects.filter(user_id=user_id)

    # Separate the designs into two lists
    design_generation_list = []
    style_transfer_list = []

    for design in user_designs:
        image_url = f"{settings.MEDIA_URL}{design.image_path}"

        # Clean input_image_path only
        input_image_url = ""
        if design.input_image_path:
            cleaned_input_path = design.input_image_path.replace('media/', '').lstrip('/')
            input_image_url = f"{settings.MEDIA_URL}{cleaned_input_path}"

        data = {
            'design_name': design.design_name,
            'image_path': image_url,
            'created_at': design.created_at.strftime('%B %d, %Y'),
            'promote': design.promote,
            'type': design.type
        }

        if design.type == "style_transfer":
            data['input_image_path'] = input_image_url
            style_transfer_list.append(data)
        elif design.type == "design_generation":
            design_generation_list.append(data)

    context = {
        'design_generation': design_generation_list,
        'style_transfer': style_transfer_list
    }

    return render(request, 'history.html', context)


from django.db import models
from django.shortcuts import get_object_or_404
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse
import os
import json
import uuid
from django.conf import settings

def generate_design(request):
    print("Started")
    if request.method == 'POST':
        user_id = request.session.get('user_id')
        if not user_id:
            return JsonResponse({'error': 'User not logged in.'}, status=401)

        user = get_object_or_404(RegisterUser, id=user_id)
        print("HELLO")
        data = json.loads(request.body)
        prompt = data.get('prompt')
        image_path = data.get('image_path')  # Existing image for editing
        design_name = data.get('design_name', f"design_{uuid.uuid4().hex[:8]}")
        promote = data.get('promote', False)  # Get promote field from request

        if not prompt or not design_name:
            return JsonResponse({'error': 'Missing required fields.'}, status=400)

        # Create user-specific folder
        user_folder = os.path.join(settings.MEDIA_ROOT, f"designs/{user_id}")
        os.makedirs(user_folder, exist_ok=True)

        # Handle existing image editing or new generation
        if image_path:
            if not image_path.startswith(f"designs/{user_id}/"):
                image_path = os.path.join(user_folder, os.path.basename(image_path))
            output_image_path = os.path.join(user_folder, f"{design_name}.png")
            transfer_style(prompt, image_path, output_image_path)
        else:
            output_image_path = os.path.join(user_folder, f"{design_name}.png")
            remodel_image(prompt, output_image_path)
        print("Hi")
        if output_image_path:
            # Save image record to database
            UserDesigns.objects.create(
                user=user,
                design_name=design_name,
                image_path=output_image_path,
                promote=prompt,
                type='design_generation'
            )

            static_image_path = f"/media/designs/{user_id}/{design_name}.png"
            return JsonResponse({'image_path': static_image_path})
        else:
            return JsonResponse({'error': 'Failed to generate design.'}, status=500)

    return JsonResponse({'error': 'Invalid request method.'}, status=405)

def generate_design1(request):
    if request.method == 'POST':
        try:
            user_id = request.session.get('user_id')
            if not user_id:
                return JsonResponse({'error': 'User not logged in.'}, status=401)

            user = get_object_or_404(RegisterUser, id=user_id)

            prompt = request.POST.get('message')
            print(prompt)
            uploaded_image = request.FILES.get('image')
            existing_image_path = request.POST.get('image_path')
            design_name = f"design_{uuid.uuid4().hex[:8]}"
            promote = request.POST.get('promote', False)  # Get promote field from request

            if not prompt and not existing_image_path:
                return JsonResponse({'error': 'No input provided.'}, status=400)
            if not design_name:
                return JsonResponse({'error': 'Design name is required.'}, status=400)

            # Create user-specific folder
            user_folder = os.path.join(settings.MEDIA_ROOT, f"designs/{user_id}")
            os.makedirs(user_folder, exist_ok=True)

            # Handling new uploads
            if uploaded_image:
                fs = FileSystemStorage(location='media/designs')
                image_path = fs.save(uploaded_image.name, uploaded_image)
                image_path = os.path.join('media/designs', image_path)
            elif existing_image_path:
                print(existing_image_path)
                image_path = existing_image_path
                if not image_path.startswith(f"designs/{user_id}/"):
                    image_path = os.path.join(user_folder, os.path.basename(image_path))
                print(image_path)
            else:
                return JsonResponse({'error': 'No image provided.'}, status=400)

            # Define output path
            output_image_path = os.path.join(user_folder, f"edited_{design_name}.png")
            
            # Call function to apply style transfer
            transfer_style(prompt, image_path, output_image_path)

            if output_image_path:
                # Save image record to database
                UserDesigns.objects.create(
                    user=user,
                    design_name=design_name,
                    image_path=output_image_path,
                    input_image_path= image_path,
                    promote=prompt,
                    type='style_transfer'
                )

                static_image_path = f"/media/designs/{user_id}/edited_{design_name}.png"
                return JsonResponse({'image_path': static_image_path})
            else:
                return JsonResponse({'error': 'Failed to generate design.'}, status=500)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request method.'}, status=405)

import os
import logging
import datetime
from chatterbot import ChatBot
from chatterbot.response_selection import get_random_response
from django.http import JsonResponse
from django.shortcuts import render
import json
from django.views.decorators.csrf import csrf_exempt

import os
import logging
import datetime
import json
from chatterbot import ChatBot
from chatterbot.response_selection import get_random_response
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

# For session management
import os
import datetime
import logging
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
from chatterbot.conversation import Statement
from chatterbot.response_selection import get_random_response

# Function to handle the bot's response
def botreply(messagein, db_location="database.db", conversation_id="default"):
    # Check if database exists
    if not os.path.exists(db_location):
        error = f"{datetime.datetime.now()}\nERROR IN REPLYING\nModel does not exist at {db_location}\n"
        print(error)
        return "Sorry! I am resting right now. Please come back later."

    logging.getLogger('chatterbot').setLevel(logging.WARNING)

    # Initialize ChatBot
    chatbot = ChatBot(
        'Chatting Bot',
        logic_adapters=[
            {
                'import_path': 'chatterbot.logic.BestMatch',
                'default_response': 'Sorry, I didn’t quite get that. Can you rephrase?',
                'maximum_similarity_threshold': 0.77
            },
            {
                'import_path': 'chatterbot.logic.MathematicalEvaluation'
            },
            {
                'import_path': 'chatterbot.logic.SpecificResponseAdapter',
                'input_text': 'Help me!',
                'output_text': 'Mail your query here.'
            },
            {
                'import_path': 'chatterbot.logic.SpecificResponseAdapter',
                'input_text': 'Can you help?',
                'output_text': 'Sure! What do you need help with?'
            }
        ],
        database_uri=f'sqlite:///{db_location}',
        response_selection_method=get_random_response,
        read_only=True  # Prevents training from user input; good for deployment
    )

    # Define exit keywords
    exit_keywords = ['goodbye', 'thanks', 'thank you', 'bye', 'see you']
    if any(keyword in messagein.lower() for keyword in exit_keywords):
        response = "Goodbye! It was nice talking to you. See you next time!"
    else:
        response = str(chatbot.get_response(messagein))

    # Output the conversation
    print("\nYOU (Input):", messagein)
    print("Virtual Tutoring BOT:", response, "\n")
    return response

# View to render the chatbot page
def chatbot_page(request):
    return render(request, 'chatbot.html')

# API for chatbot communication
@csrf_exempt
def chatbot_api(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_message = data.get('message', '')
            conversation_id = data.get('conversation_id', 'default')  # Retrieve the conversation ID to maintain session

            if not user_message:
                return JsonResponse({"reply": "Please enter a valid message."}, status=400)

            bot_response = botreply(user_message, conversation_id=conversation_id)

            return JsonResponse({"reply": bot_response}, status=200)
        except json.JSONDecodeError:
            return JsonResponse({"reply": "Invalid request format."}, status=400)
    else:
        return JsonResponse({"reply": "Invalid request method."}, status=405)


from .models import RegisterUser
@csrf_exempt
def register(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        mobile = request.POST.get('mobile')
        password = request.POST.get('password')
        print(name,email,password,mobile)
        errors = []

        if not all([name, email, mobile, password]):
            return HttpResponse("<script>alert('All fields are required');window.location.href='/login_page/';</script>")

        try:
            validate_email(email)
        except ValidationError:
            errors.append("Invalid email format.")

        if RegisterUser.objects.filter(email=email).exists():
            errors.append("This email is already registered.")

        if not re.match(r"^\+?1?\d{9,15}$", mobile):
            errors.append("Enter a valid mobile number.")
        
        if RegisterUser.objects.filter(mobile=mobile).exists():
            errors.append("This mobile number is already registered.")

        if len(password) < 6:
            errors.append("Password must be at least 6 characters long.")

        if errors:
            return HttpResponse(
                f"<script>alert('{', '.join(errors)}');window.location.href='/login_page/';</script>"
            )

        user = RegisterUser.objects.create(name=name, email=email, mobile=mobile, password=password)

        return HttpResponse(
            "<script>alert('Account created successfully.');window.location.href='/login_page/';</script>"
        )
    else:
        return render(request, 'login.html')




@csrf_exempt
def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        print(email,password)
        if not all([email, password]):
            return HttpResponse("<script>alert('All fields are required');window.location.href='/login_page/';</script>")

        try:
            validate_email(email)
        except ValidationError:
            return HttpResponse("<script>alert('Invalid email format');window.location.href='/login_page/';</script>")

        try:
            user = RegisterUser.objects.get(email=email)
        except RegisterUser.DoesNotExist:
            return HttpResponse("<script>alert('Invalid email or password');window.location.href='/login_page/';</script>")
        # print("111111111111111111111111111111111111")
        if not password==user.password:
            return HttpResponse("<script>alert('Invalid email or password');window.location.href='/login_page/';</script>")

        request.session['user_id'] = user.id
        request.session['user_email'] = user.email

        return HttpResponse("<script>alert('Login successful');window.location.href='/front_page/';</script>")
    else:
        return render(request, 'login.html')

        