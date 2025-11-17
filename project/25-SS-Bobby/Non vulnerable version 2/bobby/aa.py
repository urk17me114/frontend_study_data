from login.models import Subject, TeacherAvailability, ClassSection, Room, TimeSlot

# Clear previous data
Subject.objects.all().delete()
TeacherAvailability.objects.all().delete()
ClassSection.objects.all().delete()
Room.objects.all().delete()
TimeSlot.objects.all().delete()

# Subjects
subjects_data = [
    ("Math", 5, ""),
    ("English", 4, ""),
    ("History", 3, ""),
    ("PE", 2, "Gym"),
    ("Art", 2, ""),
    ("Geography", 3, ""),
    ("Physics", 2, ""),
    ("Chemistry", 2, ""),
    ("Biology", 2, ""),
    ("Physics Lab", 2, "Lab"),
    ("Chemistry Lab", 2, "Lab"),
    ("Biology Lab", 2, "Lab")
]

subjects = []
for name, periods, room_type in subjects_data:
    subjects.append(Subject.objects.create(name=name, periods_per_week=periods, specialized_room=room_type))

# Class Sections
#c1 = ClassSection.objects.create(name="Class 1")
#c2 = ClassSection.objects.create(name="Class 2")
#c3 = ClassSection.objects.create(name="Class 3")
#c4 = ClassSection.objects.create(name="Class 4")
#c5 = ClassSection.objects.create(name="Class 5")
#c6 = ClassSection.objects.create(name="Class 6")
#c7 = ClassSection.objects.create(name="Class 7")
c8 = ClassSection.objects.create(name="Class 8")
c9 = ClassSection.objects.create(name="Class 9")
c10 = ClassSection.objects.create(name="Class 10")

for cls in [c8, c9, c10]:
    cls.subjects.set(subjects)  # All subjects for each grade


# New Teachers
t4 = TeacherAvailability.objects.create(username="BSE038", name="Teft Bridge", max_periods_per_day=6, max_periods_per_week=30)
t4.subjects.set([subjects[0]])
t4.class_sections.set([c8, c9, c10])

t5 = TeacherAvailability.objects.create(username="HOY695", name="Lift Reshi", max_periods_per_day=6, max_periods_per_week=30)
t5.subjects.set([subjects[1]])
t5.class_sections.set([c8, c9, c10])

t6 = TeacherAvailability.objects.create(username="IXX858", name="Sophia Williams", max_periods_per_day=6, max_periods_per_week=30)
t6.subjects.set([subjects[3]])
t6.class_sections.set([c8, c9, c10])

t7 = TeacherAvailability.objects.create(username="LIE157", name="Kaladin Stormblessed", max_periods_per_day=5, max_periods_per_week=25)
t7.subjects.set([subjects[4]])
t7.class_sections.set([c8, c9, c10])

t8 = TeacherAvailability.objects.create(username="NIM304", name="Taln Elil", max_periods_per_day=6, max_periods_per_week=30)
t8.subjects.set([subjects[5]])
t8.class_sections.set([c8, c9, c10])

t9 = TeacherAvailability.objects.create(username="QAX997", name="Dalinar Kohlin", max_periods_per_day=6, max_periods_per_week=30)
t9.subjects.set([subjects[6]])
t9.class_sections.set([c8, c9, c10])

t10 = TeacherAvailability.objects.create(username="XFE995", name="Shallan Davar", max_periods_per_day=6, max_periods_per_week=30)
t10.subjects.set([subjects[7]])
t10.class_sections.set([c8, c9, c10])

t11 = TeacherAvailability.objects.create(username="YAR363", name="Jasnah Ivory", max_periods_per_day=6, max_periods_per_week=30)
t11.subjects.set([subjects[8]])
t11.class_sections.set([c8, c9, c10])


# Rooms
Room.objects.create(name="Room 101", room_type="Regular")
Room.objects.create(name="Room 102", room_type="Regular")
Room.objects.create(name="Room 103", room_type="Regular")
Room.objects.create(name="Room 103", room_type="Regular")
Room.objects.create(name="Room 103", room_type="Regular")
Room.objects.create(name="Room 201", room_type="Regular")
Room.objects.create(name="Room 202", room_type="Regular")
Room.objects.create(name="Room 203", room_type="Regular")
Room.objects.create(name="Room 201", room_type="Regular")
Room.objects.create(name="Room 202", room_type="Regular")
Room.objects.create(name="Room 203", room_type="Regular")
Room.objects.create(name="Room 301", room_type="Regular")
Room.objects.create(name="Room 302", room_type="Regular")
Room.objects.create(name="Room 303", room_type="Regular")
Room.objects.create(name="Room 401", room_type="Lab")
Room.objects.create(name="Room 402", room_type="Lab")
Room.objects.create(name="Room 403", room_type="Lab")



# TimeSlots (Mon-Fri, Periods 1–7)
days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri']
for day in days:
    for period in range(1, 6):
        TimeSlot.objects.create(day=day, period=period)

print("Sample data created successfully.")
