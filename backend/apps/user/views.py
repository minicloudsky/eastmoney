# Create your views here.
import random
import re

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token

from apps.user.models import User


def random_str(randomlength=8):
    str = ''
    chars = 'abcdefghijklmnopqrstuvwsyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    length = len(chars) - 1
    for i in range(randomlength):
        str += chars[random.randint(0, length)]
    return str


class RegisterView(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data
        username = data.get('username', '')
        password = data.get('password', '')
        email = data.get('email', '')
        if len(username) < 5 or len(password) < 8:
            return Response(status=200, data={"code": 200, "msg": "用户名或者密码太短", "data": {}})
        if not re.match(r'^[0-9a-zA-Z_]{0,19}@[0-9a-zA-Z]{1,13}\.[com,cn,net]{1,3}$', email):
            return Response(status=200, data={"code": 200, "msg": "邮箱格式不正确，请重新输入邮箱", "data": {}})
        password = make_password(password, None, 'pbkdf2_sha256')
        if User.objects.filter(username=username).first():
            return Response(status=200, data={"code": 200, "msg": "该用户已经注册,请换个用户名注册", "data": {}})
        register_user = User.objects.create(
            username=username, password=password, email=email)
        register_user.save()
        if register_user:
            return Response(status=status.HTTP_201_CREATED,
                            data={"code": 200, "msg": "注册成功", "data": {"user": register_user.username}})


class LoginView(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data
        username = data.get('username', '')
        password = data.get('password', '')
        if not username or not password:
            return Response(status=status.HTTP_200_OK, data={"code": 200, "msg": '用户名或密码不能为空', 'data': {}})
        user = authenticate(request, username=username, password=password)
        if not user:
            return Response(status=status.HTTP_200_OK, data={"code": 200, "msg": '该用户未注册', 'data': {}})
        login(request, user)
        token = Token.objects.get_or_create(user=request.user)
        token = token[0].key if not token[1] else ''
        user_info = {
            'userid': request.user.id,
            'username': request.user.username,
            'token': token,
        }
        return Response(status=status.HTTP_202_ACCEPTED, data={"code": 200, "msg": "登录成功", "data": user_info})


class AuthenticatePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        data = request.data
        username = request.user.username
        password = data.get('password', '')
        if not password:
            return Response(status=status.HTTP_200_OK,
                            data={"code": 200, "msg": '密码不能为空', 'data': {"is_valid_password": 0}})
        user = authenticate(request, username=username, password=password)
        if not user:
            return Response(status=status.HTTP_200_OK,
                            data={"code": 200, "msg": '密码错误', 'data': {"is_valid_password": 0}})

        return Response(status=status.HTTP_202_ACCEPTED,
                        data={"code": 200, "msg": "密码验证成功", "data": {"is_valid_password": 1}})


class ResetPasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        email_title = "找回密码"
        code = random_str()
        request.session["code"] = code
        email_body = "验证码为：{0}".format(code)
        send_status = send_mail(email_title, email_body,
                                "xxxx@163.com", ["xxxx@qq.com", ])
        return Response(status=status.HTTP_200_OK, data={"code": 200, "msg": '验证码已发送，请查收邮件', 'data': {}})

    def post(self, request, *args, **kwargs):
        user = request.user
        if not user:
            return Response(status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION,
                            data={"code": 200, "msg": "用户未登录", "data": {}})
        data = request.data
        username = data.get('username', '')
        password = data.get('password', '')
        new_password = data.get('new_password', '')
        if not username or not password or not new_password:
            return Response(status=status.HTTP_200_OK,
                            data={"code": 200, "msg": '用户名或密码不能为空', 'data': {"is_valid_password": 0}})
        user = authenticate(request, username=username, password=password)
        if not user:
            return Response(status=status.HTTP_200_OK,
                            data={"code": 200, "msg": '密码错误', 'data': {"is_valid_password": 0}})
        user.set_password(new_password)
        user.save()
        return Response(status=status.HTTP_200_OK, data={"code": 200, "msg": '修改密码成功', 'data': {}})


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        logout(request)
        return Response(status=status.HTTP_201_CREATED, data={"code": 200, "msg": "注销成功", "data": {}})
