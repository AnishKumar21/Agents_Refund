
import sys
from pathlib import Path
from uuid import uuid4

sys.path.insert(
    0,
    str(Path(__file__).resolve().parents[1] / "agent"),
)

from agent import agent
from evaluations.dataset import dataset
from deepeval.integrations.langchain import CallbackHandler


def extract_tool_names(response):
    """Extract tool names from LangChain's returned messages."""
    tool_names = []

    for message in response.get("messages", []):
        # AI messages contain tool calls.
        for tool_call in getattr(message, "tool_calls", []) or []:
            name = tool_call.get("name")
            if name:
                tool_names.append(name)

        # Tool messages identify the tool that actually executed.
        if getattr(message, "type", None) == "tool":
            name = getattr(message, "name", None)
            if name:
                tool_names.append(name)

    return tool_names


def check_case(golden, answer, actual_tools):
    """Run basic checks against the expected answer and tools."""
    expected_tools = [
        tool.name for tool in (golden.expected_tools or [])
    ]

    # Check that every expected tool was called.
    missing_tools = [
        name for name in expected_tools
        if name not in actual_tools
    ]
    tools_pass = not missing_tools

    # Scenario-specific checks.
    case_input = golden.input.lower()
    answer_lower = answer.lower()

    if "book and the pen" in case_input:
        answer_pass = (
            "30" in answer_lower
            and "refund" in answer_lower
        )
    elif "refund for the book" in case_input and "user123" in case_input:
        answer_pass = (
            "23" in answer_lower
            and "refund" in answer_lower
        )
    elif "just want to know what i purchased" in case_input:
        answer_pass = (
            "book" in answer_lower
            and "pen" in answer_lower
            and "issue_refund_ticket" not in actual_tools
        )
    elif "user999" in case_input:
        answer_pass = (
            "username" in answer_lower
            or "valid" in answer_lower
        )
    elif "water bottle" in case_input and "backpack" not in case_input:
        answer_pass = (
            "30" in answer_lower
            and (
                "not eligible" in answer_lower
                or "outside" in answer_lower
                or "not qualify" in answer_lower
            )
            and "issue_refund_ticket" not in actual_tools
        )
    elif "backpack and water bottle" in case_input:
        answer_pass = (
            "45" in answer_lower
            and "backpack" in answer_lower
            and "water bottle" in answer_lower
        )
    elif "sneakers" in case_input:
        answer_pass = (
            "not purchased" in answer_lower
            or "no purchase" in answer_lower
            or "not found" in answer_lower
        ) and "issue_refund_ticket" not in actual_tools
    else:
        answer_pass = bool(answer.strip())

    return answer_pass, tools_pass, missing_tools


def main():
    results = []

    for index, golden in enumerate(dataset.goldens, start=1):
        print(f"\n{'=' * 60}")
        print(f"Test {index}/{len(dataset.goldens)}")
        print(f"Input: {golden.input}")

        config = {
            "configurable": {"thread_id": str(uuid4())},
            "callbacks": [CallbackHandler()],
        }

        try:
            response = agent.invoke(
                {"messages": [{"role": "user", "content": golden.input}]},
                config=config,
            )

            messages = response.get("messages", [])
            answer = str(messages[-1].content) if messages else ""
            actual_tools = extract_tool_names(response)

            answer_pass, tools_pass, missing_tools = check_case(
                golden, answer, actual_tools
            )

            print(f"\nAgent answer:\n{answer}")
            print(f"\nTools called: {actual_tools}")
            print(f"Answer check: {'PASS' if answer_pass else 'FAIL'}")
            print(f"Tool check:   {'PASS' if tools_pass else 'FAIL'}")

            if missing_tools:
                print(f"Missing expected tools: {missing_tools}")

            passed = answer_pass and tools_pass
            results.append((index, passed))

        except Exception as exc:
            print(f"ERROR: {type(exc).__name__}: {exc}")
            results.append((index, False))

    print(f"\n{'=' * 60}")
    print("EVALUATION SUMMARY")

    for index, passed in results:
        print(f"Test {index}: {'PASS' if passed else 'FAIL'}")

    passed_count = sum(passed for _, passed in results)
    total = len(results)

    print(f"\nScore: {passed_count}/{total}")
    if total:
        print(f"Pass rate: {passed_count / total:.1%}")


if __name__ == "__main__":
    main()
