"""
dairy_management/utils/calculations.py
Fat/SNF Price Calculation Engine — called on Milk Collection Entry before_save
"""
import frappe
from frappe.utils import flt


def get_milk_rate(fat: float, snf: float, route: str = None, date: str = None) -> float:
    """
    Look up rate from the active Rate Slab for the given fat and SNF percentages.
    Falls back to base_rate if no matching matrix row found.
    """
    slab = frappe.db.get_value(
        "Rate Slab",
        {
            "effective_from": ["<=", date or frappe.utils.today()],
            "effective_to": [">=", date or frappe.utils.today()],
            "disabled": 0,
        },
        ["name", "base_rate"],
        order_by="effective_from desc",
        as_dict=True,
    )

    if not slab:
        frappe.throw("No active Rate Slab found for the collection date.")

    # Look up matrix row matching fat and snf ranges
    rate = frappe.db.sql(
        """
        SELECT rate_per_litre FROM `tabRate Slab Row`
        WHERE parent = %s
          AND fat_from <= %s AND fat_to >= %s
          AND snf_from <= %s AND snf_to >= %s
        LIMIT 1
        """,
        (slab.name, fat, fat, snf, snf),
    )

    return flt(rate[0][0]) if rate else flt(slab.base_rate)


def calculate_collection_amount(doc, method=None):
    """Called via hooks on Milk Collection Entry before_save."""
    try:
        doc.rate_per_litre = get_milk_rate(
            doc.fat_percentage,
            doc.snf_percentage,
            doc.route,
            doc.collection_date,
        )
        doc.amount = flt(doc.quantity_litres) * flt(doc.rate_per_litre)
    except frappe.ValidationError:
        raise
    except Exception as e:
        frappe.log_error(str(e), "Milk Rate Calculation Failed")
