from shiny.playwright import controller
from shiny.run import ShinyAppProc
from playwright.sync_api import Page
from shiny.pytest import create_app_fixture

app = create_app_fixture("../src/app.py")

def test_unfiltered_df(page: Page, app: ShinyAppProc) -> None:
    """Test the initial unfiltered df is correct
    
    This is important to make sure the data that all plots are based on is correct.
    """
    page.goto(app.url)
    page.get_by_role("tab", name="Data Table").click()
    page.locator("#tbl").wait_for()

    df = controller.OutputDataFrame(page, "tbl")
    df.expect_nrow(202)

def test_filtered_df(page: Page, app: ShinyAppProc) -> None:
    """Test filtered df after selecting North America only
    
    This is important to make sure the filtered data is giving correct results.
    """
    page.goto(app.url)
    page.get_by_role("tab", name="Data Table").click()
    check_box = controller.InputCheckboxGroup(page, "input_region")
    check_box.set(["North America"])
    page.locator("#tbl").wait_for()

    df = controller.OutputDataFrame(page, "tbl")
    df.expect_nrow(27)

def test_filter_reset(page: Page, app: ShinyAppProc) -> None:
    """Test the reset filter button
    
    This is important so we know users are actually able to reset the dashboard
    and are working with a fresh start of the filters.
    """
    page.goto(app.url)
    page.get_by_role("tab", name="Data Table").click()
    check_box = controller.InputCheckboxGroup(page, "input_region")
    check_box.set(["North America"])
    page.locator("#tbl").wait_for()

    df = controller.OutputDataFrame(page, "tbl")
    df.expect_nrow(27)

    reset = controller.InputActionButton(page, "reset_regions")
    reset.click()
    page.locator("#tbl").wait_for()

    df = controller.OutputDataFrame(page, "tbl")
    df.expect_nrow(202)