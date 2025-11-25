# Python JSON module
# Expand previous Homework 5/6/7 with additional class, which allow to provide records by JSON file:
# 1.Define your input format (one or many records)
# 2.Default folder or user provided file path
# 3.Remove file if it was successfully processed


import os
import json
from python_classes import NewsFeedPublisher
from python_strings_hw import normalize_letter_case


class JSONNewsImporter:
    def __init__(self, publisher: NewsFeedPublisher, input_file_path=None):
        # If no file path is provided, default to 'json_input_news.json' in current directory
        self.input_file = input_file_path or os.path.join(os.getcwd(), "json_input_news.json")
        self.publisher = publisher

    def process_json_file(self):
        # Check if the input file exists
        if not os.path.exists(self.input_file):
            print(f"File '{self.input_file}' not found.")
            return

        # Check if input data provided in the JSON format, load JSON content
        with open(self.input_file, "r", encoding="utf-8") as file:
            try:
                news = json.load(file)
            except json.JSONDecodeError as e:
                print(f"Invalid JSON format: {e}")
                return

        # Additional check if file content is a list as expected
        if not isinstance(news, list):
            print("JSON file must contain a list of records.")
            return

        # Process each news block
        for block in news:
            record_type = block.get("type", "").lower()

            if "news" in record_type:
                text = normalize_letter_case(block.get("text", ""))
                city = block.get("city", "").title()
                result, db_record = self.publisher.create_news(text, city)
                if db_record:
                    self.publisher.db_saver.db_insert_news(*db_record)


            elif "private ad" in record_type:
                text = normalize_letter_case(block.get("text", ""))
                expiration = block.get("expiration", "")
                result, db_record = self.publisher.create_private_ad(text, expiration)

                if "Invalid" in result or "cannot be earlier" in result:
                    print(result)
                    continue

                if db_record:
                    self.publisher.db_saver.db_insert_private_ad(*db_record)

            elif "horoscope" in record_type:
                sign = block.get("sign", "")
                message = normalize_letter_case(block.get("message", ""))
                result, db_record = self.publisher.create_horoscope(sign, message)

                if "Invalid zodiac sign" in result:
                    print(result)
                    continue

                if db_record:
                    self.publisher.db_saver.db_insert_horoscope(*db_record)

            else:
                print(f"Unknown record type: {record_type}")
                continue

            self.publisher.publish(result)
            print(f"Published: {record_type}")

        # Delete the file after successful processing
        os.remove(self.input_file)
        print(f"File '{self.input_file}' processed and removed.")


if __name__ == "__main__":
    publisher = NewsFeedPublisher()

    # Process JSON records
    json_importer = JSONNewsImporter(publisher)
    json_importer.process_json_file()