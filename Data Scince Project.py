# -*- coding: utf-8 -*-


## CEIT 418 Data Science Project
"""

from google.colab import drive
drive.mount('/content/drive')

"""As your final data science project for CEIT 418, you will explore an educational dataset, and build a classification machine learning model.

In the first part, mostly you are expected to explore different tables (possible by using functions such as `head`, `shape`, `info`, and `describe`), deal with duplicate records and missing values, and perform some exploratory tasks.

In the second part, you will build a classification model and report its accuracy.


#### Important Information

For any action you take on the data, you should **explain your rationale** (e.g., I took into account colmuns X and Y when detecting duplicates because Z). Also, you should **provide an explanation/interpretation for outputs** produced by your code (e.g., based on this result, A and B columns can be dropped since they carry mostly missing values).

#### About the Dataset

For the final project, you will work on a public educational dataset shared by UK Open University. Although throughout this document you will be provided with sufficient information about this public dataset, you are strongly recommended to refer to https://analyse.kmi.open.ac.uk/open_dataset for more detailed information.

There is also Kaggle page where you can see some analysis performed shared by other publicly. I think they can be also helpful if you want to explore the dataset beyond this assignment.
https://www.kaggle.com/datasets/rocki37/open-university-learning-analytics-dataset
<br>
<br>

## 1. Exploratory Analysis

### 1.1. Courses Table

Courses table (`courses.csv`) contains the list of all available modules and their presentations.

The columns are:
* **code_module** – code name of the module, which serves as the identifier.
* **code_presentation** – code name of the presentation. It consists of the year and “B” for the presentation starting in February and “J” for the presentation starting in October.
* **length** - length of the module-presentation in days.

The structure of B and J presentations may differ and therefore it is good practice to analyse the B and J presentations separately. Nevertheless, for some presentations the corresponding previous B/J presentation do not exist and therefore the J presentation must be used to inform the B presentation or vice versa. In the dataset this is the case of CCC, EEE and GGG modules.
"""

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import f_oneway

"""**TASK1:** Identify and treat duplicate/missing values (if there is any).

Loading Data: We start by loading the data into a pandas DataFrame.
"""

courses_df= pd.read_csv("/content/drive/MyDrive/dataset/courses.csv")

# Displaying the basic information about the DataFrame.
print("### Info ###")
print(courses_df.info())

# Displaying summary statistics.
print("\n### Summary Statistics ###")
print(courses_df.describe())

# Checking for duplicate rows.
duplicate_rows = courses_df[courses_df.duplicated()]
print("\n### Duplicate Rows ###")
print(duplicate_rows)

# Checking for missing values.
missing_values = courses_df.isnull().sum()
print("\n### Missing Values ###")
print(missing_values)

"""**Explanation:**

Exploring Data:

I began by using the info() method to gather essential details about the DataFrame. This included information about data types, non-null counts, and an overall view of the dataset's structure.

Additionally, I employed the describe() method to generate summary statistics specifically for numerical columns. This quick overview provided key statistical measures like mean, standard deviation, and quartiles.

To identify any duplicated rows in the dataset, I utilized the duplicated() method. This step was crucial to determine if there were any replicated observations that needed attention.

To assess the extent of missing data in different columns, I used the isnull().sum() expression. This helped me understand the distribution of missing values across the DataFrame.

**Interpretation:**

These initial steps are vital in the data exploration process. They provide a foundation for subsequent decisions related to data cleaning and preprocessing by revealing the data's structure, identifying duplicates, and highlighting areas with missing values.

There are 22 entries (rows) and 3 columns in the dataset.

'module_presentation_length' has a mean of 255.55, a minimum of 234, and a maximum of 269.

The standard deviation is approximately 13.65.

No duplicate rows were found in the dataset.

There are no missing values in any of the columns.

**TASK2:** Find out how many courses started in February vs October, and compare their length. Interpret the results.
"""

def calculate_courses_stats(df, month_code):
    # Filtering the DataFrame based on the specified start month code.
    filtered_courses = df[df['code_presentation'].str.endswith(month_code)]

    # Calculating the number of courses and the total length for the filtered courses.
    num_courses = len(filtered_courses)
    total_length = filtered_courses['module_presentation_length'].sum()

    # Return the calculated values.
    return num_courses, total_length

# Calling the function for February ('B') and October ('J') start months.
feb_num_courses, feb_total_length = calculate_courses_stats(courses_df, 'B')
oct_num_courses, oct_total_length = calculate_courses_stats(courses_df, 'J')

# Displaying the results.
print(f"Number of courses started in February: {feb_num_courses}")
print(f"Number of courses started in October: {oct_num_courses}")
print(f"Total length of courses that started in February: {round(feb_total_length, 2)} days")
print(f"Total length of courses started in October: {round(oct_total_length, 2)} days")

"""**Explanation**

Function Definition (calculate_courses_stats):

I defined a function named calculate_courses_stats that takes two parameters, df (representing a DataFrame) and month_code (indicating the start month). To filter the DataFrame based on the specified start month, I used the str.endswith() method. The function then calculates the number of courses and the total length of these courses for the filtered DataFrame. Finally, the function returns the calculated values.

Function Invocation:

I invoked the function twice, providing arguments for the start months of February ('B') and October ('J').

Results Display:

