-- --------------------------------------------------------------------------------
-- Routine DDL
-- Note: comments before and after the routine body will not be stored by the server
-- --------------------------------------------------------------------------------
DELIMITER $$

CREATE PROCEDURE `enrollmentsystem`.`process_sched` (fullsched varchar(20), out output varchar(20), out output2 int, out output3 int)
BEGIN
	declare sched_time varchar(20);
    declare sched_day varchar(10);
    declare sched_start int;
    declare sched_end int;
	
    set sched_day = left(fullsched, 3);
    set sched_time = right(fullsched, 9);
    set sched_start = left(sched_time, 4);
    set sched_end = right(sched_time, 4);
    
    set output = sched_day;
    set output2 = sched_start;
    set output3 = sched_end;
END
