import re
from math import ceil
from decimal import Decimal
import unittest

string_example="all I did today; i 20m, 35m, 2.5h, 2h40m v 40m 35m 1.2h e 30, 60m  "

class MinutesTest(unittest.TestCase):
    def test_calculate_total_minutes_in(self):
        self.assertEqual(calculate_total_minutes_in(), 602)
        # check seprators (a comma, a space, a comma followed by spaces) to be handled properly:
        self.assertEqual(calculate_total_minutes_in("all I did today; ,,,, i 20m ,  ,  35m,2.5h,2h  ,     40m v 40m,35m,    1.2h e    30,, 60m , "), 602)
        # input string that does not contain ';' character:
        self.assertEqual(calculate_total_minutes_in("all I did today"), 0)
        # input string is empty:
        self.assertEqual(calculate_total_minutes_in(""), 0)
        # input string contains a lot of not meaningful charscters:
        self.assertEqual(calculate_total_minutes_in("all I did today;r i y 20m, g 35m, 2.5h, 2hu40m v 40m 35m r1.2h e 30, 60m i pp"), 602)
        # input string contains floats:
        self.assertEqual(calculate_total_minutes_in("all I did today; 2.5854589999999999h"), 156)
        self.assertEqual(calculate_total_minutes_in("all I did today; 1.00000000000000000000001"), 2)
        self.assertEqual(calculate_total_minutes_in("all I did today; 2.55465456456456h 60.6546456456564m  "), 214)
        self.assertEqual(calculate_total_minutes_in("all I did today; 2.55465456456456h60.6546456456564m 0.0000000001 "), 214)
        # input string does not contain any time enties, just not meaningful charscters including "h" and "m":
        self.assertEqual(calculate_total_minutes_in("all I did today; f d t h g e t y m  l"), 0)
        # just some random test cases:
        self.assertEqual(calculate_total_minutes_in("all I did today"), 0)
        self.assertEqual(calculate_total_minutes_in("all I did today;1 1 1 1 1 1 1"), 7)
        self.assertEqual(calculate_total_minutes_in("all I did today;1m 1m 1m 1m 1m 1m 1h 1m"), 67)
        self.assertEqual(calculate_total_minutes_in("all I did today;1m 1m 1m 1m 1m 1m 1m1h 10m0h"), 77)
        self.assertEqual(calculate_total_minutes_in("all I did today;1m 1m 1m 1m 1m 1m 1m1h 10m000000000000000001h"), 137)
        self.assertEqual(calculate_total_minutes_in("all I did today; i 20m, 35m, 2.5h, 3h40m v"), 425)


def calculate_total_minutes_in(time_tailored_string=string_example):
    total_minutes = 0
    if ';' not in time_tailored_string:
        return total_minutes  
    else: 
        tokens = re.split(',\s*|[,\s]', time_tailored_string.split(";")[1])
        tokens_with_numbers = [x for x in tokens if any(c.isdigit() for c in x)]

        for token in tokens_with_numbers:
            if ('h'in token) or ('m'in token):
                matched_hours = re.search(r'[\d.]+($|(?=[h]))', token)
                if matched_hours is not None:
                    hours = matched_hours.group(0)
                else:
                    hours = 0
                matched_minutes = re.search(r'[\d.]+($|(?=[m]))', token)
                if matched_minutes is not None:
                    minutes = matched_minutes.group(0)
                else:
                    minutes = 0
            else:
                minutes = re.search(r'[0-9]*\.?[0-9]*', token).group(0)
                hours = 0
            total_minutes += Decimal(hours)*60 + Decimal(minutes)
        return ceil(total_minutes)


if __name__ == "__main__":
    unittest.main()