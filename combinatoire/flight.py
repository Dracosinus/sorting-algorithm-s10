from datetime import datetime, time

class Flight:
    def __init__(self, price, stops, orig, dest, depart, arrive, airline_display, conf_role):
        self.price = price
        self.stops = stops
        self.orig = orig
        self.dest = dest
        self.depart = depart
        self.arrive = arrive
        self.airline_display = airline_display
        self.conf_role = conf_role

    @classmethod
    def from_xml_element(cls, element):
        price = float(element.find('price').text)
        stops = element.find('stops').text
        orig = element.find('orig').text
        dest = element.find('dest').text
        depart = datetime.fromisoformat(element.find('depart').text)
        arrive = datetime.fromisoformat(element.find('arrive').text)
        airline_display = element.find('airline_display').text

        return cls(price, stops, orig, dest, depart, arrive, airline_display, 'incoming')
    
    def to_string(self):
        print('Price:', self.price)
        print('Stops:', self.stops)
        print('Origin:', self.orig)
        print('Destination:', self.dest)
        print('Departure:', self.depart)
        print('Arrival:', self.arrive)
        print('Airline:', self.airline_display)
        print('ConfRole:', self.conf_role)
        print('---')

