-- see data
select * 
from assignments.stock.daily_store_stock_levels 
limit 10
-- see agg data for better understanding of the data
select distinct store
from assignments.stock.daily_store_stock_levels 
group by 1
order by 1
-- see time ranges on data 
select distinct year(to_date(date,'dd/mm/yyyy')) as year_of_data ,month(to_date(date,'dd/mm/yyyy')) as month_of_data
from assignments.stock.daily_store_stock_levels
group by 1,2
order by 2; -- see 23 --> 25 year 
-- Q1 + Q2
/*The maximum quantity of sales between consecutive deliveries of extra stock to the 
store*/

--with CTE 
with stock_change as (

select 
opening_stock - lag(opening_stock) over(order by date) as diff_between_deliveries,
from assignments.stock.daily_store_stock_levels

)

select max(diff_between_deliveries) as result from stock_change

-- with subQ
select max(diff_between_deliveries) as result 
from
(
select opening_stock - lag(opening_stock) over(order by date) as diff_between_deliveries,
from assignments.stock.daily_store_stock_levels
) 

as self

--result = 1332


--more clean code, using qualify on anowflake,to present all data related to result

select 

rank() over (order by diff_between_deliveries desc) as Ranking,
date as seasonal_date_to_analyze,
year_of_date as on_year,
month_of_date as on_month,
day_of_date as on_day,
concat('Q - ', quarter_of_date) as the_quarter_to_match_and_analyze,
store as store_to_analyze_and_replicate_markting,
diff_between_deliveries as new_target_range_top_boundary

from

(
select 
date,
year(to_date(date,'dd/mm/yyyy')) as year_of_date,
month(to_date(date,'dd/mm/yyyy')) as month_of_date,
day(to_date(date,'dd/mm/yyyy')) as day_of_date,
quarter(to_date(date,'dd/mm/yyyy')) as quarter_of_date,
store,
opening_stock,
opening_stock - lag(opening_stock) over(order by date) as diff_between_deliveries
from assignments.stock.daily_store_stock_levels
) 

as self

where diff_between_deliveries is not null 
qualify Ranking between 1 and 5 -- moshe: for the task i needed only rank 1
order by Ranking asc