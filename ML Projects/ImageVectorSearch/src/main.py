# main.py
from fastapi import FastAPI, Query
from image_embedding import ImageEmbed

app = FastAPI()
image_embed = ImageEmbed()

def perform_search(query_image_url: str, skip: int, limit: int):
    # Your existing search_image method
    result = image_embed.search_image(query_image_url)
    # Extract the top results based on skip and limit
    top_results = result[skip: skip + limit]
    return {"query_image_url": query_image_url, "top_results": top_results}

@app.get("/search_images/{query_image_url}")
async def search_images(query_image_url: str, skip: int = Query(0, description="Number of results to skip"), limit: int = Query(20, description="Number of results to return")):
    """
    Search for similar images and return the top results.

    :param query_image_url: URL of the query image.
    :param skip: Number of results to skip (default is 0).
    :param limit: Number of results to return (default is 20).
    :return: List of top matching image URLs.
    """
    return perform_search(query_image_url, skip, limit)
