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

<!-- Column Descriptions:
1. Location:
2-3. ItinID & MktID: vaguely demonstrates the order in which tickets were ordered (lower ID #'s being ordered first)
4. MktCoupons: the number of coupons in the market for that flight
5. Quarter: 1, 2, 3, or 4, all of which are in 2018
6. Origin: the city out of which the flight begins
7. OriginWac: USA State/Territory World Area Code
8. Dest: the city out of which the flight begins
9. DestWac: USA State/Territory World Area Code
10. Miles: the number of miles traveled
11. ContiguousUSA: binary column -- (2) meaning flight is in the contiguous (48) USA states, and (1) meaning it is not (ie: Hawaii, Alaska, off-shore territories)
12. NumTicketsOrdered: number of tickets that were purchased by the user
13. Airline Company: the two-letter airline company code that the user used from start to finish (key codes below)
14. PricePerTicket: target prediction column

<h3>Check for correlations:</h3>
<br/>
<img width="500" alt="Correlation" src="https://user-images.githubusercontent.com/80112729/118389956-0fe8de80-b65f-11eb-843b-88d56d725ea5.png">
From the correlation heat map, it is observed that “Miles” is the most correlated feature to the target feature (price), the rest have very little influence on the target feature.
<br/>

<br/>
<h3>Relationship between price per ticket vs miles:</h3>
<img width="500" alt="Price vs Miles" src="https://user-images.githubusercontent.com/80112729/118390229-90f4a580-b660-11eb-9c05-11e18e34893e.png">
From the above lineplot, a mild linear relationship is observed between price per ticket and miles.
<br/>


<br/>
<h3>Main competitors:</h3>
<img width="500" alt="competitors" src="https://user-images.githubusercontent.com/80112729/118394569-0324b480-b678-11eb-898f-757341a0c443.png">
<br/>

Main competitors: 
1. WN -- Southwest Airlines Co.
2. DL -- Delta Air Lines Inc. 
3. AA -- American Airlines Inc.        
4. UA -- United Air Lines Inc.


<br/>
<h3>Variance score on different models:</h3>
<img width="500" alt="VS" src="https://user-images.githubusercontent.com/80112729/118395188-927f9700-b67b-11eb-9750-3591a832d51e.png">
<br/>

<br/>
<h3>Price predictions:</h3>
<img width="500" alt="price predict" src="https://user-images.githubusercontent.com/80112729/118395228-c22e9f00-b67b-11eb-8820-5ee96b54c036.png">
<br/>

Future improvements:
1. Add features into datasets
2. Consider parameters affecting the ticket price(Service fee, fuel surcharge, date and time) -->
