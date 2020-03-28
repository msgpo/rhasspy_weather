import logging

log = logging.getLogger(__name__)

# Class used by WeatherReport and WeatherForecast
# filled by WeatherForecast and used by WeatherReport
# to generate the answer to the request
class WeatherInterval:
    def __init__(self, switch=False):
        self.min_temperature = 99
        self.max_temperature = 0
        self.weather_condition_list = []
        self.pressure = 0
        self.humidity = 0
        self.wind_speed = 0
        self.wind_direction = 0
        self.__rain = 0
        self.__thunderstorm = 0
        self.__mist = 0
        self.__snow = 0
        self.__clouds = 0
        self.__clear = 0
        self.__change_count = 0
        self.switch = switch

    # puts information into itself
    def add_information(self, weather_at_time):
        self.__change_count = self.__change_count + 1
        if weather_at_time.temperature > self.max_temperature:
            self.max_temperature = weather_at_time.temperature
        if weather_at_time.temperature < self.min_temperature:
            self.min_temperature = weather_at_time.temperature
        if weather_at_time.weather_condition_obj not in self.weather_condition_list:
            self.weather_condition_list.append(weather_at_time.weather_condition_obj)
        self.increase_counter(weather_at_time.weather_condition)

    # counts how many occurrences of a certain weather type there are
    def increase_counter(self, counter):
        if counter == "Rain" or counter == "Drizzle": 
            self.__rain = self.__rain + 1
        elif counter == "Thunderstorm":
            self.__thunderstorm = self.__thunderstorm + 1
        elif counter == "Snow":
            self.__snow = self.__snow + 1
        elif counter == "Clouds":
            self.__clouds = self.__clouds + 1
        elif counter == "Clear":
            self.__clear = self.__clear + 1
        elif counter == "Mist":
            self.__mist = self.__mist + 1

    @property
    def is_rain_chance(self):
        return self.__rain > 0

    @property
    def is_thunderstorm_chance(self):
        return self.__thunderstorm > 0

    @property
    def is_snow_chance(self):
        return self.__snow > 0

    @property
    def is_cloudy(self):
        return self.__clouds > 0

    @property
    def is_misty(self):
        return self.__mist > 0

    @property 
    def is_clear(self):
        return self.__clear > 0

    @property
    def contains_information(self):
        return self.__change_count > 0

    # puts together the output string from the
    #conditions saved in weather_condition_list
    @property
    def weather_description(self):
        selected = []
        for x in self.weather_condition_list:
            if selected == []:
                selected.append(x)
            else:
                for y in selected:
                    if x.condition == y.condition:
                        if x.severity > y.severity:
                            selected.remove(y)
                            selected.append(x)
                    else:
                        if self.switch:
                            # clear sky and clouds in the same period of time
                            # seems fishy so lets remove the clear sky if we
                            # know about clouds
                            if y.condition == "Clear" and x.condition == "Clouds":
                                selected.remove(y)
                            # still fishy so if we already have clouds lets not
                            # add a clear sky
                            if not (x.condition == "Clear" and y.condition == "Clouds"):
                                selected.append(x)
                        else:
                            selected.append(x)
        description = ""
        for x in selected:
            if description == "":
                description = x.description
            else:
                from rhasspy_weather.globals import config
                description = description + " " + config.locale.combine_word + " " + x.description
        return description