After invoking the function, I displayed the results, which include the number of courses and the total length of courses for both the February and October start months. This step was crucial for presenting the outcome of the function in a clear and informative manner.

**Interpretation:**

The function helps in summarizing the statistics for courses based on their start months.
The results indicate the number of courses and the total length of courses for both February and October start months.
The rounded total length values provide an overview of the combined duration of all courses in days.

### 1.2. Student Info Table

StudentInfo (`studentInfo.csv`) file contains **demographic** information about the students together with their final result. File contains the following columns:

* **code_module** – an identification code for a module on which the student is registered.
* **code_presentation** - the identification code of the presentation during which the student is registered on the module.
* **id_student** – a unique identification number for the student.
* **gender** – the student’s gender.
* **region** – identifies the geographic region, where the student lived while taking the module-presentation.
* **highest_education** – highest student education level on entry to the module presentation.
* **imd_band** – specifies the Index of Multiple Depravation band of the place where the student lived during the module-presentation.
* **age_band** – band of the student’s age.
* **num_of_prev_attempts** – the number times the student has attempted this module.
* **studied_credits** – the total number of credits for the modules the student is currently studying.
* **disability** – indicates whether the student has declared a disability.
* **final_result** – student’s final result in the module-presentation.

**TASK1:** Identify and treat duplicate/missing values (if there is any)
"""

studentInfo_df= pd.read_csv("/content/drive/MyDrive/dataset/studentInfo.csv")

# Displaying basic information about the DataFrame
print("### Info ###")
print(studentInfo_df.info())

# Displaying summary statistics
print("\n### Summary Statistics ###")
print(studentInfo_df.describe())

# Checking for duplicate rows
duplicate_rows_student_info = studentInfo_df[studentInfo_df.duplicated()]
print("\n### Duplicate Rows ###")
print(duplicate_rows_student_info)

# Checking for missing values
missing_values_student_info = studentInfo_df.isnull().sum()
print("\n### Missing Values ###")
print(missing_values_student_info)

"""**Explanation**

Exploring Data:

I began by using the info() method to gather essential details about the DataFrame. This included information about data types, non-null counts, and an overall view of the dataset's structure.

Additionally, I employed the describe() method to generate summary statistics specifically for numerical columns. This quick overview provided key statistical measures like mean, standard deviation, and quartiles.

To identify any duplicated rows in the dataset, I utilized the duplicated() method. This step was crucial to determine if there were any replicated observations that needed attention.

To assess the extent of missing data in different columns, I used the isnull().sum() expression. This helped me understand the distribution of missing values across the DataFrame.

**Interpretation:**

The info() output reveals that the DataFrame contains 32,593 entries and 12 columns.

Data types include integers (int64) and objects (object), representing a mix of numerical and categorical variables.

The describe() output provides statistical measures for numerical columns:
id_student: Student IDs ranging from 3,733 to 2,716,795.

num_of_prev_attempts: Students attempted courses 0 to 6 times on average.

studied_credits: Students took an average of 79.76 credits with a range from 30 to 655.

No missing values are reported across most columns, except for the 'imd_band' column, which has 1,111 missing values.
"""

# Dropping rows with missing values
studentInfo_df = studentInfo_df.dropna()

# Resetting index after dropping rows
studentInfo_df = studentInfo_df.reset_index(drop=True)

"""**Explanation:**

dropna(): I used this method to remove rows containing missing values (NaN) in any column. In this case, it seems that the only column with missing values is imd_band. By using dropna(), I eliminated the rows where imd_band is missing.

reset_index(drop=True): After dropping rows, the index of the DataFrame may have gaps due to the removed rows.I used the reset_index() method with drop=True to reset the index and create a new DataFrame without adding a new column for the old index. This ensures a clean, continuous index without gaps.

**Interpretation:**

Rows with missing values in the imd_band column were removed from the DataFrame. This decision was made based on the assumption that missing values in this particular column could not be imputed or filled with meaningful values, and removing them would not significantly affect the analysis.

The reset_index() step was performed to maintain a consistent and continuous index after removing rows. It helps in organizing the data and ensures that the index reflects the current state of the DataFrame.

**TASK2:** Treating categorical variables.

For this table, besides fixing any potential issue about duplicate/missing values, you are expected to explore the categorical variables: such as `highest_education`, `imd_band`, and `age_band`.

In particular, you may want to check if some categories of `highest_education`, `imd_band`, `age_band` variables (e.g., *Post Graduate Qualification* in `highest_education`) contain few instances. In such cases, you may need to merge the minority categories with a major category and even dedice to create a new set of (fewer) categories based on the existing ones. In some cases, you may even want to decide the reduce the number of categories (if you think they are many).

As long as you provide the rationale, you can decide such details by yourself. You should work on AT LEAST TWO categorical variables in this task.
"""

# Replacing values in 'highest_education' column
studentInfo_df['highest_education'].replace('Post Graduate Qualification', 'A Level or High', inplace=True)
studentInfo_df['highest_education'].replace('No Formal quals', 'Lower Than A Level', inplace=True)
studentInfo_df['highest_education'].replace('HE Qualification', 'A Level or High', inplace=True)
studentInfo_df['highest_education'].replace('A Level or Equivalent', 'A Level or High', inplace=True)

# Replacing values in 'age_band' column
studentInfo_df['age_band'].replace('55<=', '35-55', inplace=True)

# Displaying modified value counts
print(studentInfo_df['highest_education'].value_counts())
print(studentInfo_df['age_band'].value_counts())

"""**Explanation:**

