# Python Classes. OOP HW
# Create a tool, which will do user generated news feed:
# 1.User select what data type he wants to add
# 2.Provide record type required data
# 3.Record is published on text file in special format
#
# You need to implement:
# 1.News – text and city as input. Date is calculated during publishing.
# 2.Privat ad – text and expiration date as input. Day left is calculated during publishing.
# 3.Your unique one with unique publish rules.

import datetime


class NewsFeedPublisher:
    # List of valid zodiac signs for horoscope validation
    ZODIAC_SIGNS = {
        "aries", "taurus", "gemini", "cancer", "leo", "virgo",
        "libra", "scorpio", "sagittarius", "capricorn", "aquarius", "pisces"
    }

    def __init__(self, news_file="news_feed.txt"):
        # Initialize with a default output file to store news
        self.news_file = news_file

    def create_news(self, text: str, city: str) -> str:
        # Get current date and time in readable string format
        news_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        # Format the news content
        news_content = f"NEWS -----\n{text}\n{city}, {news_date}"
        return news_content

    def create_private_ad(self, text: str, expiration_date: str) -> str:
        try:
            # Convert expiration date string to datetime
            exp_date = datetime.datetime.strptime(expiration_date, "%Y-%m-%d")
            today = datetime.datetime.now()

            # Check if expiration date is in the past
            if exp_date.date() < today.date():
                return "Expiration date cannot be earlier than today."

            # Calculate days left until expiration
            days_left = (exp_date - datetime.datetime.now()).days
            # Format the private ad content
            private_ad_content = f"PRIVATE AD -----\n{text}\nActual until: {expiration_date}, {days_left} days left"
            return private_ad_content
        except ValueError:
            # Handle invalid date format
            return "Invalid expiration date format. Use YYYY-MM-DD."

    def create_horoscope(self, sign: str, message: str) -> str:
        # Validate zodiac sign
        if sign.lower() not in self.ZODIAC_SIGNS:
            return f"Invalid zodiac sign: '{sign}'. Please enter one of: {', '.join(self.ZODIAC_SIGNS)}"
        # Get current date in readable string format
        date_str = datetime.datetime.now().strftime("%Y-%m-%d")
        # Format the horoscope content
        horoscope_content = f"HOROSCOPE -----\nSign: {sign.capitalize()}\n{message}\nDate: {date_str}"
        return horoscope_content

    def publish(self, content: str):
        # Append the formatted content to the file
        with open(self.news_file, "a", encoding="utf-8") as file:
            file.write(content + "\n\n")  # Add spacing between news records

    def process_news_input(self):
        # Display menu options for user
        print("Choose record type to add:")
        print("1 – News")
        print("2 – Private Ad")
        print("3 – Horoscope")

        # Get user choice
        user_choice = input("Enter your choice (1/2/3): ").strip()

        # Initialize new record as empty
        record = ""

        # Handle News entry
        if user_choice == "1":
            text = input("Enter news text: ")
            city = input("Enter city: ")
            record = self.create_news(text, city)

        # Handle Private Ad entry
        elif user_choice == "2":
            text = input("Enter private ad text: ")
            expiration_date = input("Enter expiration date (YYYY-MM-DD): ")
            record = self.create_private_ad(text, expiration_date)

            # Check for validation errors
            if "Invalid expiration date format" in record or "cannot be earlier" in record:
                print(record)
                return

        # Handle Horoscope entry
        elif user_choice == "3":
            sign = input("Enter your zodiac sign: ")
            message = input("Enter horoscope message: ")
            record = self.create_horoscope(sign, message)

            # Check for validation errors
            if "Invalid zodiac sign" in record:
                print(record)
                return

        # Handle invalid type user choice
        else:
            print("Invalid choice.")
            return

        # Save the news record to file
        self.publish(record)
        print("Record published successfully!")


# Start the tool
if __name__ == "__main__":
    NewsFeedPublisher().process_news_input()
