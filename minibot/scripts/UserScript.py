def run(bot):
    sensor = bot.get_sensor_by_name("ColorSensor")
    
    for i in range(0, 10):
    	print(sensor.get_color_name(), sensor.read())