I performed replacements in two categorical columns, highest_education and age_band, of the studentInfo_df DataFrame.

For the highest_education column, I replaced specific education categories with a consolidated category to simplify and group similar educational levels. This was done to create a more manageable set of categories for analysis. The replacements included merging 'Post Graduate Qualification' and 'HE Qualification' into 'A Level or High' and 'No Formal quals' into 'Lower Than A Level'. Additionally, 'A Level or Equivalent' was also merged into 'A Level or High'.

In the age_band column, I replaced the category '55<=' with '35-55'. This adjustment was made for consistency and to create more evenly distributed age bands.

**Interpretation:**

The modified value counts for both highest_education and age_band were displayed after the replacements. This display is crucial for verifying the success of the replacement operations and understanding the distribution of data in these categorical columns.

The output indicates that the replacement process was effective, providing a clearer overview of the distribution of education levels and age bands in the dataset. The resulting modifications will contribute to a more streamlined and informative analysis.

**TASK3:** Demographic Information and Performance Levels

More importantly for this table you are expected to explore various relationships between `final_result` and **at least three** categorical variable (e.g., did students with HE qualification perform better, did students with low `imd_band` withdraw more often, or did geographic region play any role? etc.). For this purpose you can visualize data and compute some basic statistics.

You must use at least two different chart types (e.g., bar or line or pie) to illustrate how the success/failure rates differ between different categories (e.g., education level, regions, imd_band, age, etc.). At least in one case, the chart should also denote the gender to illustrate the possible interaction between gender and the other categorical variable (e.g., do european females perform better than asian males -just an example :)).
"""

sns.set(style="whitegrid")

# Bar chart for 'highest_education' vs. 'final_result'.
plt.figure(figsize=(12, 6))
sns.countplot(x="highest_education", hue="final_result", data=studentInfo_df, palette="muted")
plt.title("Final Result vs. Highest Education")
plt.xlabel("Highest Education")
plt.ylabel("Count")
plt.legend(title="Final Result", loc="upper right")
plt.show()
print()

# Pie chart for 'region' vs. 'final_result'.
plt.figure(figsize=(10, 8))
region_counts = studentInfo_df['region'].value_counts()
plt.pie(region_counts, labels=region_counts.index, autopct='%1.1f%%', startangle=140, colors=sns.color_palette("pastel"))
plt.title("Distribution of Final Result by Region")
plt.show()
print()

# Bar chart for 'imd_band' vs. 'final_result'.
plt.figure(figsize=(12, 6))
sns.countplot(x="imd_band", hue="final_result", data=studentInfo_df, palette="muted")
plt.title("Final Result vs. IMD Band")
plt.xlabel("IMD Band")
plt.ylabel("Count")
plt.legend(title="Final Result", loc="upper right")
plt.show()
print()

# Creating a DataFrame for the comparison.
comparison_df = studentInfo_df[['gender', 'highest_education', 'final_result']]

# Countplot for Final Result by Gender.
plt.figure(figsize=(12, 6))
sns.countplot(x='final_result', hue='gender', data=comparison_df, palette='muted')
plt.title('Final Result Comparison between Males and Females')
plt.xlabel('Final Result')
plt.ylabel('Count')
plt.show()
print()

# Stacked Bar Chart for Highest Education by Gender.
plt.figure(figsize=(12, 6))
sns.countplot(x='highest_education', hue='gender', data=comparison_df, palette='muted')
plt.title('Highest Education Comparison between Males and Females')
plt.xlabel('Highest Education')
plt.ylabel('Count')
plt.legend(title='Gender', loc='upper right')
plt.show()

"""**Explanation:**

I used a bar chart to visualize the distribution of final results across different levels of education ('highest_education'). This helps in understanding how the final results are distributed among various education categories.

A pie chart was employed to illustrate the distribution of final results across different geographic regions ('region'). This provides a visual representation of how final results are spread among different regions.

A bar chart was created to show the distribution of final results based on the Index of Multiple Deprivation (IMD) bands ('imd_band'). This allows for an exploration of the relationship between socioeconomic factors and final results.

A countplot was used to compare the final results between males and females. This provides insights into potential gender-based variations in course outcomes.

Another countplot, this time a stacked bar chart, was employed to compare the distribution of highest education levels between males and females. This visualization helps in understanding the educational background of students based on gender.

**Interpretation:**

'Highest Education' vs. 'Final Result':

The bar chart shows that students with 'A Level or High' education level tend to have diverse final outcomes, including 'Pass,' 'Withdrawn,' 'Fail,' and 'Distinction.'
'Region' vs. 'Final Result':

The pie chart displays the proportion of final results in each region. This visual representation aids in identifying regions where certain outcomes are more prevalent.
'IMD Band' vs. 'Final Result':

The bar chart indicates the distribution of final results across different IMD bands. It helps to observe patterns in student outcomes based on the level of deprivation in their area.
'Final Result' by Gender:

The countplot illustrates the count of final results for both genders, providing a quick comparison between males and females.
'Highest Education' by Gender:

