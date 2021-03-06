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


# In[2]:


#Analysis of Tumor treatment results

# Store the Mean Tumor Volume Data Grouped by Drug and Timepoint 
drug_mean_tumor_vol = data_combine[["Drug", "Timepoint","Tumor Volume (mm3)"]]
drug_mean_tumor_vol_grouped = drug_mean_tumor_vol.groupby(['Drug', 'Timepoint'])

# Convert to DataFrame
tumorvol = pd.DataFrame(drug_mean_tumor_vol_grouped["Tumor Volume (mm3)"].agg(np.mean))

# Preview DataFrame
tumorvol_indexed = tumorvol.reset_index()
tumorvol_indexed.head(100)


# In[3]:


# Store the Standard Error of Tumor Volumes Grouped by Drug and Timepoint
tumorvol = data_combine.groupby(['Drug', 'Timepoint']).sem()

# Convert to DataFrame
tumorvol_pd = pd.DataFrame(tumorvol[["Tumor Volume (mm3)"]])

# Preview DataFrame
tumorvol_sem = tumorvol_pd.reset_index()
tumorvol_sem.head()


# In[4]:


# Minor Data Munging to Re-Format the Data Frames
drug_vol = tumorvol_indexed.pivot(index="Timepoint", columns="Drug", values="Tumor Volume (mm3)")

# Preview that Reformatting worked
drug_vol.head() 


# In[5]:


# Generate the Plot (Accounting for percentages)
x_axis = np.arange(0, len(drug_vol), 1)
cap_vol = plt.errorbar(x_axis, drug_vol["Capomulin"], yerr=drug_vol["Capomulin"], linestyle = "-.",marker="o", color="red", label="Capomulin")
inf_vol = plt.errorbar(x_axis, drug_vol["Infubinol"], yerr=drug_vol["Infubinol"], linestyle = "--",marker="x", color="blue", label="Infubinol")
ket_vol = plt.errorbar(x_axis, drug_vol["Ketapril"], yerr=drug_vol["Ketapril"], linestyle = ":", marker="s", color="green", label="Ketapril")
pla_vol = plt.errorbar(x_axis, drug_vol["Placebo"], yerr=drug_vol["Placebo"], linestyle = "-.", marker="d", color="black", label="Placebo")
plt.legend(handles=[cap_vol, inf_vol, ket_vol, pla_vol], loc="upper left")
plt.title("Tumor Response to Treatment")
plt.ylabel("Tumor Volume (mm3)")
plt.xlabel("Time (Days)")
plt.grid()
plt.yticks(np.arange(0,200,20),("0", "35", "40", "45", "50","55","60","65","70"))
plt.xticks(np.arange(0,10,2),("0", "10", "20", "30", "40"))
# Save the Figure
plt.savefig('Tumor Response to Treatment.png')

# Show the Figure
plt.show()


# In[6]:


# Store the Mean Met. Site Data Grouped by Drug and Timepoint 
metastatic_mean = pd.DataFrame(data_combine.groupby(["Drug", "Timepoint"]).mean()["Metastatic Sites"])

# Preview DataFrame
metastatic_mean.head()


# In[7]:


# Store the Standard Error associated with Met. Sites Grouped by Drug and Timepoint 
metastatic_sem = pd.DataFrame(data_combine.groupby(["Drug", "Timepoint"]).sem()["Metastatic Sites"])

# Preview DataFrame
metastatic_sem.head()


# In[8]:


# Minor Data Munging to Re-Format the Data Frames
metastatic_vol = metastatic_mean.reset_index().pivot(index="Timepoint", columns="Drug", values="Metastatic Sites")
metastatic_sem_pivot = metastatic_sem.reset_index().pivot(index="Timepoint", columns="Drug", values="Metastatic Sites")

# Preview that Reformatting worked
metastatic_vol.head()


# In[9]:


# Generate the Plot (with Error Bars)
x_axis = np.arange(0, len(drug_vol), 1)
cap_met = plt.errorbar(x_axis, metastatic_vol["Capomulin"], yerr=metastatic_sem_pivot["Capomulin"], linestyle = "-",marker="o", color="red", label="Capomulin")
inf_met = plt.errorbar(x_axis, metastatic_vol["Infubinol"], yerr=metastatic_sem_pivot["Infubinol"], linestyle = "-",marker="x", color="blue", label="Infubinol")
ket_met = plt.errorbar(x_axis, metastatic_vol["Ketapril"], yerr=metastatic_sem_pivot["Ketapril"], linestyle = "-", marker="s", color="green", label="Ketapril")
pla_met = plt.errorbar(x_axis, metastatic_vol["Placebo"], yerr=metastatic_sem_pivot["Placebo"], linestyle = "-", marker="d", color="black", label="Placebo")
plt.legend(handles=[cap_met, inf_met, ket_met, pla_met], loc="best")
plt.title("Metastatic Spread During Treatment")
plt.ylabel("Metastatic Sites")
plt.xlabel("Treatment Duration (Days)")
plt.grid()
plt.xticks(np.arange(0,10,2),("0", "10", "20", "30", "40"))

