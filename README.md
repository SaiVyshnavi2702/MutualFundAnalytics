\# Bluestock Mutual Fund Analytics



\## Project Overview



Bluestock Mutual Fund Analytics is a data-driven mutual fund analysis project covering fund performance, risk, investor behaviour, SIP trends, portfolio concentration, and interactive dashboard visualization.



The project uses historical mutual fund NAV data, fund master information, fund performance metrics, investor transactions, portfolio holdings, AUM data, SIP inflows, category-wise inflows, folio counts, and benchmark index data.



\## Objectives



\- Analyze mutual fund performance and historical returns.

\- Calculate risk-adjusted performance metrics such as Sharpe ratio, Alpha and Beta.

\- Analyze downside risk using VaR and CVaR.

\- Study investor transaction and SIP behaviour.

\- Analyze investor cohorts and SIP continuity.

\- Measure portfolio sector concentration using HHI.

\- Build a simple risk-based mutual fund recommender.

\- Develop an interactive Power BI dashboard.

\- Provide business insights and recommendations for mutual fund analysis.



\## Project Structure



```text

MutualFundAnalytics/

│

├── data/

│   ├── raw/

│   └── processed/

│

├── database/

│

├── notebooks/

│   ├── 01\_Data\_Loading\_and\_Exploration.ipynb

│   ├── 02\_NAV\_EDA.ipynb

│   ├── 03\_fund\_house\_aum\_EDA.ipynb

│   ├── 04\_sip\_analysis\_EDA.ipynb

│   ├── 05\_category\_inflow\_EDA.ipynb

│   ├── 06\_folio\_analysis\_EDA.ipynb

│   ├── 07\_fund\_performance\_EDA.ipynb

│   ├── 08\_Investors\_Transactions\_EDA.ipynb

│   ├── 09\_portfolio\_holdings\_analysis.ipynb

│   ├── 10\_Benchmark\_Indices\_EDA.ipynb

│   ├── 11\_AMFI\_Code\_Validation.ipynb

│   ├── 12\_fund\_master\_exploration.ipynb

│   ├── EDA\_Analysis.ipynb

│   ├── Performance\_Analytics.ipynb

│   └── Advanced\_Analytics.ipynb

│

├── reports/

│

├── sql/

│   ├── schema.sql

│   └── queries.sql

│

├── dashboard/

│

├── Bluestock\_MF\_Dashboard/

│

├── charts/

│

├── data\_ingestion.py

├── data\_cleaning.py

├── live\_nav\_fetch.py

├── recommender.py

├── run\_pipeline.py

├── load\_to\_sqlite.py

├── load\_csv\_to\_sqlite.py

├── create\_star\_schema.py

├── verify\_database.py

├── requirements.txt

└── README.md

