from constants import START_OF_DAY, END_OF_DAY, MIDDLE_OF_A_DAY
from datetime import timedelta

class RoomInDay():
    def __init__(self, day:str, room:str, start, end, listOfLesson = []) -> None:
        self.day = day
        self.room = room
        self.listOfLesson = listOfLesson
        self.start = start
        self.end = end

    def get_criterium(self):
        if len(self.listOfLesson) > 4:
            return -10000
        if self.start == self.end:
            return 0
        if self.start.hour < 7:
            return -10000
        if self.end.hour > 19:
            return -10000
        a = (self.start - START_OF_DAY).total_seconds()/3600
        b = (END_OF_DAY - self.end).total_seconds()/3600
        return a * b
    
    def append_lesson(self, lesson):
        self.listOfLesson.append(lesson)
        half_duration = timedelta(minutes=self.getDuration() // 2)
        self.start = MIDDLE_OF_A_DAY - half_duration
        self.end = MIDDLE_OF_A_DAY + half_duration
        
    def getDuration(self):
        duration = 0
        for lesson in self.listOfLesson:
            duration += lesson.duration
        duration += (len(self.listOfLesson) - 1) * 15
        return duration
    
    def setStartTimes(self):
        current_time = self.start
        for lesson in self.listOfLesson:
            lesson.setStartTime(current_time)
            current_time += timedelta(minutes=lesson.duration + 15)

    