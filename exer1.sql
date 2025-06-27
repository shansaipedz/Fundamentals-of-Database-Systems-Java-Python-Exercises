CREATE PROCEDURE `sample2` (in Studid int, in subid int, out output varchar(20))
BEGIN
declare no_more_products int default 0;
DECLARE conflict BOOLEAN DEFAULT FALSE;
declare sched1 varchar(20);
declare sched2 int;
declare sched3 int;
declare temp varchar(20);
declare checker cursor for
	select sched from (students left outer join enroll on students.studid = enroll.studid) left outer join subjects on subjects.subjid = enroll.subjid where enroll.studid = Studid;
DECLARE CONTINUE HANDLER FOR NOT FOUND
	SET no_more_products = 1;

call sample(Studid, subid, @a,@b,@c);
select @a into sched1;
select @b into sched2;
select @c into sched3;

open checker;
fetch checker into temp;
REPEAT
	-- Extract year, month, and day from expiration date
	call process_sched(checker, @sched_day,@sched_start,@sched_end);
	-- Check if the product is expired
	IF sched2 > sched_start THEN
		SET conflict = TRUE;
	elseif num = YEAR(NOW()) and num <= MONTH(NOW())  THEN
		SET conflict = TRUE;
	END IF;
	-- If the product is not expired, insert the order
	IF NOT num THEN
		INSERT INTO enroll (studid, subjid) VALUES (studid, subjid);
	END IF;
	FETCH checker INTO temp;
UNTIL no_more_products = 1
END REPEAT;
CLOSE checker;

END
------------------------------------
CREATE PROCEDURE `sample` (studid int, subid int, out output int, out output2 int, out output3 varchar(10))
BEGIN
	declare fullsched varchar(20);
    declare sched_time varchar(20);
    declare sched_day varchar(10);
    declare sched_start int;
    declare sched_end int;
	
    select sched into fullsched from subjects where subjid = subid;
    
    set sched_day = left(fullsched, 4);
    set sched_time = right(fullsched, 9);
    set sched_start = left(sched_time, 4);
    set sched_end = right(sched_time, 4);
    
    set output = sched_start;
    set output2 = sched_end;
    set output3 = sched_day;
END
------------------------------------
CREATE PROCEDURE `process_sched` (fullsched varchar(20), out output varchar(20), out output2 int, out output3 int)
BEGIN
	declare sched_time varchar(20);
    declare sched_day varchar(10);
    declare sched_start int;
    declare sched_end int;
	
    set sched_day = left(fullsched, 4);
    set sched_time = right(fullsched, 9);
    set sched_start = left(sched_time, 4);
    set sched_end = right(sched_time, 4);
    
    set output = sched_day;
    set output2 = sched_start;
    set output3 = sched_end;
END
---------------------- IN PROGRESS -----------------------------------------------------------
-- --------------------------------------------------------------------------------
-- Routine DDL
-- Note: comments before and after the routine body will not be stored by the server
-- --------------------------------------------------------------------------------
DELIMITER $$

CREATE PROCEDURE `enrollmentsystem`.`main` (in Studid int, in subid int, out output varchar(20))
BEGIN
declare no_more_rows int default 0;
DECLARE enrollment_count INT;
DECLARE conflict_count INT default 0;
DECLARE conflict BOOLEAN DEFAULT FALSE;
declare sched1 varchar(20);
declare sched2 int;
declare sched3 int;
declare temp varchar(20);
declare checker cursor for
	select sched from (students left outer join enroll on students.studid = enroll.studid) left outer join subjects on subjects.subjid = enroll.subjid where enroll.studid = Studid;
DECLARE CONTINUE HANDLER FOR NOT FOUND
	SET no_more_rows = 1;

call current_sched(subid, @a,@b,@c);
select @a into sched1;
select @b into sched2;
select @c into sched3;
set output = 'conflict';
SELECT COUNT(*) INTO enrollment_count from (students left outer join enroll on students.studid = enroll.studid) left outer join subjects on subjects.subjid = enroll.subjid where enroll.studid = Studid; 
set enrollment_count = enrollment_count + 1;

open checker;
fetch checker into temp;

REPEAT
	
	-- Extract year, month, and day from expiration date
	
	call process_sched(temp, @sched_day,@sched_start,@sched_end);

	IF ((sched2 >= @sched_start AND sched2 <= @sched_end) OR (sched3 >= @sched_start AND sched3 <= @sched_end)) AND (sched1 = @sched_day) THEN
    SET conflict = TRUE;
	SET conflict_count = conflict_count + 1;
	END IF;

	
	
	set enrollment_count = enrollment_count - 1;
    
	FETCH checker INTO temp;
UNTIL no_more_rows = 1
END REPEAT;

-- If the product is not expired, insert the order
	IF NOT conflict and conFlict_count = 0 THEN
		INSERT INTO enroll (studid, subjid) VALUES (Studid, subid);
        set output = 'enrolled';
	END IF;

CLOSE checker;

END
////////////////////
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
/////////////////////////////////////////
-- --------------------------------------------------------------------------------
-- Routine DDL
-- Note: comments before and after the routine body will not be stored by the server
-- --------------------------------------------------------------------------------
DELIMITER $$

CREATE PROCEDURE `enrollmentsystem`.`current_sched` (subid int, out output varchar(20), out output2 int, out output3 int)
BEGIN
	declare fullsched varchar(20);
    declare sched_time varchar(20);
    declare sched_day varchar(20);
    declare sched_start int;
    declare sched_end int;
	
    select sched into fullsched from subjects where subjid = subid;
    
    set sched_day = left(fullsched, 3);
    set sched_time = right(fullsched, 9);
    set sched_start = left(sched_time, 4);
    set sched_end = right(sched_time, 4);
    
    set output = sched_day;
    set output2 = sched_start;
    set output3 = sched_end;
END
