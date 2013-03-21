# This is the test file which will get the data from staag for a date interval and print it

from staagg import Staagg

if __name__ == '__main__':
    from datetime import datetime
    start_date = datetime.strptime('2013-03-18 00:00:00', '%Y-%m-%d %H:%M:%S')
    end_date = datetime.strptime('2013-03-20 23:59:59', '%Y-%m-%d %H:%M:%S')
    staagg = Staagg(key = '<YOUR-API-KEY>', start_date = start_date,
	    end_date = end_date)
    print staagg.get()
