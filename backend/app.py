from flask import Flask, render_template, request, redirect, url_for
import csv
import os

app = Flask(__name__)

CSV_FILE = 'votes.csv'


votes = {}
if os.path.exists(CSV_FILE) and os.path.getsize(CSV_FILE) > 0:
    with open(CSV_FILE, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if len(row) == 2:
                option, count = row
                votes[option] = int(count)
            else:
                print("Invalid row in CSV:", row)
else:
    for i in range(1, 110):
        option_name = f"Option {i}"
        votes[option_name] = 0





@app.route('/')
def index():
    return render_template('index.html', votes=votes)


@app.route('/vote', methods=['POST'])
def vote():
    option = request.form['option']
    num_votes_str = request.form['num_votes']
    

    if num_votes_str.strip():
        try:
            num_votes = int(num_votes_str)
        except ValueError:
            return "Invalid number of votes. Please enter a valid number."
        
        votes[option] += num_votes
    
        with open(CSV_FILE, 'w') as file:
            writer = csv.writer(file)
            for option, count in votes.items():
                writer.writerow([option, count])
    else:
        return render_template('index.html', votes=votes)
    
    return redirect(url_for('index'))



@app.route('/winner')
def winner():
    if not votes:
        return "No votes recorded yet."
    
    males = {}
    females = {}

    for key in votes.keys():
        if key[0] == "5":
            males[key] = votes[key]
        elif key[0] == "A":
            females[key] = votes[key]
    
    top_males = sorted(males, key=males.get, reverse=True)[:5]
    top_females = sorted(females, key=females.get, reverse=True)[:5]
    return render_template('winner.html', top_males=top_males, top_females=top_females)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)