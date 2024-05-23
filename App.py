from flask import Flask, render_template, request, url_for, flash, session, redirect
from markupsafe import escape
from flask_sqlalchemy import SQLAlchemy
from passlib.hash import sha256_crypt
import gemini
import requests
import datetime

from DBHelper import DBConnector
from MailHelper import MailConnector

## Segregate it to separate file 
def get_weather_data(api_key: str, location: str, start_date: str, end_date: str) -> dict:
    """
    Retrieves weather data from Visual Crossing Weather API for a given location and date range.

    Args:
        api_key (str): API key for Visual Crossing Weather API.
        location (str): Location for which weather data is to be retrieved.
        start_date (str): Start date of the date range in "MM/DD/YYYY" format.
        end_date (str): End date of the date range in "MM/DD/YYYY" format.

    Returns:
        dict: Weather data in JSON format.

    Raises:
        requests.exceptions.RequestException: If there is an error in making the API request.
    """
    # Date Formatting as per API "YYYY-MM-DD"

    base_url = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{location}/{start_date}/{end_date}?unitGroup=metric&include=days&key={api_key}&contentType=json"

    try:
        response = requests.get(base_url)
        response.raise_for_status()
        data = response.json()
        # print(json.dumps(data, indent=4, sort_keys=True))
        return data
    except requests.exceptions.RequestException as e:
        print("Error:", e.__str__)


app = Flask(__name__, template_folder="template")
app.config['DEBUG'] = True

## Later add this to .env config file
api_key = "685ZPJJQC234JJ3PA9X4Y3L57"
app.secret_key = "S20sX2t98IyiuBIzlTO9ZPMMyaMIv39"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/about")
def callAbout():
    return render_template("about.html")

@app.route("/login")
def callLogin():
    return render_template("login.html")

@app.route("/login", methods=['POST'])
def loginUser():
    data = request.form
    email = data['email']
    password = data['password']

    obj = DBConnector()
    userData = obj.selectUserPass(email)
    if userData:
        print("Checking Password")
        if sha256_crypt.verify(password, userData[5]):
            print("In Session Creation")
            session['userId'] = userData[0]
            session['fname'] = userData[1]
            session['lname'] = userData[2]
            session['email'] = userData[3]
            session['phone'] = userData[4]
            flash("Login Successful", "success")
            return render_template("index.html")
    
    flash("Login Failed","danger")
    return render_template("index.html")

@app.route("/signup")
def callSignup():
    return render_template("signup.html")

@app.route("/signup", methods=['POST'])
def registerUser():
    data = request.form
    fname = data['first_name']
    lname = data['last_name']
    email = data['email']
    phone = data['phone']
    password = sha256_crypt.encrypt(data['password'])

    obj = DBConnector()

    obj.insertUser(fname, lname, email, phone, password)
    ## Need to add session for userId
    print("In Session Creation")
    session['fname'] = fname
    session['lname'] = lname
    session['email'] = email
    session['phone'] = phone
    flash("User Sign Up Successful", "success")
    return render_template("index.html")

    # if obj.insertUser(fname, lname, email, phone, password):
        
    
    # flash("Unable to Sign Up", "danger")
    # return render_template("signup.html")

@app.route("/logout")
def callLogout():
    session.clear()
    return render_template("index.html")
    

@app.route("/service")
def callService():
    return render_template("service.html")

@app.route("/product")
def callProduct():
    return render_template("product.html")

@app.route("/gallery")
def callGallery():
    return render_template("gallery.html")

@app.route("/feature")
def callFeature():
    return render_template("feature.html")

@app.route("/team")
def callTeam():
    return render_template("team.html")

@app.route("/testimonial")
def callTestimonial():
    return render_template("testimonial.html")

@app.route("/contact")
def callContact():
    return render_template("contact.html")

@app.route("/contactus", methods=["POST"])
def contactUsMail():
    name = request.form.get("name")
    subject = request.form.get("subject")
    message = request.form.get("message")
    email = request.form.get("email")

    mailObj = MailConnector()

    if mailObj.send_email(subject, message):
        print("Mail sent successfully")
        mailObj.send_confirmation(name, email)
        print("Confirmation sent successfully")
    else:
        print("Unable to send mail")

    return render_template("contact.html")

@app.route("/dashboard", methods=['POST'])
def callDashboard():
    if request.method == "POST":
        global source, destination, start_date, end_date
        source = request.form.get("source")
        destination = request.form.get("destination")
        start_date = request.form.get("date")
        end_date = request.form.get("return")
        # Calculating the number of days
        no_of_day = (datetime.datetime.strptime(end_date, "%Y-%m-%d") - datetime.datetime.strptime(start_date, "%Y-%m-%d")).days
        # Process the route input here
        if no_of_day < 0:
            flash("Return date should be greater than the Travel date (Start date).", "danger")
            return redirect(url_for("index"))
        else:
            try:
                weather_data = get_weather_data(api_key, destination, start_date, end_date)
            except requests.exceptions.RequestException as e:
                flash("Error in retrieving weather data.{e.Error}", "danger")
                return redirect(url_for("index"))
        
        """Debugging"""
        # Json data format printing
        # print(json.dumps(weather_data, indent=4, sort_keys=True))
        try:
            plan = gemini.generate_itinerary(source, destination, start_date, end_date, no_of_day)
        except Exception as e:
            flash("Error in generating the plan. Please try again later.", "danger")
            return redirect(url_for("index"))
        if weather_data:
            # Render the weather information in the template
            print("got Weather data and plan")
            return render_template("dashboard.html", weather_data=weather_data, plan=plan)
    
    return render_template('service.html')

# if __name__ == "__main__":
#     app.run()