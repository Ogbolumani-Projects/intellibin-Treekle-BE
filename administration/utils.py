def update_bin(compartments, data):
   
    compartments.weight = data.get("weight", compartments.weight)
    compartments.temperature = data.get("temperature", compartments.temperature)
    compartments.bin_level = data.get("bin_level", compartments.bin_level)
    compartments.type_of_waste = data.get("type_of_waste", compartments.type_of_waste)

    compartments.save()