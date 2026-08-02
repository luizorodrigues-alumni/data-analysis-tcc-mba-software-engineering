
from src.maturity_analysis import run_maturity_analysis_by_score, generate_profile_cross_analysis
from src.run_charts import run_all_charts


if __name__ == "__main__":
	# run_all_charts()
	df, _ = run_maturity_analysis_by_score()
	generate_profile_cross_analysis(df)
	
