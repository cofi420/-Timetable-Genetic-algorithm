from datetime import datetime

START_OF_DAY = datetime.now().replace(hour = 7, minute = 0, second = 0, microsecond = 0)
END_OF_DAY = datetime.now().replace(hour = 19, minute = 0, second = 0, microsecond = 0)
MIDDLE_OF_A_DAY = datetime.now().replace(hour = 13, minute = 0, second = 0, microsecond = 0)
DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
AVERAGE_DURATION = 120 
