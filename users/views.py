from django.shortcuts import render
from rest_framework import viewsets
from .models import Users
from .serializers import UsersSerializer
from django.http import JsonResponse
from rest_framework.views import APIView

class UsersViewSet(viewsets.ModelViewSet):
    queryset = Users.objects.all()
    serializer_class = UsersSerializer

class LoginUser(APIView):
    def post(self, request):
        phone = request.data.get('phone')
        password = request.data.get('password')
        if not phone:
            return JsonResponse({"status":'fail','message':'Enter Phone Number'},status = 400)
        elif not password:
            return JsonResponse({"status":'fail','message':'Enter Password'}, status = 400)
        try:
            user = Users.objects.get(user_phone = phone)
            if user.user_pass != password or user.user_phone != phone:
                return JsonResponse({"status":"fail","message":'Incorrect Credentials'},status = 400)
            elif Users.objects.filter(user_phone = phone).exists():
                request.session['user_name'] = user.user_name
                request.session['user_phone'] = user.user_phone
                request.session['user_password'] = user.user_pass
                return JsonResponse({"status":"pass","message":'Login Successful', 'currentUser':request.session.get('user_name'), 'user':{'user_name':request.session.get('user_name'), 'user_phone':request.session.get('user_phone')}}, status = 200)
            else:
                return JsonResponse({"status":"fail","message":'Invalid Credentials'}, status = 400)
        except Users.DoesNotExist as e:
            return JsonResponse({'status':'fail','message':str(e)}, status = 500)
class LogoutUser(APIView):
    def post(self, request):
        request.session.flush()
        return JsonResponse({"status":"pass","message":'Logout Successful'}, status = 200)
    
class ApproveUser(APIView):
    def post(self, request):
        user_id = request.data.get('user_id')
        if not user_id:
            return JsonResponse({"status":'fail','message':'User ID is required'},status = 400)
        try:
            user = Users.objects.get(user_id=user_id)
            user.user_approval = True if user.user_approval == False else False
            user.user_status = 'approved' if user.user_approval == True else 'pending'  
            user.save()
            return JsonResponse({"status":"pass","message":'User Approved Successfully', 'user_status':user.user_status,"user_approval":user.user_approval}, status = 200)
        except Users.DoesNotExist as e:
            return JsonResponse({"status":"fail","message":str(e)}, status = 404)
        
class RejectUser(APIView):
    def post(self, request):
        user_id = request.data.get('user_id')
        reason = request.data.get('reason')
        if not user_id:
            return JsonResponse({"status":'fail','message':'User ID is required'},status = 400)
        elif not reason:
            return JsonResponse({"status":'fail','message':'Rejection reason is required'},status = 400)
        try:
            user = Users.objects.get(user_id=user_id)
            user.user_approval = False if user.user_approval == True else True
            user.user_status = 'rejected' if user.user_approval == False else 'pending'  
            user.message = reason
            user.save()
            return JsonResponse({"status":"pass","message":'User Rejected Successfully', 'user_status':user.user_status,'user_approval':user.user_approval}, status = 200)
        except Users.DoesNotExist as e:
            return JsonResponse({"status":"fail","message":str(e)}, status = 404)
