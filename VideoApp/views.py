from django.http import HttpResponse
from VideoApp.project import display_video
from rest_framework.views import APIView
from VideoApp.serializers import EnterTextAndDurationSerializer
from rest_framework.response import Response
from rest_framework import status

import imageio
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from skimage.transform import resize
from IPython.display import HTML

import torch
from diffusers import DiffusionPipeline, DPMSolverMultistepScheduler
from diffusers.utils import export_to_video
from IPython.display import HTML
from base64 import b64encode


def display_video(video):
    fig = plt.figure(figsize=(4.2,4.2))  #Display size specification
    fig.subplots_adjust(left=0, right=1, bottom=0, top=1)
    mov = []
    for i in range(len(video)):  #Append videos one by one to mov
        img = plt.imshow(video[i], animated=True)
        plt.axis('off')
        mov.append([img])

    #Animation creation
    anime = animation.ArtistAnimation(fig, mov, interval=100, repeat_delay=1000)

    plt.close()
    return anime

class EnterTextAndDurationAPIView(APIView):
    serializer_class = EnterTextAndDurationSerializer
    def post(self,request, *args, **kwargs):
        try:
            serializers = EnterTextAndDurationSerializer(data=request.data)
            if serializers.is_valid():
                prompt = serializers.data.get('prompt')
                video_duration_seconds = serializers.data.get('video_duration_seconds')

                pipe = DiffusionPipeline.from_pretrained("damo-vilab/text-to-video-ms-1.7b", torch_dtype=torch.float16, variant="fp16")
                pipe.scheduler = DPMSolverMultistepScheduler.from_config(pipe.scheduler.config)
                pipe.enable_model_cpu_offload()
                pipe.enable_vae_slicing()

                #@title Generate your video
                prompt = 'Teacher and students in the class room' #@param {type:"string"}
                video_duration_seconds = 10 #@param {type:"integer"}
                num_frames = video_duration_seconds * 10
                video_frames = pipe(prompt, negative_prompt="low quality", num_inference_steps=25, num_frames=num_frames).frames
                video_path = export_to_video(video_frames)
                video = imageio.mimread(video_path)  #Loading video
                HTML(display_video(video).to_html5_video())  #Inline video display in HTML5

                return Response(data='Thanks',status=status.HTTP_200_OK)
            else:
                return Response(data=serializers.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            return Response(data=f"""{error}""", status=status.HTTP_400_BAD_REQUEST)
def text_to_video(request):
    response = display_video