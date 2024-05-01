from datetime import datetime, timedelta

class Lesson():
    def __init__(self, duration, lecture_name, start_time = datetime.now()):
        self.duration = duration
        self.lecture_name = lecture_name
        self.start_time = start_time

    def __str__(self) -> str:
        return "lecture name: " + self.lecture_name + ", duration: " + str(self.duration) + ", start time: " + str(self.start_time.time()) + ", end time: " + str((self.start_time + timedelta(minutes=self.duration)).time())

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Lesson):
            return False
        return (
            self.duration == other.duration
            and self.lecture_name == other.lecture_name
            and self.start_time == other.start_time
        )
    
    def setStartTime(self, start_time):
        self.start_time = start_time