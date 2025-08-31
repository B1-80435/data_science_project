# 🛒 Cart Abandonment Analysis & Dashboard  

## 📌 Overview  
This project explores **cart abandonment patterns in e-commerce** and provides actionable insights into user behavior, product performance, and recovery strategies.  

It includes:  
- 📊 A **Jupyter Notebook** with end-to-end data exploration, preprocessing, and insights.  
- 📈 An interactive **Streamlit dashboard** that visualizes KPIs, trends, and user/product-level insights in real time.  

---

## 🚀 Features  

### 🔍 Analysis (Jupyter Notebook)  
- Data cleaning and preprocessing  
- Cart vs. purchase event tracking  
- Cart abandonment segmentation (by product, category, brand, and user)  
- Time-based insights: peak abandonment hours, daily/weekly trends  
- Recovery rate estimation  

### 📊 Streamlit Dashboard  
- **KPI Cards**: Abandonment rate, recovery rate, repeat abandoners, etc.  
- **User Insights**: Top abandoners, engagement metrics  
- **Product Insights**: Most abandoned products, price bucket sensitivity  
- **Brand & Category Insights**: Top abandoned brands/categories  
- **Behavioral Insights**: Average carts before abandonment, time-to-abandon  
- **Time Insights**: Abandonments over time, hourly & weekday patterns  

---

## 🖼️ Dashboard Preview  
*(Insert screenshot here after running the app)*  

---

## ⚙️ Tech Stack  
- **Python**  
- **Pandas** / **NumPy**  
- **Matplotlib** / **Seaborn**  
- **Streamlit** (interactive dashboard)  
- **Google Sheets API (gspread)** for data loading  

---

## 📂 Project Structure  

```
📦 Cart-Abandonment-Analysis
│
├── Cart_Abandonment.ipynb     # Exploratory analysis & insights
├── stdb.py                    # Streamlit dashboard script
├── requirements.txt           # Dependencies
└── README.md                  # Project documentation
```

---

## ▶️ How to Run  

### 1️⃣ Clone the repo  
```bash
git clone https://github.com/<your-username>/cart-abandonment.git
cd cart-abandonment
```

### 2️⃣ Install dependencies  
```bash
pip install -r requirements.txt
```

### 3️⃣ Run Jupyter Notebook (for analysis)  
```bash
jupyter notebook Cart_Abandonment.ipynb
```

### 4️⃣ Run the Streamlit Dashboard  
```bash
streamlit run stdb.py
```

---

## 📊 Key Insights from Myntra Dataset (Sample)  
- 🚫 **30% customer engagement drop** due to cart abandonment.  
- 🔁 Repeat abandoners form a significant share of lost sales.  
- ⏰ Most abandonments happen during **evening hours**.  
- 🏷️ Specific brands and categories dominate abandonment patterns.  
- 💡 Recovery campaigns can boost re-engagement by **15–22%**.  

---

## ✅ Applications  
- Helps **product & marketing teams** identify drop-off points.  
- Provides insights for **personalized recovery campaigns**.  
- Optimizes **inventory planning & pricing strategies**.  

---

## 📌 Next Steps  
- Add predictive modeling for churn/abandonment likelihood  
- Integrate real-time alerts for high abandonment spikes  
- Experiment with recovery strategies (discounts, reminders)  

---

## 🤝 Contributing  
Pull requests are welcome! Feel free to fork this repo, improve the analysis, or add new features.  

---

## 📬 Contact  
👤 **Tanzeel Mansuri**  
📍 Bengaluru, India  
✉️ [tanzeel1705@gmail.com](mailto:tanzeel1705@gmail.com)  
🔗 [LinkedIn](https://www.linkedin.com/in/tanzeel-mansuri) | [GitHub](https://github.com/B1-80435)  
