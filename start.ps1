Start-Process "http://127.0.0.1:5500/website_simulation/index.html"
Start-Process "http://127.0.0.1:5500/training_portal/index.html"
python -m http.server 5500 --bind 127.0.0.1
127.0.0.1