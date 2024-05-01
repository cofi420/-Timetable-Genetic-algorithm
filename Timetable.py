import random
from RoomInDay import RoomInDay
from datetime import timedelta
from constants import MIDDLE_OF_A_DAY

class Timetable():
    def __init__(self, listOfRoomsOfADay):
        self.listOfRoomsOfADay = listOfRoomsOfADay
    
    def criterium(self):
        sum = 0
        for elem in self.listOfRoomsOfADay:
            sum += elem.get_criterium()
        return sum

    def __str__(self) -> str:
        ret_val = ""
        for room_in_a_day in self.listOfRoomsOfADay:
            ret_val += f"Day: {room_in_a_day.day}, Room: {room_in_a_day.room}, Start: {room_in_a_day.start.time()}, End: {room_in_a_day.end.time()}\n"
            for lesson in room_in_a_day.listOfLesson:
                ret_val += (str(lesson) + "\n")
            ret_val += "\n\n"
            
        return ret_val
    
    def swapLesson(self):
        room1 = random.choice(self.listOfRoomsOfADay)
        room2 = random.choice(self.listOfRoomsOfADay)
        lesson1 = random.choice(room1.listOfLesson)
        lesson2 = random.choice(room2.listOfLesson)
        lesson1, lesson2 = lesson2, lesson1        

    def appendLesson(self, lesson, day, room):
        found = False
        for room_in_a_day in self.listOfRoomsOfADay:
            if room_in_a_day.day == day and room_in_a_day.room == room:
                room_in_a_day.append_lesson(lesson)
                
                found = True
        if not found:
            half_duration = timedelta(minutes=lesson.duration // 2)
            start = MIDDLE_OF_A_DAY - half_duration
            end = MIDDLE_OF_A_DAY + half_duration
            self.listOfRoomsOfADay.append(RoomInDay(day, room, start, end, [lesson]))

    def setTimes(self):
        for room_in_a_day in self.listOfRoomsOfADay:
            room_in_a_day.setStartTimes()



        