from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from memoryz.repository import get_memory_repository # Assuming this is the correct import path
from typing import List, Any

# Initialize the repository globally
# In a real application, you might use dependency injection or a more robust state management
# Note: The current InMemoryMemoryRepository2 structure ties the 'query' object to the user store.
# This global repository instance will manage multiple user stores.
repo = get_memory_repository()

app = FastAPI()

class BuildRequest(BaseModel):
    user_id: str
    # Add fields for data to build from if needed later.
    # Based on the current repository code, build() is called without args internally.
    # If building requires data, the repository/query structure needs adjustment.

class QueryRequest(BaseModel):
    user_id: str
    query_text: str

class QueryResponse(BaseModel):
    results: List[Any] # Assuming query can return various types of results

@app.post("/build")
async def build_knowledge_base(request: BuildRequest):
    """
    Triggers the knowledge base build process for a specific user.
    Note: Based on the current InMemoryMemoryRepository2 implementation,
    the build process is tied to the internal 'query' object created
    when a user's store is first accessed. This API endpoint
    accesses that internal object to call its build method.
    A cleaner approach might involve refactoring the repository
    or introducing a dedicated Queryer service.
    """
    try:
        # Access or create the user's store to get the internal 'query' object
        # The _get_user_store method initializes the 'query' object if it doesn't exist
        user_memories, user_data = repo._get_user_store(request.user_id)

        # Access the object assumed to have the build() method
        # Based on InMemoryMemoryRepository2, this object is stored under the 'memories' key
        # Let's try accessing it directly from the internal store structure as observed:
        user_store_data = repo._memory_store.get(request.user_id)
        if not user_store_data:
             # If user store doesn't exist, _get_user_store will create it and the query object
             user_memories, user_data = repo._get_user_store(request.user_id)
             query_obj = user_memories # Still using this based on the code, but it's likely wrong.

             # Let's assume the 'query' object is actually stored under a different key, or the repository instance itself should have the methods.
             # Given the user said "Queryer.build()", let's assume there's an object/instance somewhere that *is* the Queryer.
             # In InMemoryMemoryRepository2, the object created by `director.construct()` is assigned to `self._memory_store[user_id]['memories']`.
             # So, let's try to access that specific object.
             query_obj = repo._memory_store[request.user_id]['memories']

        else:
             query_obj = user_store_data['memories']


        # Call the build method
        if hasattr(query_obj, 'build'):
            query_obj.build()
            return {"message": f"Knowledge base build process initiated for user {request.user_id}"}
        else:
             raise HTTPException(status_code=500, detail="Internal query object does not have a 'build' method.")

    except KeyError:
         raise HTTPException(status_code=404, detail=f"User {request.user_id} store not found after initialization attempt.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred during build: {str(e)}")

@app.post("/query")
async def query_knowledge_base(request: QueryRequest):
    """
    Queries the knowledge base for a specific user.
    Note: Accesses the internal 'query' object associated with the user's store.
    """
    try:
        # Access the user's store to get the internal 'query' object
        user_store_data = repo._memory_store.get(request.user_id)
        if not user_store_data:
             raise HTTPException(status_code=404, detail=f"User {request.user_id} not found or knowledge base not initialized.")

        # Access the object assumed to have the query() method
        query_obj = user_store_data['memories']

        # Call the query method
        if hasattr(query_obj, 'query'):
            results = query_obj.query(request.query_text)
            return QueryResponse(results=results)
        else:
             raise HTTPException(status_code=500, detail="Internal query object does not have a 'query' method.")

    except KeyError:
         raise HTTPException(status_code=404, detail=f"User {request.user_id} store not found.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred during query: {str(e)}")

# To run this API:
# Save the code as api.py
# Run the command: uvicorn api:app --reload
# The API will be available at http://127.0.0.1:8000