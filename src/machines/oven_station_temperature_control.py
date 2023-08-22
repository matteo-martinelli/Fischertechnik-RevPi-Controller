import random

# currently function is a linear function with linear clutuations
# TODO: for future demonstration use a sin/cos function to smoothen the fluctuation curve
# TODO: implement a function for a heatup curve, by default it is exponential form 1 degree per minute to 12 per minute
# TODO: insulation not yet used, could be considered if oven model is not the "ideal" oven
def update_temperature(outside_temperature, current_inside_temperature, 
                       wanted_temperature, flucutation, 
                       min_oven_set_temperature, max_oven_set_temperature, 
                       time_passed, insulation) -> "tuple[float, str|None]" :
    inside_temp = current_inside_temperature
    state_oven = None
    for i in range(time_passed):
        state = calc_state(current_inside_temperature=inside_temp, 
                           wanted_temperature=wanted_temperature, 
                           room_temperature=outside_temperature, 
                           fluctuation=flucutation, 
                           minimum_set_temperature=min_oven_set_temperature, 
                           maximum_set_temperature=max_oven_set_temperature)
        if state == "heating":
            # insert exp heating function here
            inside_temp = inside_temp + 12
            state_oven = "heating"
        if state == "cooling":
            # insert cooling function here
            inside_temp = inside_temp - 3.5
            state_oven = "cooling"
        if state == "warming":
            # insert fluctuation function sin/cos here
            flucutation_range = random.random()
            pos_neg_random = random.randint(0, 2)
            # negative fluctuation
            if (pos_neg_random == 0): 
                inside_temp = inside_temp - flucutation*flucutation_range
            # positive fluctuation
            elif(pos_neg_random == 1):
                inside_temp = inside_temp + flucutation*flucutation_range
            else: 
                print('illegal randomly extract value')
            state_oven = "warming"
    return inside_temp, state_oven

# handle all states of the oven
def calc_state(current_inside_temperature, wanted_temperature, 
               room_temperature, fluctuation, minimum_set_temperature, 
               maximum_set_temperature):
    if current_inside_temperature < wanted_temperature :
        return "heating"
    elif current_inside_temperature > room_temperature and wanted_temperature <= room_temperature:
        return "cooling"
    elif wanted_temperature <= room_temperature: 
        return "idle"
    elif current_inside_temperature > wanted_temperature - fluctuation and current_inside_temperature < wanted_temperature + fluctuation: 
        return "warming"
    elif wanted_temperature > maximum_set_temperature: 
        return "illegal"
    elif current_inside_temperature > maximum_set_temperature: 
        return "cooling"
    elif wanted_temperature < minimum_set_temperature: 
        return "illegal"