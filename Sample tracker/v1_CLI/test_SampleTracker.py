"""
Testing sample tracker using Pytest
"""

import os
import json
import pytest
from SampleTracker import (Sample, SolidSample, LiquidSample, SampleLogger, SampleManager)

"""Clean files before each test"""
@pytest.fixture(autouse=True)
def clean_files():
    """Reset JSON files before each test"""
    
    with open("samples.json", "w") as f:
        json.dump([], f)
        
    with open("sample_log.json", "w") as f:
        json.dump([], f)
        
    yield
    
    """Optional cleanup after test"""
    # os.remove(samples.json)
    # os.remove(sample_log.json)
    

def test_create_sample():
    """Test for: Creating an entry"""
    
    sample = Sample("Test", "2000-01-01", "TestRun-1", "Lab 1", "Shelf 1")
    
    assert sample.Name == "Test"
    assert sample.Status == "Not tested"
    assert sample.ID is not None
    
    
    
def test_update_status():
    """Test for: Updating sthe status of a sample"""
    
    sample = Sample("Test", "2000-01-01", "TestRun-1", "Lab 1", "Shelf 1")
    sample.update_status("Tested")
    assert sample.Status == "Tested"
    
    
    
def test_manager():
    """Test for: Adding and deleting a sample using Sample Manager"""
    
    manager = SampleManager() # Load sample manager
    
    sample = SolidSample(
        "Sodium sulfate",
        "2026-01-02",
        "20260101-1",
        "Lab 1",
        "Shelf 1",
        "Black cap bottle",
        "30ml",
        "5g")
    
    manager.add_sample(sample)
    assert len(manager.samples) == 1
    
    manager.delete_sample(sample.ID)
    assert len(manager.samples) == 0

    

def test_log_writing():
    """Test for: Writing of logs for sample recording"""
    sample = Sample("LogTest", "2026-01-03", "20260103-1", "Lab1", "Shelf 1")
    
    SampleLogger.log_creation(sample)

    with open("sample_log.json", "r") as f:
        logs = json.load(f)

    assert logs[0]["Event"] == "CREATED"
    
    

if __name__ == "__main__":
    test_create_sample()
    test_manager()
    test_update_status()
    test_log_writing()