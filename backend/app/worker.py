from playwright.sync_api import sync_playwright
from sqlalchemy.orm import Session
from uuid import UUID
import asyncio

from .database import SessionLocal
from .models import Job
from .websocket_manager import manager


def emit(job_id, event, message):

    print(f"{event} -> {message}")

def run_job(job_id: UUID):

    db: Session = SessionLocal()

    job = db.query(Job).filter(
        Job.job_id == job_id
    ).first()

    try:

        job.status = "running"
        db.commit()

        emit(
            job_id,
            "browser.launched",
            "Launching Chromium browser"
        )

        with sync_playwright() as p:

            browser = p.chromium.launch(
                headless=True
            )

            page = browser.new_page()

            emit(
                job_id,
                "page.navigating",
                f"Opening {job.url}"
            )

            page.goto(job.url)

            emit(
                job_id,
                "page.loaded",
                "Page loaded successfully"
            )

            page.mouse.wheel(0, 1200)

            emit(
                job_id,
                "action.taken",
                "Scrolled page"
            )

            page.hover(".product_pod")

            emit(
                job_id,
                "action.taken",
                "Hovered over first product"
            )

            books = page.query_selector_all(
                ".product_pod"
            )

            data = []

            for book in books[:5]:

                title = book.query_selector(
                    "h3 a"
                ).get_attribute("title")

                price = book.query_selector(
                    ".price_color"
                ).inner_text()

                data.append({
                    "title": title,
                    "price": price
                })

            emit(
                job_id,
                "data.extracted",
                "Extracted product titles and prices"
            )

            screenshot_path = (
                f"screenshots/{job_id}.png"
            )

            page.screenshot(
                path=screenshot_path,
                full_page=True
            )

            emit(
                job_id,
                "screenshot.captured",
                "Screenshot saved"
            )

            browser.close()

            emit(
                job_id,
                "browser.closed",
                "Browser closed successfully"
            )

        job.status = "completed"
        job.result = data

        db.commit()

        emit(
            job_id,
            "job.completed",
            "Automation completed successfully"
        )

    except Exception as e:

        job.status = "failed"
        job.error = str(e)

        db.commit()

        emit(
            job_id,
            "job.failed",
            str(e)
        )

    finally:

        db.close()