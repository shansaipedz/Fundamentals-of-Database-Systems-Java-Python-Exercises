USE `enrollmentsystem`;
DELIMITER $$

CREATE TRIGGER `Students_AINS` AFTER INSERT ON Students FOR EACH ROW
BEGIN
declare no_more_rows int default 0;
declare temp varchar(20);
declare checker cursor for
	select subjcode from subjects;
DECLARE CONTINUE HANDLER FOR NOT FOUND
	SET no_more_rows = 1;
call courseyear(new.studid, @studcourse,@studyear);
open checker;
fetch checker into temp;

REPEAT
	select subjid from subjects where subjcode = temp;
	call process_subjcode(temp, @course,@yr);
	if @course = @studcourse and @yr = @studyear then
		insert into enroll(studid,subjid) values(new.studid,subjid);
	end if;
    
	FETCH checker INTO temp;
UNTIL no_more_rows = 1
END REPEAT;

CLOSE checker;
end

///////
-- --------------------------------------------------------------------------------
-- Routine DDL
-- Note: comments before and after the routine body will not be stored by the server
-- --------------------------------------------------------------------------------
DELIMITER $$

CREATE PROCEDURE `enrollmentsystem`.`process_subjcode` (subjcode varchar(20), out output varchar(20), out output2 int)
BEGIN
	declare fullcourse varchar(20);
    declare subjectyear int;

    set fullcourse = left(subjcode, 2);
    set subjectyear = substring(subjcode, 3, 1);
    
    set output = fullcourse;
    set output2 = subjectyear;
END
///////////
-- --------------------------------------------------------------------------------
-- Routine DDL
-- Note: comments before and after the routine body will not be stored by the server
-- --------------------------------------------------------------------------------
DELIMITER $$

CREATE PROCEDURE `enrollmentsystem`.`courseyear` (Studid int, out output varchar(20), out output2 int)
BEGIN
	declare course varchar(20);
    declare studyear int;
	select studcourse,studyear into course,studyear from students where studid = Studid;
	
    set course = right(course, 2);
    set studyear = left(studyear, 1);
    
    set output = course;
    set output2 = studyear;
END
--------------------------- FINAL ---------------------------------------
CREATE DEFINER = CURRENT_USER TRIGGER `enrollmentsystem`.`insertstudents` AFTER INSERT ON `students` FOR EACH ROW
BEGIN
declare no_more_rows int default 0;
declare temp varchar(20);
declare studcourse varchar(20);
declare studyear varchar(20);
declare subjcourse varchar(20);
declare subjectyear varchar(20);
declare subjectid int;

declare checker cursor for
	select subjcode from subjects;
DECLARE CONTINUE HANDLER FOR NOT FOUND
	SET no_more_rows = 1;

set studcourse = right(new.studcourse, 2);
set studyear = left(new.yrlvl, 1);

open checker;
fetch checker into temp;
REPEAT
	select subjid into subjectid from subjects where subjcode = temp;
	set subjcourse = left(temp, 2);
    set subjectyear = substring(temp, 3, 1);
	if subjcourse = studcourse and subjectyear = studyear then
		insert into enroll(studid,subjid) values(new.studid,subjectid);
	end if;
    
	FETCH checker INTO temp;
UNTIL no_more_rows = 1
END REPEAT;
CLOSE checker;
END;
----------------------------------------------------------------------
CREATE DEFINER = CURRENT_USER TRIGGER `enrollmentsystem`.`subjects_AFTER_INSERT` AFTER INSERT ON `subjects` FOR EACH ROW
BEGIN
declare no_more_rows int default 0;
declare temp int;
declare student_id int;
declare checker cursor for
	select studid from students where right(studcourse, 2) = left(new.subjcode, 2) AND LEFT(yrlvl, 1) = substring(new.subjcode, 3, 1);
DECLARE CONTINUE HANDLER FOR NOT FOUND
	SET no_more_rows = 1;

OPEN checker;
FETCH checker INTO temp;
REPEAT
	select studid into student_id from students where studid = temp;
	INSERT INTO enroll (studid, subjid) VALUES (student_id, NEW.subjid);
    FETCH checker INTO temp;
    UNTIL no_more_rows = 1
END REPEAT;
CLOSE checker;
END
