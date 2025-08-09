# Issue #9 Analysis: Create Missing src Directory Structure

## Issue Summary
- **Title**: 🚨 Critical: Create Missing src Directory Structure
- **Type**: Bug Fix (Critical)
- **Priority**: Critical
- **Labels**: bug, critical, infrastructure

## Problem Description
Main application files cannot start due to missing `src/` directory structure. The main files attempt to import from `src.routes` but this directory doesn't exist in the root.

## Root Cause
The project is missing the fundamental directory structure that the main application files expect:
- Missing `src/` directory in project root
- Missing `src/routes/` subdirectory
- Missing `__init__.py` files for proper Python package structure

## Required Solution
1. Create `src/` directory in project root
2. Create `src/routes/` subdirectory
3. Create proper `__init__.py` files for Python package structure

## Acceptance Criteria
- [ ] src/ directory exists in project root
- [ ] src/routes/ directory exists
- [ ] src/__init__.py file created
- [ ] src/routes/__init__.py file created
- [ ] Directory structure allows Python imports to resolve

## Files to Create
- `src/__init__.py`
- `src/routes/__init__.py`

## Impact
This is a blocking issue for all main applications - they cannot start without this directory structure.

## Estimated Time
2 hours (though this should be much quicker to implement)



## Code Analysis Findings

### Files Attempting to Import from src.routes:
1. `flask_server_fixes.py` - imports user, location, quest, narrative, equipment, combat blueprints
2. `main_clean.py` - imports user, location, quest, narrative, equipment, combat blueprints  
3. `main_quest_only.py` - imports quests blueprint
4. `main_robust.py` - imports quests, dynamic_quests blueprints
5. `shadowlands-backend/src/main.py` - imports quests, dynamic_quests blueprints

### Existing Blueprint Files Found:
- `combat.py` - contains `combat_bp` blueprint
- `equipment.py` - contains `equipment_bp` blueprint  
- `narrative.py` - contains `narrative_bp` blueprint
- `quest.py` - contains `quest_bp` blueprint

### Missing Blueprint Files:
- `user.py` - needs `user_bp` blueprint
- `location.py` - needs `location_bp` blueprint
- `quests.py` - needs `quests_bp` blueprint (different from quest.py)
- `dynamic_quests.py` - needs `dynamic_quests_bp` blueprint

### Existing Working Structure:
- `shadowlands-backend/src/routes/` already exists with proper structure
- Contains `quests.py` and `dynamic_quests.py` with proper blueprints

### Solution Required:
1. Create `src/` directory in project root
2. Create `src/routes/` subdirectory  
3. Create `src/__init__.py` and `src/routes/__init__.py`
4. Move existing blueprint files to `src/routes/`
5. Create missing blueprint files (user.py, location.py)
6. Ensure quests.py and dynamic_quests.py are available in src/routes/