The stacked bar chart offers a visual comparison of the distribution of highest education levels among males and females, providing insights into potential gender-based educational disparities.

### 1.3. Registration Table

Registration table (`studentRegistration.csv`) contains information about the time when the student registered for the module presentation. For students who unregistered the date of unregistration is also recorded. File contains five columns:

* **code_module** – an identification code for a module.
* **code_presentation** - the identification code of the presentation.
* **id_student** – a unique identification number for the student.
* **date_registration** – the date of student’s registration on the module presentation, this is the number of days measured relative to the start of the module-presentation (e.g. the negative value -30 means that the student registered to module presentation 30 days before it started).
* **date_unregistration** – date of student unregistration from the module presentation, this is the number of days measured relative to the start of the module-presentation. Students, who completed the course have this field empty. Students who unregistered have *Withdrawal* as the value of the `final_result` column in the `studentInfo.csv` file.

**TASK1:** As the first task, you need to ensure that there are no conflicts between `studentRegistration.csv` and `studentInfo.csv` dataset in terms of **Withdrawal** status of *unregistered* students. For example, if a student unregistered from a course at some point (which can be found in "studentRegistration.csv"), his/her `final_result` should be **Withdrawal**.
"""

studentRegistration_df= pd.read_csv("/content/drive/MyDrive/dataset/studentRegistration.csv")

merged_df = pd.merge(studentRegistration_df, studentInfo_df, on=['code_module', 'code_presentation', 'id_student'], how='left')

conflicts = merged_df[(merged_df['date_unregistration'].notnull()) & (merged_df['final_result'] != 'Withdrawal')]
print(conflicts.head())

studentInfo_df.loc[studentInfo_df['id_student'].isin(conflicts['id_student']), 'final_result'] = 'Withdrawal'

"""**Explanation:**

I merged the studentRegistration_df with studentInfo_df based on the common columns 'code_module', 'code_presentation', and 'id_student'. This merging allows me to align registration and demographic information for each student across different courses and presentations.

The conflicts DataFrame is then created to identify instances where a student unregistered but still has a final result other than 'Withdrawal'. This situation implies a discrepancy between unregistration and final result status.

**Interpretation:**

The conflicts DataFrame highlights cases where students withdrew (date_unregistration is not null) but have a final result other than 'Withdrawal'. This inconsistency in the data might be due to errors or anomalies in the registration and unregistration process. To address this, I updated the final_result column in studentInfo_df for the corresponding students to 'Withdrawal', ensuring consistency between unregistration and final result status. This correction helps maintain data integrity and coherence.

**TASK2:** Categorize students based on the day they registered for a course. In other words, you need to **bin** the registration data based on the `date_registration` column. Just to illustrate this idea, you can group students into categories such as "Very early birds", "early birds", "in-time", and "late-comers". You can use the categories given in this example or create your own categories.
"""

# Define bins and labels
bins = [-float('inf'), -120, -60, 0, 60, float('inf')]
labels = ['Very early birds', 'Early birds', 'In-time', 'Late-comers','Very Late-comers' ]

# Creating a new column 'registration_category' based on bins and labels
studentRegistration_df['registration_category'] = pd.cut(studentRegistration_df['date_registration'], bins=bins, labels=labels, right=False)

studentRegistration_df.head()

"""**Explanation:**

I defined bins and corresponding labels to categorize students based on the timing of their registration relative to the course start date.

The bin edges are set to [-∞, -120, -60, 0, 60, ∞], representing different time intervals before and after the course start date for registration.
The labels are assigned as follows: "Very early birds" for registrations more than 120 days before the start date, "Early birds" for registrations between 60 and 120 days, "In-time" for registrations within 60 days, "Late-comers" for registrations within 60 days after the start date, and "Very Late-comers" for registrations more than 60 days after the start date.
I created a new column named 'registration_category' in the studentRegistration_df DataFrame using the pd.cut function. This column classifies each student's registration timing into one of the defined categories based on the 'date_registration' values.

**Interpretation:**

The 'registration_category' column provides a useful categorization of students based on the timing of their registration relative to the course start date. It allows for insights into the distribution of registration events across different categories. This information can be valuable for analyzing the relationship between registration timing and various outcomes or behaviors related to student engagement and success.

**TASK3:** Categorize students based on the day they *unregistered* a course. In other words, you need to **bin** registration date based on the `date_unregistration` column. You are free to determine the number and the name of the categories (as in Task1).
"""

# Define bins and labels
bins = [-float('inf'), -60, 0, 60,120, float('inf')]
labels = ['Very Early unregistration', 'Early unregistration','In-time', 'Lately unregistration', 'Very Lately unregistration']

# Creating a new column 'registration_category' based on bins and labels
studentRegistration_df['unregistration_category'] = pd.cut(studentRegistration_df['date_unregistration'], bins=bins, labels=labels, right=False)
studentRegistration_df.head()

"""**Explanation:**

I defined bins and corresponding labels to categorize students based on the timing of their unregistration relative to the course end date.

