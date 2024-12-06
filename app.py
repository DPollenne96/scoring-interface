#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os
from flask import jsonify 
from flask import Flask, render_template_string, request, redirect, url_for
from IPython.display import HTML
import threading
from werkzeug.serving import make_server
from collections import defaultdict
from datetime import datetime

# INITIALIZE NAMES AND APP
app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

players = defaultdict(int)

ALL_NAMES = [
    "Ahd EL TEREFI",
    "Alexandra CAMPOS",
    "Amandine JEANNOTIN",
    "Amit SHUKLA",
    "Ana VELASCO ORTEGA",
    "Andrea FOSCHINI",
    "Annabelle HELPS",
    "Arina DIVO",
    "Caio DE PAULA CAMARGO PISANO",
    "Carlos MIER Y LEON",
    "Christelle Peiyun TAN",
    "Dennis CHIA",
    "Dennis PAPIROWSKI",
    "Diana NASRIL",
    "Eleonora FROLOVA",
    "Fabian VANDEMAELE",
    "Gaurav DIXIT",
    "Ignacio ORTEGA BAENA",
    "Jass LIEW",
    "Jenna PENDER",
    "Joanne SEBASTIAN",
    "Juan ALVARADO VICTORIA",
    "Juan WU",
    "Karim AWAD",
    "Kate WOSKA",
    "Keshav NEPAL",
    "Laure POTTER",
    "Limin LOU",
    "Meizi YAN",
    "Nathalie MEHANNA",
    "Nawel GHIAR",
    "Omar KHAN",
    "Patricia NEO",
    "Philippe ROSE",
    "Roby BUYUNG",
    "Safisah RAHIM",
    "Saif HASAN",
    "Samia ALI",
    "Samia ELFEKIH",
    "Sky DOU",
    "Stefan NEL",
    "Suhaila ABDUL HALIM",
    "Sushant JAIN",
    "Thomas PESQUET",
    "Tom BIHUN",
    "Vaughan COETZEE",
    "Victoria RODRIGUES",
    "Yan AZAR",
    "Yasir SAEED",
    "Zeina AL MOUALLEM"
]

