import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

def plot_eda(data: pd.DataFrame,
             cutoff_time: int = 28,
             n_district: int = 11):
    
    """Helpers to visualize data
    Args: 
        data: pd.DataFrame needs visualization
        cutoff_time: days since last day when campaign starts
        n_district: int Number of district to be visualize
    Returns:
    """
    
    df = data.copy()
    sns.set_style("darkgrid")
    df["Treament_District_1"] = 0
    df["Treament_District_1"].iloc[-cutoff_time:] = 1
    length = df.shape[0]
    for i in range(1, n_district + 1):
        fig, axs = plt.subplots(3, 1, figsize = (15,12))
        sns.lineplot(x = range(df.shape[0]), y = f"District_{i}", 
                     data = df, color="blue", label=f"baseline", ax=axs[0])
        sns.lineplot(x = range(length-cutoff_time, length), y = f"District_{i}",
                     data = df.iloc[-cutoff_time:], color="red", label="after campaign Dist 1 launched", ax=axs[0])
        axs[0].set_title("Daily Consumption")
        sns.distplot(df[f"District_{i}"].iloc[:length-cutoff_time], color="blue", label=f'baseline', ax=axs[1])
        sns.distplot(df[f"District_{i}"].iloc[-cutoff_time:], color="red", label=f"after campaign Dist 1 lauched", ax=axs[1])
        axs[1].set_xlim([10000, 50000])

        sns.boxplot(df[f"District_{i}"].iloc[:length-cutoff_time], color="blue", ax=axs[2])
        sns.boxplot(df[f"District_{i}"].iloc[-cutoff_time:], color="red", ax=axs[2])
        axs[2].set_xlim([10000, 50000])
        axs[1].legend()
        axs[1].set_title("Consumption Distribution")
        fig.suptitle(f"Water Consumption in District {i}")
        plt.show()

class Preproc:
    
    """
    Decompose timeseries into weekly/yearly seasonality with Fourier series
    """
    
    def __init__(self):
        pass
        
    def __add_day_month__(self, 
                          X: pd.DataFrame) -> pd.DataFrame:
        """
        Add day and month to be prepared for yearly and weekly seasonality
        """
        X = X.copy(deep=True)
        # Add day columns
        if "Day" not in X:
            X["Day"] = list(range(0, X.shape[0]))
        if "Month" in X:
            return X
        
        X["Month"] = 1
        start = 0
        end = 31
        # Add month column
        for k in range(1, 13):
            start = end
            if k == 2:
                lenth_month = 28 # Feb
            elif k == 3:
                lenth_month = 31 # March
            elif k == 4:
                lenth_month = 30 # April
            elif k == 5:
                lenth_month = 31 # May
            elif k == 6:
                lenth_month = 30 # June
            elif k == 7:
                lenth_month = 31 # July
            elif k == 8:
                lenth_month = 31 # August
            elif k == 9:
                lenth_month = 30 # September
            elif k == 10:
                lenth_month = 31 # October
            elif k == 11:
                lenth_month = 30 # November
            else:
                lenth_month = 31 # December
            end = start + lenth_month
            X["Month"].iloc[start:end] = k
        
        return X
    
    def fourier_seasonality(self,
                            X: pd.DataFrame,
                            weekly: bool = True, 
                            yearly: bool = True,
                            order: int = 3) -> pd.DataFrame:
        """
        Decompose seasonality into Fourier series
        Args:
            X: pd.DataFrame
            weekly: bool
            yearly: bool
        Returns:
            pd.DataFrame
        """
        X = X.copy(deep=True)
        X = self.__add_day_month__(X)
        
        for n in range(1, order+1):
            # Weekly Seasonality
            X[f"sin_week_{n}n"] = np.sin(2*np.pi*n*X["Day"]/7)
            X[f"cos_week_{n}n"] = np.cos(2*np.pi*n*X["Day"]/7)
            # Yearly Seasonality
            X[f"sin_year_{n}n"] = np.sin(2*np.pi*n*X["Month"]/12)
            X[f"cos_year_{n}n"] = np.cos(2*np.pi*n*X["Month"]/12)
            
        return X
