from evaluation_models import ModelSetting, SensitivityAnalysisResults
import os
import pandas as pd

def check_override_result(dataset: str, analysis: ModelSetting, result_path: str) -> pd.DataFrame:
    """
        Implement logic to check if results already exist for the given dataset and analysis parameters
    """
    saved_path = os.path.join(result_path, f"{dataset}_models_evaluation.csv")
    if os.path.exists(saved_path):
        df = pd.read_csv(saved_path)
    else:
        df = pd.DataFrame(columns=["model_name", "maximum_velocity", "pod_3", "far_3", "csi_3", "pod_5", "far_5", "csi_5",
                                   "object_consistency", "mean_duration", "linear_rmse", "optimal_tracking"])
    
    # Check if the specific analysis parameters already exist in the dataframe
    existing = df[
        (df["model_name"] == analysis.model_name) &
        (df["maximum_velocity"] == analysis.max_velocity)
    ]

    return existing


def save_results(dataset: str, analysis: ModelSetting, results: SensitivityAnalysisResults, result_path: str):
    # Implement logic to save the results to disk
    saved_path = os.path.join(result_path, f"{dataset}_models_evaluation.csv")
    if os.path.exists(saved_path):
        df = pd.read_csv(saved_path)
    else:
        df = pd.DataFrame(columns=["model_name", "maximum_velocity", "pod_3", "far_3", "csi_3", "pod_5", "far_5", "csi_5",
                                   "object_consistency", "mean_duration", "linear_rmse", "optimal_tracking"])

    new_df = pd.Series({
        "model_name": analysis.model_name,
        "maximum_velocity": analysis.max_velocity,
        "pod_3": results.pod_3,
        "far_3": results.far_3,
        "csi_3": results.csi_3,
        "pod_5": results.pod_5,
        "far_5": results.far_5,
        "csi_5": results.csi_5,
        "object_consistency": results.object_consistency,
        "mean_duration": results.mean_duration,
        "linear_rmse": results.linear_rmse,
        "optimal_tracking": results.optimal_tracking
    })

    # Override the existing rows if they exist
    existing = check_override_result(dataset, analysis, result_path)
    if existing is not None and not existing.empty:
        exiting_idx = existing.index[0]
        df.loc[exiting_idx] = new_df
    else:
        df.loc[len(df)] = new_df

    df.sort_values(by=["model_name", "maximum_velocity"], inplace=True)
        
    df.to_csv(saved_path, index=False)