html_template = """
<!DOCTYPE html>
<html>
<head>
    <title>GEMBA 25, Power and Politics, Professor Kaisa</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate">
    <meta http-equiv="Pragma" content="no-cache">
    <meta http-equiv="Expires" content="0">
    <style>
        /* Base layout */
        body { 
            font-family: "Helvetica Neue", Arial, sans-serif;
            margin: 0;
            padding: 0px;
            background-color: #f5f5f5;
            color: #2f3432;
            min-height: 100vh;
        }

        .main-content {
            display: flex;
            height: calc(100vh - 62px);
            width: 100%;
        }

        /* Header */
        h1 {
            color: white;
            background-color: #215d4f;
            font-size: 24px;
            text-align: center;
            margin: 0 0 5px 0;
            padding: 10px;
            width: 100%;
            box-sizing: border-box;
        }

        h2 {
            color: #215d4f;
            font-size: 20px;
            margin-top: 0;
            text-align: center;
        }

        /* Left section */
        .left-section {
            width: 30%;
            display: flex;
            flex-direction: column;
            border-right: 2px solid #ddd;
        }

        .scoring-rules {
            background: #000000;
            color: white;
            padding: 10px;
            width: 100%;
            box-sizing: border-box;
        }

        .scoring-table {
            width: 100%;
            border-collapse: collapse;
            margin: 0;
            font-size: 14px;
        }

        .scoring-table th, 
        .scoring-table td {
            padding: 4px;
            text-align: center;
            border: 1px solid #ffffff;
        }

        .names-column {
            flex: 1;
            background: #f5f5f5;
            padding: 10px;
            overflow-y: auto;
        }

        /*.right-section {
            width: 70%;
            display: flex;  
            gap: 20px; 
            padding: 0 20px; 
        }*/

/* Modify the group-columns CSS to take on the role that right-section had */
        .group-columns {
            width: 70%;
            display: flex;
            flex: 1;
            background: #ffffff;
            padding: 0 20px;
            gap: 20px;
        }

        .group {
            flex: 1;
            padding: 15px;
            border-right: 4px solid #215d4f;
            overflow-y: auto;
            margin-right: 30px;
        }

        .group:last-child {
            border-right: none;
            margin-right: 0;
        }

        /* Group sizes */
        .group:nth-child(1) { flex: 24; }  /* Triangles */
        .group:nth-child(2) { flex: 23; }  /* Circles */
        .group:nth-child(3) { flex: 23; }  /* Squares */

        /* Player entries */
        .player-entry {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 2px;
            margin: 1px 0;
            background: #ffffff;
        }

        .group:nth-child(1) .player-entry { font-size: 17px; }  /* Triangles */
        .group:nth-child(2) .player-entry { font-size: 16px; }  /* Circles */
        .group:nth-child(3) .player-entry { font-size: 16px; }  /* Squares */

        /* Form elements */
        .score-form {
            margin: 1px 0;
            padding: 2px;
            background: #ffffff;
            border-radius: 4px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        }

        .score-input {
            width: 30px;
            padding: 2px;
            font-size: 14px;
            border: 1px solid #215d4f;
            border-radius: 4px;
            margin-right: 4px;
        }

        button {
            background-color: #215d4f;
            color: white;
            border: none;
            padding: 3px 6px;
            border-radius: 4px;
            cursor: pointer;
            font-size: 12px;
        }

        button:hover {
            background-color: #1a4940;
        }
    </style>
</head>
<body>
    <h1>GEMBA 25, Power and Politics, Professor Kaisa Snellman</h1>
    
    <div class="main-content">
        <div class="left-section">
            <div class="scoring-rules">
                <table class="scoring-table">
                    <tr>
                        <th>N chips</th>
                        <th>1</th>
                        <th>2</th>
                        <th>3</th>
                        <th>4</th>
                        <th>5</th>
                    </tr>
                    <tr>
                        <td>Gold</td>
                        <td>8</td>
                        <td>16</td>
                        <td>24</td>
                        <td>32</td>
                        <td>40</td>
                    </tr>
                    <tr>
                        <td>Green</td>
                        <td>4</td>
                        <td>8</td>
                        <td>12</td>
                        <td>16</td>
                        <td>20</td>
                    </tr>
                    <tr>
                        <td>Red</td>
                        <td>3</td>
                        <td>6</td>
                        <td>9</td>
                        <td>12 +2 /14</td>
                        <td>15 +3 /18</td>
                    </tr>
                    <tr>
                        <td>White</td>
                        <td>2</td>
                        <td>4</td>
                        <td>6</td>
                        <td>8 +5 /13</td>
                        <td>10 +7 /17</td>
                    </tr>
                    <tr>
                        <td>Blue</td>
                        <td>1</td>
                        <td>2</td>
                        <td>3</td>
                        <td>4 +8 /12</td>
                        <td>5 + 11 / 16</td>
                    </tr>
                </table>
            </div>
            <div class="names-column">
                {% for name in all_names %}
                <form class="score-form" action="{{ url_for('update_score') }}" method="post">
                    <div class="player-entry">
                        <span>{{ name }}</span>
                        <div>
                            <input type="hidden" name="name" value="{{ name }}">
                            <input type="text" name="score" value="{{ players[name] }}" class="score-input">
                            <button type="submit">Update</button>
                        </div>
                    </div>
                </form>
                {% endfor %}
            </div>
        </div>

        <div class="group-columns">
            <div class="group">
                <h2>Triangles</h2>
                {% for name, score in triangles %}
                <div class="player-entry">
                    <span>{{ name }}</span>
                    <span>{{ score }}</span>
                </div>
                {% endfor %}
            </div>
            
            <div class="group">
                <h2>Circles</h2>
                {% for name, score in circles %}
                <div class="player-entry">
                    <span>{{ name }}</span>
                    <span>{{ score }}</span>
                </div>
                {% endfor %}
            </div>
            
            <div class="group">
                <h2>Squares</h2>
                {% for name, score in squares %}
                <div class="player-entry">
                    <span>{{ name }}</span>
                    <span>{{ score }}</span>
                </div>
                {% endfor %}
            </div>
        </div>
    </div>
    <script>
    document.querySelectorAll('.score-form').forEach(form => {
        form.addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const formData = new FormData(this);
            const response = await fetch(this.action, {
                method: 'POST',
                body: formData
            });
            
            if (response.ok) {
                const result = await response.json();
                // Update the score input
                const scoreInput = this.querySelector('.score-input');
                scoreInput.value = result.new_score;
                
                // Update the groups
                updateGroups('triangles', result.triangles);
                updateGroups('circles', result.circles);
                updateGroups('squares', result.squares);
            }
        });
    });

    function updateGroups(groupName, players) {
    const groups = document.querySelectorAll('.group');
    let targetGroup;
    groups.forEach(group => {
        if (group.querySelector('h2').textContent === groupName[0].toUpperCase() + groupName.slice(1)) {
            targetGroup = group;
        }
    });
    
    let html = `<h2>${groupName[0].toUpperCase() + groupName.slice(1)}</h2>`;
    players.forEach(([name, score]) => {
        html += `
            <div class="player-entry">
                <span>${name}</span>
                <span>${score}</span>
            </div>
        `;
    });
    targetGroup.innerHTML = html;
}
    document.querySelectorAll('.score-form').forEach(form => {
        const scoreInput = form.querySelector('.score-input');
        
        scoreInput.addEventListener('change', function(e) {
            try {
                let expression = this.value;
                
                // Check if there's any math operation to perform
                if (expression.includes('+') || expression.includes('-') || 
                    expression.includes('*') || expression.includes('/')) {
                    
                    // Fixed the escape sequence by using double backslashes
                    if (/^[\\d\\s+\\-*/]+$/.test(expression)) {
                        let result = Function('return ' + expression)();
                        // Round to the nearest integer
                        result = Math.round(result);
                        this.value = result;
                    } else {
                        // If invalid characters are entered, keep the original value
                        this.value = expression;
                    }
                }
            } catch (error) {
                // If there's an error, keep the original value
                console.error('Invalid expression');
            }
        });
    });
    </script>
</body>
</html>
"""

