from gradio_client import Client

# Read text from prompt.txt
with open("prompt.txt", "r") as file:
	prompt = file.read()

client = Client("http://0.0.0.0:7860/")
result = client.predict(
		message=prompt,
		api_name="/chat"
)
print(result)
