import nltk

# Add the custom package directories to nltk.data.path
nltk.data.path.append('C:\\Users\\premh\\AppData\\Roaming\\Python\\Python311\\site-packages')
nltk.data.path.append('C:\\Program Files\\Python311\\Lib\\site-packages')


from nltk import word_tokenize, pos_tag, ne_chunk

def extract_entities(text):
    # Tokenize the input text
    tokens = word_tokenize(text)
    
    # Perform part-of-speech (POS) tagging
    tagged_tokens = pos_tag(tokens)
    
    # Perform named entity recognition (NER)
    ner_tree = ne_chunk(tagged_tokens)
    
    # List to store the extracted entities
    entities = []
    
    # Traverse the NER tree and extract entities
    for subtree in ner_tree:
        if hasattr(subtree, 'label') and subtree.label() is not None:
            entity_type = subtree.label()
            entity_text = " ".join(word for word, tag in subtree.leaves())
            entities.append((entity_text, entity_type))
    
    return entities

# Test the function
text = "Please contact John Smith at john@example.com or call +1 (123) 456-7890."
entities = extract_entities(text)

# Print the extracted entities
for entity, entity_type in entities:
    print(f"Entity: {entity} | Type: {entity_type}")
