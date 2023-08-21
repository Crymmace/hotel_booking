import pandas

df = pandas.read_csv("hotels.csv", dtype={"id": str})
df_cards = pandas.read_csv("cards.csv", dtype=str).to_dict(orient="records")
df_cards_security = pandas.read_csv("card_security.csv", dtype=str)


class Hotel:
    def __init__(self, hotel_id):
        self.hotel_id = hotel_id
        self.name = df.loc[df["id"] == self.hotel_id, "name"].squeeze()

    def book(self):
        df.loc[df["id"] == self.hotel_id, "available"] = "no"
        df.to_csv("hotels.csv", index=False)

    def available(self):
        availability = df.loc[df["id"] == self.hotel_id, "available"].squeeze()
        if availability == "yes":
            return True


class Reservation:
    def __init__(self, customer_name, hotel_object):
        self.customer_name = customer_name
        self.hotel = hotel_object

    def generate(self):
        content = f"""
        Thank you for your reservation!
        
        Here is your booking data:
        Name: {self.customer_name}
        Hotel: {self.hotel.name}
        """
        return content


class Spa(Reservation):
    def reserve_spa(self):
        content = f"""
        Thank you for your SPA reservation!

        Here is your SPA booking data:
        Name: {self.customer_name}
        Hotel: {self.hotel.name}
        """
        return content


class CreditCard:
    def __init__(self, number, expiration, holder, cvc):
        self.number = number
        self.expiration = expiration
        self.holder = holder
        self.cvc = cvc

    def validate(self):
        card_data = {"number": self.number, "expiration": self.expiration,
                     "holder": self.holder, "cvc": self.cvc}
        if card_data in df_cards:
            return True


class SecureCreditCard(CreditCard):
    def authenticate(self, given_password):
        password = df_cards_security.loc[df_cards_security["number"] == self.number, "password"].squeeze()
        if password == given_password:
            return True


print(df)
hotel_id = input("Enter the id of the hotel: ")
hotel = Hotel(hotel_id)

if hotel.available():
    credit_card = SecureCreditCard(number="1234567890123456", expiration="12/26",
                                   holder="JOHN SMITH", cvc="123")
    if credit_card.validate():
        if credit_card.authenticate(given_password="mypass"):
            hotel.book()
            name = input("Please enter your name: ")
            reservation = Spa(name, hotel)
            print(reservation.generate())
            spa = input("Would you like to book a spa package? ").lower()
            if spa == "yes":
                print(reservation.reserve_spa())
            else:
                print("Thank you, come again!")
        else:
            print("Unable to validate credit card.")
    else:
        print("Please enter a valid payment method.")
else:
    print("Hotel is not available.")

