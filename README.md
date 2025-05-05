# 🏎️ Drive to Survive — Formula 1 Analytics Web App

Welcome to the **Drive to Survive** F1 Web App — a data-rich Flask-based project for exploring Formula 1 teams, drivers, schedules, and analytics with a beautiful and interactive UI.

---

## 🚀 Features

- Animated homepage with F1 sound effects and car animation
- View, filter, and manage drivers
- Explore teams and driver lineups by season
- Interactive circuit details
- Season schedule display for 2025
- Analytical charts:
  - Season champions
  - Top constructors
  - Fastest pit stops
  - Most frequent pole sitters
  - Points progression over a season
- Informational cards for beginners explaining DRS, pit stops, flags, etc.

---

## 🛠️ Tech Stack

- **Frontend**: HTML, CSS, JS, Chart.js
- **Backend**: Python, Flask
- **Database**: MySQL
- **Data Source**: Cleaned from CSVs (drivers, constructors, races, standings, qualifying, etc.)

---

## 🗂️ Project Structure

```bash
drive-to-survive/
│
├── app.py                   # 🔁 Main Flask app
├── templates/
│   ├── index.html           # 🏠 Homepage with animation and info cards
│   ├── drivers.html         # 👨‍✈️ Driver management UI
│   ├── teams.html           # 🏁 Teams and lineups
│   ├── schedule.html        # 📅 F1 2025 schedule display
│   ├── analysis.html        # 📊 Interactive charts
│   └── navbar.html          # 🔗 Shared navigation bar
│
├── static/
│   ├── css/
│   │   └── style.css        # 🎨 All styling rules
│   ├── js/
│   │   └── scripts.js       # 🎯 JS logic (animation, event handlers)
│   └── assets/              # 🎵 Car image + audio clip
│
├── database/
│   ├── schema.sql           # 🧱 Table creation queries
│   ├── insert.sql           # 🔼 Sample data inserts (e.g. schedule)
│   └── *.csv                # 📁 Raw CSV files for import
│
└── README.md                # 📘 You are here!
```

---

## ⚙️ Setup Instructions

### 1. Clone the repo

```bash
git clone https://github.com/your-username/drive-to-survive.git
cd drive-to-survive
```

### 2. Create & activate virtual environment

```bash
python -m venv venv
source venv/bin/activate  # on Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install flask mysql-connector-python
```

### 4. Set up MySQL Database

- Import schema & data:

```bash
mysql -u root -p < database/schema.sql
mysql -u root -p < database/insert.sql
```

### 5. Run the app

```bash
python app.py
```

Visit `http://127.0.0.1:5000` in your browser 🚀

---

## 📘 How to Read the Code

- All **Flask routes** are in `app.py`
  - `/drivers`, `/teams`, `/schedule`, `/analysis` — render HTML templates
  - `/api/...` — return JSON data for frontend JS charts
- **Templates** use Jinja2 syntax to inject dynamic content
- **JS Files** use `fetch()` to pull data from Flask APIs and render interactive Chart.js graphs
- **CSS** handles red-black racing theme and transitions (e.g., fade-ins, car animation)

---

## 🧪 Key APIs

| Endpoint                       | Description                           |
|-------------------------------|---------------------------------------|
| `/api/drivers`                | Get all drivers                       |
| `/api/season-champions`       | Points + names of season winners      |
| `/api/most-poles`             | Top 10 pole sitters                   |
| `/api/points-over-season/...` | Points over rounds for a driver/year  |
| `/api/schedule`               | Pulls from `F1_2025_Schedule` table   |

---

## 📌 Notes

- The current 2025 schedule is stored locally (API didn’t have updated data)
- You can add new drivers manually via the UI form
- Each analysis tab uses a separate `<canvas>` and fetch-based chart logic

---

## 💡 Planned Improvements

- User login and session-based preferences
- Live data from official API (if 2025 is published)
- Comparison tools (e.g., Verstappen vs Hamilton over time)
- Dark/light toggle & mobile responsiveness

---

## 👥 Team

- Spoorti Sidramappa Patil 
- Manasi Manoj Koppal
- Nesar Bhaskar Ganguli 

---

## 📩 Contact

Have questions? Reach out at: `nganguli@iu.edu; mkoppal@iu.edu; spsidram@iu.edu`

---

🏁 *Let the data race begin!*
