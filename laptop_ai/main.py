from RobotAssistant import RobotAssistant 
from utils.video_stream import start_in_background
 
def main(): 
    robot_assistant = RobotAssistant()
    # Start ESP32 video processing -> push to dashboard ingest endpoints
    start_in_background()
    robot_assistant.robot_controller.run()

if __name__ == "__main__":
    main()
