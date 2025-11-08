import autogen

# 🔹 LLM Configuration
llm_config = {
    "model": "gemini-1.5-flash-latest",
    "api_key": "AIzaSyDLffsf61ikJOKA1VkkiA3juLdr_5f9Axs",
    "api_type": "google",
    "temperature": 0.7  
}

# 🔹 Task Definition - Samsung S25 Ultra Product Descriptions
task = '''
Create 10 variations of Amazon product descriptions for the Samsung S25 Ultra, 
optimized for Indian buyers nationwide. Each description must:
1. Present technical specifications in simple terms
2. Highlight India-specific features (network, climate adaptability, multi-language UI)
3. Appeal to diverse consumers (urban professionals, gamers, students, travelers)
4. Compare Samsung S25 Ultra vs. competitors (Apple iPhone 15 Pro, OnePlus 12, Google Pixel 8)
Keep each description under 80 words and ensure high engagement.
'''

# 🔹 Main Writer Agent (Generates Descriptions)
writer = autogen.AssistantAgent(
    name="Product_Writer",
    system_message="""
    You are an e-commerce content specialist creating Amazon product descriptions 
    for the Samsung S25 Ultra, tailored for the Indian market. Your descriptions must:
    1. Use professional and engaging business English.
    2. Highlight features relevant to Indian consumers (climate resistance, 5G, fast charging).
    3. Appeal to different consumer segments (gamers, professionals, students).
    4. Include clear technical specifications in easy language.
    5. Compare Samsung S25 Ultra with competitors (Apple, OnePlus, Google).
    Provide 10 unique product descriptions without any extra commentary.
    """,
    llm_config=llm_config
)

# ✍️ Generate Product Descriptions
reply = writer.generate_reply(messages=[{"content": task, "role": "user"}])
reply

# 🔹 Critic Agent (Reviews and Provides Feedback)
critic = autogen.AssistantAgent(
    name="Critic",
    is_termination_msg=lambda x: x.get("content", "").find("TERMINATE") >= 0,
    llm_config=llm_config,
    system_message="""
    You are a quality assurance specialist reviewing e-commerce product descriptions. 
    Evaluate the descriptions for:
    1. Technical accuracy
    2. Market relevance
    3. Clarity and engagement
    Provide feedback and suggestions for improvement.
    """
)

result = critic.initiate_chat(
    recipient=writer,
    message=task,
    max_turns=2,
    summary_method="last_msg"
)

import pprint
pprint.pprint(result)

result.cost 

# 🔹 Market Analyst (Ensures Relevance for Indian Buyers)
market_analyst = autogen.AssistantAgent(
    name="Market_Analyst",
    llm_config=llm_config,
    system_message="""
    You analyze Samsung S25 Ultra descriptions for Indian market suitability.
    Verify:
    1. Appeal across different regions (urban, rural)
    2. Network compatibility (Jio, Airtel, Vi, BSNL)
    3. Climate adaptability mentions (heat resistance, dust protection)
    4. Cultural neutrality and relevance
    Provide suggestions for improvement.
    """
)

# 🔹 Tech Reviewer (Ensures Accurate Specs & Features)
tech_reviewer = autogen.AssistantAgent(
    name="Tech_Reviewer",
    llm_config=llm_config,
    system_message="""
    You validate technical claims in Samsung S25 Ultra product descriptions.
    Check:
    1. Specification accuracy (Processor, Camera, Display, Battery, AI features)
    2. Feature explanations (S Pen, AI enhancements, camera zoom, 5G compatibility)
    3. Performance claims (Gaming, multitasking, battery life)
    4. Compatibility statements (5G, Wi-Fi 7, Fast Charging)
    Flag any misleading or unclear technical information.
    """
)

# 🔹 Legal Reviewer (Ensures Compliance with Indian E-Commerce Laws)
legal_reviewer = autogen.AssistantAgent(
    name="Legal_Reviewer",
    llm_config=llm_config,
    system_message="""
    You ensure compliance with Indian e-commerce regulations for Samsung S25 Ultra.
    Verify:
    1. Transparent pricing and warranty information
    2. Accuracy of environmental and sustainability claims
    3. Consumer protection adherence (return policy, disclaimers)
    Highlight any legal risks.
    """
)

# 🔹 Meta Reviewer (Final Review & Summary)
meta_reviewer = autogen.AssistantAgent(
    name="Meta_Reviewer",
    llm_config=llm_config,
    system_message="""
    You consolidate all reviews into an executive summary:
    1. Critical fixes (must be addressed)
    2. Recommended improvements
    3. Optional enhancements
    Provide final recommendations in a clear and structured format.
    """
)

# 🔹 Function for Passing Messages Between Reviewers
def reflection_message(recipient, messages, sender, config):
    return f"Please review this product description batch:\n\n{messages[-1]['content']}"

# 🔹 Review Process (Nested Reviews)
review_chats = [
    {
        "recipient": market_analyst,
        "message": reflection_message,
        "summary_method": "reflection_with_llm",
        "summary_args": {
            "summary_prompt": "Return as JSON: {'reviewer':'Market', 'feedback':[]}"
        },
        "max_turns": 1
    },
    {
        "recipient": tech_reviewer,
        "message": reflection_message,
        "summary_method": "reflection_with_llm",
        "summary_args": {
            "summary_prompt": "Return as JSON: {'reviewer':'Technical', 'feedback':[]}"
        },
        "max_turns": 1
    },
    {
        "recipient": legal_reviewer,
        "message": reflection_message,
        "summary_method": "reflection_with_llm",
        "summary_args": {
            "summary_prompt": "Return as JSON: {'reviewer':'Legal', 'feedback':[]}"
        },
        "max_turns": 1
    },
    {
        "recipient": meta_reviewer,
        "message": "Consolidate all feedback into prioritized action items",
        "max_turns": 1
    }
]

# 🔹 Register Nested Chats with Critic
critic.register_nested_chats(review_chats, trigger=writer)

# 🔹 Execute the Task
user_proxy = autogen.UserProxyAgent(
    name="Ecommerce_Manager",
    human_input_mode="NEVER",
    default_auto_reply="Continuing...",
    code_execution_config=False
)


result = critic.initiate_chat(
    recipient=writer,
    message=task,
    max_turns=2,
    summary_method="last_msg"
)

# 🔹 Print the Final Product Descriptions
print("\n🔷 FINAL SAMSUNG S25 ULTRA PRODUCT DESCRIPTIONS 🔷\n")
print(result)

import pprint
pprint.pprint(result)

result.cost 