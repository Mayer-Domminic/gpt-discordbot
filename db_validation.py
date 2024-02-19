def setup_discord_collection(database):
    # Define the validation schema
    validation_schema = {
        '$jsonSchema': {
            'bsonType': 'object',
            'required': ['user_id'],
            'properties': {
                'user_id': {
                    'bsonType': 'string',
                    'description': 'must be a string and is required'
                },
                'channels': {
                    'bsonType': 'array',
                    'description': 'must be an array of channels and is required',
                    'items': {
                        'bsonType': 'object',
                        'required': ['channel_id', 'gpt_type', 'messages'],
                        'properties': {
                            'channel_id': {
                                'bsonType': 'string',
                                'description': 'must be a string and is required'
                            },
                            'gpt_type': {
                                'bsonType': 'string',
                                'description': 'must be a string and is required'
                            },
                            'messages': {
                                'bsonType': 'array',
                                'description': 'must be an array of messages and is required',
                                'items': {
                                    'bsonType': 'object',
                                    'required': ['bot', 'message_id', 'timestamp', 'content'],
                                    'properties': {
                                        'bot': {
                                            'bsonType': 'bool',
                                            'description': 'must be a boolean indicating if the message is from the bot'
                                        },
                                        'message_id': {
                                            'bsonType': 'string',
                                            'description': 'must be a string and is required'
                                        },
                                        'timestamp': {
                                            'bsonType': 'date',
                                            'description': 'must be a date and is required'
                                        },
                                        'content': {
                                            'bsonType': 'string',
                                            'description': 'must be a string and is required'
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }

    # Check if the collection already exists
    if "discord_collection" in database.list_collection_names():
        print("`discord_collection` already exists.")
    else:
        # Create the collection with the defined validation
        database.create_collection(
            'discord_collection',
            validator=validation_schema
        )
        print('Collection `discord_collection` created with the validation schema')