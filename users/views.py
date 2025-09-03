from django.conf import settings
from rest_framework import viewsets
from users.models import Users
from users.serializers import *
from rest_framework.views import APIView
from users.models import Admin
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import send_mail

class UsersViewSet(viewsets.ModelViewSet):
    queryset = Users.objects.all().order_by('-created_at')
    serializer_class = UsersSerializer
    
class AdminViewSet(viewsets.ModelViewSet):
    queryset = Admin.objects.all()
    serializer_class = AdminSerializer

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
            request.session['user_phone'] = users.user_phone
            request.session['user_name'] = users.user_name
            request.session['user_email'] = users.user_email
            return Response({"status":"pass","message":'Login Successful'}, status = status.HTTP_200_OK)
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
