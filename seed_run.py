import asyncio
from app.seed import load_products

if __name__ == "__main__":
    asyncio.run(load_products())