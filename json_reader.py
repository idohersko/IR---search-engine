import json

def read_json_documents():
    # Use a breakpoint in the code line below to debug your script.
    with open('queries_train.json') as json_file:
        data = json.load(json_file)  # Press Ctrl+F8 to toggle the breakpoint.
        set_doc = set()
        for query in data:
            for doc in data[query]:
                set_doc.add(doc)
        print(len(set_doc))


read_json_documents()
