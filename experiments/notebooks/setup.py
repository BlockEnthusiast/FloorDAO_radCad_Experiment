import sys
import pandas as pd
from IPython import get_ipython

ipython = get_ipython()

# Append the root directory to Python path,
# this allows you to store notebooks in `experiments/notebooks/` sub-directory and access model Python modules
sys.path.append("../..")
sys.path.append("../../..")

# Configure Pandas to raise for chained assignment, rather than warn, so that we can fix the issue!
pd.options.mode.chained_assignment = 'raise'

# Set plotly as the default plotting backend for pandas
pd.options.plotting.backend = "plotly"
