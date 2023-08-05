import gpxpy
import gpxpy.gpx
from math import radians, cos, sin, asin, sqrt
import calendar


def haversine(lon1, lat1, lon2, lat2):
    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    km = 6367 * c
    return km * 1000


def unix_time(raw):
    return calendar.timegm(raw.timetuple())


class Activity:
    def __init__(self,
                 start_time,
                 end_time,
                 latitude_offset,
                 longitude_offset,
                 calories,
                 max_speed,
                 avg_speed,
                 min_speed,
                 max_height,
                 min_height,
                 distance,
                 track,
                 step_count=0,
                 duration=None,
                 sport_type=0):
        """
        Construct a track.
        :param start_time: in UNIX format
        :param end_time: in UNIX format
        :param latitude_offset: call user.get_map_offset
        :param longitude_offset: call user.get_map_offset
        :param calories: an integer
        :param max_speed: in metre per hour
        :param avg_speed: in metre per hour
        :param min_speed: in metre per hour
        :param max_height: in metre
        :param min_height: in metre
        :param distance: in metre
        :param track: a list of dictionaries, key list: ['latitude', 'longitude', 'elevation', 'time_elapsed',
        'speed', 'distance_covered']
        :param step_count: an integer. Default to zero.
        :param duration: in second. Default is None and will be automatically calculated based on start and end time.
        :param sport_type: an integer. Default to zero (run).
        :return:
        """
        self.start_time = start_time
        self.end_time = end_time
        self.latitude_offset = latitude_offset
        self.longitude_offset = longitude_offset
        self.calories = calories
        self.max_speed = max_speed
        self.avg_speed = avg_speed
        self.min_speed = min_speed
        self.max_height = max_height
        self.min_height = min_height
        self.distance = distance
        self.track = track
        self.step_count = step_count
        if duration:
            self.duration = duration
        else:
            self.duration = self.end_time - self.start_time
        self.sport_type = sport_type

    def to_dict(self):
        """
        Convert activity object into Python dictionary.
        :return: Python dictionary ready to be dumped into json.
        """
        result = {'longitudeOffset': self.longitude_offset,
                  'sportType': self.sport_type,
                  'maxSpeed': self.max_speed,
                  'calories': self.calories,
                  'aSpeed': self.avg_speed,
                  'maxHeight': self.max_height,
                  'stepcount': self.step_count,
                  'minSpeed': self.min_speed,
                  'sportTime': self.duration,
                  'endTime': self.end_time,
                  'distance': self.distance,
                  'startTime': self.start_time,
                  'latitudeOffset': self.latitude_offset,
                  'minHeight': self.min_height,
                  'location': []}
        # Track in the payload is a list of formatted strings
        # "39.992020,116.301042,40.330000,182,0.000000,253.629896"
        # latitude, longitude, elevation, time_elapsed, speed, distance_covered
        for point in self.track:
            point_string = "{},{},{},{},{},{}".format(point['latitude'],
                                                      point['longitude'],
                                                      point['elevation'],
                                                      point['time_elapsed'],
                                                      point['speed'],
                                                      point['distance_covered'])
            result['location'].append(point_string)
        return result

    @classmethod
    def from_gpx(cls, file_path, activity_start_time, calories, latitude_offset, longitude_offset):
        """
        Construct an activity from .gpx file. The .gpx file must contain location, elevation and time.
        :param file_path: path to .gpx file.
        :param activity_start_time: start time to be submitted, Python datetime object. You should use UTC time.
        :param calories: integer.
        :param latitude_offset: float number. You may get this by calling User.get_map_offset().
        :param longitude_offset: same as latitude_offset.
        :return: an activity object.
        """
        input_file = open(file_path)
        gpx = gpxpy.parse(input_file)
        input_file.close()
        point_list = gpx.tracks[0].segments[0].points

        start_time = unix_time(point_list[0].time)
        end_time = unix_time(point_list[-1].time)

        last_latitude = point_list[0].latitude
        last_longitude = point_list[0].longitude
        last_duration = 0
        distance = 0
        track = []

        max_speed = 0.0
        min_speed = 1000000.0
        max_height = 0.0
        min_height = 1000000.0

        time_offset = unix_time(activity_start_time) - start_time

        for point in point_list:
            leg_length = haversine(last_longitude, last_latitude, point.longitude, point.latitude)
            last_latitude = point.latitude
            last_longitude = point.longitude
            distance += leg_length

            duration = unix_time(point.time) - start_time
            if duration != last_duration:
                speed = leg_length / (duration - last_duration) * 3600
            else:
                speed = 0.0
            last_duration = duration

            if min_speed > speed:
                min_speed = speed
            if max_speed < speed:
                max_speed = speed
            if min_height > point.elevation:
                min_height = point.elevation
            if max_height < point.elevation:
                max_height = point.elevation

            track.append({'latitude': point.latitude,
                          'longitude': point.longitude,
                          'elevation': point.elevation,
                          'time_elapsed': duration,
                          'speed': speed,
                          'distance_covered': distance})

        duration = end_time - start_time
        avg_speed = distance / duration * 3600

        result = cls(start_time=start_time + time_offset,
                     end_time=end_time + time_offset,
                     latitude_offset=latitude_offset,
                     longitude_offset=longitude_offset,
                     calories=calories,
                     max_speed=max_speed,
                     avg_speed=avg_speed,
                     min_speed=min_speed,
                     max_height=max_height,
                     min_height=min_height,
                     distance=distance,
                     track=track)
        return result
