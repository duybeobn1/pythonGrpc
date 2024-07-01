import grpc
from concurrent import futures
import logging
import park_pb2
import park_pb2_grpc
import subprocess
import uuid
import time
from threading import Lock
from google.protobuf.timestamp_pb2 import Timestamp

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CarParkServicer(park_pb2_grpc.CarParkServiceServicer):
    def __init__(self):
        self.log_queue = []
        self.lock = Lock()
        self.streams = []

    def ProcessCommand(self, request, context):
        try:
            command = request.command
            logger.info(f"Processing command: {command}")

            script_map = {
                "start": r"/AutoExtract+Behavior/part1.py",
                "read": r"/AutoExtract+Behavior/part2.py",
            }

            script = script_map.get(command)
            if not script:
                raise ValueError("Invalid command")

            logger.info(f"Executing script: {script}")

            # Use subprocess.Popen to capture stdout and stderr in real-time
            process = subprocess.Popen(
                ["python3", "-u", script],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )

            # Read stdout and stderr in real-time
            while True:
                output = process.stdout.readline()
                if output == "" and process.poll() is not None:
                    break
                if output:
                    self._send_log_message(output.strip())

            stderr = process.communicate()[1]
            logger.error(f"Script stderr: {stderr}")

            if process.returncode != 0:
                raise RuntimeError(f"Script error: {stderr}")

            # Use predefined UUIDs for capteur IDs
            test_id = uuid.uuid4()
            capteur_ids = [
                "550e8400-e29b-41d4-a716-446655440001",
                "550e8400-e29b-41d4-a716-446655440002",
                "550e8400-e29b-41d4-a716-446655440003"
            ]
            capteur_id = capteur_ids[0]  # Just an example; choose based on your logic
            valeur = output.strip()

            result = f"{test_id},{capteur_id},{valeur}"
            return park_pb2.CommandResponse(result=result)

        except Exception as e:
            logger.error(f"Error processing command: {e}")
            context.set_details(str(e))
            context.set_code(grpc.StatusCode.INTERNAL)
            return park_pb2.CommandResponse(result="Error occurred")

    def StreamLogs(self, request, context):
        stream = []
        with self.lock:
            self.streams.append(stream)
        while True:
            while stream:
                log_message = stream.pop(0)
                yield log_message
            time.sleep(1)

    def _send_log_message(self, message):
        timestamp = Timestamp()
        timestamp.GetCurrentTime()
        log_message = park_pb2.LogMessage(message=message, timestamp=str(timestamp))
        with self.lock:
            for stream in self.streams:
                stream.append(log_message)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    park_pb2_grpc.add_CarParkServiceServicer_to_server(CarParkServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    logger.info("gRPC server started on port 50051.")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
