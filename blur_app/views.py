from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
import cv2
import time
from ultralytics import YOLO
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from io import BytesIO
import os
from django.conf import settings
import numpy as np
from celery import shared_task
from celery.result import AsyncResult
from .utils import visualize
from moviepy.editor import (
    VideoFileClip,
    AudioFileClip,
    CompositeAudioClip,
    CompositeVideoClip,
)
import json

model_path = "model/best.pt"
model = YOLO(model_path)


@shared_task(bind=False)
def process_video_task(input_path, output_path, selected_class=["face", "plate"]):
    clip = VideoFileClip(input_path)
    fps = clip.fps
    if len(selected_class) == 0:
        selected_class = ["face", "plate"]

    def process_frame(frame):
        processed_frame = visualize(
            frame, model(frame, verbose=False)[0].boxes, cls=selected_class
        )
        return processed_frame

    processed_clip = clip.fl_image(process_frame)
    audio_clip = AudioFileClip(input_path)
    processed_clip.set_audio(audio_clip)
    processed_clip.write_videofile(
        output_path, fps=fps, codec="h264_nvenc", audio_codec="aac"
    )

    return output_path


@csrf_protect
def process_video(request):
    if request.method == "POST":
        t0 = time.time()
        video = request.FILES.get("video")
        if not video:
            return JsonResponse(
                {
                    "status": "error",
                    "message": "No video file was found in the request.",
                }
            )

        data = video.read()
        video_name = f"{int(time.time())}_{video.name}"
        input_path = os.path.join(settings.MEDIA_ROOT, "in", video_name)

        with open(input_path, "wb+") as destination:
            for chunk in video.chunks():
                destination.write(chunk)
        out_file = os.path.join(settings.MEDIA_ROOT, "out", f"{int(time.time())}.mp4")
        selected_class = request.POST.getlist("labels")
        task = process_video_task.delay(
            input_path=input_path, output_path=out_file, selected_class=selected_class
        )

        while not task.ready():

            result = task.get()
            if result and os.path.isfile(result):
                with open(result, "rb") as f:
                    response = HttpResponse(f.read(), content_type="video/mp4")
                    response["Content-Disposition"] = "attachment; filename=output.mp4"
                    t2 = time.time()
                    print(t2 - t0)
                    return response
            else:
                return JsonResponse(
                    {
                        "status": "error",
                        "message": "Task returned None or result file not found.",
                    }
                )
    else:
        return render(request, "index.html")
