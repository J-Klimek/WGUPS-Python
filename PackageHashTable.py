# Package Hash table
class PackageHashTable:
    # Constructor with starting capacity of 40 packages.
    def __init__(self, start_capacity=40):
        # Initialize the hash table with empty entries
        self.table = []
        for i in range(start_capacity):
            self.table.append([])

    # Function to add packages to the package_hash_table using Package ID as the KEY
    # and other Package attributes as the VALUE.
    def add_package(self, p_id, package):
        package_index = hash(p_id) % len(self.table)
        package_list = self.table[package_index]

        for pkg in package_list:
            if pkg[0] == p_id:
                pkg[1] = package
                return True
        p_id_package = [p_id, package]
        package_list.append(p_id_package)
        return True

    # Function to find and remove Package from the hash table based on Package ID.
    def remove_package(self, pkg_id):
        package_index = hash(pkg_id) % len(self.table)
        package_list = self.table[package_index]
        pkg = self.search_by_id(pkg_id)
        pkg_id_package = [pkg_id, pkg]
        for pkg in package_list:
            if pkg[0] == pkg_id:
                package_list.remove(pkg_id_package)

    # Searches for a Package with matching Package ID (KEY) in the hash table.
    # Returns the Package if found, or None if not found (VALUE).
    def search_by_id(self, p_id):
        # gets the package index where this pID would be.
        package_index = hash(p_id) % len(self.table)
        package_list = self.table[package_index]

        for pkg in package_list:
            if pkg[0] == p_id:
                return pkg[1]
            return None

