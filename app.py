from flask import Flask, render_template, request, redirect, url_for
import csv
import os

app = Flask(__name__)

# Dateiname für die CSV-Datei
CSV_FILE = 'votes.csv'

# Initialisierung der Abstimmungsergebnisse aus der CSV-Datei, falls vorhanden
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
    # Wenn die CSV-Datei nicht vorhanden ist oder leer ist, verwenden wir die initialen Abstimmungsergebnisse
    for i in range(1, 110):
        option_name = f"Option {i}"
        votes[option_name] = 0

@app.route('/')
def index():
    return render_template('index real.html', votes=votes)

@app.route('/vote', methods=['POST'])
def vote():
    option = request.form['option']
    num_votes = int(request.form['num_votes'])
    
    # Aktualisierung der Abstimmungsergebnisse
    votes[option] += num_votes
    
    # Aktualisierung der CSV-Datei
    with open(CSV_FILE, 'w') as file:
        writer = csv.writer(file)
        for option, count in votes.items():
            writer.writerow([option, count])
    
    return redirect(url_for('index'))

@app.route('/winner')
def winner():
    if not votes:
        return "No votes recorded yet."
    
    # Finde die Top-3-Optionen mit den meisten Stimmen
    top_three = sorted(votes, key=votes.get, reverse=True)[:3]
    return render_template('winner.html', top_three=top_three)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
