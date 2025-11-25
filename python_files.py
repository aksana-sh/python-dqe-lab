# Python Module. Files
# Expand previous Homework 5 with additional class, which allow to provide records by text file:
# 1.Define your input format (one or many records)
# 2.Default folder or user provided file path
# 3.Remove file if it was successfully processed
# 4.Apply case normalization functionality form Homework 3/4

import os
from python_classes import NewsFeedPublisher
from python_strings_hw import normalize_letter_case


class FileNewsImporter:
    def __init__(self, publisher: NewsFeedPublisher, input_file_path=None):
        # If no file path is provided, default to 'input_records.txt' in the current working directory
        self.input_file = input_file_path or os.path.join(os.getcwd(), "input_news.txt")
        self.publisher = publisher  # Store the NewsFeedPublisher instance

    def process_file(self):
        # Check if the input file exists
        if not os.path.exists(self.input_file):
            print(f"File '{self.input_file}' not found.")
            return  # Exit if file is missing

        # Read the entire content of the input file
        with open(self.input_file, "r", encoding="utf-8") as file:
            input_news = file.read()

        # Split the content into separate news blocks, remove unintended blank records
        news_blocks = input_news.strip().split("\n\n")

        # Process each news block
        for block in news_blocks:
            # Clean and split each news block into lines, skipping empty lines
            lines = [line.strip() for line in block.strip().split("\n") if line.strip()]
            if not lines:
                continue  # Skip empty lines

            # First line in each block indicates the type of record (News, Private Ad, Horoscope)
            record_type = lines[0].lower()

            # Convert the remaining lines into a dictionary:
            data = {
                line.split(":", 1)[0].strip().lower(): line.split(":", 1)[1].strip()
                for line in lines[1:]
            }

            # Handle News record
            if "news" in record_type:
                # Get and normalize the content for text and city
                text = normalize_letter_case(data.get("text", ""))
                city = data.get("city", "").title()
                # Create formatted news content for publishing
                result, db_record = self.publisher.create_news(text, city)
                if db_record:
                    self.publisher.db_saver.db_insert_news(*db_record)

            # Handle Private Ad record
            elif "private ad" in record_type:
                # Get and normalize (if needed) the content for text and expiration date
                text = normalize_letter_case(data.get("text", ""))
                expiration = data.get("expiration", "")
                # Create formatted private ad content for publishing
                result, db_record = self.publisher.create_private_ad(text, expiration)

                # If the ad has an invalid or past expiration date, skip publishing
                if "Invalid" in result or "cannot be earlier" in result:
                    print(result)
                    continue

                if db_record:
                    self.publisher.db_saver.db_insert_private_ad(*db_record)

            # Handle Horoscope record
            elif "horoscope" in record_type:
                # Get and normalize the sign and horoscope message
                sign = data.get("sign", "")
                message = normalize_letter_case(data.get("message", ""))
                # Create formatted private ad content for publishing
                result, db_record = self.publisher.create_horoscope(sign, message)

                # If the zodiac sign is invalid, skip publishing
                if "Invalid zodiac sign" in result:
                    print(result)
                    continue

                if db_record:
                    self.publisher.db_saver.db_insert_horoscope(*db_record)

            # Handle unknown record types
            else:
                print(f"Unknown record type: {record_type}")
                continue

            # Publish the formatted result to the output file
            self.publisher.publish(result)
            print(f"Published: {record_type}")

        # Delete the input file after processing
        os.remove(self.input_file)
        print(f"File '{self.input_file}' processed and removed.")


if __name__ == "__main__":
    publisher = NewsFeedPublisher()
    importer = FileNewsImporter(publisher)
    importer.process_file()