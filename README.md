⚡ EV Smart Charging Scheduler (EcoCharge Dashboard)
📌 Problem Statement

With the rapid growth of electric vehicles (EVs), managing charging efficiently has become a critical challenge—especially for fleet operators.

Key problems include:

⚡ High electricity costs during peak hours
🚐 Multiple vehicles competing for charging resources
📊 Lack of data-driven decision making
⏱️ Inefficient charging schedules leading to energy wastage and higher bills

Fleet managers often charge vehicles without considering dynamic electricity pricing, resulting in unnecessary expenses and suboptimal energy usage.

💡 Solution

EcoCharge Dashboard is a smart EV charging optimization system that:

🔍 Analyzes electricity prices (hourly)
🧠 Calculates optimal charging schedules for each vehicle
⚡ Suggests cheapest time slots to charge
💰 Compares optimized vs normal charging cost
📊 Provides interactive dashboard & visual insights
🚀 Key Features
🚐 Fleet management system (add/remove vehicles dynamically)
⚡ Adjustable charging speed simulation
🕒 Smart scheduling using cheapest electricity hours
📉 Cost optimization & savings calculation
📊 Real-time visualization of price trends
🎯 “Best Time to Charge” recommendation
✨ Modern UI with animations (glassmorphism design)

⚙️ How It Works
User inputs:
  Current battery %
  Required battery %
  Charging speed
System:
  Calculates required charging hours
  Sorts electricity prices (lowest → highest)
  Assigns cheapest available time slots
Output:
  Optimal charging schedule
  Total optimized cost
  Comparison with normal charging
  Savings percentage

🛠️ Tech Stack
👨‍💻 Frontend
🎨 Streamlit UI
✨ Custom CSS (glassmorphism + animations)
⚙️ Backend
🐍 Python
📊 Data Handling
🐼 Pandas (data processing & scheduling logic)
📈 Visualization
📊 Streamlit built-in charts (area chart)

📦 Project Structure
📁 EV-Smart-Scheduler
│── app.py        # Main Streamlit application
│── README.md     # Project documentation

▶️ How to Run
pip install streamlit pandas
streamlit run app.py

📊 Example Output
🚐 Fleet overview table
⚡ Smart charging schedule
📉 Electricity price graph
💰 Cost comparison (optimized vs normal)
📈 Savings percentage

🌟 Future Enhancements
🔌 Real-time electricity price API integration
🤖 AI-based demand prediction
☀️ Solar energy optimization
📱 Mobile app version
🔄 Smart grid integration

👨‍💻 Team

Team Techies 🚀
