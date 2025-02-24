# Startup Success Forecasting Framework (SSFF)

The Startup Success Forecasting Framework (SSFF) is a pioneering approach designed to automate the evaluation of startup success potential. Leveraging a blend of traditional machine learning models, Large Language Models (LLMs), and real-time market data analysis, SSFF aims to transform the landscape of venture capital investment by providing deep, actionable insights into the viability of early-stage startups.

Link to Paper: https://arxiv.org/abs/2405.19456

## Project Structure

```
project_root/
│
├── models/
│   ├── neural_network.keras
│   ├── random_forest_classifier.joblib
│   └── trained_encoder_RF.joblib
│
├── EDA/
│   └── (exploratory data analysis scripts)
│
├── algorithms/
│   ├── embedding.py
│   ├── similarity.py
│   └── preprocessing.py
│
├── agents/
│   ├── base_agent.py
│   ├── market_agent.py
│   ├── founder_agent.py
│   ├── product_agent.py
│   ├── vc_scout_agent.py
│   └── integration_agent.py
│
├── utils/
│   ├── config.py
│   └── api_wrapper.py
│
├── main.py
└── README.md
```

## Environment Setup

To set up the environment for this project, follow these steps:

1. Ensure you have Python 3.7+ installed on your system.

2. Clone the repository:
   ```
   git clone https://github.com/your-username/Startup-Success-Forecasting-Framework.git
   cd Startup-Success-Forecasting-Framework
   ```

3. Create a virtual environment:
   ```
   python -m venv myenv
   ```

4. Activate the virtual environment:
   - On Windows:
     ```
     myenv\Scripts\activate
     ```
   - On macOS and Linux:
     ```
     source myenv/bin/activate
     ```

5. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

6. Create a `.env` file in the project root and add your API keys:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   SERPAPI_API_KEY=your_serpapi_api_key_here
   ```

7. To deactivate the virtual environment when you're done:
   ```
   deactivate
   ```

8. To run the project: streamlit run app.py


NEXT STEPS:
1. Add more data sources (e.g. Crunchbase, LinkedIn, Twitter, etc.)
2. Refit quantitative analysis for patent evalutation
3. Add sourcing agents and automate intake.
4. Connect IM generator to model following intake.

