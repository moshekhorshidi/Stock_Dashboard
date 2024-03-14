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
store,
lag(to_date(date,'dd/mm/yyyy')) over(partition by store order by to_date(date,'dd/mm/yyyy')) as from_date,
to_date(date,'dd/mm/yyyy') as to_date,
to_date(date,'dd/mm/yyyy') - lag(to_date(date,'dd/mm/yyyy')) over(partition by store order by to_date(date,'dd/mm/yyyy')) as date_diff,
opening_stock,
lag(opening_stock) over(partition by store order by store) as provios_restock,
opening_stock - lag(opening_stock) over(partition by store order by store) as diff_stock_between_deliveries
from assignments.stock.daily_store_stock_levels

)

select

store,
diff_stock_between_deliveries as Max_Qty_Sales,
from_date,
to_date
from stock_change
where provios_restock is not null
qualify dense_rank() over(partition by store order by diff_stock_between_deliveries desc) = 1
order by from_date


-- with subQ
select

store,
diff_stock_between_deliveries as Max_Qty_Sales,
from_date,
to_date 
from

(
select
store,
lag(to_date(date,'dd/mm/yyyy')) over(partition by store order by to_date(date,'dd/mm/yyyy')) as from_date,
to_date(date,'dd/mm/yyyy') as to_date,
to_date(date,'dd/mm/yyyy') - lag(to_date(date,'dd/mm/yyyy')) over(partition by store order by to_date(date,'dd/mm/yyyy')) as date_diff,
opening_stock,
lag(opening_stock) over(partition by store order by store) as provios_restock,
opening_stock - lag(opening_stock) over(partition by store order by store) as diff_stock_between_deliveries
from assignments.stock.daily_store_stock_levels
) 

as self

where provios_restock is not null
qualify dense_rank() over(partition by store order by diff_stock_between_deliveries desc) = 1
order by from_date

--more clean code, using qualify on anowflake,to present all data related to result

select 
store as store_to_analyze_and_replicate_markting,
diff_stock_between_deliveries as new_target_range_top_boundary,
from_date as seasonal_date_to_analyze,
year(from_date) as on_year,
month(from_date) as on_month,
day(from_date) as on_day,
concat('Q - ', quarter(from_date)) as the_quarter_to_match_and_analyze

from

(

select
store,
lag(to_date(date,'dd/mm/yyyy')) over(partition by store order by to_date(date,'dd/mm/yyyy')) as from_date,
to_date(date,'dd/mm/yyyy') as to_date,
to_date(date,'dd/mm/yyyy') - lag(to_date(date,'dd/mm/yyyy')) over(partition by store order by to_date(date,'dd/mm/yyyy')) as date_diff,
opening_stock,
lag(opening_stock) over(partition by store order by store) as provios_restock,
opening_stock - lag(opening_stock) over(partition by store order by store) as diff_stock_between_deliveries
from assignments.stock.daily_store_stock_levels

) 

as self

where diff_stock_between_deliveries is not null 
qualify dense_rank() over(partition by store order by diff_stock_between_deliveries desc) = 1
order by year(from_date)
