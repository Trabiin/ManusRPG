#!/usr/bin/env python3
"""
Manual fix for the remaining corrupted buttons in MobileGameInterface.jsx
"""

def manual_fix():
    file_path = '/home/ubuntu/shadowlands-rpg/src/components/game/MobileGameInterface.jsx'
    
    # Read the file
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Find and replace the corrupted game button
    corrupted_game = '''            <button
              onClick={(e) = className="min-h-[44px] min-w-[44px] touch-manipulation select-none" onTouchStart={(e) => e.preventDefault()}> {
                    e.preventDefault();
                    () => {
                setActivePanel('game');
                setShowMenu(false);
              (e);
                }}
                onTouchEnd={(e) => {
                    e.preventDefault();
                    e.stopPropagation();
                    () => {
                setActivePanel('game');
                setShowMenu(false);
              (e);
                }}}
              className="w-full text-left p-3 bg-gray-700 rounded text-gray-200 hover:bg-gray-600 focus:bg-gray-600 active:bg-gray-600 focus:bg-gray-600 active:bg-gray-600 focus:bg-gray-600 active:bg-gray-600 focus:bg-gray-600 active:bg-gray-600"
            >'''
    
    fixed_game = '''            <button
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
    
    # Apply the fix
    if corrupted_game in content:
        content = content.replace(corrupted_game, fixed_game)
        print("✅ Fixed game button")
    else:
        print("⚠️ Game button pattern not found")
    
    # Fix the overlay click handler if it exists
    corrupted_overlay = '''            onClick={(e) => {
                    e.preventDefault();
                    () => setShowMenu(false)(e);
                }}'''
    
    fixed_overlay = '''            onClick={(e) => {
              e.preventDefault();
              setShowMenu(false);
            }}
            onTouchEnd={(e) => {
              e.preventDefault();
              e.stopPropagation();
              setShowMenu(false);
            }}'''
    
    if corrupted_overlay in content:
        content = content.replace(corrupted_overlay, fixed_overlay)
        print("✅ Fixed overlay click handler")
    else:
        print("⚠️ Overlay pattern not found")
    
    # Write the fixed content back
    with open(file_path, 'w') as f:
        f.write(content)
    
    print("✅ Manual fix completed")
    return True

if __name__ == "__main__":
    manual_fix()

