#


from libs.back_test.main import Series, DataFrame
import pandas as pd

pd.to_DataFrame = DataFrame
pd.to_Series = Series
