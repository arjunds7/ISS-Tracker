import requests as rfq
import datetime as dt
import smtplib
import time

my_email = "your email"
my_password = "your password"

MY_LAT = 52.5200
MY_LNG = 13.4050


def is_iss_overhead():
    """Check if the ISS is above your specified Latitude and Longitude"""
    iss_response = rfq.get(url="http://api.open-notify.org/iss-now.json")
    data = iss_response.json()
    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])
    if MY_LAT - 5 <= iss_latitude <= MY_LAT + 5 and MY_LNG - 5 <= iss_longitude <= MY_LNG:
        return True


def is_night():
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LNG,
        "formatted": 0
    }
    time_response = rfq.get(url="https://api.sunrise-sunset.org/json", params=parameters)
    time_data = time_response.json()
    time_now = dt.datetime.now().hour
    sunrise = int(time_data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(time_data["results"]["sunset"].split("T")[1].split(":")[0])
    if time_now >= sunset or time_now <= sunrise:
        return True


while True:
    time.sleep(60)
    if is_iss_overhead() and is_night():
        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(user=my_email, password=my_password)
            connection.sendmail(from_addr=my_email,
                                to_addrs="email to which mail to be sent",
                                msg="Subject: Look up the sky\n\n There is the ISS.\n Yahoooooo")
