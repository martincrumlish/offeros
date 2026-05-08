"""Compatibility entrypoint for OfferOS Sales Page Studio v2.

The production renderer lives in build_sales_page_studio.py so the source of
truth is not split between an old Page Kit implementation and the new studio.
"""

from build_sales_page_studio import main


if __name__ == "__main__":
    raise SystemExit(main())
