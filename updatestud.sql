CREATE PROCEDURE updatestud (IN newyr varchar(10), in id int)
BEGIN
update students set yrlvl = newyr where studid=id;
END