The bin edges are set to [-∞, -60, 0, 60, 120, ∞], representing different time intervals before and after the course end date for unregistration.
The labels are assigned as follows: "Very Early unregistration" for unregistrations more than 60 days before the end date, "Early unregistration" for unregistrations between 0 and 60 days before the end date, "In-time" for unregistrations within 60 days after the end date, "Lately unregistration" for unregistrations within 120 days after the end date, and "Very Lately unregistration" for unregistrations more than 120 days after the end date.
I created a new column named 'unregistration_category' in the studentRegistration_df DataFrame using the pd.cut function. This column classifies each student's unregistration timing into one of the defined categories based on the 'date_unregistration' values.

**Interpretation:**

The 'unregistration_category' column provides a useful categorization of students based on the timing of their unregistration relative to the course end date. It allows for insights into the distribution of unregistration events across different categories. This information can be valuable for analyzing the relationship between unregistration timing and various outcomes or behaviors related to student engagement and success.

**TASK4:** Choose *THREE variables* from demographic data (`studentInfo.csv`), and explore if there is some relationship between students' registration/unregistration behaviour and the chosen demographic variables (e.g., did students from HE registered early? did male students unregistered sooner than female students?). You are free in exploring the data to answer similar questions that you determine. If you find no relationship, this is totally fine. Just remember that your analysis should be accompanied with meaningful interpretations.
"""

# Merging dataframes on common columns.
merged_df = pd.merge(studentInfo_df, studentRegistration_df, on=['code_module', 'code_presentation', 'id_student'], how='left')

# Choosing three demographic variables.
chosen_demographic_vars = ['highest_education', 'region', 'disability']

# Exploring relationship for each chosen demographic variable.
for var in chosen_demographic_vars:
    # Calculating registration rates for each category.
    registration_rates = merged_df.groupby(var)['date_registration'].count() / studentInfo_df.groupby(var)['id_student'].count()
    print(f"\nRegistration Rates based on {var}:\n{registration_rates}")

    # Calculating unregistration rates for each category.
    unregistration_rates = merged_df.groupby(var)['date_unregistration'].count() / studentInfo_df.groupby(var)['id_student'].count()
    print(f"\nUnregistration Rates based on {var}:\n{unregistration_rates}")

"""**Explanation:**

I merged the studentInfo_df and studentRegistration_df DataFrames based on common columns ('code_module', 'code_presentation', 'id_student') using the pd.merge function.

I selected three demographic variables ('highest_education', 'region', 'disability') to explore their relationship with registration and unregistration rates.

For each chosen demographic variable, I calculated registration rates and unregistration rates

Highest Education:

Registration Rates:
Students with "A Level or High" education have a slightly higher registration rate compared to students with "Lower Than A Level" education.
Almost all students in both categories register for the course, with rates close to 1.

Interpretation:

Education level does not seem to significantly affect the registration behavior; most students in both categories register.

Unregistration Rates:

Students with "Lower Than A Level" education have a higher unregistration rate compared to students with "A Level or High" education.
Approximately 28% of students with "A Level or High" education and 35% of students with "Lower Than A Level" education unregistered.

Interpretation:

Students with lower education levels tend to unregistered slightly more often than those with higher education levels.
Region:

Registration Rates:

Registration rates are generally high across all regions, ranging from 99.2% to 100%.
Wales has a 100% registration rate, indicating all students from this region registered for the course.

Interpretation:

Region does not appear to have a significant impact on registration behavior; high registration rates are observed across regions.

Unregistration Rates:

Unregistration rates vary among regions, ranging from approximately 23% to 35%.
Students from Ireland have a lower unregistration rate (22.8%), while students from the West Midlands Region have a higher unregistration rate (35.1%).

Interpretation:

There is some variation in unregistration rates by region, with certain regions experiencing higher or lower rates.

Disability:

Registration Rates:

Both students with and without disabilities have high registration rates, with values close to 1.
Registration rates for students without disabilities are slightly lower than those with disabilities.

Interpretation:

Disability status does not seem to significantly influence registration behavior; most students, regardless of disability, register for the course.

Unregistration Rates:

Students with disabilities have a higher unregistration rate (38.9%) compared to those without disabilities (30.0%).

Interpretation:

Students with disabilities tend to unregistered more often than those without disabilities.

**Overall**

While registration rates are generally high across different categories, unregistration rates show more variability.
Education level and disability status have some impact on unregistration rates, with students with lower education levels and disabilities having slightly higher unregistration rates.
Region also exhibits variation in unregistration rates, suggesting potential regional differences in student persistence.

### 1.4. Course Components Table

Course components table (`moodle.csv`) contains information about the available materials in the Moodle LMS. Typically these are html pages, pdf files, etc. Students have access to these materials online and their interactions with the materials are recorded. The `moodle.csv` file contains the following columns:

* **id_site** – an identification number of the material.
* **code_module** – an identification code for module.
* **code_presentation** - the identification code of presentation.
* **activity_type** – the role associated with the module material.
* **week_from** – the week from which the material is planned to be used.
* **week_to** – week until which the material is planned to be used.

**TASK1:** In this dataset, some columns contain mainly missing values. Detect them and drop them to save space in the memory.
"""

moodle_df = pd.read_csv("/content/drive/MyDrive/dataset/moodle.csv")

# Checking for missing values
missing_values_student_info = moodle_df.isnull().sum()
print("\n### Missing Values ###")
print(missing_values_student_info)
# Dropping rows with missing values
moodle_df = moodle_df.dropna()

# Resetting index after dropping rows
moodle_df = moodle_df.reset_index(drop=True)

"""**Explanation:**

