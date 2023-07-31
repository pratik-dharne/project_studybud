from rest_framework.decorators import api_view
from rest_framework.response import Response
from base.models import Room
from .serializers import RoomSerializer


@api_view(['GET'])
def getroutes(request):
    
    routes = [
        'GET/api',
        'GET/api/rooms',
        'GET/api/rooms/:id'
    ]
    
    return Response(routes)

@api_view(['GET'])
def getrooms(request):
    
    rooms=Room.objects.all()
    rooms=RoomSerializer(rooms,many=True) # many signifies multiple object to serialise
    return Response(rooms.data)


@api_view(['GET'])
def getroom(request,pk):
    
    rooms=Room.objects.get(id=pk)
    rooms=RoomSerializer(rooms,many=False) 
    return Response(rooms.data)