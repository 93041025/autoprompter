import openai
import json

# Set up your OpenAI API key
openai.api_key = "your_openai_api_key_here"

# Read the text from the file
def read_until_specific_char(file, specific_char="$$"):
    result = []
    while True:
        c = file.read(1)
        if not c or c == specific_char:
            break
        result.append(c)
    return "".join(result)

# Generate a prompt for the completion using OpenAI API
def generate_prompt(completion):
    response = openai.Completion.create(
        engine="davinci-codex",
        prompt=f"Given the text below, generate a relevant prompt for the completion:\n\n---\n{completion}\n---",
        max_tokens=50,
        n=1,
        stop=None,
        temperature=0.5,
    )
    generated_prompt = response.choices[0].text.strip()
    return generated_prompt

# Main function
def main():
    with open("input.txt", "r") as file, open("generated.txt", "w") as output_file:
        first = True
        while True:
            completion = read_until_specific_char(file)
            if not completion:
                break
            generated_prompt = generate_prompt(completion)
            generated_pair = {
                "prompt": generated_prompt,
                "completion": completion.rstrip(specific_char)
            }
            if first:
                first = False
            else:
                output_file.write(",\n")
            json.dump(generated_pair, output_file)
            if file.read(1) == "":
                break

if __name__ == "__main__":
    main()
