import pymongo

def connect_to_db():
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    print("MongoDB Client:", client)
    db = client['pibdata']
    return db['press_releases']

def store_in_db(data, url=None):
    collection = connect_to_db()
    
    if url:
        # Assuming data is a single dictionary
        filter_query = {"title": data["title"]}
        update_query = {"$set": data}

        # Update the document if it exists, otherwise insert a new one
        result = collection.update_one(filter_query, update_query, upsert=True)
        if result.matched_count > 0:
            print(f"Document with title '{data['title']}' updated successfully.")
        else:
            print(f"Document with title '{data['title']}' inserted successfully.")
        
        # Return the updated or inserted document
        return collection.find_one(filter_query)
    
    else:
        # Assuming data is a list of dictionaries
        result_data = []
        for item in data:
            filter_query = {"title": item["title"]}
            update_query = {"$set": item}
            
            # Update the document if it exists, otherwise insert a new one
            result = collection.update_one(filter_query, update_query, upsert=True)
            if result.matched_count > 0:
                print(f"Document with title '{item['title']}' updated successfully.")
            else:
                print(f"Document with title '{item['title']}' inserted successfully.")
            
            # Append the updated or inserted document to result_data
            result_data.append(collection.find_one(filter_query))
        
        return result_data
