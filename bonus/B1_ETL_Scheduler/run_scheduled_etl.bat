@echo off

cd /d D:\MutualFundAnalytics

python bonus\B1_ETL_Scheduler\scheduled_etl.py

exit /b %ERRORLEVEL%
