# James Klimek - WGU Student ID # 010170747
# Data Structures and Algorithms II WGUPS Routing Program

import datetime
import Package
from PackageHashTable import *
from Package import *
from Truck import *
import csv


# Function to prompt user to enter Package ID when searching for a specific package
def find_package_prompt():
    print("\nEnter a Package ID:")
    return input("\t>> ")


# Function to Display all packages with attributes organized by Truck
def print_all_packages(i, t):
    print("\n\n\tAll Packages:\n")

    print("\tPackage ID |\tDelivery Address\t|\tDeliver By Time"
          "\t|\tWeight\t|\tSpecial Notes\t|\tCurrent Location\t|\tStatus\n"
          "\t--------------------------------------------------------------------------------------------------"
          "---------------------------------------------------")
    print("\n\tTime: {}".format(t))
    print("\nTruck 1:")
    for i in range(len(all_pkgs.table)):
        pkg = all_pkgs.search_by_id(i + 1)
        if "Truck 1" in pkg.status:
            print("\tPackage: {}".format(pkg))
    print("\nTruck 2:")
    for i in range(len(all_pkgs.table)):
        pkg = all_pkgs.search_by_id(i + 1)
        if "Truck 2" in pkg.status:
            print("\tPackage: {}".format(pkg))
    print("\nTruck 3:")
    for i in range(len(all_pkgs.table)):
        pkg = all_pkgs.search_by_id(i + 1)
        if "Truck 3" in pkg.status:
            print("\tPackage: {}".format(pkg))
    print("\nPackages at Hub: ")
    for i in range(len(all_pkgs.table)):
        pkg = all_pkgs.search_by_id(i + 1)
        if "Waiting" in pkg.status:
            print("\tPackage: {}".format(pkg))


# Function to display a Package based on a specific Package ID
def print_package(p_id):
    print("\t\tPackage: {}\n".format(all_pkgs.search_by_id(p_id)))


# Function to display all Packages still at the Hub and not loaded on a truck
def print_pkgs_at_hub(i):
    print("\nPackages at HUB: ")
    # get data from packageHashTable
    for i in range(len(package_hash_table.table)):
        if package_hash_table.search_by_id(i + 1) is None:
            continue
        else:
            print("\tPackage: {}".format(package_hash_table.search_by_id(i + 1)))


# Function to display all trucks with attributes and the sum total of all trucks miles
def print_all_trucks():
    print("Truck 1\n", Truck_1)
    print("Truck 2\n", Truck_2)
    print("Truck 3\n", Truck_3)
    print("-----------------------------| "
          "TOTAL MILES OF ALL TRUCKS: {}"
          " |-----------------------------\n".format(Truck_1.mileage + Truck_2.mileage + Truck_3.mileage))


# Function to Load all trucks with packages at the Hub
# Certain packages are loaded on to specific trucks based on package delivery times or special notes
def load_truck():
    for i in range(len(package_hash_table.table)):
        pkg = package_hash_table.search_by_id(i + 1)
        if pkg is None:
            continue
        else:
            pkg_sp_notes = pkg.get_sp_notes()
            pkg_delivery_time = pkg.get_delivery_time()
            pkg_zip = pkg.get_zip()
            pkg_id = pkg.get_id()
            if "truck 2" in pkg_sp_notes:
                Truck_2.pkg_count += 1
                Truck_2.packages.append(pkg)
                pkg.set_status("At HUB : On {}".format(Truck_2.truck_name))
            elif "Delayed" in pkg_sp_notes and "10:30" in pkg_delivery_time and pkg_zip != 84117:
                Truck_2.pkg_count += 1
                Truck_2.packages.append(pkg)
                if "Delayed" in pkg_sp_notes:
                    pkg.set_status("Awaiting Arrival, Assigned to : {}".format(Truck_2.truck_name))
                else:
                    pkg.set_status("At HUB : On {}".format(Truck_2.truck_name))
            elif (("Delayed" in pkg_sp_notes or pkg_id == 9 and "10:30" not in pkg_delivery_time)
                  and Truck_1.pkg_count < 16):
                Truck_1.pkg_count += 1
                Truck_1.packages.append(pkg)
                if "Delayed" in pkg_sp_notes:
                    pkg.set_status("Awaiting Arrival, Assigned to : {}".format(Truck_1.truck_name))
                else:
                    pkg.set_status("At HUB : On {}".format(Truck_1.truck_name))
            elif ("Delayed" in pkg_sp_notes or "Must be delivered with" in pkg_sp_notes or
                    pkg_delivery_time == "9:00 AM" or pkg_zip == 84117 or pkg_id == 19 or pkg_id == 13):
                Truck_3.pkg_count += 1
                Truck_3.packages.append(pkg)
                if "Delayed" in pkg_sp_notes:
                    pkg.set_status("Awaiting Arrival, Assigned to: {}".format(Truck_3.truck_name))
                else:
                    pkg.set_status("At HUB : On {}".format(Truck_3.truck_name))
    # Load all remaining packages at the Hub onto trucks
    for i in range(len(package_hash_table.table)):
        pkg = package_hash_table.search_by_id(i + 1)
        if pkg is None:
            continue
        else:
            pkg_id = pkg.get_id()

            if pkg in Truck_1.packages or pkg in Truck_2.packages or pkg in Truck_3.packages:
                package_hash_table.remove_package(pkg_id)
                continue
            if Truck_1.pkg_count < 16:
                while Truck_1.pkg_count < 16:
                    Truck_1.packages.append(pkg)
                    pkg.set_status("At HUB : On {}".format(Truck_1.truck_name))
                    Truck_1.pkg_count += 1
                    package_hash_table.remove_package(pkg_id)
                    break
            elif Truck_2.pkg_count < 16:
                while Truck_2.pkg_count < 16:
                    Truck_2.packages.append(pkg)
                    pkg.set_status("At HUB : On {}".format(Truck_2.truck_name))
                    Truck_2.pkg_count += 1
                    package_hash_table.remove_package(pkg_id)
                    break
            else:
                while len(package_hash_table.table) >= 0:
                    Truck_3.packages.append(pkg)
                    pkg.set_status("At HUB : On {}".format(Truck_3.truck_name))
                    Truck_3.pkg_count += 1
                    package_hash_table.remove_package(pkg_id)
                    break
    return


