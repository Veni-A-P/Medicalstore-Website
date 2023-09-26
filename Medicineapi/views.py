from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from rest_framework.status import ( HTTP_400_BAD_REQUEST,HTTP_404_NOT_FOUND,HTTP_200_OK,HTTP_201_CREATED)
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from Medicine.models import Medicine 
from .serializers import MedicineSerializer
from django.db.models import Q

#signup 

@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))

def signup(request):
    username =request.data.get('username')
    email =request.data.get('email') 
    password=request.data.get('password')
    confirm_password=request.data.get('confirm_password')
    
    if username is None or email is None or password is None or  confirm_password is None:
        return Response({'error': 'Please provide username,email, password and confirm password'},status=HTTP_400_BAD_REQUEST)
    
    elif password!= confirm_password:
        return Response({'error': "Your password and confirm password are not Same!!"},status=HTTP_400_BAD_REQUEST)
    
    elif User.objects.filter(username=username).exists():
        return Response({'error': 'Username already taken'}, status=HTTP_400_BAD_REQUEST)
    
    elif User.objects.filter(email=email).exists():
        return Response({'error': 'email already taken'}, status=HTTP_400_BAD_REQUEST)
    else:
        user = User.objects.create_user(username=username, password=password,email=email)
        user.save()
    return Response({'success': 'User created successfully'},status= HTTP_201_CREATED)    
   
# login 

@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))

def login(request):
    username = request.data.get("username")
    password = request.data.get("password")
    if username is None or password is None:
        return Response({'error': 'Please provide both username and password'},status=HTTP_400_BAD_REQUEST)
    
    user = authenticate(username = username, password = password)
    
    if not user:
        return Response({'error': 'Invalid Credentials'},status=HTTP_404_NOT_FOUND)
    else:
        token, _ = Token.objects.get_or_create(user=user)
    
    return Response({'token': token.key},status=HTTP_200_OK) 

# create 

@api_view(['POST'])
@permission_classes([IsAuthenticated])

def add_medicine(request):
    if request.method =='POST':
        serializer = MedicineSerializer(data=request.data)
        if serializer.is_valid():
            medicine =serializer.save()
            response_data = {
                "Id":medicine.id,
                "Name":medicine.Name,
                "Type":medicine.Type,
                "Price":medicine.Price,
                "Manufacturing_date":medicine.Manufacturing_date,
                "Expiry_date" : medicine.Expiry_date 
            } 
            return Response(response_data,status=HTTP_201_CREATED)  
        else:
            return Response(serializer.errors,status=HTTP_400_BAD_REQUEST) 

#list 
      
@api_view(['GET']) 
@permission_classes([IsAuthenticated]) 
def list_medicine(request):
  
        medicine = Medicine.objects.all()
        serializer = MedicineSerializer(medicine,many = True)
        return Response(serializer.data)
    
#update

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_medicine(request,id):
    try:
        medicine = Medicine.objects.get(id=id)    
    except Medicine.DoesNotExist:
          return Response({'error':"Medicine not found"},status=HTTP_404_NOT_FOUND)
    
    serializer = MedicineSerializer(instance=medicine, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data,status=HTTP_200_OK)
    else:
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
  
 
#delete 

@api_view(['DELETE']) 
@permission_classes([IsAuthenticated])
def delete_medicine(request,id):
    medicine =Medicine.objects.get(id=id)
    medicine.delete()
    return Response('Deleted')

#search 

@api_view(['GET'])
@permission_classes([IsAuthenticated]) 
def search(request):
    query =request.GET.get('query')
    if query:
        medicines = Medicine.objects.filter(Q(Name__icontains=query))
        serializer = MedicineSerializer(medicines, many=True)
        return Response(serializer.data)
    else:
        return Response({"error":"No medicine found"},status=HTTP_404_NOT_FOUND)