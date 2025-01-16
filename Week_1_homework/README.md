# Docker and SQL Homework Solutions

## Question 1: Understanding Docker First Run
Run Docker with the `python:3.12.8` image in an interactive mode, using the entrypoint `bash`.

**What's the version of pip in the image?**  
**Answer:** 24.3.1

---

## Question 2: Understanding Docker Networking and Docker Compose
Given the following `docker-compose.yaml`, what is the hostname and port that pgAdmin should use to connect to the PostgreSQL database?

**Answer:** `db:5432`

---

## Question 3: Trip Segmentation Count
During the period of October 1st, 2019 (inclusive) and November 1st, 2019 (exclusive), how many trips, respectively, happened:

1. Up to 1 mile
2. Between 1 (exclusive) and 3 miles (inclusive)
3. Between 3 (exclusive) and 7 miles (inclusive)
4. Between 7 (exclusive) and 10 miles (inclusive)
5. Over 10 miles

**Answer:** 104,802; 198,924; 109,603; 27,678; 35,189

**SQL Query:**
```sql
SELECT 
    SUM(CASE WHEN trip_distance <= 1 THEN 1 ELSE 0 END) AS up_to_1_mile,
    SUM(CASE WHEN trip_distance > 1 AND trip_distance <= 3 THEN 1 ELSE 0 END) AS between_1_and_3_miles,
    SUM(CASE WHEN trip_distance > 3 AND trip_distance <= 7 THEN 1 ELSE 0 END) AS between_3_and_7_miles,
    SUM(CASE WHEN trip_distance > 7 AND trip_distance <= 10 THEN 1 ELSE 0 END) AS between_7_and_10_miles,
    SUM(CASE WHEN trip_distance > 10 THEN 1 ELSE 0 END) AS over_10_miles
FROM green_tripdata_2019
WHERE lpep_dropoff_datetime >= '2019-10-01' 
  AND lpep_dropoff_datetime < '2019-11-01';
```

---

## Question 4: Longest Trip for Each Day
Which was the pick-up day with the longest trip distance? Use the pick-up time for your calculations.

**Tip:** For every day, we only care about one single trip with the longest distance.

**Answer:** 2019-10-31

**SQL Query:**
```sql
SELECT 
    DATE(lpep_pickup_datetime) AS longest_day,
    MAX(trip_distance) AS max_distance
FROM green_tripdata_2019
GROUP BY lpep_pickup_datetime
ORDER BY max_distance DESC
LIMIT 1;
```

---

## Question 5: Three Biggest Pickup Zones
Which were the top pickup locations with over 13,000 in total amount (across all trips) for 2019-10-18?  
Consider only `lpep_pickup_datetime` when filtering by date.

**Answer:** East Harlem North, East Harlem South, Morningside Heights

**SQL Query:**
```sql
SELECT 
    zp."Zone" AS zone,
    SUM(total_amount) AS amount
FROM 
    green_tripdata_2019 g 
    JOIN zones zp ON g."PULocationID" = zp."LocationID"
    JOIN zones zd ON g."DOLocationID" = zd."LocationID"
WHERE 
    DATE(g."lpep_pickup_datetime") = '2019-10-18'
GROUP BY 1
HAVING SUM(total_amount) > 13000
LIMIT 5;
```

---

## Question 6: Largest Tip
For the passengers picked up in October 2019 in the zone name "East Harlem North," which was the drop-off zone that had the largest tip?  
**Note:** It's `tip`, not `trip`. We need the name of the zone, not the ID.

**Answer:** JFK Airport

**SQL Query:**
```sql
SELECT 
    zd."Zone" AS dropoff_zone,
    MAX(g.tip_amount) AS max_tip
FROM 
    green_tripdata_2019 g 
    JOIN zones zp ON g."PULocationID" = zp."LocationID"
    JOIN zones zd ON g."DOLocationID" = zd."LocationID"
WHERE 
    TO_CHAR(g."lpep_pickup_datetime", 'YYYY-MM') = '2019-10'
    AND zp."Zone" = 'East Harlem North'
GROUP BY 1
ORDER BY 2 DESC
LIMIT 1;
```

---

## Question 7: Terraform Workflow
Which of the following sequences, respectively, describes the workflow for:

1. Downloading the provider plugins and setting up the backend
2. Generating proposed changes and auto-executing the plan
3. Removing all resources managed by Terraform

**Answer:** `terraform init`, `terraform apply -auto-approve`, `terraform destroy`