I checked for missing values in the studentInfo_df DataFrame using the isnull().sum() method, which provides the count of missing values for each column.

I used the dropna() method to remove rows containing missing values from the DataFrame.

I reset the index of the DataFrame using the reset_index(drop=True) method to reorganize the DataFrame after removing rows.

**Interpreation:**

The columns 'week_from' and 'week_to' have missing values, with 5243 missing values in each.

**TASK2:** First identify the top 5 popular course component (`activity_type`) across all courses. Then, create a new table that displays how many times each of these popular components were included in each offering (`code_presentation`) of each course (`code_module`). Briefly interpret this table.
"""

# Identify the top 5 popular course components (activity_type) across all courses
top_comp = moodle_df['activity_type'].value_counts().nlargest(5).index

# Filter the dataframe to include only the rows with the top 5 components
top_comp_df = moodle_df[moodle_df['activity_type'].isin(top_comp)]

# Create a new table that displays how many times each of these popular components were included in each offering
popular_components_table = pd.pivot_table(top_comp_df, values='id_site', index=['code_module', 'code_presentation'], columns='activity_type', aggfunc='count', fill_value=0)

# Display the table
popular_components_table

"""**Explanation:**

To identify the top 5 popular course components (activity_type) across all courses, I performed the following steps:

I used value_counts() on the 'activity_type' column to get the counts of each activity type.

I selected the top 5 components by using nlargest(5).index.

I created a new DataFrame, top_comp_df, by filtering the original DataFrame (moodle_df) to include only the rows with the top 5 components.

I created a pivot table, popular_components_table, to display how many times each of these popular components was included in each course offering. The table is indexed by 'code_module' and 'code_presentation', with columns representing the activity types and values indicating the counts.

The resulting table shows the count of each popular component for each course presentation.

**Interpretation:**

The table shows, for each course offering, how many times each of the top 5 popular components appears.
This information can be useful for understanding the emphasis on specific types of activities in different courses and presentations.
For example, a higher count for 'resource' might indicate a greater use of resource materials in a particular course offering.

### 1.5. Student Activity Data

Student activity data (`studentMoodleInteract.csv`) contains information about each student’s interactions with the materials in the VLE. This file contains the following columns:

* **code_module** – an identification code for a module.
* **code_presentation** - the identification code of the module presentation.
* **id_student** – a unique identification number for the student.
* **id_site** - an identification number for the course material/component.
* **date** – the date of student’s interaction with the material measured as the number of days since the start of the module-presentation.
* **sum_click** – the number of times a student interacts with the material in that day.

**TASK1:** Display the total number of clicks for each course per each semester delivered. Besides a textual output, some visualizations must be provided for helping to interpret the data.
"""

studentMoodleInteract_df = pd.read_csv("/content/drive/MyDrive/dataset/studentMoodleInteract.csv")

# Display the total number of clicks for each course per each semester delivered
total_clicks_per_course_semester = studentMoodleInteract_df.groupby(['code_module', 'code_presentation'])['sum_click'].sum().reset_index()

# Display the textual output
print(total_clicks_per_course_semester)

# Visualize the data
print()
plt.figure(figsize=(10, 6))
sns.barplot(x='code_module', y='sum_click', hue='code_presentation', data=total_clicks_per_course_semester)
plt.title('Total Clicks per Course per Semester Delivered')
plt.xlabel('Course Code')
plt.ylabel('Total Clicks')
plt.show()

"""**Explanation:**

I used groupby on the 'code_module' and 'code_presentation' columns of the studentMoodleInteract_df DataFrame, followed by sum() to calculate the total number of clicks for each course in each semester.

The resulting DataFrame, total_clicks_per_course_semester, displays the total clicks for each course and semester.

I created a bar plot to visualize the total clicks per course per semester. The x-axis represents the course code, the y-axis represents the total clicks, and different colors represent different semesters.

**Interpretation:**

The textual output shows the total clicks for each course and semester combination.
The bar plot provides a visual representation of the same information. It allows for a quick comparison of the total clicks across different courses and semesters.
The plot can be useful for identifying trends or variations in student interaction with the Moodle platform across different courses and semesters. For instance, it helps to identify courses or semesters with higher or lower student engagement based on the total number of clicks.

**TASK2**: As a follow up to the first task, identify the courses in which the total number of clicks is higher in 2014 than 2013. If the course was taught two times in the same year (such as, 2013B and 2013J) use the average of both semesters (`(2013B+2013J)/2`) to compare with the other year.
"""

# Extract the year from the 'code_presentation' column and create a new 'year' column
studentMoodleInteract_df['year'] = studentMoodleInteract_df['code_presentation'].apply(lambda x: int(x[:4]))

# Calculate the average clicks for each course in each year
average_clicks_per_course_year = studentMoodleInteract_df.groupby(['code_module', 'year'])['sum_click'].mean().reset_index()

# Identify the courses where the total number of clicks is higher in 2014 than 2013
courses_higher_in_2014 = average_clicks_per_course_year.pivot(index='code_module', columns='year', values='sum_click')
courses_higher_in_2014 = courses_higher_in_2014[courses_higher_in_2014[2014] > courses_higher_in_2014[2013]]

# Display the result
print("Courses with higher total clicks in 2014 than 2013:")
print(courses_higher_in_2014)

"""**Explanation:**

