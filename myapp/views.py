from django.shortcuts import render,HttpResponse,redirect,get_object_or_404
from django.contrib.auth.models import User,auth
from django.contrib import messages
from django.core.mail import send_mail
from .models import user_data,quiz,Report,ngo, techcourse, engcourse, makedonation
from django.core.files.storage import FileSystemStorage
import json
from django.core.mail import send_mail
from django.http import JsonResponse
from django.db.models import F
import logging
from .forms import donate
from datetime import datetime

logger = logging.getLogger(__name__)
# Create your views here.
def index(request):
    return render(request,"index.html")

def about(request):
    return render(request,"about.html")

def logout(request):
    auth.logout(request)
    return redirect('/')

def login(request):
    if request.method=="POST":
        username=request.POST['username']
        password=request.POST['password']
        user=auth.authenticate(username=username,password=password)
        if user is not None:
            request.session['user_id'] = user.userid
            request.session['username'] = user.username
            print("Session created while login: ",user.userid,user.username)
            auth.login(request,user)
            return redirect("/")
        else:
            messages.info(request,"User not found. Signup to continue.")
            return redirect("login")
    else:
        return render(request, 'login.html')


def register(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        # Check if email or username already exists
        if user_data.objects.filter(email=email).exists():
            messages.info(request, 'Email exists. Login to continue')
            return redirect('login.html')
        elif user_data.objects.filter(username=username).exists():
            messages.info(request, 'Username already taken')
            return redirect('register.html')
        else:
            # Create new user
            user = user_data.objects.create_user(email=email, username=username, password=password, test_attempt=0)
            user.save()

            # Set session variables
            request.session['user_id'] = user.id
            request.session['username'] = user.username
            logger.info(f"Session created in register: {user.id}, {user.username}")

            # Check if the report object already exists
            if report.objects.filter(userid=user).exists():
                logger.error(f"Report for user {user.id} already exists")
                messages.error(request, 'User report already exists')
                return redirect('register.html')

            # Create report for the user
            user_report = report.objects.create(userid=user, username=username)
            user_report.save()

            return render(request, "index.html")
    
    return render(request, "register.html")

def testform(request):
    sid = request.session.get('user_id')
    username = request.session.get('username')
    
    if not sid or not username:
        return redirect('register')

    return render(request,'testform.html')



def get_questions(request, field_of_study):
    questions = quiz.objects.filter(field_of_study=field_of_study)
    Equestions = quiz.objects.filter(field_of_study="English")

    Equestions_data = [{"question_text": question.question_text,
                        "options": [question.option1, question.option2, question.option3, question.option4],
                        "correct": question.correct_option}
                        for question in Equestions]
    questions_data = [{"question_text": question.question_text,
                        "options": [question.option1, question.option2, question.option3, question.option4],
                        "correct": question.correct_option}
                        for question in questions]
    return JsonResponse({"questions": questions_data, "Equestions": Equestions_data})
    

def reportfunc(request):
    try:
        sid = request.session.get('user_id')
        username = request.session.get('username')
        
        if not sid or not username:
            logger.error("Session variables 'user_id' or 'username' not set.")
            return render(request, 'reportnotfound.html')

        user = get_object_or_404(user_data, userid=sid)
        record = get_object_or_404(Report, userid=sid)
        level = record.level
        t=techcourse.objects.filter(level=level)
        e=engcourse.objects.filter(level=level)
        
        print(f"Saved details: username={username}, user={user}, sid={sid}, percentage={record.percentage},")
        return render(request, 'report.html', {'record': record, 'user': user,'t':t,'e':e})
   
    except Exception as e:
        logger.error(f"Error retrieving report: {e}")
        return render(request, 'reportnotfound.html')

def reportnotfound(request):
    return(request,'reportnotfound.html')

def my_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            percentage = data.get('percentage')
            totalMarks = data.get('totalMarks')
            totalEMarks = data.get('totalEMarks')
            totalFMarks = data.get('totalFMarks')
            field = data.get('field')
            totalQue = data.get('totalQue')
            sid = request.session.get('user_id')
            totalQue = totalQue-1
            totalM=totalEMarks+totalFMarks
            level=0
            if percentage<=35 and percentage>=0:
                level=1
            elif percentage>35 and percentage<=75:
                level=2
            else:
                level=3
            if percentage is None or sid is None:
                return JsonResponse({'status': 'error', 'message': 'Invalid data'}, status=400)

            user1 = get_object_or_404(user_data, userid=sid)
            report, created = Report.objects.update_or_create(userid=user1, defaults={'percentage': percentage,'totalEMarks':totalEMarks,'totalFMarks':totalFMarks,'totalMarks':totalM,'totalQue':totalQue,'field':field,'level':level})
            user1.test_attempt = F('test_attempt') + 1
            user1.save()
            return JsonResponse({'status': 'success', 'message': 'Data saved successfully'})
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)


