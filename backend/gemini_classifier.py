def rule_based_fallback(query):
    q = query.lower()

    if "refund" in q:
        return "Refund Request"
    elif "late" in q or "delay" in q:
        return "Delivery Delay"
    elif "track" in q or "where is my order" in q:
        return "Order Tracking"
    elif "payment" in q or "deducted" in q:
        return "Payment Failure"
    elif "subscription" in q:
        return "Subscription Issue"
    elif "broken" in q or "damaged" in q or "quality" in q:
        return "Product Issue"
    elif len(q.strip()) < 5:
        return "Ambiguous"

    return "General Query"


def classify_query_with_gemini(query):
    try:
        prompt = f"""
        Classify this query into one category:
        [Order Tracking, Delivery Delay, Refund Request, Product Issue, Payment Failure, Subscription Issue, General Query, Ambiguous]

        Query: "{query}"

        Return only category name.
        """

        response = model.generate_content(prompt)
        category = response.text.strip()

        allowed = [
            "Order Tracking", "Delivery Delay", "Refund Request",
            "Product Issue", "Payment Failure", "Subscription Issue",
            "General Query", "Ambiguous"
        ]

        if category not in allowed:
            return rule_based_fallback(query)

        return category

    except:
        return rule_based_fallback(query)