# Function to get the distance between 2 locations from the dist_data table
def path_leg_dist(c_loc, n_loc):
    # Use row/column indexing to find current leg distance
    leg_dist = dist_data[c_loc][n_loc]
    return float(leg_dist)


# Nearest Neighbor algorithm for delivery route addresses will be visited based on the shortest distance
# to the next vertex(package address).
def next_closest_loc(truck):
    global next_loc_addr
    leg_dist = 0
    current_loc_addr = truck.current_location
    current_loc_index = 0
    next_loc_index = 0
    t_pkg_dist_list = []
    # Find the distance from the last delivered package address back to the Hub (WGU).
    if truck.pkg_count == 0:
        next_loc_addr = "Western Governors University"
        for i in range(len(dist_data)):
            if current_loc_addr in dist_data[0][i]:
                current_loc_index = i+1
                break
            elif current_loc_addr in dist_data[i][1]:
                current_loc_index = i
                break
        for j in range(len(dist_data)):
            if next_loc_addr in dist_data[0][j]:
                next_loc_index = j
                break
        leg_dist = path_leg_dist(current_loc_index, next_loc_index)
        truck.mileage += leg_dist
        return next_loc_addr

    # Check the address for every package remaining on the truck compared to the truck's current location.
    # Find the distances in the dist_data table and add them to t_pkg_dist_list.
    for pkg in range(truck.pkg_count):
        next_loc_addr = truck.packages[pkg].get_address()
        truck.packages[pkg].set_status("En Route : On {}".format(truck.truck_name))
        truck.packages[pkg].set_location(truck.current_location)
        if truck.packages[pkg].get_id() == 9:
            if time_comp(truck) >= 1020:
                truck.packages[pkg].delivery_address = "410 S State St"
                truck.packages[pkg].zip = 84111
                truck.packages[pkg].sp_notes = "ADDRESS UPDATED"
            elif truck.pkg_count == 1:
                while time_comp(truck) < 1020:
                    truck.current_time += datetime.timedelta(minutes=15)
            else:
                next_loc_addr = truck.packages[pkg+1].get_address()
                continue

        for i in range(len(dist_data)):
            if current_loc_addr in dist_data[0][i]:
                current_loc_index = i+1
                break
            elif current_loc_addr in dist_data[i][1]:
                current_loc_index = i
                break
        for j in range(len(dist_data)):
            if next_loc_addr in dist_data[0][j]:
                next_loc_index = j
                break

        leg_dist = path_leg_dist(current_loc_index, next_loc_index)
        t_pkg_dist_list.append(leg_dist)
    # Compare the distances in t_pkg_dist_list to find the next closest location (min_dist).
    # Return the address (next_loc_addr) of the shortest path distance.
    min_dist = leg_dist
    for i in range(len(t_pkg_dist_list)):
        if min_dist > t_pkg_dist_list[i] or min_dist == 0:
            min_dist = t_pkg_dist_list[i]
            next_loc_addr = truck.packages[i].get_address()
    truck.mileage += min_dist
    return next_loc_addr


