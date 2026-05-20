import random
import string


# This is the base URL shown to the user for every shortened link.
BASE_SHORT_URL = "short.ly/"

# This dictionary stores the relationship between a short code and the original URL.
# Example:
# {
#     "Ab12Cd": "https://www.example.com/very/long/link"
# }
url_mapping = {}


def generate_short_code(existing_codes):
    """Generate a unique 6-character short code."""
    characters = string.ascii_letters + string.digits

    while True:
        short_code = "".join(random.choice(characters) for _ in range(6))

        # Keep generating codes until we find one that is not already used.
        if short_code not in existing_codes:
            return short_code


def get_non_blank_input(prompt_text):
    """Ask the user for input and reject blank answers."""
    while True:
        user_input = input(prompt_text).strip()

        if user_input:
            return user_input

        print("Input cannot be blank. Please try again.")


def shorten_url():
    """Ask the user for a long URL and create a short URL for it."""
    original_url = get_non_blank_input("Enter the long URL: ")
    short_code = generate_short_code(url_mapping)
    url_mapping[short_code] = original_url

    print(f"Short URL created: {BASE_SHORT_URL}{short_code}")


def expand_url():
    """Ask the user for a short URL or code and show the original URL."""
    user_input = get_non_blank_input(
        "Enter the short URL or short code: "
    )

    # Allow the user to paste either:
    # short.ly/abc123
    # or just:
    # abc123
    if user_input.startswith(BASE_SHORT_URL):
        short_code = user_input[len(BASE_SHORT_URL):]
    else:
        short_code = user_input

    original_url = url_mapping.get(short_code)

    if original_url:
        print(f"Original URL: {original_url}")
    else:
        print("Short code not found. Please check it and try again.")


def view_all_urls():
    """Display every saved short URL and its original URL."""
    if not url_mapping:
        print("No URLs have been shortened yet.")
        return

    print("\nSaved URLs:")
    for short_code, original_url in url_mapping.items():
        print(f"{BASE_SHORT_URL}{short_code} -> {original_url}")


def display_menu():
    """Show the main menu options."""
    print("\nURL Shortener Menu")
    print("1. Shorten URL")
    print("2. Expand short URL")
    print("3. View all saved URLs")
    print("4. Quit")


def main():
    """Run the URL shortener program."""
    print("Welcome to the Python URL Shortener!")

    while True:
        display_menu()
        choice = input("Choose an option (1-4): ").strip()

        if choice == "1":
            shorten_url()
        elif choice == "2":
            expand_url()
        elif choice == "3":
            view_all_urls()
        elif choice == "4":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please enter 1, 2, 3, or 4.")


if __name__ == "__main__":
    main()
