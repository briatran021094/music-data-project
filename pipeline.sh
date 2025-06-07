# pipeline.sh
echo "Running Full Pipeline..."
python3 run_master_music_analysis.py
echo "Data pipeline complete!"

echo "Launching Dashboard..."
streamlit run dashboard_app.py
