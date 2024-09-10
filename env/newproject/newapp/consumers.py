# import cv2
# import threading
# import base64
# import numpy as np
# from channels.generic.websocket import WebsocketConsumer
# from asgiref.sync import async_to_sync

# class VideoStreamConsumer(WebsocketConsumer):
#     def connect(self):
#         self.accept()
#         self.video_stream_thread = threading.Thread(target=self.stream_video)
#         self.video_stream_thread.start()

#     def disconnect(self, close_code):
#         if hasattr(self, 'video_stream_thread'):
#             self.video_stream_thread.join()

#     def stream_video(self):
#         cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

#         while True:
#             ret, frame = cap.read()
#             if not ret:
#                 break
#             _, buffer = cv2.imencode('.jpg', frame)
#             jpg_as_text = base64.b64encode(buffer).decode('utf-8')
#             self.send(text_data=jpg_as_text)

#         cap.release()

import json
import subprocess
from channels.generic.websocket import WebsocketConsumer
from .models import CameraFeed

class VideoStreamConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()
        print('WebSocket connection established.')

        # Retrieve and display camera feed information
        camera_feeds = CameraFeed.objects.all()
        for camera in camera_feeds:
            print(f'Camera Feed: ID={camera.id}, Status={camera.status}, Is Streaming={camera.is_streaming}')

        # Start streaming from the first active camera
        try:
            camera = CameraFeed.objects.filter(status='active').first()
            if camera:
                print(f'Selected Camera: {camera.name} (ID: {camera.id})')
                self.start_stream({'camera_id': camera.id})
            else:
                self.send(text_data=json.dumps({'error': 'No available camera feed found.'}))
                print('No available camera feed found.')
        except CameraFeed.DoesNotExist:
            self.send(text_data=json.dumps({'error': 'Camera feed does not exist.'}))

    def disconnect(self, close_code):
        self.stop_stream()
        print(f'WebSocket connection closed with code {close_code}.')

    def start_stream(self, data):
        camera_id = data.get('camera_id')
        print(f'Start stream request received for camera_id {camera_id}')
        
        if not camera_id:
            self.send(text_data=json.dumps({'error': 'Camera ID is required.'}))
            return

        try:
            camera = CameraFeed.objects.get(id=camera_id)
            feed_url = camera.feed_url
            print(f'Feed URL retrieved: {feed_url}')

            ffmpeg_command = [
                'ffmpeg',
                '-rtsp_transport', 'tcp',  # Use TCP for RTSP if needed
                '-i', feed_url,
                '-vf', 'scale=320:240',
                '-f', 'image2pipe',
                '-vcodec', 'mjpeg',
                '-preset', 'ultrafast',
                '-'
            ]
            self.process = subprocess.Popen(ffmpeg_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            camera.is_streaming = True
            camera.save()
            self.send(text_data=json.dumps({'status': 'Streaming started'}))
            print('Streaming started.')
            self.stream_video()

        except CameraFeed.DoesNotExist:
            self.send(text_data=json.dumps({'error': 'Camera feed does not exist.'}))
            print(f'Camera feed with id {camera_id} does not exist.')

    def stream_video(self):
        print('Starting video streaming...')
        buffer = b''

        try:
            while True:
                data = self.process.stdout.read(40960)  # Increase the chunk size
                if not data:
                    print('No data received from FFmpeg.')
                    break

                buffer += data

                while True:
                    start_index = buffer.find(b'\xff\xd8')  # JPEG start marker
                    end_index = buffer.find(b'\xff\xd9') + 2  # JPEG end marker

                    if start_index != -1 and end_index != -1:
                        frame = buffer[start_index:end_index]

                        # Send the frame to WebSocket as binary data
                        self.send(bytes_data=frame)
                        print(f'Frame sent to WebSocket. Frame size: {len(frame)} bytes')

                        buffer = buffer[end_index:]
                    else:
                        break

                stderr = self.process.stderr.read().decode('utf-8')
                if stderr:
                    print(f'FFmpeg stderr: {stderr}')

        except Exception as e:
            print(f'Error during streaming: {e}')
        finally:
            self.stop_stream()

    def stop_stream(self):
        if hasattr(self, 'process') and self.process:
            self.process.terminate()
            self.process.wait()
            print('Stopped FFmpeg process.')

        try:
            camera = CameraFeed.objects.filter(is_streaming=True).first()
            if camera:
                camera.is_streaming = False
                camera.save()
                print('Streaming status updated for camera.')
        except CameraFeed.DoesNotExist:
            print('Camera feed does not exist.')

