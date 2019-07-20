import os

import dialogflow_v2 as dialogflow


def get_answer(message_text, session_id):
    """ Get agent answer for client message """

    project_id = os.environ.get('DIALOG_FLOW_PROJECT_ID')

    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)

    text_input = dialogflow.types.TextInput(text=message_text, language_code='ru')
    query_input = dialogflow.types.QueryInput(text=text_input)
    response = session_client.detect_intent(session=session, query_input=query_input)

    return response.query_result.fulfillment_text, response.query_result.intent.display_name


def create_intent(title, questions, answer):
    """ Create intent in agent """

    project_id = os.environ.get('DIALOG_FLOW_PROJECT_ID')

    intents_client = dialogflow.IntentsClient()
    parent = intents_client.project_agent_path(project_id)

    training_phrases = []
    for question in questions:
        part = dialogflow.types.Intent.TrainingPhrase.Part(text=question)
        training_phrase = dialogflow.types.Intent.TrainingPhrase(parts=[part])
        training_phrases.append(training_phrase)

    text = dialogflow.types.Intent.Message.Text(text=[answer])
    message = dialogflow.types.Intent.Message(text=text)

    intent = dialogflow.types.Intent(
        display_name=title,
        training_phrases=training_phrases,
        messages=[message])

    response = intents_client.create_intent(parent, intent)

    return response
