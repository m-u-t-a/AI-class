from gigachat import GigaChat
from datetime import datetime

def ask_gigachat_and_save_response(question: str, output_file: str = "gigachat_response.txt"):
    try:
        # Client init
        giga = GigaChat(credentials="ZDkxYWIyYWQtNzA3Zi00MGM3LWJkZDItMzYyYmFlMmY5ZTU1OjMzYTk5MWM2LWZkOGUtNDkyMS05MGFlLTE2MjdhZDVlZGI2OQ==", verify_ssl_certs=False)

        # Get token, check connection
        token = giga.get_token()
        print("Successfully connect to GigaChat API")

        # Sending request (text generation this time)
        print(f"Sending request: '{question}'")
        response = giga.chat(question)
        answer = response.choices[0].message.content

        file_content = f"""=== REQUEST ===
Date/Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Question: {question}

=== ANSWER ===
{answer}
"""
        with open(output_file, "w", encoding="utf-8") as file:
            file.write(file_content)

        print(f"Answer saved to '{output_file}'")

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    # Example
    QUESTION = "Какие основные принципы обработки обращений граждан в органы власти?"
    OUTPUT_FILE = "gigachat_response.txt"

    ask_gigachat_and_save_response(QUESTION, OUTPUT_FILE)
