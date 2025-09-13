import asyncio

from pymongo import AsyncMongoClient


async def main():
    uri = "mongodb://root:pass@127.0.0.1:27017/?authSource=admin&serverSelectionTimeoutMS=5000"
    client = AsyncMongoClient(uri)
    db = client["recommendation_engine"]

    await db.command("ping")
    print("Pinged your deployment. You successfully connected to MongoDB!")

    collections = await db.list_collection_names()
    print(f"Collections: {collections}")

    await client.close()


if __name__ == "__main__":
    asyncio.run(main())
