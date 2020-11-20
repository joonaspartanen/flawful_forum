from django.http.response import HttpResponse
from django.http import JsonResponse
from forum.models import Message
from django.shortcuts import redirect, render
from .models import Message
from django.views.decorators.csrf import csrf_exempt
from django.db import connection
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.models import User
import json

def index(request):
    initialize_users()

    messages = Message.objects.all()
    return render(request, 'forum/index.html', {'messages': messages})


# VULNERABILITY: The controller allows POST requests without proper CSRF token.
@csrf_exempt
def posts(request):
    if request.method == 'POST':
        subject = request.POST.get('subject')
        body = request.POST.get('body')
        author = request.user

        # VULNERABILITY: The app uses raw SQL queries with unsanitized input. For example, posting a message with body "); DROP TABLE forum_message; -- would delete the whole DB table.
        query = 'INSERT INTO forum_message (subject, body, author_id) VALUES ("%s", "%s", "%s")' % (subject, body, author.id)
        with connection.cursor() as cursor:
            # VULNERABILITY: executescript() allows executing multiple queries.
            cursor.executescript(query)
            connection.commit()
        return redirect(index)

    # VULNERABILITY: The app relies on front-end validation and does not check if the requesting user is the author of the message to be deleted.
    # => Other users messages can be deleted for example with: curl -d '{"id": 1}' -H "Content-Type: application/json" -X DELETE http://localhost:8000/forum/posts/
    if request.method == 'DELETE':
        content = json.loads(request.body)
        msg = Message.objects.get(id=content["id"])
        if msg:
            msg.delete()
            return HttpResponse(status=200)
        else:
            return HttpResponse(status=403)

    return redirect(index)

# VULNERABILITY: The controller allows POST requests without proper CSRF token.
@csrf_exempt
def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        if user is not None:
            auth_login(request, user)

    return redirect(index)

# VULNERABILITY: Uses GET requests for actions with side-effects.
def logout(request):
    auth_logout(request)
    return redirect(index)

def users(request):
    return render(request, 'forum/users.html')

# VULNERABILITY: The servers sends sensitive user information that can be easily examined.
def all_users(request):
    users = User.objects.all()
    return JsonResponse(list(users.values()), safe=False)

# On startup, the application creates two test users whose passwords can be found in the source code. An obvious vulnerability.
def initialize_users():
    if not User.objects.filter(username="superadmin").exists():
        User.objects.create_superuser("superadmin", "admin@example.com", "verysecret")

    if not User.objects.filter(username="testuser").exists():
        User.objects.create_user("testuser", "user@example.com", "quitesecret")