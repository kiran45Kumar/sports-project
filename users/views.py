from django.conf import settings
from rest_framework import viewsets
from users.models import User, Users
from users.serializers import *
from rest_framework.views import APIView
from users.models import Admin
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import send_mail
from django.contrib.auth.hashers import make_password, check_password

class UsersViewSet(viewsets.ModelViewSet):
    queryset = Users.objects.all().order_by('-created_at')
    serializer_class = UsersSerializer
    
class AdminViewSet(viewsets.ModelViewSet):
    queryset = Admin.objects.all()
    serializer_class = AdminSerializer

class AdminLogin(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        admin = Admin.objects.get(email = email)
        if not email:
            return Response({"status":'fail','message':'Enter email'},status = status.HTTP_400_BAD_REQUEST)
        elif not password:
            return Response({"status":'fail','message':'Enter password'},status = status.HTTP_400_BAD_REQUEST)
        try:
            if admin.password != password:
                return Response({"status":'fail','message':'Incorrect Password'},status = status.HTTP_400_BAD_REQUEST)
            elif Admin.objects.filter(email = email, password = password).exists():
                request.session['admin_email'] = admin.email
                return Response({"status":'pass','message':'Login Successful'},status = status.HTTP_200_OK)
        except Admin.DoesNotExist as a:
                return Response({"status":'fail','message':str(a)},status = status.HTTP_404_NOT_FOUND)
        except Exception as e:
                return Response({"status":'fail','message':str(e)},status = status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        

class LoginUser(APIView):
    def post(self, request):
        phone = request.data.get('phone')
        password = request.data.get('password')
        if not phone:
            return Response({"status":'fail','message':'Enter Phone Number'},status = status.HTTP_400_BAD_REQUEST)
        elif not password:
            return Response({"status":'fail','message':'Enter Password'}, status = status.HTTP_400_BAD_REQUEST)
        try:
            users = Users()
            users.user_phone = phone
            users.user_pass = password
            users.save()
            if Users.objects.filter(user_phone = phone,user_pass = password).exists():
                request.session['user_phone'] = users.user_phone
                request.session['user_name'] = users.user_name
                request.session['user_email'] = users.user_email
                return Response({"status":"pass","message":'Login Successful'}, status = status.HTTP_200_OK)
            else:
                return Response({"status":"fail","message":'Login Failed'}, status = status.HTTP_200_OK)
        except Users.DoesNotExist as e:
            return Response({'status':'fail','message':str(e)}, status = status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'status':'fail','message':str(e)}, status = status.HTTP_500_INTERNAL_SERVER_ERROR)


class LogoutUser(APIView):
    def post(self, request):
        request.session.flush()
        return Response({"status":"pass","message":'Logout Successful'}, status = status.HTTP_200_OK)
    
class ApproveUser(APIView):
    def post(self, request):
        user_id = request.data.get('user_id')
        if not user_id:
            return Response({"status":'fail','message':'User ID is required'},status = status.HTTP_400_BAD_REQUEST)
        try:
            user = Users.objects.get(user_id=user_id)
            user.user_approval = True if user.user_approval == False else False
            user.user_status = 'approved' if user.user_approval == True else 'pending'  
            user.save()
            return Response({"status":"pass","message":'User Approved Successfully', 'user_status':user.user_status,"user_approval":user.user_approval}, status = status.HTTP_200_OK)
        except Users.DoesNotExist as e:
            return Response({"status":"fail","message":str(e)}, status = status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'status':'fail','message':str(e)}, status = status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class RejectUser(APIView):
    def post(self, request):
        user_id = request.data.get('user_id')
        reason = request.data.get('reason')
        if not user_id:
            return Response({"status":'fail','message':'User ID is required'},status = status.HTTP_400_BAD_REQUEST)
        elif not reason:
            return Response({"status":'fail','message':'Rejection reason is required'},status = status.HTTP_400_BAD_REQUEST)
        try:
            user = Users.objects.get(user_id=user_id)
            user.user_approval = False if user.user_approval == True else True
            user.user_status = 'rejected' if user.user_approval == False else 'pending'  
            user.message = reason
            user.save()
            return Response({"status":"pass","message":'User Rejected Successfully', 'user_status':user.user_status,'user_approval':user.user_approval}, status = status.HTTP_200_OK)
        except Users.DoesNotExist as e:
            return Response({"status":"fail","message":str(e)}, status = status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'status':'fail','message':str(e)}, status = status.HTTP_500_INTERNAL_SERVER_ERROR)

