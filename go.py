import json

with open("ui\camera_index.json", "rt", encoding="utf-8") as file:
    settings = json.load(file)

settings["ri"] = "cyberforum"

with open("ui\camera_index.json", "wt", encoding="utf-8") as file:
    json.dump(settings, file, indent=1)