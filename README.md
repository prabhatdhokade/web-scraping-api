# Web Scraping API

This project provides a FastAPI-based web scraping tool that allows users to scrape product information from e-commerce websites and store the data in a database.

## Features

- Scrape product information (title, price, image URL) from target websites
- Store scraped data in a SQLite database
- Retrieve stored product information via API
- Basic authentication using API tokens
- Configurable scraping settings (target URL, page limit, proxy)

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/prabhatdhokade/web-scraping-api.git
    cd web-scraping-api
    ```

2. Install the required packages:

    ```bash
    pip install -r requirements.txt
    ```

3. Set up the database:

    ```bash
    python -c "from app.database import Base, engine; Base.metadata.create_all(bind=engine)"
    ```

## Usage

1. Start the FastAPI server:

    ```bash
    uvicorn app.main:app --reload
    ```

2. Use the following API endpoints:

### Scrape Products

- **Endpoint:** `/scrape`
- **Method:** POST
- **Authentication:** Required (API token in header)
- **Request Body:**

    ```json
    {
        "target_url": "https://dentalstall.com/shop/",
        "page_limit": 5,
        "proxy": "http://203.24.108.161:80"
    }
    ```

- **Example curl command:**

    ```bash
    curl -X POST "http://localhost:8000/scrape" -H "x-token: Prabhat@2024" -H "Content-Type: application/json" -d '{"target_url": "https://dentalstall.com/shop/", "page_limit": 5, "proxy": "http://203.24.108.161:80"}'
    ```

### Retrieve Products

- **Endpoint:** `/products`
- **Method:** GET
- **Query Parameters:**
    - `skip` (optional): Number of products to skip (default: 0)
    - `limit` (optional): Maximum number of products to return (default: 100)

- **Example curl command:**

    ```bash
    curl "http://localhost:8000/products?skip=0&limit=10"
    ```

## Data Storage

All the scraped results will be stored in a `products.json` file and in the `products` table of the SQLite database.

## Known Issues and Improvements

1. The product search logic in BeautifulSoup HTML response can be improved for better accuracy and efficiency.
2. Redis caching might not work on all machines. If you encounter issues, comment out lines 72 and 78 in `scraper.py`.
3. Given more time, the caching mechanism could be enhanced for better performance.
4. Error handling and logging can be improved for better debugging and monitoring.
5. The scraping logic could be made more robust to handle different website structures.

## Note

This tool was developed within a limited timeframe. With additional time and resources, it can be further improved and optimized for production use.
