from typing import List

from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from app.models import ScrapingSettings, Product, DBProduct
from app.scraper import WebScraper
from app.storage import DatabaseStorage
from app.notification import ConsoleNotification
from app.auth import verify_token
from app.database import engine, Base, get_db

Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.post("/scrape")
async def scrape_website(settings: ScrapingSettings, token: str = Depends(verify_token), db: Session = Depends(get_db)):
    print(f"Scraping started...")
    scraper = WebScraper(DatabaseStorage(), ConsoleNotification())
    await scraper.scrape(settings)
    return {"message": "Scraping completed successfully"}


@app.get("/products", response_model=List[Product])
def read_products(skip: int = 0, limit: int = 200, db: Session = Depends(get_db)):
    products = db.query(DBProduct).offset(skip).limit(limit).all()
    return products


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
