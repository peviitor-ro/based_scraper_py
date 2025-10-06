#!/usr/bin/env python3
"""
Test script to validate the scraper validation logic.
This tests various valid and invalid scraper outputs.
"""

import json
import sys
import os

# Add the parent directory to the path to import from __test__
sys.path.insert(0, '/home/runner/work/based_scraper_py/based_scraper_py')

# Import the validation logic (we'll test it directly)
required_keys = ['company', 'job_title', 'job_link']
optional_keys = ['city', 'county', 'remote']
allowed_keys = required_keys + optional_keys
allowed_remote_values = ['remote', 'on-site', 'hybrid']

def validate_job(job):
    """Validate a single job object according to the new rules"""
    # Check that all required keys are present
    for req_key in required_keys:
        if req_key not in job:
            raise Exception(f"Required key '{req_key}' is missing! \n {job}")
    
    # Check each key in the job
    for key, value in job.items():
        # Reject keys that are not in the allowed list
        if key not in allowed_keys:
            raise Exception(f"Key '{key}' is not allowed! Allowed keys are: {', '.join(allowed_keys)}")

        # Check that required keys have non-None values
        if key in required_keys and value == None:
            raise Exception(f"Required key '{key}' has no value! \n {job}")
        
        # Validate remote field format
        if key == 'remote':
            # Remote must be a list
            if not isinstance(value, list):
                raise Exception(f"Key 'remote' must be a list, got {type(value).__name__}! \n {job}")
            
            # Check each value in the remote list
            for remote_val in value:
                # Must be lowercase
                if remote_val != remote_val.lower():
                    raise Exception(f"Remote value '{remote_val}' must be lowercase! \n {job}")
                
                # Must be in allowed values
                if remote_val not in allowed_remote_values:
                    raise Exception(f"Remote value '{remote_val}' is not allowed! Allowed values are: {', '.join(allowed_remote_values)} \n {job}")

def test_valid_cases():
    """Test valid scraper outputs"""
    print("Testing valid cases...")
    
    # Test 1: Minimal valid job (only required fields)
    job1 = {
        "company": "TestCompany",
        "job_title": "Software Engineer",
        "job_link": "https://example.com/job1"
    }
    try:
        validate_job(job1)
        print("✅ Test 1 passed: Minimal valid job")
    except Exception as e:
        print(f"❌ Test 1 failed: {e}")
        return False
    
    # Test 2: Job with city and county
    job2 = {
        "company": "TestCompany",
        "job_title": "Software Engineer",
        "job_link": "https://example.com/job2",
        "city": "București",
        "county": "București"
    }
    try:
        validate_job(job2)
        print("✅ Test 2 passed: Job with city and county")
    except Exception as e:
        print(f"❌ Test 2 failed: {e}")
        return False
    
    # Test 3: Job with remote field (single value)
    job3 = {
        "company": "TestCompany",
        "job_title": "Software Engineer",
        "job_link": "https://example.com/job3",
        "remote": ["remote"]
    }
    try:
        validate_job(job3)
        print("✅ Test 3 passed: Job with remote=['remote']")
    except Exception as e:
        print(f"❌ Test 3 failed: {e}")
        return False
    
    # Test 4: Job with remote field (multiple values)
    job4 = {
        "company": "TestCompany",
        "job_title": "Software Engineer",
        "job_link": "https://example.com/job4",
        "remote": ["on-site", "remote"]
    }
    try:
        validate_job(job4)
        print("✅ Test 4 passed: Job with remote=['on-site', 'remote']")
    except Exception as e:
        print(f"❌ Test 4 failed: {e}")
        return False
    
    # Test 5: Job with hybrid remote
    job5 = {
        "company": "TestCompany",
        "job_title": "Software Engineer",
        "job_link": "https://example.com/job5",
        "remote": ["hybrid"]
    }
    try:
        validate_job(job5)
        print("✅ Test 5 passed: Job with remote=['hybrid']")
    except Exception as e:
        print(f"❌ Test 5 failed: {e}")
        return False
    
    # Test 6: Job with all allowed keys
    job6 = {
        "company": "TestCompany",
        "job_title": "Software Engineer",
        "job_link": "https://example.com/job6",
        "city": "Cluj-Napoca",
        "county": "Cluj",
        "remote": ["remote", "on-site", "hybrid"]
    }
    try:
        validate_job(job6)
        print("✅ Test 6 passed: Job with all allowed keys")
    except Exception as e:
        print(f"❌ Test 6 failed: {e}")
        return False
    
    # Test 7: Job with empty remote list
    job7 = {
        "company": "TestCompany",
        "job_title": "Software Engineer",
        "job_link": "https://example.com/job7",
        "remote": []
    }
    try:
        validate_job(job7)
        print("✅ Test 7 passed: Job with empty remote list")
    except Exception as e:
        print(f"❌ Test 7 failed: {e}")
        return False
    
    return True

