import copy
import random
from constants import AVERAGE_DURATION, DAYS, MIDDLE_OF_A_DAY
from RoomInDay import RoomInDay
from Timetable import Timetable
from datetime import timedelta
import numpy as np
from Lesson import Lesson


def load(path) -> tuple[list[str], list[Lesson]]:
    with open(path, "r") as f:
        rooms = [room.strip() for room in f.readline().split(":")[1].split(",")]
        f.readline()
        lines = f.readlines()
        lessons = []
        for line in lines:
            data = line.split(",")
            lesson = Lesson(int(data[1].strip()), data[0].strip())
            lessons.append(lesson)
            line = f.readline()
    return rooms, lessons

def generate_initial_chromosomes(pop_size, rooms: list, lessons: list):
    population = []
    for _ in range(pop_size):
        lessons_copy = copy.deepcopy(lessons)
        rooms_in_a_day = []
                    
        for i in range(5): # iterate over days
            day = DAYS[i]
            for j in range(5): # iterate over rooms
                room = rooms[j]
                duration = 0
                room_in_a_day_list = []
                while True:
                    if len(lessons_copy) == 0:
                        break
                    lesson = random.choice(lessons_copy)
                    duration += lesson.duration
                    room_in_a_day_list.append(lesson)
                    lessons_copy.remove(lesson)
                    if duration >= AVERAGE_DURATION + 120:
                        break
                    duration += 15 #Pauza

                half_duration = timedelta(minutes=duration // 2)
                start = MIDDLE_OF_A_DAY - half_duration
                end = MIDDLE_OF_A_DAY + half_duration
                room_in_day = RoomInDay(day, room, start, end, room_in_a_day_list)

                rooms_in_a_day.append(room_in_day)
        timetable = Timetable(rooms_in_a_day)
        population.append(timetable)
    
    return population
    

def natural_selection(chromosomes: list[Timetable], n_keep):
    return chromosomes[:n_keep]

def roulette_selection(parents):
    pairs = []
    i = 0
    for i in range(0, len(parents), 2):
        weights = []
        for i in range(len(parents)):
            weights.append((i+1)*random.random())
        if (weights[0] >= weights[1]):
            maxInd1 = 0
            maxInd2 = 1
        else:
            maxInd1 = 1
            maxInd2 = 0
        
        for i in range(2, len(parents)):
            if weights[i] > weights[maxInd1]:
                maxInd2 = maxInd1
                maxInd1 = i
            elif weights[i] > weights[maxInd2]:
                maxInd2 = 1
        pairs.append([parents[maxInd1], parents[maxInd2]])
        
    return pairs


def getLessonInfo(timetable, lesson):
    for room_in_a_day in timetable.listOfRoomsOfADay:
        if lesson in room_in_a_day.listOfLesson:
            return (room_in_a_day.day, room_in_a_day.room)
    return None, None

def crossover(parents, lessons):
    child1, child2 = Timetable([]), Timetable([])
    children = []
    for parent1, parent2 in parents:
        for lesson in lessons:
            r = random.random()
            parent1_day, parent1_room = getLessonInfo(parent1, lesson)
            parent2_day, parent2_room = getLessonInfo(parent2, lesson)
            if r < 0.5:
                child1.appendLesson(lesson, parent1_day, parent1_room)
                child2.appendLesson(lesson, parent2_day, parent2_room)
            else:
                child1.appendLesson(lesson, parent2_day, parent2_room)
                child2.appendLesson(lesson, parent1_day, parent1_room)
        children.append(child1)
        children.append(child2)

    return children


def mutation(timetables: list[Timetable], mutation_rate):
    mutated_chromosomes = []
    for timetable in timetables:
        if random.random() < mutation_rate:
            timetable.swapLesson()
        mutated_chromosomes.append(timetable)
    
    return mutated_chromosomes

def rank_chromosomes(timetables):
    return sorted(timetables, key = lambda timetable: timetable.criterium(), reverse=True)   

def elitis(chromosomes_old,chromosomes_new, elitis_rate, population_size):
    old_ind_size = int(np.round(population_size*elitis_rate))
    return chromosomes_old[:old_ind_size] + chromosomes_new[:(population_size-old_ind_size)]


def population_stats(timetables: list[Timetable]): 
    i, sum = 0, 0
    while i < len(timetables) - 1:
        sum += timetables[i].criterium()
        i += 1
    average = sum / i
    return timetables[0].criterium(), average

def genetic(population_size, mutation_rate = 0.2, elitis_rate=0.1, max_iter = 100):
    rooms, lessons = load("dataset/data_timetable.txt")
    
    avg_list = []
    best_list = []
    all_avg_list = []
    generations_list = []
    all_best_list = []
    curr_best = 10000
    same_best_count = 0
    
    timetables = generate_initial_chromosomes(population_size, rooms, lessons)

    for iter in range(max_iter):
        
        ranked_parents = rank_chromosomes(timetables)     
        best, average = population_stats(ranked_parents)
        parents = natural_selection(ranked_parents, population_size)     

        pairs = roulette_selection(parents) 
            
        children = crossover(pairs, lessons)
        timetables = mutation(children, mutation_rate)


        ranked_children = rank_chromosomes(timetables)
        timetables=elitis(ranked_parents,ranked_children, elitis_rate, population_size)
        timetables[0].setTimes()
        
        print("Generation: ",iter+1," Curr best: {:.3f}".format(best), 
            "X = {} ".format(str(timetables[0])))
        print("-------------------------")
        
        avg_list.append(average)
        if best < curr_best:
            best_list.append(best)
            curr_best = best
            same_best_count = 0
        else:
            same_best_count += 1
            best_list.append(best)
        
        if (timetables[0].criterium() > 400):
            avg_list = avg_list[:iter]
            best_list = best_list[:iter]
            all_avg_list.append(avg_list)
            all_best_list.append(best_list)
            generations_list.append(iter)
            
            print("\nSolution found! Chromosome content: X = {:.3f} \n".format(timetables[0].criterium()))
            return
            
        if same_best_count > 20:
            print("\nStopped due to convergance. Best chromosome X = {:.3f} \n".format(timetables[0].criterium()))
        
            avg_list = avg_list[:iter]
            best_list = best_list[:iter]
            all_avg_list.append(avg_list)
            all_best_list.append(best_list)
            generations_list.append(iter)
            
            return
        
        if iter == 499:
            avg_list = avg_list[:iter]
            best_list = best_list[:iter]
            all_avg_list.append(avg_list)
            all_best_list.append(best_list)
            generations_list.append(iter)
            print("\nStopped due to max number of iterations, solution not found. Best chromosome X = {:.3f} \n".format(timetables[0].criterium()))
            return