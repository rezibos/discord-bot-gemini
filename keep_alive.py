import os
import time
from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def home():
    return f"""
    <html>
        <head>
            <title>Discord Bot Gemini - Railway</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    text-align: center;
                    margin-top: 50px;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                }}
                .container {{
                    max-width: 600px;
                    margin: 0 auto;
                    padding: 20px;
                }}
                .status {{
                    color: #00ff88;
                    font-size: 28px;
                    margin: 20px 0;
                }}
                .info {{
                    background: rgba(255,255,255,0.1);
                    padding: 20px;
                    border-radius: 15px;
                    margin: 20px 0;
                }}
                .command {{
                    background: rgba(0,0,0,0.3);
                    padding: 10px;
                    margin: 10px 0;
                    border-radius: 5px;
                    font-family: monospace;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>🤖 Discord Bot Gemini</h1>
                <p class="status">Status: Online ✅</p>
                <p>🚀 Hosted on Railway.app</p>
                
                <div class="info">
                    <h3>📋 Available Commands:</h3>
                    <div class="command">!tanya [pertanyaan] - Tanya ke Gemini AI</div>
                    <div class="command">!help - Tampilkan bantuan</div>
                    <div class="command">!ping - Cek status bot</div>
                    <div class="command">!pc++ - Link pembelajaran C++</div>
                </div>
                
                <p><small>🕐 Last updated: {time.ctime()}</small></p>
                <p><small>💜 Powered by Railway</small></p>
            </div>
        </body>
    </html>
    """

def run(port=8080):
    app.run(host='0.0.0.0', port=port, debug=False)

def keep_alive(port=8080):
    t = Thread(target=run, args=(port,))
    t.daemon = True
    t.start()
    print(f"🌐 Keep alive server started on port {port}")