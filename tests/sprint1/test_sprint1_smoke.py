import re

import pytest
from playwright.sync_api import expect

from pages.contact_page import ContactPage
from pages.home_page import HomePage
from pages.login_page import LoginPage


@pytest.mark.smoke
@pytest.mark.ui
def test_smoke_search(page):
    """Goal: search finds matching products.
    Precondition: none.
    Expected: every displayed product name contains the search keyword."""
    home = HomePage(page).open().search("pliers")
    expect(home.search_completed).to_be_visible()
    names = home.product_names.all_inner_texts()
    assert names and all("pliers" in name.lower() for name in names), names


@pytest.mark.smoke
@pytest.mark.ui
def test_smoke_add_product_to_cart(page):
    """Goal: add a product to the cart.
    Precondition: product 'Claw Hammer' exists.
    Expected: the cart badge shows one item."""
    product = HomePage(page).open().open_product("Claw Hammer")
    product.add_to_cart()
    expect(product.toast).to_contain_text("Product added to shopping cart")
    expect(product.cart_quantity).to_have_text("1")


@pytest.mark.smoke
@pytest.mark.ui
def test_smoke_wrong_login_is_rejected(page):
    """Goal: invalid login is rejected.
    Precondition: the e-mail does not belong to an account.
    Expected: an invalid-credentials error is shown."""
    login = LoginPage(page).open().login("nobody-here@example.com", "wrong-password")
    expect(login.error).to_contain_text("Invalid email or password")
    expect(page).to_have_url(re.compile(r"/auth/login$"))


@pytest.mark.smoke
@pytest.mark.ui
def test_smoke_empty_contact_form_shows_validation_errors(page):
    """Goal: required contact fields are validated.
    Precondition: none.
    Expected: the blank form shows all required-field errors."""
    contact = ContactPage(page).open()
    contact.submit()
    expect(contact.errors.first).to_be_visible()
    expect(contact.errors).to_have_count(5)
