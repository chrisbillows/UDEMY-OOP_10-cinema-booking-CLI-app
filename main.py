from fpdf import FPDF
import random
import sqlite3
import string


class User:
    """Represents a User that can buy a cinema seat"""

    def __init__(self, name):
        self.name = name

    def buy(self, seat, card):
        """Buys the Ticket if the card is valid"""
        if seat.is_free():
            if card.validate(price=seat.get_price()):
                seat.occupy()
                ticket = Ticket(user=self, price=seat.get_price(), seat_number=seat_id)
                ticket.to_pdf()
                return "Purchase successful!"
            else:
                return "Card declined."
        else:
            return "Sorry, that seat is taken. Please try again."


class Seat:
    """Represents a cinema seat that can booked by a user"""

    database = "cinema.db"

    def __init__(self, seat_id):
        self.seat_id = seat_id

    def get_price(self):
        """Get the price of a certain Seat"""
        connection = sqlite3.connect(self.database)
        cursor = connection.cursor()
        cursor.execute("""
        SELECT price FROM Seat WHERE seat_id=? 
        """, [self.seat_id])
        price = cursor.fetchall()[0][0]
        connection.close()
        return price

    def is_free(self):
        """Check database if selected Seat is available"""
        connection = sqlite3.connect(self.database)
        cursor = connection.cursor()
        cursor.execute("""
        SELECT taken FROM Seat WHERE seat_id=? 
        """, [self.seat_id])
        result = cursor.fetchall()[0][0]
        connection.close()

        if result == 0:
            return True
        else:
            return False

    def occupy(self):
        """If Seat is empty, change value of taken in db from 0 to 1 to indicate taken"""
        if self.is_free():
            connection = sqlite3.connect(self.database)
            connection.execute("""
            UPDATE Seat SET taken=? WHERE seat_id=? 
            """, [1, self.seat_id])
            connection.commit()
            connection.close()


class Card:
    """Represents a bank card needed to finalise a Seat Purchase"""

    database = "banking.db"

    def __init__(self, type, number, cvc, holder):
        self.type = type
        self.number = number
        self.cvc = cvc
        self.holder = holder

    def validate(self, price):
        """Checks if Card is valid and has balance. Subtracts price from balance."""
        connection = sqlite3.connect(self.database)
        cursor = connection.cursor()
        cursor.execute("""
        SELECT balance FROM Card WHERE number=? and cvc=?
        """, [self.number, self.cvc])
        result = cursor.fetchall()

        if result:
            balance = result[0][0]
            if balance >= price:
                connection.execute("""
                UPDATE Card SET balance = ? WHERE number=? and cvc=?
                """, [balance - price, self.number, self.cvc])
                connection.commit()
                connection.close()
                return True


class Ticket:
    """Represents a cinema Ticket purchased by a User"""

    def __init__(self, user, price, seat_number):
        self.user = user
        self.price = price
        self.seat_number = seat_number
        self.id = "".join([random.choice(string.ascii_letters) for i in range(6)])

    def to_pdf(self):
        """Creates a PDF ticket"""
        pdf = FPDF(orientation='P', unit='pt', format='A4')
        pdf.add_page()

        pdf.set_font(family="Times", style="B", size=24)
        pdf.cell(w=0, h=80, txt="Your Digital Ticket", border=1, ln=1, align="C")

        pdf.set_font(family="Times", style="B", size=14)
        pdf.cell(w=100, h=25, txt="Name: ", border=1)
        pdf.set_font(family="Times", style="", size=12)
        pdf.cell(w=0, h=25, txt=self.user.name, border=1, ln=1)
        pdf.cell(w=0, h=5, txt="", border=0, ln=1)

        pdf.set_font(family="Times", style="B", size=14)
        pdf.cell(w=100, h=25, txt="Ticket ID: ", border=1)
        pdf.set_font(family="Times", style="", size=12)
        pdf.cell(w=0, h=25, txt=self.id, border=1, ln=1)
        pdf.cell(w=0, h=5, txt="", border=0, ln=1)

        pdf.set_font(family="Times", style="B", size=14)
        pdf.cell(w=100, h=25, txt="Price: ", border=1)
        pdf.set_font(family="Times", style="", size=12)
        pdf.cell(w=0, h=25, txt=str(self.price), border=1, ln=1)
        pdf.cell(w=0, h=5, txt="", border=0, ln=1)

        pdf.set_font(family="Times", style="B", size=14)
        pdf.cell(w=100, h=25, txt="Seat Number: ", border=1)
        pdf.set_font(family="Times", style="", size=12)
        pdf.cell(w=0, h=25, txt=str(self.seat_number), border=1, ln=1)
        pdf.cell(w=0, h=5, txt="", border=0, ln=1)

        pdf.output("sample.pdf", 'F')


if __name__ == "__main__":

    name = input("Your full name: ")
    seat_id = input("Preferred seat number: ")
    card_type = input("Your card type: ")
    card_number = input("Your card number: ")
    card_cvc = input("Your card cvc: ")
    card_holder = input("Card holder name: ")

    user = User(name=name)
    seat = Seat(seat_id=seat_id)
    card = Card(type=card_type, number=card_number, cvc=card_cvc, holder=card_holder)

    print(user.buy(seat=seat, card=card))
