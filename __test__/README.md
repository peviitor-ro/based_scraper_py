# Scraper Validation Tests

This directory contains validation tests for the scraper system.

## Files

### runTest.py
Main validation script that checks scrapers against the required output format.
It runs all changed scraper files and validates their JSON output.

**Validation Rules:**

1. **Required keys** (must be present with non-None values):
   - `company`: The company name
   - `job_title`: The job title
   - `job_link`: URL to the job posting

2. **Optional keys** (may be present):
   - `city`: City location(s)
   - `county`: County location(s)
   - `remote`: Work arrangement options (must be a list)

3. **Remote field validation** (when present):
   - Must be a list (even if empty)
   - All values must be lowercase
   - Only allowed values: `remote`, `on-site`, `hybrid`
   - Valid examples:
     ```json
     {"remote": ["remote"]}
     {"remote": ["on-site", "hybrid"]}
     {"remote": ["remote", "on-site", "hybrid"]}
     {"remote": []}
     ```

4. **All other keys are rejected** - no additional fields are allowed.

### test_validation.py
Unit tests for the validation logic. Tests both valid and invalid scraper outputs
to ensure the validation rules work correctly.

Run with:
```bash
python3 __test__/test_validation.py
```

### publish.py
Script for publishing validated jobs to the API.

## Running Tests

To run the validation tests:

```bash
# Run unit tests
python3 __test__/test_validation.py

# Run validation on changed scrapers
python3 __test__/runTest.py
```

## Example Valid Scraper Output

```json
[
  {
    "company": "ExampleCompany",
    "job_title": "Software Engineer",
    "job_link": "https://example.com/jobs/123",
    "city": "București",
    "county": "București",
    "remote": ["remote", "on-site"]
  },
  {
    "company": "ExampleCompany",
    "job_title": "Data Scientist",
    "job_link": "https://example.com/jobs/124"
  }
]
```

## Common Validation Errors

### ❌ Using 'country' field
```json
{
  "company": "Test",
  "job_title": "Engineer",
  "job_link": "https://example.com/job",
  "country": "Romania"  // NOT ALLOWED
}
```
**Error:** `Key 'country' is not allowed! Allowed keys are: company, job_title, job_link, city, county, remote`

### ❌ Remote as string
```json
{
  "company": "Test",
  "job_title": "Engineer",
  "job_link": "https://example.com/job",
  "remote": "remote"  // Should be ["remote"]
}
```
**Error:** `Key 'remote' must be a list, got str!`

### ❌ Uppercase remote value
```json
{
  "company": "Test",
  "job_title": "Engineer",
  "job_link": "https://example.com/job",
  "remote": ["Remote"]  // Should be lowercase
}
```
**Error:** `Remote value 'Remote' must be lowercase!`

### ❌ Invalid remote value
```json
{
  "company": "Test",
  "job_title": "Engineer",
  "job_link": "https://example.com/job",
  "remote": ["work-from-home"]  // Not in allowed list
}
```
**Error:** `Remote value 'work-from-home' is not allowed! Allowed values are: remote, on-site, hybrid`

### ❌ Missing required field
```json
{
  "job_title": "Engineer",
  "job_link": "https://example.com/job"
  // Missing 'company'
}
```
**Error:** `Required key 'company' is missing!`
