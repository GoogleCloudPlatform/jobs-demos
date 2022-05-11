from ctypes import addressof
from borb.pdf.document.document import Document
from borb.pdf.page.page import Page
from borb.pdf.canvas.layout.page_layout.multi_column_layout import SingleColumnLayout
from borb.pdf.canvas.layout.page_layout.page_layout import PageLayout
from decimal import Decimal
from borb.pdf.canvas.layout.image.image import Image
from borb.pdf.canvas.layout.table.fixed_column_width_table import (
    FixedColumnWidthTable as Table,
)
from borb.pdf.canvas.layout.text.paragraph import Paragraph
from borb.pdf.canvas.layout.layout_element import Alignment
from borb.pdf.canvas.color.color import HexColor, HexColor
from borb.pdf.canvas.layout.table.table import TableCell
from borb.pdf.pdf import PDF

from datetime import datetime, timedelta
import random
import typing

grey_1 = "ececec"
grey_2 = "bbbbbb"
dark = "1e1e1e"
light = "ffffff"


class Product:
    """
    This class represents a purchased product
    """

    def __init__(self, name: str, quantity: int, price_per_sku: float):
        self.name: str = name
        assert quantity >= 0
        self.quantity: int = quantity
        assert price_per_sku >= 0
        self.price_per_sku: float = price_per_sku


def format_price(amount):
    return "${:,.2f}".format(amount)


def _build_invoice_information(company, address_1, address_2, phone, invoice_num):
    table_001 = Table(number_of_rows=4, number_of_columns=3, column_widths=[Decimal(5), Decimal(1), Decimal(1)],)

    table_001.add(
        Paragraph(
            company, font="Courier-Bold", font_size=16, horizontal_alignment=Alignment.LEFT
        )
    )
    table_001.add(
        Paragraph(
            "Invoice", font="Helvetica-Bold", horizontal_alignment=Alignment.RIGHT
        )
    )
    table_001.add(Paragraph("#%d" % invoice_num))

    # 2
    table_001.add(Paragraph(address_1))
    table_001.add(
        Paragraph("Date", font="Helvetica-Bold",
                  horizontal_alignment=Alignment.RIGHT)
    )
    now = datetime.now() + timedelta(days=random.randint(0, 60))
    table_001.add(Paragraph("%d/%d/%d" % (now.day, now.month, now.year)))

    # 3
    table_001.add(Paragraph(address_2))
    table_001.add(
        Paragraph(
            "Due Date", font="Helvetica-Bold", horizontal_alignment=Alignment.RIGHT
        )
    )
    due = now + timedelta(days=random.randint(0, 60))
    table_001.add(Paragraph("%d/%d/%d" % (due.day, due.month, due.year)))
    
    # 4
    table_001.add(Paragraph(phone))
    table_001.add(Paragraph(" "))
    table_001.add(Paragraph(" "))

    table_001.set_padding_on_all_cells(
        Decimal(2), Decimal(2), Decimal(2), Decimal(2))
    table_001.no_borders()
    return table_001


def _build_billing_and_shipping_information(company, address_1, address_2, phone):
    table_001 = Table(number_of_rows=5, number_of_columns=1)
    table_001.add(
        Paragraph(
            "Bill to:",
            font_color=HexColor(grey_2),
        )
    )

    table_001.add(Paragraph(company, font="Helvetica-Bold"))  # BILLING
    # table_001.add(Paragraph("[Company Name]"))  # SHIPPING
    table_001.add(Paragraph(address_1))  # BILLING
    # table_001.add(Paragraph("[Street Address]"))  # SHIPPING
    table_001.add(Paragraph(address_2))  # BILLING
    # table_001.add(Paragraph("[City, State, ZIP Code]"))  # SHIPPING
    table_001.add(Paragraph(phone))  # BILLING
    # table_001.add(Paragraph("[Phone]"))  # SHIPPING
    table_001.set_padding_on_all_cells(
        Decimal(2), Decimal(2), Decimal(2), Decimal(2))
    table_001.no_borders()
    return table_001


