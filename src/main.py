from maturity_analysis import run_maturity_analysis_by_score, generate_profile_cross_analysis
from qualitative_analysis import generate_qualitative_reports
from run_charts import run_all_likert_scale_charts

def main() -> None:
	# Generate Likert scale charts
	print("\n####### Generating Likert scale charts... #######\n")
	run_all_likert_scale_charts()

	# Run maturity analysis and generate cross-analysis charts
	print("\n####### Running maturity analysis and generating cross-analysis charts... #######\n")
	df, _ = run_maturity_analysis_by_score()
	generate_profile_cross_analysis(df=df)

	# Generate qualitative reports
	print("\n####### Generating qualitative reports... #######\n")
	generate_qualitative_reports(df=df)
	

if __name__ == "__main__":
	main()