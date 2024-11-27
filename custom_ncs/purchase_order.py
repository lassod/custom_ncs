import frappe
import locale

def check_user_limit(doc, method):
    """
    Checks the current user's purchase limit before allowing a Purchase Order to be submitted.
    """

    # Get the current logged-in user
    current_user = frappe.session.user

    # Fetch the user's purchase restriction from the "Purchase Order Limit" Doctype
    restriction = frappe.get_value(
        "Purchase Order Limit",
        {"user": current_user},  # Filters by the current user
        ["set_limit"],  # Fetches the "set_limit" field
        as_dict=True,
    )

    # If no restriction exists or no limit is set, allow submission
    if not restriction or not restriction.get("set_limit"):
        return

    # Convert the limit to a float
    limit = float(restriction["set_limit"])

    # Set locale for Nigerian currency format (optional: ensure the locale is installed)
    try:
        locale.setlocale(locale.LC_ALL, 'en_NG')  # Nigerian English locale
    except locale.Error:
        locale.setlocale(locale.LC_ALL, '')  # Default locale fallback

    # Format the values
    formatted_limit = locale.currency(limit, grouping=True, symbol=True)
    formatted_total = locale.currency(doc.grand_total, grouping=True, symbol=True)

    # Validate the grand total against the user's limit
    if doc.grand_total > limit:
        frappe.throw(
            f"Purchase Order cannot be submitted. Your limit is {formatted_limit}, but the total is {formatted_total}."
        )
