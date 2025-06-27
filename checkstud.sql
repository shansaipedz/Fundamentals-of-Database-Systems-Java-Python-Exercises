DELIMITER $$
CREATE PROCEDURE checkstud(IN stdid int, OUT status varchar(20))
BEGIN

declare units INT default 0;

select sum(subjunits) into units from students, enroll, subjects where students.studid=enroll.studid and enroll.subjid=subjects.subjid and enroll.studid= stdid;

if units > 15 then
	set status = 'Not allowed to enroll';
elseif units <=15 then
	set status = 'allowed to enroll';
else
	set status = 'Not enrolled yet';

end if;

END$$
DELIMITER ;
