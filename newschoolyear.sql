CREATE PROCEDURE newschoolyear()
BEGIN
declare counter int default 1;
declare yr varchar(10) default '1st';

while counter <= 100 DO
select yrlvl into yr from students where studid = counter;
if yr = '1st' then
set yr='2nd';
elseif yr = '2nd' then
set yr = '3rd';
elseif yr = '3rd' then
set yr = '4th';
else
set yr = '4th';
end if;
call updatestud(yr,counter);
set counter = counter + 1;
end while;
END