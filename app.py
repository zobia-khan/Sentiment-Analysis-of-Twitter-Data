import os
import psycopg2
from flask import Flask, render_template, flash, redirect, request, url_for, session
import csv
import snscrape.modules.twitter as sntwitter
import pandas as pd
import itertools
import pythainlp

import matplotlib
matplotlib.use('Agg')  # Set the backend to 'Agg' for non-interactive mode
from werkzeug.utils import secure_filename #for taking filename only not its path
from datetime import datetime
import asyncio
from PredictionandAnalysisEnglish import pre_process
from PredictionandAnalysisRomanUrdu import pre_process_roman_urdu
from PredictionandAnalysisUrdu import pre_process_urdu
from PredictionandAnalysisMix import process_mix


app = Flask(__name__)
app.config['SECRET_KEY']='my super secret key'


UPLOAD_FOLDER ="/Users/Zobia/FYP Web/media/uploaded"
#Allowed file extension is .csv
ALLOWED_EXTENSIONS = set(['csv'])

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def get_db_connection():
    conn = psycopg2.connect(
        host="localhost",
        database="flask_db",
        user="postgres",
        port="5432",
        password="1234")
    return conn


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS
    

@app.route('/index')
def index():
    username = session.get('email')
    if not username:
        return redirect('/login')  # Redirect to login page if user is not logged in
    else:
        return render_template('index.html')

# async def process_file(file_path, option):
#     if option == 'english':
#         pre_process(file_path)
#     elif option == 'urdu':
#         pre_process_urdu(file_path)
#     elif option == 'roman_urdu':
#         pre_process_roman_urdu(file_path)
#     elif option == 'mix_data':
#         process_mix(file_path)
async def process_file(file, option):
    try:
        if option == 'english':
            pre_process(file)
        elif option == 'urdu':
            pre_process_urdu(file)
        elif option == 'roman_urdu':
            pre_process_roman_urdu(file)
        elif option == 'mix_data':
            process_mix(file)
        else:
            raise ValueError("Invalid option selected.")

        return 'File uploaded and option processed successfully.'
    except Exception as e:
        error_message = f"An error occurred: {str(e)}"
        return error_message


def tweeter_scrapper(text, numberOfTweets, start, end):

    # Creating list to append tweet data to
    tweets_list = []

    # Using TwitterSearchScraper to scrape data and append tweets to list
    for i, tweet in enumerate(sntwitter.TwitterSearchScraper(
            '{text} since:{start} until:{end}'.format(text=text, start=start, end=end)).get_items()):
        if i > numberOfTweets:
            break
        tweets_list.append([tweet.content])
    # Creating a dataframe from the tweets list above
    tweets_df = pd.DataFrame(tweets_list,
                             columns=['text'])

    tweets_all_df = pd.concat([tweets_df], axis=0)
    tweets_all_df.to_csv('text_verify.csv', sep=',', index=False)


def urdu_tweet_scrapper(text, numberOfTweets, start, end):

    # Creating list to append tweet data to
    tweets_list = []

    # Using TwitterSearchScraper to scrape data and append tweets to list
    for i, tweet in enumerate(sntwitter.TwitterSearchScraper(
            '{text} since:{start} until:{end}'.format(text=text, start=start, end=end)).get_items()):
        if i > numberOfTweets:
            break

        if tweet.lang == "ur": # only append the tweet if the language is Urdu
            text = pythainlp.util.normalize(tweet.content) # normalize the text to remove diacritics and make the text consistent
            tweets_list.append([text])
    
    # Creating a dataframe from the tweets list above
    tweets_df = pd.DataFrame(tweets_list,
                             columns=['text'])

    tweets_all_df = pd.concat([tweets_df], axis=0)
    tweets_all_df.to_csv('urdu.csv', sep=',', index=False, encoding='utf-8-sig')


