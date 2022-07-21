from django.shortcuts import render
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import re
from .serializers import *
from .models import *
from .serializers import *
from .utils import get_duration,validate_video


def homeView (request,*args, **kwargs):
	return render(request, 'index.html')

class VideoUploadView(APIView):
    """ For uploading/receiving videos. """

    def post(self, request, format = None):
        video_file = request.FILES.get('video')
        # video_file = request.data.getlist('video')[0]
        video_size = round(video_file.size / 1048576,2) # converting the bytes to MB
        video_format = video_file.name.split(".")[-1]

        try:
            # Sometimes we may get duration like 600.01 sec for a 10 minutes and some milisec long video and we are omitting the miliseconds here using int().
            # We could've rounded with 0 but it might sometimes be inappropiate, as round(6000.92,0) gives 601.0
            video_duration = int(get_duration(video_file.temporary_file_path())) 
            error_messages = validate_video(video_size,video_format,video_duration)
        
            if error_messages:
                return Response({'error':error_messages}, status=status.HTTP_400_BAD_REQUEST)

            Video.objects.create(video=video_file, size=video_size, duration=video_duration, extension=video_format)
            return Response({'The video has been uploaded.'}, status=status.HTTP_201_CREATED)

        except Exception as e:
            # print(e)
            return Response({'Some unknown internal error occured. Please try again.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class VideoListView(APIView):
    """ For listing all the videos. The date is accepted in Year-month-day format. """
    
    def get(self,request, format=None):
        initial_date = request.query_params.get('initial_date',timezone.datetime(2022,1,1)) 
        final_date = request.query_params.get('final_date', timezone.now())
        min_size = request.query_params.get('min_size', 0)
        max_size = request.query_params.get('max_size', 1025) # range checks files lesser than 1025, i.e upto 1024
        video_format = request.query_params.get('extension', None)
        
        try:
            if type(initial_date) == str:
                initial_date = timezone.datetime.strptime(initial_date, '%Y-%m-%d').date()
            if type(final_date) == str:
                final_date = timezone.datetime.strptime(final_date, '%Y-%m-%d').date() + timezone.timedelta(days=1) # adding 1 day to made compatible with range

            videos = Video.objects.filter(size__range=[min_size,max_size], created__range=[initial_date,final_date],
                                        extension__in=[video_format] if video_format else ['mp4','mkv'])
            serializer = VideoSerializer(videos, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        except Exception as e:
            print(e)
            # returns error message, ex:- if date time format doesn't match then it gives error message 
            return Response({'error':f'{e}'}, status=status.HTTP_400_BAD_REQUEST)


class VideoChargesView(APIView):
    """ For providing charges info  """

    def get(self, request, format=None):
        size = request.query_params.get('size')
        duration = request.query_params.get('length') # expecting video length format as minute:second
        video_format = request.query_params.get('extension')
        error = ""         

        if not (size and duration and video_format):
            error = "Please provide all the required parameters (size, length and extension)."
        elif bool(re.match(r"[0-9]*:[0-9]*$", duration)) == False:
            error = "Please provide the video length in Minutes:Seconds format"
        if error:
            return Response({'error':error}, status=status.HTTP_400_BAD_REQUEST)

        #converting the duration in Minutes:Seconds format to seconds
        duration = duration.split(":")
        duration = int(duration[0])*60 + int(duration[1])
        error_messages = validate_video(int(size),video_format,duration)
        
        if error_messages:
            return Response({'error':error_messages}, status=status.HTTP_400_BAD_REQUEST)
        if int(size) < 500:
            charge = (5+12.5) if duration < 378 else (5+20) # 378 seconds = 6 minutes 18 seconds
        else:
            charge = (12.5+12.5) if duration < 378 else (12.5+20) # 378 seconds = 6 minutes 18 seconds

        return Response({'charges':charge}, status=status.HTTP_200_OK)

        