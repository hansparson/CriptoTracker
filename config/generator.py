
import datetime
import random
import time
import uuid


class GeneratorTools(object):
    def generate_api_call_id():
        """
        Generate unique api call id
        """
        now_time = int(time.time())
        current_date = datetime.datetime.now()

        hour_tm = current_date.hour
        minute_tm = current_date.minute
        second_tm = current_date.second

        start_id = str(now_time) + str(hour_tm) + str(minute_tm) + str(second_tm)
        random_num = random.randint(1, 10000000)
        api_call = 'API_CALL_{}_{}'.format(str(start_id), str(random_num))
        return api_call
    
    def generate_user_id():
        user_id = str(uuid.uuid4())
        return user_id