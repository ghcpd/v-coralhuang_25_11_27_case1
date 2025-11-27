# FEATURE_SPEC: Tag-based Todo System

Problem: The simple todo app lacks a way to categorize and filter tasks.

Use Cases:
- Add tags to new tasks
- Add/remove tags to existing tasks
- Filter by single or multiple tags with AND/OR logic
- View counts of tags for quick insights
- Backwards compatible with untagged tasks

Requirements:
- Functions to add/list/filter tasks and tags
- Tag normalization (case-insensitive)
- No duplicate tags
- Robust error handling for invalid input and indices

Success Metrics:
- All functions listed in the deliverables are implemented
- A comprehensive pytest suite covers unit & integration tests
- Setup scripts allow onboarding in <5 minutes
