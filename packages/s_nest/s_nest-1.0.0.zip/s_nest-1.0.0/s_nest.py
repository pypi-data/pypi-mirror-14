#create by SongXY
#Created on: 2016.3.7
#update: 2016.3.7
import pymongo

class infoSearch():
    
    def linkdatabase(self,key):
        
        client = pymongo.MongoClient("localhost",27017)
        db = client.shiyan
        collection = db.person 
        
        for data in collection.find({"name":{'$regex':key}}):
            print(data)
        
if __name__ == "__main__":

    print("Please input the key of the protein,Example:cui")
    key = input()     
    searchKey = infoSearch()
    searchKey.linkdatabase(key)
           
    
 