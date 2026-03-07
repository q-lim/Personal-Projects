"""
Console App for Sample Tracker
Records laboratory samples
Version 1: CLI version
"""

from SampleTracker import Sample, SolidSample, LiquidSample, SampleManager



def create_sample(manager):
    """Create a new sample entry"""
    
    print("\nCreate New Sample:")
    print("1. Solid sample")
    print("2. Liquid sample")
    
    choice = input("Choose sample type: ")
    
    name = input("Sample name: ")
    date = input("Sample date: ")
    exp_number = input("Experiment number: ")
    lab = input("Laboratory: ")
    storage = input("Storage location: ")
    
    if choice.lower() in ["1", "solid", "solid sample"]:
        stor_med = input("Storage medium: ")
        stor_med_vol = input("Storage medium volume: ")
        sample_mass = input("Sample mass: ")
        
        sample = SolidSample(
            name,
            date,
            exp_number,
            lab,
            storage,
            stor_med,
            stor_med_vol,
            sample_mass
            )
        
    elif choice.lower() in ["2", "liquid", "liquid sample"]:
        bottle = input("Bottle type: ")
        bottle_vol = input("Bottle volume: ")
        sample_vol = input("Sample volume: ")
        
        sample = LiquidSample(
            name,
            date,
            exp_number,
            lab,
            storage,
            bottle,
            bottle_vol,
            sample_vol
            )
    
    else:
        print("Invalid selection.")
        return
    
    manager.add_sample(sample)
    print("Sample added.")
    
    
    
def list_samples(manager):
    """List out all samples recorded"""
    
    print("\nAll samples:")
    samples = manager.list_samples()
    
    if not samples:
        print("No samples found.")
        return
    
    for s in samples:
        print(f"ID: {s.ID}")
        print(f"Name: {s.Name}")
        print(f"Status: {s.Status}")
        print("-" * 30)
        


def update_sample_status(manager):
    """Changes sample status based on user input"""
    
    sample_id = input("Enter sample ID to update: ")
    sample = manager.find_sample(sample_id)
    
    if not sample:
        print("Sample not found.")
        return
    
    new_status = input("Enter latest sample status: ")
    sample.update_status(new_status)
    manager.save_samples()
    print(f"{sample.Name} status updated to {new_status}")
    
    
    
def delete_sample(manager):
    """Deletes sample based on sample ID"""
    
    sample_id = input("Enter ID of sample to delete: ")
    manager.delete_sample(sample_id)
    print("Sample deleted (if ID existed).")
    
    
def main():
    """Main function"""
    manager = SampleManager()
    
    while True:
        print("\n-----[ Sample Tracker programme ]-----")
        print("1. List sample")
        print("2. Add samples")
        print("3. Update sample status")
        print("4. Delete samples")
        print("5. Exit")
        
        choice = input("\nSelect option: ")
        
        if choice == "1":
            list_samples(manager)
        elif choice == "2":
            create_sample(manager)
        elif choice == "3":
            update_sample_status(manager)
        elif choice == "4":
            delete_sample(manager)
        elif choice == "5":
            print("Exiting...")
            break
        else:
            print("Invalid selection\n")



if __name__ == "__main__":
    main()