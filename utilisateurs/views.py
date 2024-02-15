from django.shortcuts import render, redirect
from django.core.validators import validate_email
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.http import HttpResponseForbidden

from django.core.mail import EmailMessage
from django.template.loader import render_to_string

from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
import codecs

# Create your views here.

def login_user(request):
    User = get_user_model()
    if request.method == "POST":
        email = request.POST.get('email', None)
        password = request.POST.get('password', None)

        user = User.objects.filter(email=email).first()
        if user:
            auth_user = authenticate(username=user.username, password=password)
            if auth_user:
                login(request, auth_user)
                if user.chef_projet:
                    return redirect('chef')
                elif user.gestionnaire_financier:
                    return redirect('finance')
                elif user.porteur_projet:
                    return redirect('porteur')
                else:
                    return redirect('regie')
            else:
                print("mot de pass incorrecte")
        else:
            print("User does not exist")

    return render(request, 'utilisateurs/login.html', {})


def register(request):
    error = False
    message = ""
    if request.method == "POST":
        name = request.POST.get('name', None)
        email = request.POST.get('email', None)
        password = request.POST.get('password', None)
        repassword = request.POST.get('repassword', None)
        # Email
        try:
            validate_email(email)
        except:
            error = True
            message = "Enter un email valide svp!"
        # password
        if error == False:
            if password != repassword:
                error = True
                message = "Les deux mot de passe ne correspondent pas!"
        # Exist
        user = User.objects.filter(Q(email=email) | Q(username=name)).first()
        if user:
            error = True
            message = f"Un utilisateur avec email {email} ou le nom d'utilisateur {name} exist déjà'!"

        # register
        if error == False:
            user = User(
                username=name,
                email=email,
            )
            user.save()

            user.password = password
            user.set_password(user.password)
            user.save()

            return redirect('login')

            # print("=="*5, " NEW POST: ",name,email, password, repassword, "=="*5)

    context = {
        'error': error,
        'message': message
    }
    return render(request, 'utilisateurs/register.html', context)


@login_required(login_url='login')
def home(request):
    return render(request, 'utilisateurs/admin.html', {})

def chef(request):
    return render(request,'utilisateurs/chef.html')

def finance(request):
    return render(request,'utilisateurs/finance.html')

def porteur_projet(request):
    return render(request,'utilisateurs/porteur.html')

def regie(request):
    return render(request,'utilisateurs/regie.html')


def log_out(request):
    logout(request)
    return redirect('sing_in')


def forgot_password(request):
    error = False
    success = False
    message = ""
    if request.method == 'POST':
        email = request.POST.get('email')
        user = User.objects.filter(email=email).first()
        if user:
            token=default_token_generator.make_token(user)
            uid=urlsafe_base64_encode(force_bytes(user.id))
            url_site=request.META['HTTP_HOST']
            context={
                'token':token,
                'uid':uid,
                'url_site': f'http://{url_site}'
            }
            print("processus de recuperation de mot de passe")
            html = render_to_string('utilisateurs/template_email.html',context)
            msg = EmailMessage(
                "Modification de mot de pass!",
                html,
                "CWEBSERVICES<mhsawadogo99@gmail.com>",
                [user.email]
            )

            msg.content_subtype = 'html'
            msg.send()

            message = "processus de recuperation de mot de passe entammé vérifiez également vos spam !"
            success = True
        else:
            print("user does not exist")
            error = True
            message = "utilisateur inexistant"

    context = {
        'success': success,
        'error': error,
        'message': message
    }
    return render(request, "utilisateurs/forgot_password.html", context)


def update_password(request,token,uid):
    try:
        id_utilisateur=urlsafe_base64_decode(uid)
        decode_uid=codecs.decode(id_utilisateur, 'utf-8')
        utilisateur=User.objects.get(id=decode_uid)

    except:
        return HttpResponseForbidden("Operation refusé; vous n'avez pas la permission de modifier le mot de passe. Utilisateur introuvable")

    token_verification=default_token_generator.check_token(utilisateur,token)
    if not token_verification:
        return HttpResponseForbidden("Operation refusé; vous n'avez pas la permission de modifier le mot de passe. Le token est incalide ou expiré")

    error = False
    success = False
    message = ""
    if request.method=='POST':

        password=request.POST.get('password')
        repeat_password=request.POST.get('repeat-password')
        if password==repeat_password:
            try:
                validate_password(password,utilisateur)
                utilisateur.set_password(password)
                utilisateur.save()
                success=True
                message="Votre mot de passe a été modifier avec succès !"
            except ValidationError as e:
                error=True
                message= str(e)

        else:
            error=True
            message="veuillez tapper le même mot de passe deux fois"

    context={
            'error':error,
            'success':success,
            'message':message

        }

    return render(request, "utilisateurs/update_password.html",context)





