import re

string_example="all I did today;r i vlad 20m, 20, 20m, g 35m, 2.5h, 2hu40m v 40h20m vlad 132h20m r1.2h e 30, 60m i pp"

def get_spent_time(worklog):
    LOG_REGEX = r'(?P<log>([A-Za-z-_]{1,}|)( +([0-9]{1,})(\.|)([hm]+|)([0-9]{1,}([hm]+|))))'
    spent_by_dev = {}
    last_dev = 'john_doe'
    for m in re.finditer(LOG_REGEX, worklog):
        log = m.group('log')
        log_arr = log.split()
        if log.strip().isdigit():
            spent_by_dev[last_dev]['m'] += float(log)
        elif len(log_arr) == 1:
            stripped = log.strip()
            last_c = stripped[-1:]
            if last_c == 'm':
                spent_by_dev[last_dev]['m'] += float(stripped[:-1])
            elif last_c == 'h':
                spent_by_dev[last_dev]['h'] += float(stripped[:-1])
        else:
            dev, spent = log_arr
            h_idx = spent.find('h')
            m_idx = spent.find('m')
            h = 0
            m = 0
            if h_idx != -1:
                h = float(spent[0:h_idx])
            if m_idx != -1:
                m = float(spent[h_idx + 1: m_idx])
            if dev in spent_by_dev:
                spent_by_dev[dev]['h'] += h 
                spent_by_dev[dev]['m'] += m
            else:
                spent_by_dev[dev] = {'h': h, 'm': m}

        #total spent
        total = {'h': 0, 'm': 0}
        for dev in spent_by_dev:
            total['h'] += spent_by_dev[dev]['h']
            total['m'] += spent_by_dev[dev]['m']
        #m => h 
        m_to_h = total['m']//60
        total['h'] +=  m_to_h
        total['m'] -= m_to_h*60

        last_dev = dev

    return spent_by_dev, total


if __name__ == "__main__":
    by_dev, total = get_spent_time(string_example)
    print(by_dev)