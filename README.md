# Web-scraping-project-Estate-pricing

<h3>Goal: Find insights and actions plans from estate pricing data</h3>

<!-- ################################################################################################ -->

<br/>
<h3>Data Collection: Web Scraping</h3>
<img width="800" alt="DF" src="https://user-images.githubusercontent.com/80112729/119645828-0a567a00-be51-11eb-8754-bd2097b0be94.png">
<br/>


Step 1: Request and parse website as HTML using Selenium and BS4

Step 2: Find all "table" "tr" and "td" elements and extract contents via get_text()

Step 3: Loop through the above process through all the months and years from 2002 (240 pages in total)

<!-- ################################################################################################ -->

<h3>Data Preprocessing: Data Cleaning</h3>

<br/>
<h3>Original DataFrame:</h3>
<img width="500" alt="DF" src="https://user-images.githubusercontent.com/80112729/119641257-0bd17380-be4c-11eb-983f-3c917644892e.png">
<br/>


Step 1: Remove unnecessary columns

Step 2: Checking for null values

Step 3: Rename columns

Step 4: Convert date column as datetime type and set it as index

Step 5: Convert string numbers into numerical values

Step 6: Check and remove duplicate values

<br/>
<h3>Finalised DataFrame:</h3>
<img width="800" alt="DF" src="https://user-images.githubusercontent.com/80112729/119642065-eb55e900-be4c-11eb-9b87-4e99a3b3456a.png">
<br/>

Note 1: 1 sq m = 10.764 sq ft.

Note 2: "H": 27/F or above; "M": 14/F to 26/F; "L": 13/F or below.

<!-- ################################################################################################ -->

<h3>Check for correlations:</h3>

<br/>
<img width="500" alt="Correlation" src="https://user-images.githubusercontent.com/80112729/119647006-5ce46600-be52-11eb-84b4-36b4bb67c04b.png">
From the correlation heat map, it is observed that “Miles” is the most correlated feature to the target feature (price), the rest have very little influence on the target feature.
<br/>


Future improvements:
1. Add features into datasets
2. Consider parameters affecting the ticket price(Service fee, fuel surcharge, date and time) -->
