from playwright.sync_api import sync_playwright
from sqlalchemy.orm import Session
from uuid import UUID
import os

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

            # Open website
            page.goto(
                job.url,
                timeout=60000
            )

            page.wait_for_load_state(
                "networkidle"
            )

            emit(
                job_id,
                "page.loaded",
                "Page loaded successfully"
            )

            # Scroll page
            page.mouse.wheel(0, 1500)

            emit(
                job_id,
                "action.taken",
                "Scrolled page"
            )

            # Optional GitHub search automation
            if "github.com" in job.url.lower():

                try:

                    search_box = page.locator(
                        'input[placeholder="Search or jump to..."]'
                    )

                    search_box.click()

                    search_box.fill(
                        "playwright"
                    )

                    page.keyboard.press("Enter")

                    emit(
                        job_id,
                        "action.taken",
                        "Searched for Playwright on GitHub"
                    )

                except Exception as e:

                    emit(
                        job_id,
                        "warning",
                        f"GitHub search skipped: {str(e)}"
                    )

            # Optional Wikipedia automation
            elif "wikipedia.org" in job.url.lower():

                try:

                    search_box = page.locator(
                        'input[name="search"]'
                    )

                    search_box.fill(
                        "Artificial Intelligence"
                    )

                    page.keyboard.press("Enter")

                    emit(
                        job_id,
                        "action.taken",
                        "Searched Artificial Intelligence on Wikipedia"
                    )

                except Exception as e:

                    emit(
                        job_id,
                        "warning",
                        f"Wikipedia search skipped: {str(e)}"
                    )

            # Create screenshots folder
            os.makedirs(
                "screenshots",
                exist_ok=True
            )

            screenshot_path = (
                f"screenshots/{job_id}.png"
            )

            # Capture screenshot
            page.screenshot(
                path=screenshot_path,
                full_page=True
            )

            emit(
                job_id,
                "screenshot.captured",
                f"Screenshot saved at {screenshot_path}"
            )

            browser.close()

            emit(
                job_id,
                "browser.closed",
                "Browser closed successfully"
            )

        # Final result
        job.status = "completed"

        job.result = {
            "message": "Automation completed successfully",
            "screenshot": screenshot_path
        }

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
