# Feature Specification: Tag System for Todo App

## Problem
Users need to categorize tasks with arbitrary labels (tags) and query tasks by tag(s). The core todo app lacks tag functionality.

## Use Cases
- Add a task with tags
- Add/remove tags to existing tasks
- Filter tasks by one or more tags (AND/OR)
- Show tag counts and list all tags

## Requirements
- Add new functions implementing tag support (see README API)
- Tests: unit, integration, backward compatibility, error handling
- Scripts to create virtualenv & run tests on Windows/Linux

## Success Metrics
- All tests pass in CI using the provided run scripts
- Backward-compatible behavior preserved
- New functions implemented and documented
