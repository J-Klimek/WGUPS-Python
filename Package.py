class Package:
    # Constructor for Package Object
    def __init__(self, p_id, p_current_location, p_delivery_address, p_city, p_state, p_zip,
                 p_delivery_time, p_weight, p_sp_notes, p_status):
        self.id = p_id
        self.current_location = p_current_location
        self.delivery_address = p_delivery_address
        self.city = p_city
        self.state = p_state
        self.zip = p_zip
        self.location_name = ""
        self.delivery_time = p_delivery_time
        self.weight = p_weight
        self.sp_notes = p_sp_notes
        self.status = p_status

    def __str__(self):  # overwrite print(Package) for display
        return (" %s\t|\t%s, %s, %s %s\t|\t%s\t|\t%s\t|\t%s\t|\t%s\t|\t%s" %
                (self.id, self.delivery_address, self.city, self.state, self.zip,
                 self.delivery_time, self.weight, self.sp_notes, self.current_location, self.status))

    def get_id(self):
        return self.id

    def get_address(self):
        return self.delivery_address

    def get_city(self):
        return self.city

    def get_state(self):
        return self.state

    def get_zip(self):
        return self.zip

    def get_delivery_time(self):
        return self.delivery_time

    def get_weight(self):
        return self.weight

    def get_sp_notes(self):
        return self.sp_notes

    def get_status(self):
        return self.status

    def set_status(self, status):
        self.status = status

    def set_location(self, location):
        self.current_location = location