# Save the Figure
plt.savefig('Metastatic Spread During Treatment.png')

# Show the Figure
plt.show()


# In[10]:


# Store the Count of Mice Grouped by Drug and Timepoint (W can pass any metric)
survival_data = data_combine.groupby(["Drug", "Timepoint"])

# Convert to DataFrame
survival_df = pd.DataFrame(survival_data["Mouse ID"].count())
survival_renamed = survival_df.rename(columns={"Mouse ID":"Mouse Count"})
survival_noindex = survival_renamed.reset_index()

# Preview DataFrame
survival_noindex.head()


# In[11]:


# Minor Data Munging to Re-Format the Data Frames
survival_rates = survival_noindex.pivot(index="Timepoint", columns="Drug", values="Mouse Count")

# Preview the Data Frame
survival_rates.head()


# In[12]:


# Generate the Plot (Accounting for percentages)
x_axis = np.arange(0, len(drug_vol), 1)
y_axis = [survival_rates["Capomulin"]*4, survival_rates["Infubinol"]*4, survival_rates["Ketapril"]*4, survival_rates["Placebo"]*4]
labels = ["Capomulin", "Infubinol", "Ketapril", "Placebo"]
colors = ["red", "blue", "green", "black"]
linestyles = ["-", "-", "-", "-"]
markers = ["o", "^", "s", "d"]
for i in range(len(y_axis)):
    plt.plot(x_axis, y_axis[i], color=colors[i], linestyle = linestyles[i], marker=markers[i], label=labels[i])
plt.legend()
plt.title("Survival During Treatment")
plt.ylabel("Survival Rate (%)")
plt.xlabel("Time (Days)")
plt.grid()
plt.xticks(np.arange(0,10,2),("0", "10", "20", "30", "40"))

# Save the Figure
plt.savefig('Survival During Treatment.png')

# Show the Figure
plt.show()


# In[13]:


# Calculate the percent changes for each drug
drug = [list(drug_vol["Capomulin"]), list(drug_vol["Ceftamin"]), list(drug_vol["Infubinol"]), 
        list(drug_vol["Ketapril"]), list(drug_vol["Naftisol"]), list(drug_vol["Placebo"]), 
        list(drug_vol["Propriva"]), list(drug_vol["Ramicane"]), list(drug_vol["Stelasyn"]), 
        list(drug_vol["Zoniferol"])]
drugname=["Capomulin", "Ceftamin", "Infubinol","Ketapril","Naftisol","Placebo",
          "Propriva","Ramicane", "Stelasyn", "Zoniferol"]
drug_change =[]
for x in range(len(drug)):
    percent_ = (drug[x][-1]-drug[x][0])/drug[x][0]*100
    drug_change.append(percent_)

# Display the data to confirm
df = {'Drug' : drugname, 'Percentage change' : drug_change }
pd.DataFrame(df)


# In[16]:


# Store all Relevant Percent Changes into a Tuple
tuple_percentage = tuple(zip(drugname, drug_change))

# Splice the data between passing and failing drugs
percent_df = pd.DataFrame({"Drug":drugname, "Percent Change":drug_change})
colors = []
label = ("Capomulin", "Infubinol", "Ketapril", "Placebo")
for change in range(0, len(drug_change)):
    if drug_change[change] > 0:
        colors.append("red")
    else:
        colors.append("green")
percent_df["Colors"] = colors
y_axis = [percent_df["Percent Change"][0],percent_df["Percent Change"][2],percent_df["Percent Change"][3],percent_df["Percent Change"][5]]
x_axis = np.arange(0,len(y_axis), 1)
color_axis = [percent_df["Colors"][0],percent_df["Colors"][2],percent_df["Colors"][3],percent_df["Colors"][5]]
labels = [percent_df["Percent Change"][0],percent_df["Percent Change"][2],percent_df["Percent Change"][3],percent_df["Percent Change"][5]]



plt.bar(x_axis, y_axis, color =color_axis, width = 1, edgecolor="black"  )
plt.title("Tumor Change Over 45 Day Treatment")
plt.ylabel("% Tumor Volume Change")
plt.grid()
plt.yticks(np.arange(-20,100,20),("-20", "0", "20", "40", "60"))
plt.xticks(np.arange(0,4,1),label)

# Save the Figure
plt.savefig('Tumor Change Over 45 Day Treatment.png')

# Show the Figure
plt.show()


# In[ ]:




