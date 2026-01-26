
import json
import subprocess
import logging
from channels.generic.websocket import WebsocketConsumer
from newapp.models import CameraFeed

logger = logging.getLogger(__name__)

class VideoStreamConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()
        logger.info('WebSocket connection established.')

        camera_feeds = CameraFeed.objects.all()
        for camera in camera_feeds:
            logger.info(f'Camera Feed: ID={camera.id}, Status={camera.status}, Is Streaming={camera.is_streaming}')

        try:
            camera = CameraFeed.objects.filter(status='active').first()
            if camera:
                logger.info(f'Selected Camera: {camera.name} (ID: {camera.id})')
                self.start_stream({'camera_id': camera.id})
            else:
                self.send(text_data=json.dumps({'error': 'No available camera feed found.'}))
                logger.warning('No available camera feed found.')
        except CameraFeed.DoesNotExist:
            self.send(text_data=json.dumps({'error': 'Camera feed does not exist.'}))
            logger.error('Camera feed does not exist.')

    def disconnect(self, close_code):
        self.stop_stream()
        logger.info(f'WebSocket connection closed with code {close_code}.')

    def start_stream(self, data):
        camera_id = data.get('camera_id')
        logger.info(f'Start stream request received for camera_id {camera_id}')
        
        if not camera_id:
            self.send(text_data=json.dumps({'error': 'Camera ID is required.'}))
            logger.warning('Camera ID is missing in start_stream request.')
            return

        try:
            camera = CameraFeed.objects.get(id=camera_id)
            feed_url = camera.feed_url
            logger.info(f'Feed URL retrieved: {feed_url}')

            ffmpeg_command = [
                'ffmpeg',
                '-rtsp_transport', 'tcp',
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
            logger.info('Streaming started.')
            self.stream_video()

        except CameraFeed.DoesNotExist:
            self.send(text_data=json.dumps({'error': 'Camera feed does not exist.'}))
            logger.error(f'Camera feed with id {camera_id} does not exist.')

    def stream_video(self):
        logger.info('Starting video streaming...')
        buffer = b''

        try:
            while True:
                data = self.process.stdout.read(40960)
                if not data:
                    logger.warning('No data received from FFmpeg.')
                    break

                buffer += data

                while True:
                    start_index = buffer.find(b'\xff\xd8')
                    end_index = buffer.find(b'\xff\xd9') + 2

                    if start_index != -1 and end_index != -1:
                        frame = buffer[start_index:end_index]

                        self.send(bytes_data=frame)
                        logger.debug(f'Frame sent to WebSocket. Frame size: {len(frame)} bytes')

                        # Skip saving the image and just log the frame size
                        logger.info(f'Frame size: {len(frame)} bytes')

                        buffer = buffer[end_index:]
                    else:
                        break

                stderr = self.process.stderr.read().decode('utf-8')
                if stderr:
                    logger.error(f'FFmpeg stderr: {stderr}')

        except Exception as e:
            logger.error(f'Error during streaming: {e}')
        finally:
            self.stop_stream()

    def stop_stream(self):
        if hasattr(self, 'process') and self.process:
            self.process.terminate()
            self.process.wait()
            logger.info('Stopped FFmpeg process.')

        try:
            camera = CameraFeed.objects.filter(is_streaming=True).first()
            if camera:
                camera.is_streaming = False
                camera.save()
                logger.info('Streaming status updated for camera.')
        except CameraFeed.DoesNotExist:
            logger.error('Camera feed does not exist.')

