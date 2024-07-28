import openai
import os

openai.api_key = 'API-key'

def generate_response(messages):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            max_tokens=150,
            temperature=0.7
        )
        return response.choices[0].message['content'].strip()
    except Exception as e:
        return f"An error occurred: {e}"

def start_conversation():
    print("\n** Family Role-Playing Simulation **")
    roles = {
        "Parent": "You are a parent dealing with a complex family issue. Your goal is to provide guidance, offer understanding, and find a resolution.",
        "Child": "You are a child expressing your feelings and thoughts about the situation. Your responses should be honest and reflect your current state."
    }
    
    print("Available Roles:")
    for role in roles.keys():
        print(f"- {role}")
    
    role = input("Choose your role (Parent, Child): ")
    if role not in roles:
        print("Invalid role selected.")
        return
    
    problem = input("Describe the problem or situation you'd like to discuss: ")
    
    # Initial AI response
    messages = [
        {"role": "system", "content": f"You are a {role} in a family discussion."},
        {"role": "user", "content": f"Situation: {roles[role]}\nProblem: {problem}"}
    ]
    
    ai_response = generate_response(messages)
    print(f"\nAI Response as {role}: {ai_response}")
    
    while True:
        user_input = input("\nYour response (type 'exit' to end the conversation): ")
        if user_input.lower() == 'exit':
            print("Ending the conversation.")
            break
        
        # Add user response and get updated AI response
        messages.append({"role": "user", "content": user_input})
        ai_response = generate_response(messages)
        
        print(f"\nAI Response as {role}: {ai_response}")

def main():
    while True:
        print("\n** Role-Playing Scenarios **")
        print("1. Start Family Role-Playing Simulation")
        print("2. Exit")
        
        choice = input("Select an option (1-2): ")
        
        if choice == '1':
            start_conversation()
        elif choice == '2':
            print("Exiting the role-playing scenarios. Have a great day!")
            break
        else:
            print("Invalid choice, please select a number between 1 and 2.")

if __name__ == "__main__":
    main()