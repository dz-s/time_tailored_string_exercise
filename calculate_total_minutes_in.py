import re

string_example="all I did today;r i vlad 20m, g 35m, 2.5h, 2hu40m v 40h20m vlad 132h20m r1.2h e 30, 60m i pp"

def get_spent_time(worklog):
    LOG_REGEX = r'(?P<log>[A-Za-z-_]{1,} +([0-9]{1,}[hm]+([0-9]{1,}[hm]+|)))'
    spent_by_dev = {}
    for m in re.finditer(LOG_REGEX, worklog):
        log = m.group('log')
        dev, spent = log.split()
        h_idx = spent.find('h')
        m_idx = spent.find('m')
        h = 0
        m = 0
        if h_idx != -1:
            h = int(spent[0:h_idx])
        if m_idx != -1:
            m = int(spent[h_idx + 1: m_idx])
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

    return spent_by_dev, total


if __name__ == "__main__":
    by_dev, total = get_spent_time(string_example)
    print(total)