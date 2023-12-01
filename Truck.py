class Truck:
    # Constructor for Truck Object initializing the speed with 18(mph),
    # the load capacity to 16 (number of packages a truck can carry at one time), mileage of 0.0,
    # package count of 0, location of Western Governors University(HUB) and the current time.
    def __init__(self, t_name, st_time):
        self.truck_name = t_name
        self.speed = 18  # Average speed of the truck
        self.packages = []  # List of packages on the truck for delivery.
        self.load_capacity = 16  # Max number of packages a truck can carry.
        self.mileage = round(0.0, 2)  # mileage of the truck.
        self.pkg_count = 0  # Number of packages currently on the truck.
        self.current_location = "Western Governors University"
        self.current_time = st_time

    def __str__(self):  # Override print(Truck) for display purposes.
        return ("\tLoad Capacity: %s\n\tSpeed: %s\n\tPackages: \n\t\t%s\n\t"
                "Mileage: %s\n\tPackage Count: %s\n\tCurrent Location: %s\n" %
                (self.load_capacity, self.speed, self.pkg_list_to_string(), round(self.mileage, 2),
                 self.pkg_count, self.current_location))

    def pkg_list_to_string(self):
        return '\n\t\t'.join(str(i) for i in self.packages)

    def get_current_location(self):
        return self.current_location

    def get_package_id(self):
        return self.packages[0].get_id()

    def get_package_address(self):
        return self.packages[0].get_address()

    def get_mileage(self):
        mileage = self.mileage
        return round(mileage, 2)

    def get_pkg_count(self):
        return self.pkg_count