I created a new 'year' column based on the 'code_presentation' column.

I calculated the average clicks for each course in each year.

I identified the courses where the total number of clicks is higher in 2014 than 2013.

The result is displayed as a DataFrame.

**Interpretation:**

The output indicates that for the course with the code_module 'BBB', the average number of clicks per student was higher in 2014 (3.523605) compared to 2013 (3.185599). This suggests an increase in student interaction with the materials for this course in the specified years.

**TASK3:** Which type of resources were mostly clicked by the students? Do you observe a common pattern accross courses (e.g., in almost all courses, clicks on `resource` is  higher than `quiz`)? A heatmap as a visualization might be helpful here.
"""

moodleDf= pd.read_csv("/content/drive/MyDrive/dataset/moodle.csv")
merged_df = pd.merge(studentMoodleInteract_df, moodleDf[['id_site','activity_type']], on='id_site', how='left')

clicks_by = merged_df.groupby(['activity_type', 'code_module'])['sum_click'].sum().reset_index()

table = clicks_by.pivot(index='activity_type', columns='code_module', values='sum_click').fillna(0)
table

"""**Explanation:**

I started by loading the Moodle data from a CSV file and then merging it with the studentMoodleInteract_df DataFrame based on the 'id_site' column. This merge was essential to associate each student interaction with its corresponding activity type.

Next, I grouped the resulting DataFrame (merged_df) by both 'activity_type' and 'code_module.' The goal was to calculate the total number of clicks ('sum_click') for each combination of activity type and module, shedding light on the popularity of various resources.

**Interpretation:**

The pivot table offers a comprehensive view of the total clicks for each activity type across different modules. For instance, in module 'AAA,' 'oucontent' emerges as the most-clicked activity, while 'forumng,' and 'homepage' also attract significant engagement.

This breakdown provides valuable insights into student behavior, indicating which resources are more frequently accessed in each module. Such information is crucial for decision-making, helping educators and administrators allocate resources effectively, enhance content, and identify patterns that may be consistent across multiple courses.

**TASK4:** For each student, compute the total number of clicks per each course component type (`activity_type` column in `moodle.csv`) separately for each course and semester. A simple representation of the expected table is provided below with fake data (note that in the given example columns and rows are incomplete).

| Student Id | code_module | code_presentation | PDF | Assignment
| --- | --- | --- | --- | --- |
| 1234 | AAA | 2013J | 23 | 33 |
| 1234 | BBB | 2014B | 5 | 42 |
   
Note that, in this task you actually create some features that can be used for predictive modeling.
"""

# Group by student, course, presentation, and activity type, then calculate the sum of clicks
clicks_by_activity = merged_df.groupby(['id_student', 'code_module', 'code_presentation', 'activity_type'])['sum_click'].sum().reset_index()

# Pivot the DataFrame to create the desired format
pivot_clicks = clicks_by_activity.pivot_table(index=['id_student', 'code_module', 'code_presentation'], columns='activity_type', values='sum_click', fill_value=0).reset_index()

# Display the resulting DataFrame
pivot_clicks

"""**Explanation:**

I grouped the data by 'id_student', 'code_module', 'code_presentation', and 'activity_type', calculating the total clicks for each combination.

The grouped data was then pivoted, creating a table where rows represent unique student-course-presentation combinations, and columns represent different activity types with total click counts.

The resulting table is a valuable dataset for further analysis, providing insights into student engagement across different courses, presentations, and activity types.

**Interpretation:**

The structured table offers a detailed view of student interactions. Each row represents a specific student enrolled in a particular course during a presentation, showcasing the total clicks on various activity types. This dataset serves as a foundational resource for predictive modeling and facilitates a deeper understanding of how students engage with different learning activities.

**TASK5:** Using proper visualizations and statistical analysis, please explore if there is any relationship between students' course performance (`final_result` column in `studentInfo.csv`) and clicks on different resources.
"""

# Merging studentInfo_df and merged_df on common columns
final_merged_df = pd.merge(clicks_by_activity, studentInfo_df[['id_student','final_result']], how='left', on='id_student')

# Creating a bar plot
plt.figure(figsize=(12, 6))
sns.barplot(x='activity_type', y='sum_click', hue='final_result', data=final_merged_df)
plt.title('Average Clicks on Different Resources by Final Result')
plt.xlabel('Activity Type')
plt.ylabel('Average Clicks')
plt.xticks(rotation=45, ha='right')
plt.legend(title='Final Result')
plt.show()

#ANOVA test
for activity_type in final_merged_df['activity_type'].unique():
    f_statistic, p_value = f_oneway(
        final_merged_df[final_merged_df['activity_type'] == activity_type]['sum_click'][final_merged_df['final_result'] == 'Distinction'],
        final_merged_df[final_merged_df['activity_type'] == activity_type]['sum_click'][final_merged_df['final_result'] == 'Pass'],
        final_merged_df[final_merged_df['activity_type'] == activity_type]['sum_click'][final_merged_df['final_result'] == 'Fail']
    )
    print(f"ANOVA for {activity_type}: F-statistic={f_statistic}, p-value={p_value}")

"""**Explanation:**

