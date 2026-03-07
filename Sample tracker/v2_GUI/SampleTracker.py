"""
Sample tracker using OOP
Version 1
"""

import os
import json
from datetime import datetime
import uuid # Universally Unique Identifier

class SampleLogger:
    """To log samples"""
    
    log_file = os.path.join(os.getcwd(), "sample_log.json")

    @classmethod
    def write_log(cls, log_entry):
        logs = []
        
        # Load existing logs
        if os.path.exists(cls.log_file):
            with open(cls.log_file, "r") as f:
                try:
                    logs = json.load(f)
                except json.JSONDecodeError:
                    logs = []
        
        # Add entry to logs
        logs.append(log_entry)
        
        # Write updated log file
        with open(cls.log_file, "w") as f:
            json.dump(logs, f, indent=4)
            
    @classmethod
    def log(cls, event_type, sample_id, message):
        log_entry = {
            "Timestamp": datetime.now().isoformat(),
            "Event": event_type,
            "Sample ID": sample_id,
            "Message": message
            }
        print(f"[{log_entry['Timestamp']}] {event_type} - {message}")
        cls.write_log(log_entry)

    @classmethod
    def log_creation(cls, sample):
        cls.log("CREATED", sample.ID, f"Sample {sample.Name} created")
        
    @classmethod
    def log_status_change(cls, sample):
        cls.log("STATUS UPDATED", sample.ID, f"Sample {sample.Name} status changed to {sample.Status}")
        
    @classmethod
    def log_deletion(cls, sample_id):
        cls.log("DELETED", sample_id, "Sample deleted")

class Sample:
    """Sample object"""
    
    #__init__ sets the values for the object
    def __init__(self, name, date, exp_number, lab_loc, stor_loc):
        self.ID = str(uuid.uuid4()) # Universally Unique Identifier, 128-bit number
        self.Name = name
        self.Date = date
        self.ExpNumber = exp_number
        self.LabLoc = lab_loc
        self.StorLoc = stor_loc
        self.Status = "Not tested"
        self.CreatedAt = datetime.now().isoformat()
        
    def update_status(self, new_status):
        self.Status = new_status
        SampleLogger.log_status_change(self)

    def info_to_dict(self):
        return {
            "Type": self.__class__.__name__,
            "ID": self.ID,
            "Name": self.Name,
            "Date": self.Date,
            "Experiment Number": self.ExpNumber,
            "Lab": self.LabLoc,
            "Location": self.StorLoc,
            "Status": self.Status,
            "Entry created": self.CreatedAt
            }
           


class SolidSample(Sample):
    """Solid sample, inherits sample object"""
    
    def __init__(self, name, date, exp_number, lab_loc, stor_loc, stor_med, stor_med_vol, sample_mass):
        super().__init__(name, date, exp_number, lab_loc, stor_loc)
        self.State = "Solid"
        self.StorMed = stor_med
        self.StorMedVol = stor_med_vol
        self.SampleMass = sample_mass

    def info_to_dict(self):
        base = super().info_to_dict()
        base.update({
            "State": self.State,
            "Storage Medium": self.StorMed,
            "Storage Medium Volume": self.StorMedVol,
            "Sample Mass": self.SampleMass
            })
        return base

        
class LiquidSample(Sample):
    """Liquid sample, inherits sample object"""
    
    def __init__(self, name, date, exp_number, lab_loc, stor_loc, bottle, bottle_vol, sample_vol):
        super().__init__(name, date, exp_number, lab_loc, stor_loc)
        self.State = "Liquid"
        self.Bottle = bottle
        self.BottleVol = bottle_vol
        self.SampleVol = sample_vol
        
    def info_to_dict(self):
        base = super().info_to_dict()
        base.update({
            "State": self.State,
            "Bottle Type": self.Bottle,
            "Bottle Volume": self.BottleVol,
            "Sample Volume": self.SampleVol
            })
        return base


class SampleManager:
    """To track samples in inventory"""
    
    sample_file = os.path.join(os.getcwd(), "samples.json")
    
    def __init__(self):
        self.samples = self.load_samples()
        
    def load_samples(self):
        if not os.path.exists(self.sample_file):
            return []
        
        with open(self.sample_file, "r") as f:
            try:
                filedata = json.load(f)
            except json.JSONDecodeError:
                return []
            
        samples = [] # List to store the data
        
        for item in filedata:
            sample_type = item["Type"]
            
            if sample_type == "SolidSample":
                sample = SolidSample(
                    item["Name"],
                    item["Date"],
                    item["Experiment Number"],
                    item["Lab"],
                    item["Location"],
                    item["Storage Medium"],
                    item["Storage Medium Volume"],
                    item["Sample Mass"]
                    )
            
            elif sample_type == "LiquidSample":
                sample = LiquidSample(
                    item["Name"],
                    item["Date"],
                    item["Experiment Number"],
                    item["Lab"],
                    item["Location"],
                    item["Bottle Type"],
                    item["Bottle Volume"],
                    item["Sample Volume"]
                    )
            
            else:
                continue
            
            sample.ID = item["ID"]
            sample.Status = item["Status"]
            sample.CreatedAt = item["Entry created"]
            
            samples.append(sample) # Append sample information into the list
            
        return samples
    
    def save_samples(self):
        """Save samples into JSON file"""
        
        with open(self.sample_file, "w") as f:
            json.dump([s.info_to_dict() for s in self.samples], f, indent=4)
    
    def add_sample(self, sample):
        """Add sample into JSON file"""
        
        self.samples.append(sample)
        self.save_samples()
        SampleLogger.log_creation(sample)
    
    def delete_sample(self, sample_id):
        """Delete samples from JSON file"""
        
        self.samples = [s for s in self.samples if s.ID != sample_id]
        self.save_samples()
        SampleLogger.log_deletion(sample_id)
        
    def find_sample(self, sample_id):
        """Search for a sample"""
        
        for s in self.samples:
            if s.ID == sample_id:
                return s
        return None
    
    def list_samples(self):
        """Return a list of all samples"""
        
        return self.samples

