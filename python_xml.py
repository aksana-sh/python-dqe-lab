# Python XML
# Expand previous Homework 5/6/7/8 with additional class, which allow to provide records by XML file:
# 1.Define your input format (one or many records)
# 2.Default folder or user provided file path
# 3.Remove file if it was successfully processed


import os
import xml.etree.ElementTree as ET
from python_classes import NewsFeedPublisher
from python_strings_hw import normalize_letter_case


class XMLNewsImporter:
    def __init__(self, publisher: NewsFeedPublisher, input_file_path=None):
        # If no file path is provided, default to 'xml_input_news.xml' in current directory
        self.input_file = input_file_path or os.path.join(os.getcwd(), "xml_input_news.xml")
        self.publisher = publisher

    def process_xml_file(self):
        # Check if the XML file exists
        if not os.path.exists(self.input_file):
            print(f"File '{self.input_file}' not found.")
            return

        try:
            # Parse the XML file and get the root element
            tree = ET.parse(self.input_file)
            root = tree.getroot()
        except ET.ParseError as e:
            # Handle invalid XML format
            print(f"Invalid XML format: {e}")
            return

        # Iterate through each record in the XML
        for record in root.findall("record"):
            # Get the type value of the record and normalize it to lowercase
            record_type = record.get("type", "").lower()

            # Handle News
            if "news" in record_type:
                # Extract and normalize text and city
                text = normalize_letter_case(record.findtext("text", ""))
                city = record.findtext("city", "").title()
                # Generate formatted news content
                result, db_record = self.publisher.create_news(text, city)
                if db_record:
                    self.publisher.db_saver.db_insert_news(*db_record)

            # Handle Private Ad
            elif "private ad" in record_type:
                # Extract and normalize text and expiration date
                text = normalize_letter_case(record.findtext("text", ""))
                expiration = record.findtext("expiration", "")
                # Generate formatted private ad content
                result, db_record = self.publisher.create_private_ad(text, expiration)

                # Skip publishing if expiration is invalid or in the past
                if "Invalid" in result or "cannot be earlier" in result:
                    print(result)
                    continue

                if db_record:
                    self.publisher.db_saver.db_insert_private_ad(*db_record)

            # Handle Horoscope
            elif "horoscope" in record_type:
                # Extract and normalize zodiac sign and message
                sign = record.findtext("sign", "")
                message = normalize_letter_case(record.findtext("message", ""))
                # Generate formatted horoscope content
                result, db_record = self.publisher.create_horoscope(sign, message)

                # Skip publishing if zodiac sign is invalid
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

        # Delete the XML file after successful processing
        os.remove(self.input_file)
        print(f"File '{self.input_file}' processed and removed.")


if __name__ == "__main__":
    publisher = NewsFeedPublisher()

    # Process XML records
    xml_importer = XMLNewsImporter(publisher)
    xml_importer.process_xml_file()
