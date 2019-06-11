# Maddy Scott
# 06 June 2019
# Practicing making a plan in Trident

from pydent import AqSession, models

#open password file
f = open("Aquarium_password.txt", "r")
if f.mode != "r":
    raise Exception('Lol ur file aint where it should be')
pw = f.read();
session = AqSession("maddyscott", pw, "http://52.27.43.242/")

#make plan
p = models.Plan(name = "MyPlan")
p.connect_to_session(session)


#make an array with all the strains
#all_strains = {23462, 23430, 23392, 23303, 23302, 23160, 22998, 19490, 16950, 16949, 16636, 12378}
all_strains = {23462}
for strain in all_strains:
    sample = session.Sample.find(strain)
    all_items = sample.items
    for item in all_items:
        if item.object_type.name == "Yeast Glycerol Stock":
            
            #streak plate
            streak_plate_type = session.OperationType.where({"deployed": True, "name": "Streak Plate"})[0]
            streak_plate_op = streak_plate_type.instance() 
            streak_plate_op.set_output("Streak Plate", sample = sample)
            streak_plate_op.set_input("Yeast Strain", sample = sample, item = item)
            
            #check plate
            check_plate_type = session.OperationType.where({"deployed": True, "name": "Check Divided Yeast Plate"})[0]
            check_plate_op = check_plate_type.instance()
            check_plate_op.set_output("Plate", sample = sample)
            check_plate_op.set_output("Plate", sample = sample)
        
            #dilute to defined density
            dilute_type = session.OperationType.where({"deployed": True, "name": "Dilute to defined density (Divided Plate)"})[0]
            dilute_op = dilute_type.instance()
            dilute_op.set_output = ("Culture", sample)
            
            #TODO: add in parameter for desired event density
            dilute_op.set_input = ("Plate", sample)
            dilute_op.set_input = ("Density goal (events per ul)", 10)
            
            #add to plan
            p.add_operation(streak_plate_op)
            p.add_operation(check_plate_op)
            p.add_operation(dilute_op)
            
            #wire
            p.wire(check_plate_op.output("Plate"), dilute_op.input("Plate"))
            
            p.wire(streak_plate_op.output("Streak Plate"), check_plate_op.input("Plate"))
            
            
            p.create()
            p.estimate_cost()
        
            
            
            
    #add the operations to the plan for that sample
    #find the glycerol stock item and send it to streak plates

