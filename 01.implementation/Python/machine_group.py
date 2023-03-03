from machine import Machine

class MachineGroup(Machine):
    def __init__(self, id1):
        super().__init__(id1)
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
        
        self.saw_count = 0
        self.oven_count = 0
        self.vacuum_count = 0
        self.delivery_count = 0
        self.oven_ready = False


    # Extendend from the abc of the Ancestor Machine class
    # modify after the ancestor method
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
    # the vacuum gripper is at the turntable. Turntable is pointing at the vacuum.
    def start_position(self):
        self.vacuum_to_turntable()
        self.turntable_to_vacuum()
        self.move_feeder_out()
                
    # Rotates the turntable to the saw.
    # Does not rotate if the turtable is at the conveyor.
    def turntable_to_saw(self):
        if not self.__turntable_pos_saw and not self.__turntable_pos_conveyor:
            self.__act_rot_clockwise = True
        else:
            self.__act_rot_clockwise = False
        
    # Rotates the turntable to conveyor.
    def turntable_to_conveyor(self):
        if not self.__turntable_pos_conveyor:
            self.__act_rot_clockwise = True
        else:
            self.__act_rot_clockwise = False
      
    # Rotates the turntable to the vacuum.
    def turntable_to_vacuum(self):
        if not self.__turntable_pos_vacuum:
            self.__act_rot_counter_clockwise = True
        else:
            self.__act_rot_counter_clockwise = False
            
    # Uses the saw on the package. sawCount >= 20 is an artbitrary number.
    def use_saw(self):
        if self.__turntable_pos_saw and not self.saw_count >= 20:
            self.__act_saw  = True
            self.saw_count += 1
        else:
            self.__act_saw  = False
            
    # Moves the vacuum gripper to the oven.
    def vacuum_to_oven(self):
        #print('vacuumToOven')
        if not self.__vacuum_gripper_at_oven:
            self.__act_gripper_to_oven = True
        else:
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
        if not self.oven_ready  and self.__vacuum_gripper_at_oven:
            if not self.__oven_feeder_in:
                self.__compressor = True
                self.__valve_oven_door = True
                self.__act_oven_inward = True
            else:
                self.__act_oven_inward = False
                self.__compressor = False
                self.__valve_oven_door = False
                
                #haha, flashing lights go brrrr
                if self.oven_count % 2 == 1:
                    self.__oven_light = True
                else:
                    self.__oven_light = False
            
                self.oven_count += 1

            if self.oven_count >= 30:
                self.__oven_light = False
                self.oven_ready = True
                self.oven_count = 0

    # Brings the feeder outside to the vacuum gripper along with the readied 
    # product. Requires the product to have been in the oven before via
    #  startOven().
    def end_oven(self):
        #print('endOven')
        if self.oven_ready:
            self.move_feeder_out()
                
    # Moves the feeder inside the oven.
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

    # Moves the feeder outside of the oven.
    def move_feeder_out(self):
        #print('moveFeederOut')
        if not self.__oven_feeder_out:
            self.__compressor = True
            self.__valve_oven_door = True
            self.__act_oven_outward = True
        else:
            self.__act_oven_outward = False
            self.__compressor = False
            self.__valve_oven_door = False

    # Takes the product with the vacuum gripper. The vacuum gripper should be
    # at oven and the product must have been inside of it.
    # It is intended to use this operation with moveProductToTurntable()
    def grip_product(self):
        #print('gripProduct')
        if self.__oven_feeder_out and self.oven_ready and self.__vacuum_gripper_at_oven and self.vacuum_count < 10:
            self.__compressor = True
            self.__act_lower_valve = True
            self.vacuum_count += 1
  
    # The gripper brings the product to Turntable. The time required to grip 
    # it is stimulated with the self.vacuumCount count. +50
    def move_product_to_turntable(self):
        #print('moveProductToTurntable')
        if self.vacuum_count >= 10 and self.vacuum_count < 15:
            self.__valve = True
            self.vacuum_count += 1
        elif self.vacuum_count >= 15 and self.vacuum_count < 25:
            self.__act_lower_valve = False
            self.vacuum_count += 1
        elif self.vacuum_count >= 25 and self.vacuum_count < 30:
                self.__compressor = False
                self.vacuum_count += 1
        elif self.vacuum_count >= 30:
            self.vacuum_to_turntable()

    # Brings product from vacuum to saw, uses it and then brings it to the 
    # conveyor.
    # After it hits the sensor, brings the turntable back to the vacuum.
    # Requires the product to have been picked up by the vacuum before.
    # sawCount >= x comes from the useSaw() operation.
    # Note: this operation does not turn off the compressor.
    def deliver_product(self):
        #print('deliverProduct')
        if self.__processing_sens_delivery and self.vacuum_count >= 30 and self.__vacuum_gripper_at_turntable:
            if self.delivery_count < 15:
                self.__compressor = True
                self.__act_lower_valve = True
                self.delivery_count += 1
            elif self.delivery_count < 25 and self.delivery_count >= 15:
                self.__valve = False
                self.delivery_count += 1
            elif self.delivery_count < 35 and self.delivery_count >= 25:
                self.__compressor = False
                self.__act_lower_valve = False
                self.delivery_count += 1
            else:
                if self.saw_count == 0:
                    self.turntable_to_saw()
                self.use_saw()
                if self.saw_count >= 20:
                    self.turntable_to_conveyor()
                if self.__turntable_pos_conveyor:
                    self.__compressor = True
                    self.__valve_feeder = True
                    self.__act_conveyor_Forward = True

    # Sets all valuables and the ovenReady flag to the
    # starting values.
    def reset_station(self):
        #print('resetStation')
        self.saw_count = 0
        self.oven_count = 0
        self.vacuum_count = 0
        self.delivery_count = 0
        self.oven_ready = False
        
    # Brings the vacuum over to to the oven. The product goes
    # inside and outside. Then it is brought to the turntable.
    # It is operated upon by the saw and finally is brought to the conveyor.
    # The machine resets once the product reaches the sensor.
    def process_product(self):
        print('processProduct')
        if self.__processing_sens_delivery:
            if not self.oven_ready:
                self.vacuum_to_oven()
            self.start_oven()
            self.end_oven()
            self.grip_product()
            self.move_product_to_turntable()
            self.deliver_product()
        else:
                self.__compressor = False
                self.__valve_feeder = False
                self.__act_conveyor_Forward = False
                self.turntable_to_vacuum()
                if self.__turntable_pos_vacuum:
                    self.reset_station()
