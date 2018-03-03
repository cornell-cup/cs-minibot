def run(bot):
    import time
    
    sensor = bot.get_sensor_by_name("ColorSensor")
    for i in range(0,20):
    	color = sensor.get_color_name()
    	print(color)
    	time.sleep(1)