class SendEmail(APIView):
    def post(self, request):
        email = request.data.get('email')
        if not email:
            return Response({"status": "fail", "message": "Email is required"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = Users.objects.get(user_email=email)
            if user:
                send_mail(
                'Subject - Password Reset',
                'Please find the link below to reset your password:\n\nhttp://localhost:3000/reset-password/',
                settings.EMAIL_HOST_USER,
                [user.user_email],
                fail_silently=False,
                )
            return Response({"status": "pass", "message": "Email sent successfully"}, status=status.HTTP_200_OK)
        except Users.DoesNotExist as e:
            return Response({"status": "fail", "message": str(e)}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'status':'fail','message':str(e)}, status = status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class ResetPassword(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        confirm_password = request.data.get('confirm_password')
        password_pattern = r"^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$"
        if not email:
            return Response({"status": "fail", "message": "Email is required"}, status=status.HTTP_400_BAD_REQUEST)
        elif not password:
            return Response({"status": "fail", "message": "Password is required"}, status=status.HTTP_400_BAD_REQUEST)
        elif not confirm_password:
            return Response({"status": "fail", "message": "Confirm password is required"}, status=status.HTTP_400_BAD_REQUEST)
        elif password != confirm_password:
            return Response({"status": "fail", "message": "Passwords do not match"}, status=status.HTTP_400_BAD_REQUEST)
        elif not re.match(password_pattern, password):
            return Response({"status": "fail", "message": "<h1>Password must be at least 8 characters long and include <br> uppercase, lowercase, number, and special character.</h1>"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = Users.objects.get(user_email=email)
            user.user_pass = password
            user.save()
            send_mail(
                'Subject - Password Reset',
                'Your password has been reset successfully.',
                settings.EMAIL_HOST_USER,
                [user.user_email],
                fail_silently=False,    
            )
            return Response({"status": "pass", "message": "Password reset successfully"}, status=status.HTTP_200_OK)
        except Users.DoesNotExist as e:
            return Response({"status": "fail", "message": str(e)}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'status':'fail','message':str(e)}, status = status.HTTP_500_INTERNAL_SERVER_ERROR)
class RegisterUser(APIView):
    def post(self, request):
        email = request.data.get('email')
        phone = request.data.get('phone')
        password = request.data.get('password')
        if not email:
            return Response({"status":'fail','message':'Enter email'},status = status.HTTP_400_BAD_REQUEST)
        elif not phone:
            return Response({"status":'fail','message':'Enter phone number'},status = status.HTTP_400_BAD_REQUEST)
        elif not password:
            return Response({"status":'fail','message':'Enter password'}, status = status.HTTP_400_BAD_REQUEST)
        try:
            if User.objects.filter(email = email).exists():
                return Response({"status":'fail','message':'Email already exists'},status = status.HTTP_400_BAD_REQUEST)
            elif User.objects.filter(phone_no = phone).exists():
                return Response({"status":'fail','message':'Phone number already exists'},status = status.HTTP_400_BAD_REQUEST)
            else:
                user = User()
                user.email = email
                user.phone_no = phone
                user.password = make_password(password)
                user.save()
                return Response({"status":"pass","message":'Sign up successful'}, status = status.HTTP_200_OK)
        except Exception as e:
            return Response({'status':'fail','message':str(e)}, status = status.HTTP_500_INTERNAL_SERVER_ERROR) 
class Login(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        if not email:
            return Response({"status":'fail','message':'Enter Email'},status = status.HTTP_400_BAD_REQUEST)
        elif not password:
            return Response({"status":'fail','message':'Enter Password'}, status = status.HTTP_400_BAD_REQUEST)
        try:
            user = User.objects.get(email=email)
            if not user:
                return Response({"status":"fail","message":'Login Failed, User does not exist'}, status = status.HTTP_200_OK)
            if not check_password(password, user.password):
                return Response({"status":"fail","message":'Login Failed, Incorrect Password'}, status = status.HTTP_200_OK)
            request.session['user_phone'] = user.phone_no
            request.session['user_email'] = user.email
            return Response({"status":"pass","message":'Login Successful'}, status = status.HTTP_200_OK)
        except User.DoesNotExist as e:
            return Response({'status':'fail','message':str(e)}, status = status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'status':'fail','message':str(e)}, status = status.HTTP_500_INTERNAL_SERVER_ERROR)
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-created_at')
    serializer_class = UserSerializer