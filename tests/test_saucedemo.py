from playwright.sync_api import Page, expect
import pytest


def test_sauce_demo_dem_2(page: Page, record_property):
    record_property("test_key", "DEM-2")
    page.goto('https://saucedemo.com')

    page.get_by_placeholder('Username').fill('standard_user')    
    page.get_by_placeholder('Password').fill('secret_sauce')    
    page.get_by_role('button',name='login').click()
    #expect(page).to_have_url('https://saucedemo.com/inventory.html')
    expect(page).to_have_url('https://www.saucedemo.com/inventory.html')
    page.get_by_role('button', name='Add to cart').first.click()

def login(page: Page, user, password):
    page.goto('https://saucedemo.com')
    page.get_by_placeholder('Username').fill(user)
    page.get_by_placeholder('Password').fill(password)
    page.get_by_role('button', name='Login').first.click()


@pytest.mark.parametrize(
        'user, password',
        [
            ('standard_user','secret_sauce'),
            ('visual_user','secret_sauce')
        ]
)


def test_login_dem_2(page,user, password):
    login(page,user,password)
    assert 'inventory' in page.url

