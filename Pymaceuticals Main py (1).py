#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Dependencies and Setup
get_ipython().run_line_magic('matplotlib', 'inline')
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# Hide warning messages in notebook
import warnings
warnings.filterwarnings('ignore')

# File to Load (Remember to Change These)
mouse_drug_data_to_load = "02-Homework_05-Matplotlib_Instructions_Pymaceuticals_data_mouse_drug_data.csv"
clinical_trial_data_to_load = "02-Homework_05-Matplotlib_Instructions_Pymaceuticals_data_clinicaltrial_data.csv"

# Read the Mouse and Drug Data and the Clinical Trial Data
drug_data = pd.read_csv(mouse_drug_data_to_load)
clinical_data = pd.read_csv(clinical_trial_data_to_load)

# Combine the data into a single dataset
data_combine = pd.merge(drug_data, clinical_data, on="Mouse ID", how="outer")


# Display the data table for preview
data_combine.head()


# In[3]:


#Analysis of Tumor treatment results

# Store the Mean Tumor Volume Data Grouped by Drug and Timepoint 
drug_mean_tumor_vol = data_combine[["Drug", "Timepoint","Tumor Volume (mm3)"]]
drug_mean_tumor_vol_grouped = drug_mean_tumor_vol.groupby(['Drug', 'Timepoint'])

# Convert to DataFrame
tumorvol = pd.DataFrame(drug_mean_tumor_vol_grouped["Tumor Volume (mm3)"].agg(np.mean))

# Preview DataFrame
tumorvol_indexed = tumorvol.reset_index()
tumorvol_indexed.head(100)


# In[4]:


# Store the Standard Error of Tumor Volumes Grouped by Drug and Timepoint
tumorvol = data_combine.groupby(['Drug', 'Timepoint']).sem()

# Convert to DataFrame
tumorvol_pd = pd.DataFrame(tumorvol[["Tumor Volume (mm3)"]])

# Preview DataFrame
tumorvol_sem = tumorvol_pd.reset_index()
tumorvol_sem.head()


# In[ ]:




