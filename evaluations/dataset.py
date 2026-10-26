
from deepeval.dataset import EvaluationDataset, Golden
from deepeval.test_case import ToolCall


dataset = EvaluationDataset(
    goldens=[
        # 1. Eligible items: calculate the amount and ask for confirmation.
        Golden(
            input=(
                "I am user123, I would like a refund for the book and the pen"
            ),
            expected_output=(
                "The eligible refund amount is $30 for the book and pen. "
                "Ask the user to confirm before issuing the refund ticket."
            ),
            expected_tools=[
                ToolCall(name="get_user_purchase_history"),
                ToolCall(name="get_today_date"),
                ToolCall(name="calculate_right_refund"),
            ],
        ),

        # 2. Single eligible item: ask for confirmation.
        Golden(
            input="I am user123, I would like a refund for the book",
            expected_output=(
                "The eligible refund amount is $23 for the book. "
                "Ask the user to confirm before issuing the refund ticket."
            ),
            expected_tools=[
                ToolCall(name="get_user_purchase_history"),
                ToolCall(name="get_today_date"),
                ToolCall(name="calculate_right_refund"),
            ],
        ),

        # 3. Purchase-history request: no refund action.
        Golden(
            input=(
                "I am user123, I would like no refund, "
                "I just want to know what I purchased"
            ),
            expected_output=(
                "List the items purchased by user123. "
                "Do not calculate or issue a refund."
            ),
            expected_tools=[
                ToolCall(name="get_user_purchase_history"),
            ],
        ),

        # 4. Unknown username: do not proceed with a refund.
        Golden(
            input="I am user999, I would like a refund for the book",
            expected_output=(
                "Explain that the purchase history could not be found "
                "and ask the user to verify their username."
            ),
            expected_tools=[
                ToolCall(name="get_user_purchase_history"),
            ],
        ),

        # 5. Ineligible item: explain the 30-day policy.
        Golden(
            input="I am user126, I would like a refund for the water bottle",
            expected_output=(
                "Explain that the water bottle is outside the 30-day "
                "refund window. Do not issue a refund ticket."
            ),
            expected_tools=[
                ToolCall(name="get_user_purchase_history"),
                ToolCall(name="get_today_date"),
            ],
        ),

        # 6. Mixed eligibility: offer the backpack refund only.
        Golden(
            input=(
                "I am user126, I would like a refund "
                "for the backpack and water bottle"
            ),
            expected_output=(
                "The backpack is eligible for a $45 refund. "
                "The water bottle is outside the 30-day refund window. "
                "Ask for confirmation before issuing a ticket for "
                "the backpack. Do not refund the water bottle."
            ),
            expected_tools=[
                ToolCall(name="get_user_purchase_history"),
                ToolCall(name="get_today_date"),
                ToolCall(name="calculate_right_refund"),
            ],
        ),

        # 7. Item not purchased: no refund action.
        Golden(
            input="I am user123, I would like a refund for sneakers",
            expected_output=(
                "Explain that sneakers do not appear in user123's "
                "purchase history. Do not issue a refund ticket."
            ),
            expected_tools=[
                ToolCall(name="get_user_purchase_history"),
            ],
        ),
    ]
)
