from medical_agent import get_response

while True:
    print("*-"*150)
    text = input("\nEnter: ")
    output = get_response(text.lower())
    print("\n")
    print("*-"*150)
    print(output)
