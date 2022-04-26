def translate_text_with_model(target, text, model="nmt"):
    """Translates text into the target language.

    Make sure your project is allowlisted.

    Target must be an ISO 639-1 language code.
    See https://g.co/cloud/translate/v2/translate-reference#supported_languages
    """
    from google.cloud import translate_v2 as translate

    translate_client = translate.Client()

    if isinstance(text, bytes):
        text = text.decode("utf-8")

    # Text can also be a sequence of strings, in which case this method
    # will return a sequence of results for each text.
    return translate_client.translate(text, target_language=target, model=model)

from google.cloud import translate_v3beta1 as translate


def translate_document(project_id: str, file_path: str):

    client = translate.TranslationServiceClient()

    location = "us-central1"
   

    parent = f"projects/364396599844/locations/{location}"

    # Supported file types: https://cloud.google.com/translate/docs/supported-formats
    with open(file_path, "rb") as document:
        document_content = document.read()

    document_input_config = {
        "content": document_content,
        "mime_type": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    }

    response = client.translate_document(
        request={
            "parent": parent,
            "target_language_code": "en-US",
            "document_input_config": document_input_config,
        }
    )

    return response.document_translation.byte_stream_outputs[0]