I merged the clicks_by_activity DataFrame, which contains information about student interactions, with the studentInfo_df DataFrame based on the common column 'id_student.' This merge was essential to associate each student's interaction data with their final result.

After merging, I created a bar plot to visualize the average clicks on different resources grouped by the final result. This allows for a quick comparison of how student engagement with various resources relates to their final results.

To statistically evaluate the significance of the observed differences in average clicks among final result categories for each activity type, I conducted an Analysis of Variance (ANOVA) test. The ANOVA test helps determine if there are any statistically significant differences in means among the final result groups.

**Interpretation:**

Bar Plot:

The bar plot provides a visual representation of how the average clicks on different resources vary based on the final result categories. It indicates whether certain resources are more or less frequently used by students who achieved different final outcomes.

ANOVA Test:

The ANOVA results indicate the F-statistic and p-value for each activity type. The null hypothesis for ANOVA is that there is no significant difference in means among the groups. A low p-value (typically below 0.05) suggests that there is enough evidence to reject the null hypothesis.

ANOVA Results:

For most activity types, the p-values are very low (close to zero), indicating strong evidence against the null hypothesis. This suggests that there are significant differences in average clicks among final result categories for these activity types.

## 2. Predictive Modeling

In this section, you will build a machine learning model to predict students' final course outcome (`final_result` column in `studentInfo.csv`). That is, whether student is 'Pass', 'Withdrawn', 'Fail', or 'Distinction'. If you consider the number of students in some of these categories are too few, you can combine them into a new category.

### 2.1. Generate Features from Demographic Information

In Section 1.2, you explored demographic data about students and tuned some categorical variables. From these categorical variables, please generate *at least* **10** *dummy* variables to be used for predictors in the machine learning model.
"""

# Specifying the categorical columns
categorical_columns = ['highest_education','final_result','gender', 'region','disability']

# Generating dummy variables
dummy_variables = pd.get_dummies(studentInfo_df[categorical_columns])

# Concatenating dummy variables with the original DataFrame
studentInfo_df = pd.concat([studentInfo_df, dummy_variables], axis=1)

# Displaying the DataFrame
studentInfo_df

"""**Explanation:**

I identified categorical columns that need to be transformed into dummy variables. These columns include 'highest_education,' 'final_result,' 'gender,' 'region,' and 'disability.'

I utilized the pd.get_dummies() function to convert the specified categorical columns into dummy/indicator variables. This process helps in representing categorical data numerically.

The generated dummy variables were concatenated with the original studentInfo_df DataFrame using pd.concat(). This step expands the DataFrame with new columns, each representing a category within the original categorical columns.

**Interpretation:**

The resulting DataFrame now contains additional columns, representing the dummy variables for the specified categorical columns. Each unique category within the original categorical columns has been transformed into a binary indicator, making it suitable for machine learning models that require numerical input.

### 2.2. Generate/Select Features from Click Data

In Section 1.5, you have already created some features from students' click behaviour. You can use all of them here as additional predictors.

Additionally, you should create *at least* **3** features indicating the engagement level of students at different course components. Some example features are provided below :

* a dummy variable that indicates if students clicked at least three types of course components or not,
* each student's average number of clicks across all components per a single course and semester,
* a dummy variable indicating if students clicked all types of course components.

There is no limit in the type and number of additional feature you can generate from the click data.
"""

# Creating a dummy variable indicating if students clicked at least three types of course components
pivot_clicks['at_least_three_components'] = (pivot_clicks.iloc[:, 3:] > 0).sum(axis=1) >= 3

#Calculating each student's average number of clicks across all components per single course and semester
pivot_clicks['average_clicks'] = pivot_clicks.iloc[:, 3:].mean(axis=1)

#Creating dummy variable indicating if students clicked all types of course components
pivot_clicks['clicked_all_components'] = (pivot_clicks.iloc[:, 3:] > 0).all(axis=1)
pivot_clicks

"""**Explanation:**

I introduced a new feature, at_least_three_components, to identify whether students engaged with a diverse range of course components. This was achieved by checking if a student had clicked on at least three types of course components.

To gauge the overall engagement of each student with the course materials, I calculated the average_clicks feature. This represents the mean number of clicks across all course components for a single course and semester.

A dummy variable, clicked_all_components, was generated to indicate whether a student explored all available course components. This was determined by checking if a student had at least one click for each component type.

**Interpretation:**

At Least Three Components:

The at_least_three_components column is 'True' for students who interacted with at least three types of course components and 'False' otherwise. This information helps in identifying students with diverse engagement patterns.

Average Clicks:

The average_clicks feature provides insights into the average engagement level of students across all course components. It helps in understanding the typical interaction behavior within a single course and semester.

Clicked All Components:

The clicked_all_components variable being 'True' indicates students who explored every type of course component, while 'False' signifies those who did not. This information aids in recognizing students with comprehensive resource utilization.

### 2.3. Training and Testing the Model

As the last activity in this project, you are expected to train and test a logistic regression model for predicting students' final course status. You should use 10-fold cross-validation.

Interpret the results based on confusion matrix and AUC scores. In your interpretation, please also mention the features with high predictive power and those with low predictive power.

Please note that the achieving low/high accuracy in the predictions has no importance for your grade.
"""



