import frappe

def check_user_limit(doc, method):
    """
    Checks the current user's purchase limit before allowing a Purchase Order to be submitted.
    """
    # Get the current logged-in user
    current_user = frappe.session.user

    # Fetch the user's purchase restriction from the "Purchase Order Limit" Doctype
    restriction = frappe.get_value(
        "Purchase Order Limit",
        {"user": current_user},
        ["set_limit"],
        as_dict=True,
    )

    # If no restriction exists or no limit is set, allow submission
    if not restriction or not restriction.get("set_limit"):
        return

    # Convert the limit to a float
    limit = float(restriction["set_limit"])

    # Custom currency formatting
    def format_currency(amount):
        return f"₦{amount:,.2f}"

    formatted_limit = format_currency(limit)
    formatted_total = format_currency(doc.grand_total)

    # Validate the grand total against the user's limit
    if doc.grand_total > limit:
        frappe.throw(
            f"Purchase Order cannot be submitted. Your limit is {formatted_limit}, but the total is {formatted_total}."
        )
