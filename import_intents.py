import argparse
import json

from google.api_core.exceptions import FailedPrecondition

from dialogflow_utils import create_intent


def import_intents_from_file(filepath):
    with open(filepath, 'r') as intents_file:
        data = json.load(intents_file)

    for intent_title, intent_data in data.items():
        try:
            create_intent(intent_title, intent_data['questions'], intent_data['answer'])
        except FailedPrecondition:
            print('Failed import: ', intent_title)


def main():
    """ Tool for import questions from JSON file to DialogFlow agent"""

    parser = argparse.ArgumentParser(description='Import intents from file to DialogFlow.')
    parser.add_argument('filepath', type=str, help='path to file for import')

    args = parser.parse_args()
    import_intents_from_file(args.filepath)


if __name__ == '__main__':
    main()
