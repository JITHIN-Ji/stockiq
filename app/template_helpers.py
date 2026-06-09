"""
StockIQ Jinja2 template helpers.
Register custom filters and globals used across templates.
"""


def register_template_helpers(app):
    """Call this in app factory after creating the Flask app."""

    BUCKET_ICONS = {
        "Slow Mover": "🐢",
        "Stalwart": "🏛",
        "Fast Grower": "🚀",
        "Cyclical": "🔄",
        "Turnaround": "🔁",
        "Asset Play": "🏗",
    }

    @app.template_global()
    def bucket_icon(bucket: str) -> str:
        return BUCKET_ICONS.get(bucket, "📊")

    @app.template_global()
    def growth_fmt(val) -> str:
        if val is None:
            return "N/A"
        sign = "+" if val > 0 else ""
        return f"{sign}{val:.1f}%"

    @app.template_filter("crore")
    def crore_filter(val) -> str:
        if val is None:
            return "N/A"
        if val >= 100000:
            return f"₹{val / 100000:.2f}L Cr"
        return f"₹{val:,.0f} Cr"