def _build_itemized_description_table(products: typing.List[Product] = []):
    """
    This function builds a Table containing itemized billing information
    :param:     products
    :return:    a Table containing itemized billing information
    """
    table_001 = Table(number_of_rows=15, number_of_columns=4, column_widths=[Decimal(3), Decimal(1), Decimal(2), Decimal(2)],)
    for h in ["Item", "Quantity", "Rate", "Amount"]:
        table_001.add(
            TableCell(
                Paragraph(h, font_color=HexColor(light)),
                background_color=HexColor(dark),
            )
        )

    odd_color = HexColor(grey_2)
    even_color = HexColor(light)
    for row_number, item in enumerate(products):
        c = even_color if row_number % 2 == 0 else odd_color
        table_001.add(TableCell(Paragraph(item.name), background_color=c))
        table_001.add(
            TableCell(Paragraph(str(item.quantity)), background_color=c))
        table_001.add(
            TableCell(Paragraph(format_price(item.price_per_sku)),
                      background_color=c)
        )
        table_001.add(
            TableCell(
                Paragraph(format_price(item.quantity * item.price_per_sku)),
                background_color=c,
            )
        )

    # Optionally add some empty rows to have a fixed number of rows for styling purposes
    for row_number in range(len(products), 9):
        c = even_color if row_number % 2 == 0 else odd_color
        for _ in range(0, 4):
            table_001.add(TableCell(Paragraph(" "), background_color=c))

    # subtotal
    subtotal: float = sum([x.price_per_sku * x.quantity for x in products])
    table_001.add(
        TableCell(
            Paragraph(
                "Subtotal",
                font="Helvetica-Bold",
                horizontal_alignment=Alignment.RIGHT,
            ),
            col_span=3,
        )
    )
    table_001.add(
        TableCell(Paragraph(format_price(subtotal), horizontal_alignment=Alignment.RIGHT))
    )

    # discounts
    table_001.add(
        TableCell(
            Paragraph(
                "Discounts",
                font="Helvetica-Bold",
                horizontal_alignment=Alignment.RIGHT,
            ),
            col_span=3,
        )
    )
    discounts = random.uniform(0,0.4)
    table_001.add(
        TableCell(Paragraph(format_price(discounts), horizontal_alignment=Alignment.RIGHT)))

    # taxes
    taxes: float = (subtotal - discounts) * 0.06
    table_001.add(
        TableCell(
            Paragraph(
                "Taxes", font="Helvetica-Bold", horizontal_alignment=Alignment.RIGHT
            ),
            col_span=3,
        )
    )
    table_001.add(
        TableCell(Paragraph(format_price(taxes),
                  horizontal_alignment=Alignment.RIGHT))
    )

    # total
    total: float = (subtotal - discounts) + taxes
    table_001.add(
        TableCell(
            Paragraph(
                "Total", font="Helvetica-Bold", horizontal_alignment=Alignment.RIGHT
            ),
            col_span=3,
        )
    )
    table_001.add(
        TableCell(Paragraph(format_price(total),
                  horizontal_alignment=Alignment.RIGHT))
    )
    # paid
    random_percent = random.random()
    paid: float = total * random_percent
    table_001.add(
        TableCell(
            Paragraph(
                "Amount Paid", font="Helvetica-Bold", horizontal_alignment=Alignment.RIGHT
            ),
            col_span=3,
        )
    )
    table_001.add(
        TableCell(Paragraph(format_price(paid),
                  horizontal_alignment=Alignment.RIGHT))
    )
    table_001.set_padding_on_all_cells(
        Decimal(2), Decimal(1), Decimal(1), Decimal(2))
    table_001.no_borders()
    return table_001


def generate():
    # Create document
    pdf = Document()

    # Add page
    page = Page()
    pdf.append_page(page)

    # create PageLayout
    page_layout: PageLayout = SingleColumnLayout(page)
    # page_layout.vertical_margin = page.get_page_info().get_height() * Decimal(0.1)
    # page_layout.horizontal_margin = page.get_page_info().get_height() * Decimal(0.01)

    # Invoice information table
    import randomname
    from random_address import real_random_address
    from random_phone import RandomUkPhone
    company = randomname.get_name()
    address = real_random_address()
    address_1 = address.get('address1')
    address_2 = f"{address.get('city')}, {address.get('state')} {address.get('postalCode')}"
    phone = RandomUkPhone().random_mobile()
    invoice_num = random.randint(1000, 10000)

    page_layout.add(_build_invoice_information(company, address_1, address_2, phone, invoice_num))

    # Empty paragraph for spacing
    page_layout.add(Paragraph(" "))

    # Billing and shipping information table
    page_layout.add(_build_billing_and_shipping_information( "Google", "1600 Amphitheatre Pkwy", "Mt View, CA 94043, USA", "123-456-7890"))

    # Empty paragraph for spacing
    page_layout.add(Paragraph(" "))

    # Itemized description
    num_products = random.randint(1,10)
    products = []
    for _ in range(0, num_products):
        name = randomname.generate("ip/corporate", "n/data_structures")
        products.append(Product(name, random.randint(1, 50), random.randint(10, 10000)))

    page_layout.add(_build_itemized_description_table(products))

    page_layout.add(Paragraph("Note: This is a test order. No actual transaction took place."))

    # store
    with open(f"incoming/{company}-{invoice_num}.pdf", "wb") as out_file_handle:
        PDF.dumps(out_file_handle, pdf)


if __name__ == "__main__":
    for _ in range(0, 100):
        generate()