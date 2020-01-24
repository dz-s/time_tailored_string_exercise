import re
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
                matched_minutes = re.search(r'[\d]+($|(?=[m]))', token)
                if matched_minutes is not None:
                    minutes = matched_minutes.group(0)
                else:
                    minutes = 0
            else:
                minutes = re.search(r'\d+', token).group(0)
                hours = 0
            total_minutes += int(float(hours)*60 + int(minutes))
        return total_minutes


if __name__ == "__main__":
    unittest.main()