from flask import Flask, render_template, request, redirect, url_for
import csv
import os

app = Flask(__name__)

# Dateinamen für die CSV-Dateien
MALE_CSV_FILE = 'male_votes.csv'
FEMALE_CSV_FILE = 'female_votes.csv'

# Initialisierung der Abstimmungsergebnisse aus den CSV-Dateien, falls vorhanden
male_votes = {}
female_votes = {}

def load_votes_from_csv(csv_file, votes):
    if os.path.exists(csv_file) and os.path.getsize(csv_file) > 0:
        with open(csv_file, 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                if len(row) == 3:
                    option, gender, count = row
                    if gender == 'male':
                        votes[option] = int(count)
                    else:
                        votes[option] = int(count)
                else:
                    print("Invalid row in CSV:", row)

load_votes_from_csv(MALE_CSV_FILE, male_votes)
load_votes_from_csv(FEMALE_CSV_FILE, female_votes)

# Falls die CSV-Datei nicht vorhanden ist oder leer ist, verwenden wir die initialen Abstimmungsergebnisse
if not male_votes:
    for i in range(1, 110):
        option_name = f"Option {i}"
        male_votes[option_name] = 0

if not female_votes:
    for i in range(1, 110):
        option_name = f"Option {i}"
        female_votes[option_name] = 0

@app.route('/')
def index():
    return render_template('index.html', male_votes=male_votes, female_votes=female_votes)

@app.route('/vote', methods=['POST'])
def vote():
    option = request.form['option']
    num_votes = int(request.form['num_votes'])
    gender = request.form['gender']

    if gender == 'male':
        # Aktualisierung der männlichen Abstimmungsergebnisse
        male_votes[option] += num_votes
        csv_file = MALE_CSV_FILE
    elif gender == 'female':
        # Aktualisierung der weiblichen Abstimmungsergebnisse
        female_votes[option] += num_votes
        csv_file = FEMALE_CSV_FILE
    else:
        return "Invalid gender specified."

    # Aktualisierung der CSV-Datei
    with open(csv_file, 'w') as file:
        writer = csv.writer(file)
        for option, count in male_votes.items():
            writer.writerow([option, 'male', count])
        for option, count in female_votes.items():
            writer.writerow([option, 'female', count])

    return redirect(url_for('index'))

@app.route('/winner')
def winner():
    if not male_votes and not female_votes:
        return "No votes recorded yet."

    # Finde die Top-3-Optionen mit den meisten Stimmen für Männer und Frauen
    top_three_male = sorted(male_votes, key=male_votes.get, reverse=True)[:3]
    top_three_female = sorted(female_votes, key=female_votes.get, reverse=True)[:3]
    return render_template('winner.html', top_three_male=top_three_male, top_three_female=top_three_female)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
