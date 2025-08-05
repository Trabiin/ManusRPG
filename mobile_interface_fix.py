#!/usr/bin/env python3
"""
Script to fix the remaining corrupted buttons in MobileGameInterface.jsx
"""

import re

def fix_mobile_interface():
    file_path = '/home/ubuntu/shadowlands-rpg/src/components/game/MobileGameInterface.jsx'
    
    # Read the file
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Fix the game button
    game_button_pattern = r'''            <button
              onClick=\(e\) = className="min-h-\[44px\] min-w-\[44px\] touch-manipulation select-none" onTouchStart=\(e\) => e\.preventDefault\(\)\}> \{
                    e\.preventDefault\(\);
                    \(\) => \{
                setActivePanel\('game'\);
                setShowMenu\(false\);
              \(e\);
                \}\}
                onTouchEnd=\(e\) => \{
                    e\.preventDefault\(\);
                    e\.stopPropagation\(\);
                    \(\) => \{
                setActivePanel\('game'\);
                setShowMenu\(false\);
              \(e\);
                \}\}\}
              className="w-full text-left p-3 bg-gray-700 rounded text-gray-200 hover:bg-gray-600 focus:bg-gray-600 active:bg-gray-600 focus:bg-gray-600 active:bg-gray-600 focus:bg-gray-600 active:bg-gray-600 focus:bg-gray-600 active:bg-gray-600"
            >'''
    
    game_button_replacement = '''            <button
              onClick={(e) => {
                e.preventDefault();
                setActivePanel('game');
                setShowMenu(false);
              }}
              onTouchStart={(e) => e.preventDefault()}
              onTouchEnd={(e) => {
                e.preventDefault();
                e.stopPropagation();
                setActivePanel('game');
                setShowMenu(false);
              }}
              className="w-full text-left p-3 bg-gray-700 rounded text-gray-200 hover:bg-gray-600 focus:bg-gray-600 active:bg-gray-600 min-h-[44px] min-w-[44px] touch-manipulation select-none"
            >'''
    
    # Fix the overlay click handler
    overlay_pattern = r'''          <div 
            className="flex-1"
            onClick=\(e\) => \{
                    e\.preventDefault\(\);
                    \(\) => setShowMenu\(false\)\(e\);
                \}\}'''
    
    overlay_replacement = '''          <div 
            className="flex-1"
            onClick={(e) => {
              e.preventDefault();
              setShowMenu(false);
            }}
            onTouchEnd={(e) => {
              e.preventDefault();
              e.stopPropagation();
              setShowMenu(false);
            }}'''
    
    # Apply fixes
    content = re.sub(game_button_pattern.replace('(', r'\(').replace(')', r'\)').replace('[', r'\[').replace(']', r'\]').replace('{', r'\{').replace('}', r'\}'), game_button_replacement, content, flags=re.DOTALL)
    
    # Simple string replacement for overlay since regex is complex
    if "() => setShowMenu(false)(e);" in content:
        content = content.replace(
            '''          <div 
            className="flex-1"
            onClick={(e) => {
                    e.preventDefault();
                    () => setShowMenu(false)(e);
                }}''',
            '''          <div 
            className="flex-1"
            onClick={(e) => {
              e.preventDefault();
              setShowMenu(false);
            }}
            onTouchEnd={(e) => {
              e.preventDefault();
              e.stopPropagation();
              setShowMenu(false);
            }}'''
        )
    
    # Write the fixed content back
    with open(file_path, 'w') as f:
        f.write(content)
    
    print("✅ Fixed corrupted buttons in MobileGameInterface.jsx")
    return True

if __name__ == "__main__":
    fix_mobile_interface()

