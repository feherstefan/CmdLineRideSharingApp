import random

class RideSharingMediator:
    def request_ride(self, passenger, location):
        pass

    def offer_ride(self, driver):
        pass


class ConcreteRideSharingMediator(RideSharingMediator):
    def __init__(self):
        self.drivers = []
        self.passengers = []
        self.ride_requests = {}

    def add_driver(self, driver):
        self.drivers.append(driver)

    def add_passenger(self, passenger):
        self.passengers.append(passenger)

    def request_ride(self, passenger, location):
        close_drivers = self.get_closest_drivers(location)
        passenger.show_options(close_drivers)
        return close_drivers

    def get_closest_drivers(self, location):
        # Filter only available drivers
        available_drivers = [d for d in self.drivers if d.is_available]
        close_drivers = sorted(available_drivers, key=lambda d: random.randint(1, 100))[:4]
        return close_drivers

    def confirm_ride(self, driver, passenger):
        if not driver.is_available:
            print(f"{driver.name} is not available at the moment.")
            return False

        if driver not in self.ride_requests:
            self.ride_requests[driver] = []

        self.ride_requests[driver].append(passenger)

        if self.ride_requests[driver][0] == passenger:
            if driver.accept_ride():
                passenger.assign_driver(driver)
                driver.assign_passenger(passenger)
                self.ride_requests[driver].pop(0)  # Remove the passenger from the queue
                return True
            else:
                self.ride_requests[driver].pop(0)  # Remove the passenger from the queue
                return False
        else:
            print(f"{passenger.name} is in the queue for {driver.name}. Waiting for driver's response.")
            return None


class Passenger:
    def __init__(self, name, mediator):
        self.name = name
        self.mediator = mediator
        self.driver = None

    def request_ride(self, location):
        close_drivers = self.mediator.request_ride(self, location)
        return close_drivers

    def choose_driver(self, drivers):
        while True:
            driver_name = input(f"{self.name}, enter the name of the driver you choose: ")
            selected_driver = next((d for d in drivers if d.name == driver_name), None)
            if not selected_driver:
                print("Invalid driver name. Please try again.")
                continue

            result = self.mediator.confirm_ride(selected_driver, self)
            if result is True:
                return True
            elif result is False:
                print(f"{selected_driver.name} did not accept the ride. Please choose another driver.")
            else:
                return False

    def assign_driver(self, driver):
        self.driver = driver
        print(f"{self.name} has been picked up by {driver.name}")

    def show_options(self, drivers):
        print(f"{self.name}, the closest drivers are: {', '.join([d.name for d in drivers])}")


class Driver:
    def __init__(self, name, mediator):
        self.name = name
        self.mediator = mediator
        self.passenger = None
        self.is_available = True

    def accept_ride(self):
        if not self.is_available:
            print(f"{self.name} is currently on another ride.")
            return False
        response = input(f"{self.name}, do you accept the ride? (yes/no): ")
        if response.lower() == 'yes':
            self.is_available = False
            return True
        return False

    def assign_passenger(self, passenger):
        self.passenger = passenger
        print(f"{self.name} is now driving {passenger.name}")

    def complete_ride(self):
        self.passenger = None
        self.is_available = True
        print(f"{self.name} has completed the ride and is now available.")


# Example Usage
mediator = ConcreteRideSharingMediator()

for i in range(1, 6):
    mediator.add_driver(Driver(f"Driver {i}", mediator))

passenger1 = Passenger("Passenger 1", mediator)
mediator.add_passenger(passenger1)

passenger2 = Passenger("Passenger 2", mediator)
mediator.add_passenger(passenger2)

close_drivers1 = passenger1.request_ride("Some location")
passenger1.choose_driver(close_drivers1)

close_drivers2 = passenger2.request_ride("Some location")
passenger2.choose_driver(close_drivers2)
