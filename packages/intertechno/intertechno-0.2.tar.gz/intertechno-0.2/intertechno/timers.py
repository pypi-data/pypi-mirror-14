import datetime

radix64 = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H',
           'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
           'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X',
           'Y', 'Z', 'a', 'b', 'c', 'd', 'e', 'f',
           'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n',
           'o', 'p', 'q', 'r', 's', 't', 'u', 'v',
           'w', 'x', 'y', 'z', '0', '1', '2', '3',
           '4', '5', '6', '7', '8', '9', '*', '#']

valid_weekdays = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']
        
class Timers:
    def __init__(self, password):
        self.password = password
        self.timers = []
    
    def add(self, code, time_on=None, time_off=None,
            dim=None, repeat=True, random=False, days=True):
        
        assert len(self.timers) < 15, "Maximum 15 timer values are supported."
        
        # validate hour and minute values
        assert time_on is None or (time_on[0] >= 0 and time_on[0] <= 23 and time_on[1] >= 0 and time_on[1] <= 59)
        assert time_off is None or (time_off[0] >= 0 and time_off[0] <= 23 and time_off[1] >= 0 and time_off[1] <= 59)
        
        # validate wheel code / password code+dimming
        if isinstance(code, str):
            assert code[0] >= 'A' and code[0] <= 'P'
            assert int(code[1:]) >= 0 and int(code[1:]) <= 15
            assert dim is None
        else:
            assert code >= 0 and code <= 16
            assert dim is None or (dim >= 0 and dim <= 1)
        
        # validate other parameters 
        assert isinstance(repeat, bool)
        assert isinstance(random, bool)
        assert isinstance(days, bool) or all(day in valid_weekdays for day in days)
        
        # create address
        if isinstance(code, str):
            address = code[0] + "{:02d}".format(int(code[1:]))
        else:
            address = "{:02d}".format(int(code))
            if dim is None:
                address += '*'
            else:
                address += radix64[int(dim*15)]
        
        # create time strings
        on_hour_str = radix64[time_on[0]] if time_on is not None else '*'
        on_minute_str = radix64[time_on[1]] if time_on is not None else '*'
        off_hour_str = radix64[time_off[0]] if time_off is not None else '*'
        off_minute_str = radix64[time_off[1]] if time_off is not None else '*'
        
        # create weekday, random, repeat blob
        if isinstance(days, bool):
            if days is True:
                days = valid_weekdays
            else:
                days = []
        
        blob = 0
        if 'sun' in days:
            blob |= 1
        if 'sat' in days:
            blob |= 1 << 1
        if 'fri' in days:
            blob |= 1 << 2
        if 'thu' in days:
            blob |= 1 << 3
        if 'wed' in days:
            blob |= 1 << 4
        if 'tue' in days:
            blob |= 1 << 5
        if 'mon' in days:
            blob |= 1 << 6
        if repeat is True:
            blob |= 1 << 7
        if random is True:
            blob |= 1 << 8
        
        blob_0 = radix64[int(blob/64)]
        blob_1 = radix64[blob%64]
        
        # build timer message
        msg = "".join([
            address,
            on_hour_str,
            on_minute_str,
            off_hour_str,
            off_minute_str,
            blob_0,
            blob_1])
        
        self.timers.append(msg)
        
    def compose(self):
        # build timers field
        empty = ["*********"] * (15 - len(self.timers))
        payload = "+".join(self.timers + empty)
        
        # build clock field
        dnow = datetime.datetime.now()
        clock = radix64[dnow.weekday()] + radix64[dnow.hour] + radix64[dnow.minute]
        
        # build final message
        return "?{}+{}+".format(self.password, clock) + payload + "\n"

