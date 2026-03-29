from google import genai

client = genai.Client(api_key="AIzaSyDastxpOPVrJ13HQJikc_4e4PhHs4l9tF4")

models = client.models.list()

for m in models:
    print(m.name)