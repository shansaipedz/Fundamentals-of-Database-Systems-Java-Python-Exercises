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
