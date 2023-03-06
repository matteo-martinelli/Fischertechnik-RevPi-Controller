"""
My change.
Processes time are represented by xyz_counter elements.
These counters are taken into consideration, and when they reach a certain 
value, the associated resources is released.  

Note: each unit in the counter corresponds to a rpi.mainloop cycle. 
Each rpi.mainloop cycle lasts for 50ms, standard (to be verified).
"""

from machine import Machine
import time


#class MachineGroup(Machine):
class MachineGroup(object):
    #def __init__(self, id1):   # TODO: TO BE DELETED
    def __init__(self):
        #super().__init__(id1)  # TODO: TO BE DELETED
        self.__turntable_pos_vacuum = False
        self.__turntable_pos_conveyor  = False
        self.__processing_sens_delivery = False
        self.__turntable_pos_saw = False
        self.__vacuum_gripper_at_turntable  = False
        self.__oven_feeder_in = False
        self.__oven_feeder_out  = False
        self.__vacuum_gripper_at_oven = False
        self.__sens_oven = False
        
        self.__act_rot_clockwise = False
        self.__act_rot_counter_clockwise = False
        self.__act_conveyor_Forward = False
        self.__act_saw = False
        self.__act_oven_inward = False        
        self.__act_oven_outward = False
        self.__act_gripper_to_oven = False
        self.__act_gripper_to_turntable = False
        self.__oven_light = False
        self.__compressor = False
        self.__valve = False
        self.__act_lower_valve = False
        self.__valve_oven_door = False
        self.__valve_feeder = False
        
        self.saw_count = 0          # Saw process time counter
        self.oven_count = 0         # Oven process time counter
        self.vacuum_count = 0       # Vacuum process time counter
        self.delivery_count = 0     # Delivery process time counter
        self.oven_ready = False     # Oven ready variable

        # My fields
        #self.initial_time = 0
        #self.final_time = 0


    # Extendend from the abc of the Ancestor Machine class
    # modify after the ancestor method
    # TODO: TO BE DELETED
    """
    @property
    def isExecuting(self):
        # Returns whether the machine is currently performing actions
        # Extension of the Machine abstract method.        
        if (self.__act_rot_clockwise or 
            self.__act_rot_counter_clockwise or 
            self.__act_conveyor_Forward):
            return True
        else:
            return False
    """

    # Getters, setters
    @property
    def turntable_pos_vacuum(self) -> bool:
        return self.__turntable_pos_vacuum

    @turntable_pos_vacuum.setter
    def turntable_pos_vacuum(self, value: bool):
        self.__turntable_pos_vacuum = value
        
    @property
    def turntable_pos_saw(self) -> bool:
        return self.__turntable_pos_saw

    @turntable_pos_saw.setter
    def turntable_pos_saw(self, value: bool):
        self.__turntable_pos_saw = value

    @property
    def turntable_pos_conveyor(self) -> bool:
        return self.__turntable_pos_conveyor

    @turntable_pos_conveyor.setter
    def turntable_pos_conveyor(self, value: bool):
        self.__turntable_pos_conveyor = value
        
    @property
    def sens_delivery(self) -> bool:
        return self.__processing_sens_delivery

    @sens_delivery.setter
    def sens_delivery(self, value: bool):
        self.__processing_sens_delivery = value

    @property
    def sens_oven(self) -> bool:
        return self.__sens_oven

    @sens_oven.setter
    def sens_oven(self, value: bool):
        self.__sens_oven = value
        
    @property
    def vacuum_gripper_at_oven(self) -> bool:
        return self.__vacuum_gripper_at_oven

    @vacuum_gripper_at_oven.setter
    def vacuum_gripper_at_oven(self, value: bool):
        self.__vacuum_gripper_at_oven = value

    @property
    def vacuum_gripper_at_turntable(self) -> bool:
        return self.__vacuum_gripper_at_turntable

    @vacuum_gripper_at_turntable.setter
    def vacuum_gripper_at_turntable(self, value: bool):
        self.__vacuum_gripper_at_turntable = value
        
    @property
    def oven_feeder_out(self) -> bool:
        return self.__oven_feeder_out

    @oven_feeder_out.setter
    def oven_feeder_out(self, value: bool):
        self.__oven_feeder_out = value

    @property
    def oven_feeder_in(self) -> bool:
        return self.__oven_feeder_in

    @oven_feeder_in.setter
    def oven_feeder_in(self, value: bool):
        self.__oven_feeder_in = value
        
    @property
    def act_rot_clockwise(self) -> bool:
        return self.__act_rot_clockwise

    @act_rot_clockwise.setter
    def act_rot_clockwise(self, value: bool):
        self.__act_rot_clockwise = value
        
    @property
    def act_rot_counterclockwise(self) -> bool:
        return self.__act_rot_counter_clockwise

    @act_rot_counterclockwise.setter
    def act_rot_counterclockwise(self, value: bool):
        self.__act_rot_counter_clockwise = value

    @property
    def act_conveyor_forward(self) -> bool:
        return self.__act_conveyor_Forward

    @act_conveyor_forward.setter
    def act_conveyor_forward(self, value: bool):
        self.__act_conveyor_Forward = value    
    
    @property
    def act_saw(self) -> bool:
        return self.__act_saw

    @act_saw.setter
    def act_saw(self, value: bool):
        self.__act_saw = value

    @property
    def act_oven_inward(self) -> bool:
        return self.__act_oven_inward

    @act_oven_inward.setter
    def act_oven_inward(self, value: bool):
        self.__act_oven_inward = value
        
    @property
    def act_oven_outward(self) -> bool:
        return self.__act_oven_outward

    @act_oven_outward.setter
    def act_oven_outward(self, value: bool):
        self.__act_oven_outward = value

    @property
    def act_gripper_to_oven(self) -> bool:
        return self.__act_gripper_to_oven

    @act_gripper_to_oven.setter
    def act_gripper_to_oven(self, value: bool):
        self.__act_gripper_to_oven = value
        
    @property
    def act_gripper_to_turntable(self) -> bool:
        return self.__act_gripper_to_turntable

    @act_gripper_to_turntable.setter
    def act_gripper_to_turntable(self, value: bool):
        self.__act_gripper_to_turntable = value

    @property
    def oven_light(self) -> bool:
        return self.__oven_light

    @oven_light.setter
    def oven_light(self, value: bool):
        self.__oven_light = value
        
    @property
    def compressor(self) -> bool:
        return self.__compressor

    @compressor.setter
    def compressor(self, value: bool):
        self.__compressor = value
        
    @property
    def valve(self) -> bool:
        return self.__valve

    @valve.setter
    def valve(self, value: bool):
        self.__valve = value

    @property
    def act_lower_valve(self) -> bool:
        return self.__act_lower_valve

    @act_lower_valve.setter
    def act_lower_valve(self, value: bool):
        self.__act_lower_valve = value
        
    @property
    def valve_oven_door(self) -> bool:
        return self.__valve_oven_door

    @valve_oven_door.setter
    def valve_oven_door(self, value: bool):
        self.__valve_oven_door = value
        
    @property
    def valve_feeder(self) -> bool:
        return self.__valve_feeder

    @valve_feeder.setter
    def valve_feeder(self, value: bool):
        self.__valve_feeder = value

    # Starting position is as follows:
    # The feeder is out, the oven door is closed,
    # the vacuum gripper is at the turntable. Turntable is pointing at the 
    # vacuum.
    # TODO: TO BE DELETED
    """
    def start_position(self):
        self.vacuum_to_turntable()
        self.turntable_to_vacuum()
        self.move_feeder_out()
    """
                
    # Rotates the turntable to the saw.
    # Does not rotate if the turtable is at the conveyor.
    def turntable_to_saw(self):
        # If the turntable_pos_say sensor is False and the 
        # turntable_pos_conveyor is False that is
        # if the turn-table is not aligned under the saw and is not at the 
        # conveyor
        if not self.__turntable_pos_saw and not self.__turntable_pos_conveyor:
            # Activate the turn-table rotation clockwise
            self.__act_rot_clockwise = True 
        else:
            # Deactivate the turn-table rotation clockwise
            self.__act_rot_clockwise = False    
        
    # Rotates the turntable to conveyor.
    def turntable_to_conveyor(self):
        # If the turntable_pos_conveyor sensor is False
        if not self.__turntable_pos_conveyor:
            # Activate the turntable rotation clockwise
            self.__act_rot_clockwise = True
        else:
            # Deactivate the turntable rotation clockwise
            self.__act_rot_clockwise = False
      
    # Rotates the turntable to the vacuum.
    def turntable_to_vacuum(self):
        # If the turntable_pos_vacuum sensor is False, that is 
        # if the turntable is not at the vacuum gripper carrier
        if not self.__turntable_pos_vacuum:
            # Activate the conveyor rotation clockwise
            self.__act_rot_counter_clockwise = True
        # Otherwise, if the turntable_pos_vacuum sensor is True, that is 
        # if the turntable is at the vacuum gripper carrier
        else:
            # Deactivate the conveyor rotation clockwise
            self.__act_rot_counter_clockwise = False
            
    # Uses the saw on the package. sawCount >= 20 is an artbitrary number.
    def use_saw(self):
        # If the turntable_pos_saw sensor is True and saw counter is not 
        # greater than 20 that is
        # if turntable_pos_saw is under the saw and saw counter is not greater 
        # than 20
        if self.__turntable_pos_saw and not self.saw_count >= 20:
            self.__act_saw  = True  # Activate the saw
            self.saw_count += 1     # Add 1 to the saw counter
        else:
            self.__act_saw  = False # Deactivate the saw
            
    # Moves the vacuum carrier gripper to the oven.
    def vacuum_to_oven(self):
        #print('vacuumToOven')
        # If the carrier is not in front of the oven
        if not self.__vacuum_gripper_at_oven:
            # Activate it towards the oven
            self.__act_gripper_to_oven = True
        else:
            # Dectivate it towards the oven
            self.__act_gripper_to_oven = False
            
    # Moves the vacuum gripper to the turntable.
    def vacuum_to_turntable(self):
        #print('vacuumToTurntable')
        if not self.__vacuum_gripper_at_turntable:
            self.__act_gripper_to_turntable = True
        else:
            self.__act_gripper_to_turntable = False
            
    # Brings the feeder inside the oven and initiates the cooking process. 
    # self.ovenCount >= 30 is an arbitrary number.
    def start_oven(self):
        #print('startOven')
        # If the oven is not ready and the vacuum carrier grip sensor is True, 
        # that is the carrier grip sensor is at the oven: 
        if not self.oven_ready and self.__vacuum_gripper_at_oven:
            # If the oven feeder inside sensor si False, that is the oven 
            # carrier  is outside the oven
            if not self.__oven_feeder_in:
                self.__compressor = True        # Acivate the compressor
                self.__valve_oven_door = True   # Open the door
                self.__act_oven_inward = True   # Move the feeder in the oven
            # If the oven feeder is inside the oven
            else:
                self.__act_oven_inward = False  # Deactivate the inward oven
                self.__compressor = False       # Deactivate the compressor
                self.__valve_oven_door = False  # Close the door
                
                #haha, flashing lights go brrrr
                if self.oven_count % 2 == 1:    # For making the light flash
                    self.__oven_light = True    # Activate the process light
                else:
                    self.__oven_light = False   # Deactivate the process light
            
                self.oven_count += 1            # Time counter

            # If the counter reaches 30, stop the process
            if self.oven_count >= 30:       
                self.__oven_light = False       # Deactivate the light
                self.oven_ready = True          # Set the oven to ready
                self.oven_count = 0             # Set the oven counter to 0

    # Brings the feeder outside to the vacuum gripper along with the readied 
    # product. Requires the product to have been in the oven before via
    # startOven().
    def end_oven(self):
        #print('endOven')
        # It the oven is in ready state
        if self.oven_ready:
            self.move_feeder_out()  # Move out the feeder
                
    # Moves the feeder inside the oven.
    # TODO: CAN BE DELETED
    """
    def move_feeder_in(self):
        #print('moveFeederIn')
        if not self.__oven_feeder_in:
            self.__compressor = True
            self.__valve_oven_door = True
            self.__act_oven_inward = True
        else:
            self.__act_oven_inward = False
            self.__oven_light = True
            self.__compressor = False
            self.__valve_oven_door = False
    """

    # Moves the feeder outside of the oven.
    def move_feeder_out(self):
        #print('moveFeederOut')
        # If oven_feeder_out sensor is False = the carrier is not out
        if not self.__oven_feeder_out:
            self.__compressor = True        # Activate the compressor
            self.__valve_oven_door = True   # Open the door
            self.__act_oven_outward = True  # Move the oven outside
        else:
            self.__act_oven_outward = False # Stop moving the oven carrier
            self.__compressor = False       # Deactivate the compressor
            self.__valve_oven_door = False  # Close the door

    # Takes the product with the vacuum gripper. The vacuum gripper should be
    # at oven and the product must have been inside of it.
    # It is intended to use this operation with moveProductToTurntable()
    def grip_product(self):
        #print('gripProduct')
        # If oven feeder sensor is True and oven ready is True and the vacuum 
        # gripper variable is True and vacuum counter is less than 10, 
        # that is 
        # if the oven feeder is out from the oven and the oven is in ready 
        # state and the vacuum carrieer gripper is at the oven and the vacuum 
        # counter is less than 10 
        if (self.__oven_feeder_out and self.oven_ready and 
        self.__vacuum_gripper_at_oven and self.vacuum_count < 10):
            print('vacuum count ' + str(self.vacuum_count))
            self.__compressor = True        # Activate the compressor
            self.__act_lower_valve = True   # Lower the carrier vacuum gripper
            self.vacuum_count += 1          # Add 1 to the vacuum counter
  
    # The gripper brings the product to Turntable. The time required to grip 
    # it is simulated with the self.vacuumCount count.
    # TODO: TO BE CHANGED
    def move_product_to_turntable(self):
        #print('moveProductToTurntable')
        # If vacuum count is greater than 10 and less than 15
        if self.vacuum_count >= 10 and self.vacuum_count < 15:
            self.__valve = True     # Activate the carrier vacuum gripper 
            self.vacuum_count += 1  # Add 1 to the vacuum count
        # If vacuum count is greater than 15 and less than 25
        elif self.vacuum_count >= 15 and self.vacuum_count < 25:
            self.__act_lower_valve = False  # Upper the carrier vacuum gripper
            self.vacuum_count += 1          # Add 1 to the vacuum counter
        # If vacuum count is greater than 25 and less than 30
        elif self.vacuum_count >= 25 and self.vacuum_count < 30:
                self.__compressor = False   # Deactivate the compressor
                self.vacuum_count += 1      # Add 1 to the vacuum count
        # If vacuum count is greater than 30
        elif self.vacuum_count >= 30:
            # Bring the carrier vacuum gripper to the turn-table
            self.vacuum_to_turntable()   

    # Brings product from vacuum to saw, uses it and then brings it to the 
    # conveyor.
    # After it hits the sensor, brings the turntable back to the vacuum.
    # Requires the product to have been picked up by the vacuum before.
    # sawCount >= x comes from the useSaw() operation.
    # Note: this operation does not turn off the compressor.
    def deliver_product(self):
        #print('deliverProduct')
        # If the conveyor light sensor is True and the vacuum count is greter 
        # than 30 and the carrier vacuum gripper at turntable is True, that is
        # if the processing sensor delivery have no product and the vacuum 
        # counter is greater that 30 and the vacuum gripper carrier is at the 
        # turntable
        if (self.__processing_sens_delivery and self.vacuum_count >= 30 and 
            self.__vacuum_gripper_at_turntable):
            # if the delivery count is smaller than 15
            if self.delivery_count < 15:
                self.__compressor = True        # Activate the compressor
                self.__act_lower_valve = True   # Lower the carrier vacuum grip
                self.delivery_count += 1        # Add 1 to the delivery count
            # if the delivery count is greater than 15 and smaller that 25
            elif self.delivery_count < 25 and self.delivery_count >= 15:
                self.__valve = False            # Deactivate the gripper valve
                self.delivery_count += 1        # Add 1 to the delivery count
            # if the delivery count is greater than 25 and smaller that 35
            elif self.delivery_count < 35 and self.delivery_count >= 25:
                self.__compressor = False       # Deactivate the compressor
                self.__act_lower_valve = False  # Upper the carrier vacuum valve
                self.delivery_count += 1        # Add 1 to the delivery count
            else:
                # If the saw count is 0
                if self.saw_count == 0:
                    # Rotate the turn-table towards the saw
                    self.turntable_to_saw()
                # Activate the saw
                self.use_saw()
                # If the saw conter is greater than 20
                if self.saw_count >= 20:
                    # Rotate the turn-table toward the conveyor
                    self.turntable_to_conveyor()
                # If the turntable_pos_conveyor is True
                if self.__turntable_pos_conveyor:
                    self.__compressor = True    # Activate the conveyor
                    self.__valve_feeder = True  # Activate the turntable pusher
                    # Activate the conveyor
                    self.__act_conveyor_Forward = True

    # Sets all valuables and the ovenReady flag to the
    # starting values.
    def reset_station(self):
        #print('resetStation')
        self.saw_count = 0          # Resets all counters
        self.oven_count = 0
        self.vacuum_count = 0
        self.delivery_count = 0
        self.oven_ready = False     # Sets the oven as "not ready"
        
    # Brings the vacuum over to to the oven. The product goes
    # inside and outside. Then it is brought to the turntable.
    # It is operated upon by the saw and finally is brought to the conveyor.
    # The machine resets once the product reaches the sensor.
    def process_product(self):
        #print('processProduct')
        # If the conveyor-light sensor is True = there is no product
        if self.__processing_sens_delivery:
            # If oven_ready == False
            if not self.oven_ready:
                # Move the carrier towards the oven
                self.vacuum_to_oven()
            # Start the oven
            self.start_oven()
            # End the oven
            self.end_oven()
            # Take the product with the carrier grip
            self.grip_product()
            # Move the carrier with the product towards the turntable
            self.move_product_to_turntable()
            # Deliver the product (where?)
            self.deliver_product()
        # Otherwise, if there is the product in front of the light sensor
        else:
                # Turn off the compressor
                self.__compressor = False
                # Turn off the valve feeder
                self.__valve_feeder = False
                # Turn off the conveyor belt
                self.__act_conveyor_Forward = False
                # Turn the turn-table towards the carrier
                self.turntable_to_vacuum()
                # If the turntable faces the carrier
                if self.__turntable_pos_vacuum:
                    self.reset_station()    # Resent all the station
