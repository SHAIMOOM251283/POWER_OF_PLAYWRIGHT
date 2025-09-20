import asyncio
import csv
import random  # For a bit of randomness in backoff (optional, nice touch)
from playwright.async_api import async_playwright
import os

class Extraction:
    def __init__(self):
        self.base_url = "https://openlibrary.org/search?q=subject%3A%22Computer+science%22&sort=editions&subject_facet=Computer+science"
        self.total_pages = 200  # Total pages you want to scrape
        self.concurrent_pages = 20  # Scrape this many pages in parallel
        self.all_books = []  # Store all scraped books

    async def search_open_library(self, page, page_num):
        """Scrape a single page and return book details, with retry and backoff."""
        print(f"Scraping page {page_num}...")
        books_data = []
        url = f"{self.base_url}&page={page_num}"

        max_retries = 6
        backoff_base = 2  # Exponential base
        for attempt in range(1, max_retries + 1):
            try:
                await page.goto(url, wait_until="domcontentloaded")
                await asyncio.sleep(2)  # Allow extra time for content

                await page.wait_for_selector('.searchResultItem', timeout=5000)
                books = await page.locator(".searchResultItem").all()

                for book in books:
                    try:
                        title = book.locator("h3.booktitle a")
                        title_text = await title.text_content() if await title.count() else "N/A"

                        author_elements = await book.locator(".bookauthor a").all()
                        authors_text = ", ".join([await author.text_content() for author in author_elements]) if author_elements else "N/A"

                        rating = book.locator('span[itemprop="ratingValue"]')
                        rating_text = await rating.text_content() if await rating.count() else "N/A"

                        want_to_read = book.locator('span[itemprop="reviewCount"]')
                        want_to_read_text = await want_to_read.text_content() if await want_to_read.count() else "N/A"

                        books_data.append([title_text, authors_text, rating_text, want_to_read_text])

                    except Exception as e:
                        print(f"Error extracting book data from page {page_num}: {e}")

                print(f"Finished scraping page {page_num}")
                return books_data  # Success, exit early

            except Exception as e:
                print(f"Attempt {attempt} failed for page {page_num}: {e}")

                if attempt < max_retries:
                    # Exponential backoff before next retry
                    wait_time = backoff_base ** attempt + random.uniform(0, 1)
                    print(f"Retrying page {page_num} after {wait_time:.1f} seconds...")
                    await asyncio.sleep(wait_time)
                else:
                    print(f"Page {page_num} skipped after {max_retries} failed attempts.")

        # If all retries failed, return empty list safely
        return books_data

    async def extract(self):
        """Main scraping logic: Runs multiple pages in parallel."""
        async with async_playwright() as p:
            browser = await p.firefox.launch(headless=True)
            context = await browser.new_context()

            for start_page in range(1, self.total_pages + 1, self.concurrent_pages):
                end_page = min(start_page + self.concurrent_pages, self.total_pages + 1)

                pages = [await context.new_page() for _ in range(self.concurrent_pages)]
                tasks = [
                    self.search_open_library(pages[i], page_num)
                    for i, page_num in enumerate(range(start_page, end_page))
                ]

                results = await asyncio.gather(*tasks)  # Run all tasks in parallel

                # Collect results
                for books_page in results:
                    self.all_books.extend(books_page)

                # Close all pages
                for page in pages:
                    await page.close()

            await browser.close()

            # Ensure DATA folder exists inside OpenLibrary_SCRAPER
            data_folder = os.path.join(os.path.dirname(__file__), "DATA", "data_files")
            os.makedirs(data_folder, exist_ok=True)
            # Save all books to CSV
            csv_filename = os.path.join(data_folder, "Computer_Science.csv")
            with open(csv_filename, mode="w", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)
                writer.writerow(["Title", "Author", "Rating", "Want to Read"])
                writer.writerows(self.all_books)

            print(f"Data successfully saved to {csv_filename}")

if __name__ == "__main__":
    asyncio.run(Extraction().extract())