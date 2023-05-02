import json
import time
import threading
from Booking import Booking
from datetime import datetime, timedelta
from Mail import sendMail


#default 4
max_advanced_booking = 4;

def run(booking):
    booked = False;
    if datetime.weekday(nextBookingDay_Date) in booking.get_config()["day"]:
        for period in booking.get_config()["period"]:
            if booking.book(period, nextBookingDay_Date.year, nextBookingDay_Date.month, nextBookingDay_Date.day):
                booked = True;

    if booked:
        html_table = booking.get_html_table();
        sendMail(booking.get_config()["mail"], booking.get_config()["name"], nextBookingDay_Date, html_table);

    else:
        raise Exception("No appoinment booked.")

configs = ['config/config_florian.json', 'config/config_david.json']
threads = [];
for link in configs:
    with open(link) as config_file:
        threads.append(threading.Thread(target=run, args=(Booking(json.load(config_file)),)))
    


while True:
    # Get the current time
    now = datetime.now();

    # Set the execution time to 23:59:00
    execute_time = now.replace(hour=23, minute=59)
    
    # Check if the current time is at or after the execution time
    if now >= execute_time:

        try:
            # Book
            nextBookingDay_Date = datetime.today() + timedelta(days=max_advanced_booking);

            for thread in threads:
                thread.start();
    
        except Exception as e: print(e)

        # Set the next execution time to tomorrow
        execute_time += timedelta(days=1);


    # Calculate the time to sleep until the next execution time
    time_to_sleep = (execute_time - now).total_seconds();
    print("Next update in " + str(time_to_sleep / 3600) + "h");

    # Wait until the next execution time
    time.sleep(time_to_sleep)


        