# Your existing route handlers
@app.route('/')
def index():
    timestamp = datetime.now().timestamp()
    active_players = {name: score for name, score in players.items() if score > 0}
    sorted_players = sorted(active_players.items(), key=lambda x: x[1], reverse=True)
    
    triangles = sorted_players[:15]
    circles = sorted_players[15:32]
    squares = sorted_players[32:]

    sorted_names = sorted(ALL_NAMES)
    
    return render_template_string(html_template,
                         all_names=ALL_NAMES,
                         players=players,
                         timestamp=timestamp,
                         triangles=triangles,
                         circles=circles,
                         squares=squares)

@app.route('/update_score', methods=['POST'])
def update_score():
    name = request.form['name']
    score = int(request.form['score']) if request.form['score'] else 0
    players[name] = score
    
    # Recalculate the groups
    active_players = {name: score for name, score in players.items() if score > 0}
    sorted_players = sorted(active_players.items(), key=lambda x: x[1], reverse=True)
    
    triangles = sorted_players[:15]
    circles = sorted_players[15:32]
    squares = sorted_players[32:]
    
    return jsonify({
        'success': True, 
        'new_score': score,
        'triangles': triangles,
        'circles': circles,
        'squares': squares
    })

# Server startup code
if __name__ == '__main__':
    try:
        server = make_server('127.0.0.1', 5000, app)
        thread = threading.Thread(target=server.serve_forever)
        thread.daemon = True
        thread.start()
        
        print("Server running at http://127.0.0.1:5000")
        display(HTML('<a href="http://127.0.0.1:5000" target="_blank">Click here to open the application</a>'))
        
    except Exception as e:
        print(f"Error starting server: {e}")