def test_invalid_cases():
    """Test invalid scraper outputs that should fail"""
    print("\nTesting invalid cases...")
    
    # Test 1: Missing required key (company)
    job1 = {
        "job_title": "Software Engineer",
        "job_link": "https://example.com/job1"
    }
    try:
        validate_job(job1)
        print("❌ Test 1 failed: Should reject missing 'company' key")
        return False
    except Exception as e:
        if "Required key 'company' is missing" in str(e):
            print("✅ Test 1 passed: Correctly rejects missing required key")
        else:
            print(f"❌ Test 1 failed with wrong error: {e}")
            return False
    
    # Test 2: Missing required key (job_title)
    job2 = {
        "company": "TestCompany",
        "job_link": "https://example.com/job2"
    }
    try:
        validate_job(job2)
        print("❌ Test 2 failed: Should reject missing 'job_title' key")
        return False
    except Exception as e:
        if "Required key 'job_title' is missing" in str(e):
            print("✅ Test 2 passed: Correctly rejects missing 'job_title'")
        else:
            print(f"❌ Test 2 failed with wrong error: {e}")
            return False
    
    # Test 3: Missing required key (job_link)
    job3 = {
        "company": "TestCompany",
        "job_title": "Software Engineer"
    }
    try:
        validate_job(job3)
        print("❌ Test 3 failed: Should reject missing 'job_link' key")
        return False
    except Exception as e:
        if "Required key 'job_link' is missing" in str(e):
            print("✅ Test 3 passed: Correctly rejects missing 'job_link'")
        else:
            print(f"❌ Test 3 failed with wrong error: {e}")
            return False
    
    # Test 4: Extra key not allowed (country)
    job4 = {
        "company": "TestCompany",
        "job_title": "Software Engineer",
        "job_link": "https://example.com/job4",
        "country": "Romania"
    }
    try:
        validate_job(job4)
        print("❌ Test 4 failed: Should reject 'country' key")
        return False
    except Exception as e:
        if "Key 'country' is not allowed" in str(e):
            print("✅ Test 4 passed: Correctly rejects 'country' key")
        else:
            print(f"❌ Test 4 failed with wrong error: {e}")
            return False
    
    # Test 5: Remote as string instead of list
    job5 = {
        "company": "TestCompany",
        "job_title": "Software Engineer",
        "job_link": "https://example.com/job5",
        "remote": "remote"
    }
    try:
        validate_job(job5)
        print("❌ Test 5 failed: Should reject remote as string")
        return False
    except Exception as e:
        if "must be a list" in str(e):
            print("✅ Test 5 passed: Correctly rejects remote as string")
        else:
            print(f"❌ Test 5 failed with wrong error: {e}")
            return False
    
    # Test 6: Remote with uppercase value
    job6 = {
        "company": "TestCompany",
        "job_title": "Software Engineer",
        "job_link": "https://example.com/job6",
        "remote": ["Remote"]
    }
    try:
        validate_job(job6)
        print("❌ Test 6 failed: Should reject uppercase remote value")
        return False
    except Exception as e:
        if "must be lowercase" in str(e):
            print("✅ Test 6 passed: Correctly rejects uppercase remote value")
        else:
            print(f"❌ Test 6 failed with wrong error: {e}")
            return False
    
    # Test 7: Remote with invalid value
    job7 = {
        "company": "TestCompany",
        "job_title": "Software Engineer",
        "job_link": "https://example.com/job7",
        "remote": ["invalid"]
    }
    try:
        validate_job(job7)
        print("❌ Test 7 failed: Should reject invalid remote value")
        return False
    except Exception as e:
        if "is not allowed" in str(e) and "invalid" in str(e):
            print("✅ Test 7 passed: Correctly rejects invalid remote value")
        else:
            print(f"❌ Test 7 failed with wrong error: {e}")
            return False
    
    # Test 8: Required key with None value
    job8 = {
        "company": None,
        "job_title": "Software Engineer",
        "job_link": "https://example.com/job8"
    }
    try:
        validate_job(job8)
        print("❌ Test 8 failed: Should reject None value for required key")
        return False
    except Exception as e:
        if "has no value" in str(e):
            print("✅ Test 8 passed: Correctly rejects None value for required key")
        else:
            print(f"❌ Test 8 failed with wrong error: {e}")
            return False
    
    return True

if __name__ == "__main__":
    print("=" * 60)
    print("Testing Scraper Validation Logic")
    print("=" * 60)
    
    valid_passed = test_valid_cases()
    invalid_passed = test_invalid_cases()
    
    print("\n" + "=" * 60)
    if valid_passed and invalid_passed:
        print("✅ All tests passed!")
        print("=" * 60)
        sys.exit(0)
    else:
        print("❌ Some tests failed!")
        print("=" * 60)
        sys.exit(1)