# Function to deliver package, remove from the truck's package list and subtract the truck's pkg count by 1.
# Also update the package's status to DELIVERED with current time and by which truck.
def deliver_pkg(truck, package):
    if package in truck.packages and "Wrong address" not in package.sp_notes:
        truck.packages.pop(truck.packages.index(package))
        truck.pkg_count -= 1
        package.set_location(truck.current_location)
        package.set_status("DELIVERED: AT {}\tBY {}"
                           .format((truck.current_time.strftime("%H:%M")), truck.truck_name))
    else:
        return
    return


# Function to move the truck to the next location and deliver packages.
def drive_route(truck):
    truck.current_time = elapse_time(truck)
    if "Western Governors University" in truck.current_location:
        truck.current_location = next_closest_loc(truck)
        truck.current_time = elapse_time(truck)
    # Check each package address on the truck; if it matches the current location call deliver_pkg(truck, package)
    for i in range(truck.pkg_count):
        for pkg in truck.packages:
            if pkg.get_address() in truck.current_location and "Wrong" not in pkg.get_sp_notes():
                deliver_pkg(truck, pkg)
            else:
                continue
    truck.current_time = elapse_time(truck)
    truck.current_location = next_closest_loc(truck)
    if truck.pkg_count == 0:
        truck.current_time = elapse_time(truck)


# Function to advance time based on the Truck's miles driven.
def elapse_time(truck):
    if truck.truck_name == "Truck 1":
        truck.current_time = t1_time
    elif truck.truck_name == "Truck 2":
        truck.current_time = t2_time
    elif truck.truck_name == "Truck 3":
        truck.current_time = t3_time
    time_traveled_hrs = 0
    time_traveled_mins = round((truck.mileage / 18) * 60, 0)
    if time_traveled_mins >= 60:
        time_traveled_hrs = time_traveled_mins//60
        time_traveled_mins = time_traveled_mins % 60
    updated_time = truck.current_time + datetime.timedelta(hours=time_traveled_hrs, minutes=time_traveled_mins)
    return updated_time


# Function to load package data from CSV file and load into both the package_hash_table and all_pkgs hash table.
def load_package_data(file_name):
    with open(file_name) as all_packages:
        package_data = csv.reader(all_packages, delimiter=',')
        next(package_data)  # Skips the header
        for package in package_data:
            p_id = int(package[0])
            p_current_location = "HUB"
            p_delivery_address = package[1]
            p_city = package[2]
            p_state = package[3]
            p_zip = int(package[4])
            p_delivery_time = package[5]
            p_weight = int(package[6])
            p_sp_notes = package[7]
            p_status = "At Hub, waiting to be loaded for delivery"

            # package object
            pkg = Package(p_id, p_current_location, p_delivery_address, p_city, p_state, p_zip, p_delivery_time,
                          p_weight, p_sp_notes, p_status)

            # add to hash table
            package_hash_table.add_package(p_id, pkg)
            all_pkgs.add_package(p_id, pkg)


# Function to load Distance data from csv file.
def load_distance_data(file_name):
    with open(file_name) as all_distances:
        distance_data = csv.reader(all_distances, delimiter=',')
        for row in distance_data:
            dist_data.append(row)
        # Fill the table to make the distances between locations bidirectional
        for i in range(len(dist_data)):
            if i == 0:
                continue
            if i == 27:
                break
            for j in range(len(dist_data)):
                if j <= 1:
                    continue
                dist_data[i][j] = dist_data[j-1][i+1]


