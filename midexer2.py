import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["enrollmentsystem"]

mongoquery = mydb.get_collection("students")

#result1 = mongoquery.find({})
result1 = mongoquery.find({"studcourse":"BSIT"})
result2 = mongoquery.find({"studcourse":{"$in":["BSIT","BSIM"]}})

#same result
result1 = mongoquery.find({"studcourse":"BSIT","studid":{"$gt":1}})
result1 = mongoquery.find({"$and":[{"studcourse":"BSIT"},{"studid":{"$gt":1}}]})
# or 
result1 = mongoquery.find({"$or":[{"studcourse":"BSIT"},{"studid":{"$lte":1}}]})
#and + or,, select * from students where studcourse = bsit and (studid < 5 or studname like a%)
result1 = mongoquery.find({"studcourse":"BSIT","$or":[{"studid":{"$lt":5}},{"studname":{"$regex":/^a/}}]})
# select * from students where studid > 1 and (studcourse = BSIT or studname like %a)
result1 = mongoquery.find({"studid":{"$gt":1},"$or":[{"studcourse":"BSIT"},{"studname":{"$regex":/a$/}}]})
for i in result1:
    print(i)