@app.route('/prediction_and_analysis', methods=['GET','POST'])
def prediction_and_analysis():
    username = session.get('email')
    if not username:
        return redirect('/login')  # Redirect to login page if user is not logged in
    else:
        if request.method == 'POST':
            file = request.files['file']
            if file and allowed_file(file.filename):
                #filename = secure_filename(file.filename) #remove the slashes in filename for secure uploading
                #new_filename  = f'{filename.split(".")[0]}_{str(datetime.now())}.csv'
                # # new_filename = new_filename.replace("\\","\")  
                # # file.save(os.path.join('media','/uploaded',new_filename))
                # pre_process(file)
                # process(file)
                # feature_extraction_english(file)
                # report(file)
                            # Get the selected option
                option = request.form.get('option')

                # # Call the appropriate function based on the selected option
                # asyncio.run(process_file(file, option))


                # return 'File uploaded and option processed successfully.'
                result = asyncio.run(process_file(file, option))
        
                if "error" in result.lower():
                    # flash(result)  # Display the error message to the user
                    flash('Incorrect option selected, please select option according to the language in file.')
                else:
                    flash(result)  # Display success message to the user

                return render_template('prediction_and_analysis.html')

        return render_template('prediction_and_analysis.html')

# Function to handle Roman Urdu Mix option
def handle_roman_urdu_mix(file):
    # Perform Roman Urdu Mix option logic here
    # Example: Process the uploaded file for Roman Urdu Mix language
    pass

# @app.route('/')
# def index():
#     return render_template('index.html')

@app.route('/', methods=['GET','POST'])
def signup():
    if(request.method == "POST"):
        print("again")
        var_user=request.form['user']
        var_email=request.form['email']
        var_password=request.form['password']
        
        if (var_user == "" and  var_email == "" and var_password == ""):
            flash("Form incomplete!!")
            return render_template('signup.html')
        else:
            try:
                conn = get_db_connection()
                cur = conn.cursor()
                cur.execute('SELECT username, email FROM signup;')
                data = cur.fetchall()
                print(data)
                for row in data:
                        print("in row")
                        if var_user in row or var_email in row:
                            if len(var_password) < 8:
                                print("in len check")
                                flash("You password is too short..")
                                return redirect('signup.html')
                            flash("Username or Email already exists!")
                            return redirect('signup.html')
                cur.execute("INSERT INTO signup (username, email, password) VALUES (%s,%s,%s)",
                            (var_user,var_email,var_password))
                
                conn.commit()

                print("before login in signup")
                return redirect('/login')

            except:
                conn.rollback()
                flash("Error!")
                return render_template('signup.html')
            finally:
                conn.close()
    return render_template('signup.html')

@app.route('/login', methods=['GET','POST'])
def login():
    if(request.method == "POST"):
        var_email = request.form["email"]
        var_password = request.form["password"]

        if (var_email == "" and var_password==""):
                flash('Please enter Username Password!!')
                return redirect(url_for('login'))
        else:
            try:
                conn = get_db_connection()
                cur = conn.cursor()
                print('before execute')   
                cur.execute('SELECT email, password FROM signup WHERE email=%s and password=%s',[var_email, var_password])
                data = cur.fetchone()
                print(data)
                if var_email in data and var_password in data:
                    session['email'] = request.form["email"]
                    return redirect(url_for('index'))
                else:
                    flash('Wrong Credentials!!')
            except:
                conn.rollback()
                flash("Error!")
            finally:
                conn.close()
    return render_template('login.html')

@app.route('/logout')
def logout():
    # Remove the username from the session
    del session['email']
    return redirect(url_for('login'))


@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/error', methods=['GET','POST'])
def errorpage():
    username = session.get('email')
    if not username:
        return redirect('/login')  # Redirect to login page if user is not logged in
    else:
        return render_template('error.html')

@app.route('/scrape', methods=['GET','POST'])
def scrape():
    username = session.get('email')
    if not username:
        return redirect('/login')  # Redirect to login page if user is not logged in
    else:
        # if(request.method == "POST"):
        #     var_keyword = request.form["keyword"]
        #     var_tweets = request.form["tweets"]
        #     var_start = request.form["start"]
        #     var_end = request.form["end"]

        #     if (var_keyword == "" and var_tweets=="" and var_start=="" and var_end==""):
        #             flash('Please enter all details!!')
        #             return redirect(url_for('scrape'))
        #     else:
        #         print(var_keyword, var_tweets, var_start, var_end)
        #         tweeter_scrapper(var_keyword,var_tweets,var_start,var_end)
        #         flash('scraped successfully!!')
            return render_template('scrape.html')

if __name__ == "__main__":
    app.run(debug=True)