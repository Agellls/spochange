from playwright.sync_api import Playwright, sync_playwright, expect


def get_credentials_from_file(file_path):
    with open(file_path, "r") as file:
        lines = file.readlines()  # read all lines
        for line in lines:
            parts = line.split("|")  # split the line by pipe
            if len(parts) != 2:
                continue  # skip lines that don't have exactly 2 parts
            email_part, password_part = parts
            if "Email :" in email_part and "Password :" in password_part:
                email = email_part.split(":")[1].strip()  # get email
                password = password_part.split(":")[1].strip()  # get password
                return email, password


def get_new_password(file_path):
    with open(file_path, "r") as file:
        password = file.readline().strip()  # read the first line
        return password


def write_result_to_file(email, new_password):
    with open("result.txt", "a") as file:
        file.write(f"{email}:{new_password}\n")


def delete_first_line(file_path):
    with open(file_path, "r") as file:
        lines = file.readlines()  # read all lines
    with open(file_path, "w") as file:
        file.writelines(lines[1:])  # write all lines except the first one


def count_lines(file_path):
    with open(file_path, "r") as file:
        lines = file.readlines()  # read all lines
        return len(lines)


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://open.spotify.com/")
    page.get_by_test_id("login-button").click()
    page.get_by_test_id("login-username").click()
    page.get_by_test_id("login-username").fill(email)
    page.get_by_test_id("login-password").click()
    page.get_by_test_id("login-password").fill(password)
    page.get_by_test_id("login-button").click()
    print("\nLogged in as", email)
    print("Process to change password...")
    page.get_by_test_id("user-widget-link").click()
    with page.expect_popup() as page1_info:
        page.get_by_role("menuitem", name="Account").click()
    page1 = page1_info.value
    page1.get_by_test_id("menu-item-changePassword").get_by_label(
        "Ubah kata sandi"
    ).click()
    page1.get_by_label("Sandi saat ini").click()
    page1.get_by_label("Sandi saat ini").fill(password)
    page1.get_by_label("Kata sandi baru", exact=True).click()
    page1.get_by_label("Kata sandi baru", exact=True).fill(new_password)
    page1.get_by_label("Ulangi kata sandi baru").click()
    page1.get_by_label("Ulangi kata sandi baru").fill(new_password)
    page1.get_by_role("button", name="Atur kata sandi baru").click()
    page1.get_by_role("button", name="Profil Profil").click()
    page1.get_by_role("link", name="Keluar").click()
    print("Password for", email, "has been changed")

    # ---------------------
    context.close()
    browser.close()


num_lines = count_lines("email-pass.txt")

with sync_playwright() as playwright:
    for _ in range(num_lines):
        email, password = get_credentials_from_file("email-pass.txt")
        new_password = get_new_password("new-password.txt")  # Move this line here
        run(playwright)
        write_result_to_file(email, new_password)
        delete_first_line("email-pass.txt")