def allcourse(request):
    return render(request,'allcourse.html')

def report(request):
    return render(request,'report.html')

def ngoenroll(request):
    if request.method=="POST":
        name=request.POST['name']
        contact=request.POST['contact']
        email=request.POST['email']
        address=request.POST['address']
        sid = request.session.get('user_id')
        user1 = get_object_or_404(user_data, userid=sid)
        user_email = request.user.email if request.user.is_authenticated else None
        user_name = request.user.username if request.user.is_authenticated else None
        if user_email and user_name is not None:         
            subject=f'NGO {name} registered.',
            message = f'This is confirmation mail. Thank you for entrusting us with your students and organisaton. We will do our best to upskill your students and promote your Organisation.',
            recipients = ['ifrahraufddps@gmail.com', email ]
            send_mail(
                subject,
                message,
                'ifrahraufddps@gmail.com',  
                recipients,
                fail_silently=False,
            )
        else:
            return redirect('register')
    return render(request, 'ngoenroll.html')

def explore(request):
    don=donate(request.POST)
    if don.is_valid():
            name=request.POST.get("name")
            donateto=request.POST.get("donateto")
            donation=request.POST.get("donation")
            comment=request.POST.get("comment")
            
    v=ngo.objects.all()
    if request.method=="POST":
        sid = request.session.get('user_id')
        user1 = get_object_or_404(user_data, userid=sid)
        user_email = request.user.email if request.user.is_authenticated else None
        user_name = request.user.username if request.user.is_authenticated else None
        if user_email and user_name is not None:         
            subject=f'Donation request made by {user_name}',
            message = f'Donation request has been made by :{user_name} for the NGO {donateto}.\nDonation amount proposed is INR: {donation}.\nTake forward the process by sending the amount on given number: 9123456781 For payement.\nThis number is available for UPI and transactions.\n Same number is available on Whatsapp for Queries.\n It is directly handles by the coordinator.\nFor more information read FAQs.\n\nThankyou'
            recipients = ['ifrahraufddps@gmail.com', user_email ]
            send_mail(
                subject,
                message,
                'ifrahraufddps@gmail.com',  # Sender's email
                recipients,  # Recipient's email (as a list of strings)
                fail_silently=False,
            )
            d=makedonation(userid=user1,name=name,NGO=donateto,donation=donation,comment=comment)
            d.save()
            return render(request,"explore.html",{"v":v,"d":don})
    return render(request,"explore.html",{"v":v,"d":don})

def profile(request):
    sid = request.session.get('user_id')
    username = request.session.get('username')
    if not sid or not username:
        return render(request, 'register.html')
    else:
        user = get_object_or_404(user_data, userid=sid)
        if request.method == "POST":
            newname = request.POST.get('fullname')
            dob = request.POST.get('date')
            contact = request.POST.get('contact')
            gender = request.POST.get('gender')
            email = request.POST.get('email')
            profile1 = request.POST.get('pf1', '')
            profile2 = request.POST.get('pf2', '')
            profile3 = request.POST.get('pf3', '')
            pfp = request.POST.get('pfp', '')
            # Print statements for debugging
            print(contact, newname, gender, email, profile1, profile2, profile3)

            # Handle the file upload
            # profile_image = request.FILES.get('pfp')
            # if profile_image:
            #     fs = FileSystemStorage()
            #     filename = fs.save(profile_image.name, profile_image)
            #     uploaded_file_url = fs.url(filename)
            #     user.profile_image = uploaded_file_url  # Save the file URL to the user's profile

            if not newname or not dob or not contact or not gender or not email:
                return render(request, 'pp.html', {'error': 'Please fill in all required fields.'})

            # Update or create user data
            u=user_data.objects.update_or_create(
                userid=user.userid,
                defaults={
                    'username': newname,
                    'contact': contact,
                    'gender': gender,
                    'email': email,
                    'profilelink1': profile1,
                    'profilelink2': profile2,
                    'profilelink3': profile3,
                    'pfp':pfp
                }
            )
            u.save()
    return render(request, 'pp.html')

def tc(request):
    return render(request,'tc.html')






