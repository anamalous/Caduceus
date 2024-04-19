from datetime import datetime, time, timedelta, date

# Define working hours (9 AM to 5 PM)
START_HOUR = 9
END_HOUR = 17

# Define available operation theatres (can be modified)
OPERATION_THEATRES = 6

class Surgery:
  def __init__(self, surgery_id, surgery_name, preassigned_time=None):
    self.id = surgery_id
    self.name = surgery_name
    self.preassigned_time = preassigned_time  # Preassigned time slot (time object)

class Doctor:
  def __init__(self, doctor_id, name, specialties):
    self.id = doctor_id
    self.name = name
    self.specialties = specialties  # List of surgery names

class OperationTheatre:
  def __init__(self, ot_id, compatible_surgeries):
    self.id = ot_id
    self.compatible_surgeries = compatible_surgeries  # List of surgery names (e.g., ["appendectomy", "knee replacement"])

class Schedule:
  def __init__(self, operation_theatres):
    self.slots = {hour: [None] * len(operation_theatres) for hour in range(START_HOUR, END_HOUR)}
    self.operation_theatres = operation_theatres  # List of OperationTheatre objects

  def can_schedule(self, surgery, hour):
    # Check if enough operation theatres are free and compatible
    free_and_compatible_ots = 0
    for i, ot in enumerate(self.operation_theatres):
      if self.slots[hour][i] is None and surgery.name in ot.compatible_surgeries:
        free_and_compatible_ots += 1
    return free_and_compatible_ots >= 1  # Requires enough compatible OTs

  def schedule_surgery(self, surgery):
    if surgery.preassigned_time:
      # Try to fit preassigned time
      hour = surgery.preassigned_time.hour
      if self.can_schedule(surgery, hour):
        for i, ot in enumerate(self.operation_theatres):
          if self.slots[hour][i] is None and surgery.name in ot.compatible_surgeries:
            self.slots[hour][i] = surgery
            break  # Assign to first compatible OT
        return True
      else:
        print(f"Surgery {surgery.id} cannot be scheduled at preassigned time {surgery.preassigned_time}")
    else:
      # Find a suitable slot for unassigned surgeries
      for hour in range(START_HOUR, END_HOUR):
        slot_index = self.slots[hour].index(None)
        if self.can_schedule(surgery, hour):
          for i, ot in enumerate(self.operation_theatres):
            if self.slots[hour][i] is None and surgery.name in ot.compatible_surgeries:
              self.slots[hour][i] = surgery
              # Update end time based on surgery duration
              end_time = datetime.combine(date.today(), time(hour)) + timedelta(hours=1)
              end_time = end_time.time()
              if any(slot != None for slot in self.slots[end_time.hour][slice(slot_index, slot_index+1)]):  
                for j in range(i, -1, -1):
                    self.slots[hour][j] = None
                continue
              return True
          return True
      print(f"Surgery {surgery.id} could not be scheduled within working hours")

# Sample surgeries
surgery1 = Surgery(1, "Appendectomy", time(11))  # Preassigned time
surgery2 = Surgery(2, "Knee Replacement")
surgery3 = Surgery(3, "Cataract Surgery")

doctor1 = Doctor(1, "Dr. Smith", ["Appendectomy"])
doctor2 = Doctor(2, "Dr. Jones", ["Knee Replacement"])
doctor3 = Doctor(3, "Dr. Lee", ["Cataract Surgery", "Appendectomy"])

# Sample operation theatres
ot1 = OperationTheatre(1, ["Appendectomy", "Cataract Surgery"])
ot2 = OperationTheatre(2, ["Knee Replacement", "Cataract Surgery"])
ot3 = OperationTheatre(3, ["Appendectomy"])
ot4 = OperationTheatre(4, ["Knee Replacement"])
ot5 = OperationTheatre(5, ["Cataract Surgery"])
ot6 = OperationTheatre(6, ["Appendectomy", "Knee Replacement"])

# Create schedule object
operation_theatres = [ot1, ot2, ot3, ot4, ot5, ot6]  # List of OperationTheatre objects
schedule = Schedule(operation_theatres)

# Schedule surgeries
schedule.schedule_surgery(surgery1)
schedule.schedule_surgery(surgery2)
schedule.schedule_surgery(surgery3)

def assigndoc(schedule,docs):
    for hour, slots in schedule.slots.items():
        availdocs=docs.copy()
        for j in range(len(slots)):
            if slots[j] is not None:
                n=slots[j].name
                for d in availdocs:
                    if n in d.specialties:
                        slots[j]={slots[j].id:[slots[j].name,d.name]}
                        availdocs.remove(d)
                        break
    return schedule
"""
print("Surgery Schedule:")
for hour, slots in assigndoc(schedule).slots.items():
  print(f"{hour}:00 - {slots}")

"""
