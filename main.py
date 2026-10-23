from agent import PersonalAgent


def main():
    print("=" * 55)
    print("  Personal AI Agent (Powered by Free Gemini API)")
    print("  Type 'exit' or 'quit' to stop the agent.")
    print("=" * 55)

    try:
        agent = PersonalAgent()
    except Exception as e:
        print(f"\n[Startup Error] {e}")
        return

    while True:
        try:
            user_input = input("\nYou: ").strip()
            if not user_input:
                continue
            if user_input.lower() in {"exit", "quit", "bye"}:
                print("\nAgent: Goodbye! Have a great day.")
                break

            print("\nAgent is thinking...")
            reply = agent.ask(user_input)
            print(f"\nAgent:\n{reply}")

        except (KeyboardInterrupt, EOFError):
            print("\n\nAgent: Session ended. Goodbye!")
            break


if __name__ == "__main__":
    main()