# Create the UI for running the program. Pass in the current time based on start time or highest mileage truck's time.
def interface(time):
    current_time = time
    trucks_loaded = False
    print("\n\t==================================\n\t"
          "WGUPS Package Delivery & Tracking\n\t"
          "==================================\n\t")
    print("\tCURRENT TIME:\t{}".format(current_time.strftime("%H:%M")))
    print("\n\tEnter number for selection:\n"
          "\t\t1: Search for Package by ID\n"
          "\t\t2: Show Packages at HUB\n"
          "\t\t3: Show All Packages\n"
          "\t\t4: Show Truck Information\n"
          "\t\t5: Load Trucks\n"
          "\t\t6: Advance Routes by One Location\n"
          "\t\t7: Complete All Routes\n"
          "\t\t8: Show Status Report at Specified Time\n"
          "\t\t0: Exit\n")
    response = input('\tEnter Selection >>\n')
    while True:
        if response == str('1'):
            p_id = int(find_package_prompt())
            print_package(p_id)
            next_choice = input("Search another package? Y or N\n\t>>").upper()
            while next_choice != str.upper('n'):
                p_id = int(find_package_prompt())
                print_package(p_id)
                next_choice = input("Search another package? Y or N\n>>").upper()
            if next_choice == str('N'):
                interface(current_time)
        elif response == str('2'):
            print_pkgs_at_hub(0)
            next_choice = input("\nReturn to Main Menu? Y or N\n\t>>").upper()
            while next_choice != str('Y'):
                next_choice = input("\nReturn to Main Menu? Y or N\n>>").upper()
            interface(current_time)
        elif response == str('3'):
            print_all_packages(0, current_time)
            next_choice = input("\nReturn to Main Menu? Y or N\n\t>>").upper()
            while next_choice != str('Y'):
                next_choice = input("\nReturn to Main Menu? Y or N\n>>").upper()
            interface(current_time)
        elif response == str('4'):
            print_all_trucks()
            next_choice = input("Return to Main Menu? Y or N\n\t>>").upper()
            while next_choice != str('Y'):
                next_choice = input("Return to Main Menu? Y or N\n>>").upper()
            interface(current_time)
        elif response == str('5'):
            load_truck()
            trucks_loaded = True
            print("\n\t-----Trucks are loaded and ready to go.-----\n")
            input("Press ENTER to continue").upper()
            interface(current_time)
        elif response == str('6'):
            if Truck_2.current_time <= current_time:
                drive_route(Truck_2)
                current_time = Truck_2.current_time
            if Truck_3.current_time <= current_time:
                drive_route(Truck_3)
                current_time = max(Truck_2.current_time, Truck_3.current_time)
            if Truck_2.pkg_count == 0 or Truck_3.pkg_count == 0:
                drive_route(Truck_1)
                current_time = max(Truck_1.current_time, Truck_2.current_time, Truck_3.current_time)
                interface(current_time)
            interface(current_time)
        elif response == str('7'):
            while Truck_2.pkg_count > 0:
                drive_route(Truck_2)
            while Truck_3.pkg_count > 0:
                drive_route(Truck_3)
            if Truck_2.pkg_count == 0 or Truck_3.pkg_count == 0:
                Truck_1.current_time = t1_time
                while Truck_1.pkg_count > 0:
                    drive_route(Truck_1)
                current_time = max(Truck_1.current_time, Truck_2.current_time, Truck_3.current_time)
                interface(current_time)
            next_choice = input("\nReturn to Main Menu? Y or N\n>>").upper()
            while next_choice != str('Y'):
                next_choice = input("\nReturn to Main Menu? Y or N\n>>").upper()
            current_time = max(Truck_2.current_time, Truck_3.current_time)
            interface(current_time)
        elif response == str('8'):
            search_time = int(input("Enter a Time in 24 HR Format HHMM\n>>"))

            if trucks_loaded is False:
                load_truck()
                trucks_loaded = True
            while time_comp(Truck_2) <= search_time:
                if Truck_2.pkg_count > 0:
                    drive_route(Truck_2)
                else:
                    break
                current_time = Truck_2.current_time
            while time_comp(Truck_3) <= search_time:
                if Truck_3.pkg_count > 0:
                    drive_route(Truck_3)
                else:
                    break
                current_time = max(Truck_2.current_time, Truck_3.current_time)
            while time_comp(Truck_1) <= search_time:
                if Truck_1.pkg_count > 0:
                    drive_route(Truck_1)
                else:
                    break
                current_time = max(Truck_1.current_time, Truck_2.current_time, Truck_3.current_time)

            next_choice = input("\nChoose an Option:\n"
                                "\t1: Show a Specific Package ID\n"
                                "\t2: Show All Packages\n>>")
            if next_choice == "1":
                p_id = int(find_package_prompt())
                print_package(p_id)
            elif next_choice == "2":
                print_all_packages(0, search_time)
            input("\nPress Enter to Return to Main Menu\n>>").upper()
            main()
        elif response == str('0'):
            exit()
        else:
            response = input('\tEnter Valid Selection >>')


def time_comp(truck):
    t = truck.current_time.strftime("%H%M")
    t_comp = int(t)
    return t_comp


# main Function
def main():

    interface(start_time)


dist_data = []  # Create the dist_date table for referencing distances between locations.
package_hash_table = PackageHashTable()  # Create the package hash table used for loading packages.
all_pkgs = PackageHashTable()  # Create a duplicate of package_hash_table for displaying updated package info.
load_package_data('CSVFiles/WGUPSPackageFile.csv')
load_distance_data('CSVFiles/WGUPSDistanceTable.csv')
# Set start time to 8:00AM as that is when deliveries start.
start_time = datetime.datetime(2023, 11, 18, 8, 00)

# Delayed Truck 1 Start Time to wait for an available driver and accommodate delayed packages.
# Delayed Truck 3 Start Time to accommodate delayed packages
t1_time = start_time + datetime.timedelta(hours=1, minutes=5)
t2_time = start_time + datetime.timedelta(hours=1, minutes=5)
t3_time = start_time
# Create Truck objects
Truck_1 = Truck("Truck 1", t1_time)
Truck_2 = Truck("Truck 2", t2_time)
Truck_3 = Truck("Truck 3", t3_time)


main()
