# 🌍 Climate Agent

An **AI-powered assistant** built with **Python, Chainlit, and the OpenAI Agents SDK**.  
The Climate Agent helps answer climate-related questions, provides CO₂ emission statistics, and suggests sustainable practices — all with safe, real-time responses.  

---

## 🚀 Features
- 📜 **Policy Advice** – Get recommendations on climate laws and agreements  
- 🌍 **CO₂ Statistics** – Retrieve emissions data for different locations  
- 🌱 **Green Practices** – Learn eco-friendly ways to reduce emissions  
- 🔒 **Input & Output Guardrails** – Ensure safe and reliable responses  
- ⚡ **Streaming Support** – Real-time responses powered by Chainlit  

---

## 📦 Installation

Clone the repository:
```bash
git clone https://github.com/HAJIRA-NASEEM/Climate-Agent.git
cd Climate-Agent
Install dependencies:

bash
Copy code
pip install chainlit openai python-dotenv pydantic
Set up environment variables:
Create a .env file in the root folder with your API key:

bash
Copy code
GEMINI_API_KEY=your_api_key_here
▶️ Usage
Run the Climate Agent locally:

bash
Copy code
chainlit run hello.py
📂 Project Structure
bash
Copy code
Climate-Agent/
│-- hello.py     # Main Climate Agent code
│-- .env         # Environment variables (not tracked in GitHub)
│-- README.md    # Project documentation
🤝 Contributing
Contributions are welcome! Please fork this repository and submit a pull request.

📜 License
This project is licensed under the MIT License.