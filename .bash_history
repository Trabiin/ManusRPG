export PS1="[CMD_BEGIN]\n\u@\h:\w\n[CMD_END]"; export PS2=""
export TERM=xterm-256color
export OPENAI_API_KEY="sk-hTr5CwTzq3dBc3XQS4yEJw"
export OPENAI_API_BASE="https://api.manus.im/api/llm-proxy/v1"
export OPENAI_BASE_URL="https://api.manus.im/api/llm-proxy/v1"
cd /home/ubuntu && cp /home/ubuntu/upload/.recovery/quest_engine_core.py /home/ubuntu/ && cp /home/ubuntu/upload/.recovery/quest_api_test.py /home/ubuntu/ && cp /home/ubuntu/upload/.recovery/ci1_quest_system_architecture.md /home/ubuntu/
cd /home/ubuntu && mkdir -p /home/ubuntu/shadowlands-backend/src/routes && cp /home/ubuntu/upload/.recovery/main.py /home/ubuntu/shadowlands-backend/src/ && cp /home/ubuntu/upload/.recovery/quests.py /home/ubuntu/shadowlands-backend/src/routes/
cd /home/ubuntu && cd /home/ubuntu && python3.11 -c "
from quest_engine_core import QuestEngine
engine = QuestEngine()
print('🎮 Quest Engine Test')
print(f'✅ Templates loaded: {len(engine.quest_templates)}')
for template_id, template in engine.quest_templates.items():
    print(f'   • {template.title} ({template.quest_type.value})')
print('✅ Quest engine working correctly!')
"
cd /home/ubuntu && cd /home/ubuntu && python3.11 -c "
from quest_engine_core import QuestEngine
engine = QuestEngine()

# Test character data
character_data = {
    'character_id': 'test_char_001',
    'level': 3,
    'name': 'Test Drifter',
    'attributes': {'might': 12, 'intellect': 10, 'will': 14, 'shadow': 8}
}

print('🎮 Quest Creation and Progression Test')
print('=' * 40)

# Get available quests
available = engine.get_available_quest_templates(character_data)
print(f'✅ Available quests: {len(available)}')

# Create a quest
if available:
    template_id = available[0]['template_id']
    quest = engine.create_quest_for_character(template_id, character_data['character_id'], character_data)
    
    if quest:
        print(f'✅ Created quest: {quest.title}')
        print(f'   Quest ID: {quest.quest_id}')
        print(f'   Status: {quest.status.value}')
        print(f'   Objectives: {len(quest.objectives)}')
        print(f'   Choices: {len(quest.choices)}')
        
        # Test objective progress
        if quest.objectives:
            obj_id = quest.objectives[0].objective_id
            result = engine.update_quest_objective(character_data['character_id'], quest.quest_id, obj_id)
            print(f'✅ Updated objective: {result}')
        
        print('✅ Quest system fully functional!')
    else:
        print('❌ Failed to create quest')
else:
    print('❌ No available quests found')
"
cd /home/ubuntu && sleep 3 && curl -s http://localhost:5002/api/quests/templates | head -5
cd /home/ubuntu && ps aux | grep python | grep main.py
cd /home/ubuntu && grep -n "quest" /home/ubuntu/shadowlands-backend/src/main.py
cd /home/ubuntu && pip3 install flask flask-cors flask-sqlalchemy
export PS1="[CMD_BEGIN]\n\u@\h:\w\n[CMD_END]"; export PS2=""
export TERM=xterm-256color
export OPENAI_API_KEY="sk-hTr5CwTzq3dBc3XQS4yEJw"
export OPENAI_API_BASE="https://api.manus.im/api/llm-proxy/v1"
export OPENAI_BASE_URL="https://api.manus.im/api/llm-proxy/v1"
cd /home/ubuntu && curl -s http://localhost:5002/api/health
cd /home/ubuntu && curl -s http://localhost:5002/api/quests/templates
cd /home/ubuntu && curl -s -c cookies.txt http://localhost:5002/api/session/init
cd /home/ubuntu && curl -s -b cookies.txt -X POST -H "Content-Type: application/json" -d '{"template_id": "main_001"}' http://localhost:5002/api/quests/start
cd /home/ubuntu && curl -s -b cookies.txt -X POST -H "Content-Type: application/json" -d '{"increment": 1}' http://localhost:5002/api/quests/e11a4409-bb9f-4f6b-a60e-08ebf7013d9c/objective/27fc3543-f8fa-4e95-8eeb-39a2980e6534/progress
cd /home/ubuntu && python3.11 quest_system_comprehensive_test.py
export PS1="[CMD_BEGIN]\n\u@\h:\w\n[CMD_END]"; export PS2=""
export TERM=xterm-256color
export OPENAI_API_KEY="sk-hTr5CwTzq3dBc3XQS4yEJw"
export OPENAI_API_BASE="https://api.manus.im/api/llm-proxy/v1"
export OPENAI_BASE_URL="https://api.manus.im/api/llm-proxy/v1"
cd /home/ubuntu && cd /home/ubuntu/shadowlands-backend && python3.11 src/main.py &
cd /home/ubuntu && cd /home/ubuntu/shadowlands-backend && python3.11 src/main.py
cd /home/ubuntu && cd /home/ubuntu/shadowlands-backend && python3.11 src/main_quest_only.py
export PS1="[CMD_BEGIN]\n\u@\h:\w\n[CMD_END]"; export PS2=""
export TERM=xterm-256color
export OPENAI_API_KEY="sk-hTr5CwTzq3dBc3XQS4yEJw"
export OPENAI_API_BASE="https://api.manus.im/api/llm-proxy/v1"
export OPENAI_BASE_URL="https://api.manus.im/api/llm-proxy/v1"
cd /home/ubuntu && echo "Testing sandbox" && ls /home/ubuntu/quest_engine_core.py
export PS1="[CMD_BEGIN]\n\u@\h:\w\n[CMD_END]"; export PS2=""
export TERM=xterm-256color
export OPENAI_API_KEY="sk-hTr5CwTzq3dBc3XQS4yEJw"
export OPENAI_API_BASE="https://api.manus.im/api/llm-proxy/v1"
export OPENAI_BASE_URL="https://api.manus.im/api/llm-proxy/v1"
cd /home/ubuntu && curl -s -c /tmp/integration_cookies.txt http://localhost:5002/api/session/init && curl -s -b /tmp/integration_cookies.txt -X POST -H "Content-Type: application/json" -d '{"trigger": "random_encounter"}' http://localhost:5002/api/dynamic-quests/generate
cd /home/ubuntu && curl -s -b /tmp/integration_cookies.txt -X POST -H "Content-Type: application/json" -d '{"template_id": "dynamic_betrayal_bb40f269"}' http://localhost:5002/api/quests/start
cd /home/ubuntu && python3.11 phase3_dynamic_quest_comprehensive_test.py
export PS1="[CMD_BEGIN]\n\u@\h:\w\n[CMD_END]"; export PS2=""
export TERM=xterm-256color
export OPENAI_API_KEY="sk-hTr5CwTzq3dBc3XQS4yEJw"
export OPENAI_API_BASE="https://api.manus.im/api/llm-proxy/v1"
export OPENAI_BASE_URL="https://api.manus.im/api/llm-proxy/v1"
cd /home/ubuntu && grep -n "dynamic_generator\." /home/ubuntu/shadowlands-backend/src/routes/dynamic_quests.py
cd /home/ubuntu && grep -n "quest_engine\." /home/ubuntu/shadowlands-backend/src/routes/quests.py
cd /home/ubuntu && sed -i 's/quest_engine\./get_quest_engine_instance()./g' /home/ubuntu/shadowlands-backend/src/routes/quests.py
export PS1="[CMD_BEGIN]\n\u@\h:\w\n[CMD_END]"; export PS2=""
export TERM=xterm-256color
export OPENAI_API_KEY="sk-hTr5CwTzq3dBc3XQS4yEJw"
export OPENAI_API_BASE="https://api.manus.im/api/llm-proxy/v1"
export OPENAI_BASE_URL="https://api.manus.im/api/llm-proxy/v1"
cd /home/ubuntu && cd /home/ubuntu/shadowlands-backend && python3.11 src/main_quest_only.py &
export PS1="[CMD_BEGIN]\n\u@\h:\w\n[CMD_END]"; export PS2=""
export TERM=xterm-256color
export OPENAI_API_KEY="sk-hTr5CwTzq3dBc3XQS4yEJw"
export OPENAI_API_BASE="https://api.manus.im/api/llm-proxy/v1"
export OPENAI_BASE_URL="https://api.manus.im/api/llm-proxy/v1"
cd /home/ubuntu && ps aux | grep main_robust
cd /home/ubuntu && kill 3307
export PS1="[CMD_BEGIN]\n\u@\h:\w\n[CMD_END]"; export PS2=""
export TERM=xterm-256color
export OPENAI_API_KEY="sk-hTr5CwTzq3dBc3XQS4yEJw"
export OPENAI_API_BASE="https://api.manus.im/api/llm-proxy/v1"
export OPENAI_BASE_URL="https://api.manus.im/api/llm-proxy/v1"
cd /home/ubuntu && find /home/ubuntu -type f -name "*.py" -o -name "*.js" -o -name "*.jsx" -o -name "*.json" -o -name "*.md" | sort
export PS1="[CMD_BEGIN]\n\u@\h:\w\n[CMD_END]"; export PS2=""
export TERM=xterm-256color
export OPENAI_API_KEY="sk-hTr5CwTzq3dBc3XQS4yEJw"
export OPENAI_API_BASE="https://api.manus.im/api/llm-proxy/v1"
export OPENAI_BASE_URL="https://api.manus.im/api/llm-proxy/v1"
cd /home/ubuntu && cd /home/ubuntu && python3.11 -c "
from quest_engine_core import QuestEngine
engine = QuestEngine()
print('🎮 Sandbox Connectivity Test')
print(f'✅ Quest Engine: {len(engine.quest_templates)} templates loaded')
print('✅ Sandbox connectivity: WORKING')
"
cd /home/ubuntu && curl -s http://localhost:5002/api/health
cd /home/ubuntu && ps aux | grep python | grep main_quest_only
cd /home/ubuntu && sleep 3 && curl -s http://localhost:5002/api/health
export PS1="[CMD_BEGIN]\n\u@\h:\w\n[CMD_END]"; export PS2=""
export TERM=xterm-256color
export OPENAI_API_KEY="sk-hTr5CwTzq3dBc3XQS4yEJw"
export OPENAI_API_BASE="https://api.manus.im/api/llm-proxy/v1"
export OPENAI_BASE_URL="https://api.manus.im/api/llm-proxy/v1"
cd /home/ubuntu && ps aux | grep python
cd /home/ubuntu && kill 2647 2648
cd /home/ubuntu && ps aux | grep main_quest_only
cd /home/ubuntu && kill -9 2647 2648
export PS1="[CMD_BEGIN]\n\u@\h:\w\n[CMD_END]"; export PS2=""
export TERM=xterm-256color
export OPENAI_API_KEY="sk-hTr5CwTzq3dBc3XQS4yEJw"
export OPENAI_API_BASE="https://api.manus.im/api/llm-proxy/v1"
export OPENAI_BASE_URL="https://api.manus.im/api/llm-proxy/v1"
cd /home/ubuntu && cd /home/ubuntu/shadowlands-backend && python3.11 src/main_robust.py
export PS1="[CMD_BEGIN]\n\u@\h:\w\n[CMD_END]"; export PS2=""
export TERM=xterm-256color
export OPENAI_API_KEY="sk-hTr5CwTzq3dBc3XQS4yEJw"
export OPENAI_API_BASE="https://api.manus.im/api/llm-proxy/v1"
export OPENAI_BASE_URL="https://api.manus.im/api/llm-proxy/v1"
cd /home/ubuntu && ls -la /home/ubuntu/ | grep -E "(shadowlands|quest|mobile|api|phase|todo)"
cd /home/ubuntu && ls -la /home/ubuntu/ | grep shadowlands && echo "=== Backend contents ===" && find /home/ubuntu/shadowlands-backend -type f -name "*.py" | sort
cd /home/ubuntu && ls -la /home/ubuntu/shadowlands-rpg 2>/dev/null || echo "shadowlands-rpg directory NOT FOUND" && echo "=== Checking for other expected files ===" && ls -la /home/ubuntu/*mobile* /home/ubuntu/*bundle* /home/ubuntu/*performance* /home/ubuntu/*critical* 2>/dev/null || echo "Other expected files NOT FOUND"
export PS1="[CMD_BEGIN]\n\u@\h:\w\n[CMD_END]"; export PS2=""
export TERM=xterm-256color
export OPENAI_API_KEY="sk-hTr5CwTzq3dBc3XQS4yEJw"
export OPENAI_API_BASE="https://api.manus.im/api/llm-proxy/v1"
export OPENAI_BASE_URL="https://api.manus.im/api/llm-proxy/v1"
cd /home/ubuntu && curl -s http://localhost:5002/api/health
cd /home/ubuntu && curl -s -c /tmp/dynamic_cookies.txt http://localhost:5002/api/session/init
cd /home/ubuntu && curl -s -b /tmp/dynamic_cookies.txt http://localhost:5002/api/dynamic-quests/narrative-context
cd /home/ubuntu && curl -s -b /tmp/dynamic_cookies.txt -X POST -H "Content-Type: application/json" -d '{"trigger": "random_encounter", "location_context": "Shadowlands Outskirts"}' http://localhost:5002/api/dynamic-quests/generate
cd /home/ubuntu && curl -s -b /tmp/dynamic_cookies.txt http://localhost:5002/api/dynamic-quests/themes
cd /home/ubuntu && curl -s -b /tmp/dynamic_cookies.txt http://localhost:5002/api/dynamic-quests/archetypes
cd /home/ubuntu && python3.11 phase3_dynamic_quest_comprehensive_test.py
cd /home/ubuntu && curl -s -b /tmp/dynamic_cookies.txt -X POST -H "Content-Type: application/json" -d '{"trigger": "random_encounter"}' http://localhost:5002/api/dynamic-quests/generate | head -c 200
cd /home/ubuntu && curl -s -b /tmp/dynamic_cookies.txt -X POST -H "Content-Type: application/json" -d '{"trigger": "random_encounter"}' http://localhost:5002/api/dynamic-quests/generate
cd /home/ubuntu && curl -s -b /tmp/dynamic_cookies.txt -X POST -H "Content-Type: application/json" -d '{"template_id": "dynamic_revenge_fbc5b6c2"}' http://localhost:5002/api/quests/start
export PS1="[CMD_BEGIN]\n\u@\h:\w\n[CMD_END]"; export PS2=""
export TERM=xterm-256color
export OPENAI_API_KEY="sk-hTr5CwTzq3dBc3XQS4yEJw"
export OPENAI_API_BASE="https://api.manus.im/api/llm-proxy/v1"
export OPENAI_BASE_URL="https://api.manus.im/api/llm-proxy/v1"
cd /home/ubuntu && curl -s http://localhost:5002/api/health
export PS1="[CMD_BEGIN]\n\u@\h:\w\n[CMD_END]"; export PS2=""
export TERM=xterm-256color
export OPENAI_API_KEY="sk-hTr5CwTzq3dBc3XQS4yEJw"
export OPENAI_API_BASE="https://api.manus.im/api/llm-proxy/v1"
export OPENAI_BASE_URL="https://api.manus.im/api/llm-proxy/v1"
cd /home/ubuntu && curl -s http://localhost:5002/api/health
cd /home/ubuntu && curl -s http://localhost:5002/api/quests/templates | jq .
cd /home/ubuntu && curl -s http://localhost:5002/api/quests/templates
cd /home/ubuntu && curl -s -c /tmp/cookies.txt http://localhost:5002/api/session/init
cd /home/ubuntu && curl -s -b /tmp/cookies.txt -X POST -H "Content-Type: application/json" -d '{"template_id": "main_001"}' http://localhost:5002/api/quests/start
cd /home/ubuntu && curl -s -b /tmp/cookies.txt http://localhost:5002/api/quests/active
cd /home/ubuntu && curl -s -b /tmp/cookies.txt -X POST -H "Content-Type: application/json" -d '{"increment": 1}' http://localhost:5002/api/quests/2bc9885e-678c-4026-a071-c0011de756ab/objective/8f754ee7-9653-41b7-8c10-e5866fe251ca/progress
cd /home/ubuntu && curl -s -b /tmp/cookies.txt http://localhost:5002/api/quests/statistics
cd /home/ubuntu && python3.11 quest_system_comprehensive_test.py
cd /home/ubuntu && curl -s -b /tmp/cookies.txt -X POST -H "Content-Type: application/json" -d '{"template_id": "invalid_quest"}' http://localhost:5002/api/quests/start
cd /home/ubuntu && curl -s http://localhost:5002/api/quests/active
export PS1="[CMD_BEGIN]\n\u@\h:\w\n[CMD_END]"; export PS2=""
export TERM=xterm-256color
export OPENAI_API_KEY="sk-hTr5CwTzq3dBc3XQS4yEJw"
export OPENAI_API_BASE="https://api.manus.im/api/llm-proxy/v1"
export OPENAI_BASE_URL="https://api.manus.im/api/llm-proxy/v1"
cd /home/ubuntu && ps aux | grep main_robust
cd /home/ubuntu && kill 4551
export PS1="[CMD_BEGIN]\n\u@\h:\w\n[CMD_END]"; export PS2=""
export TERM=xterm-256color
export OPENAI_API_KEY="sk-hTr5CwTzq3dBc3XQS4yEJw"
export OPENAI_API_BASE="https://api.manus.im/api/llm-proxy/v1"
export OPENAI_BASE_URL="https://api.manus.im/api/llm-proxy/v1"
cd /home/ubuntu && cd /home/ubuntu && python3.11 dynamic_quest_generation.py
export PS1="[CMD_BEGIN]\n\u@\h:\w\n[CMD_END]"; export PS2=""
export TERM=xterm-256color
export OPENAI_API_KEY="sk-hTr5CwTzq3dBc3XQS4yEJw"
export OPENAI_API_BASE="https://api.manus.im/api/llm-proxy/v1"
export OPENAI_BASE_URL="https://api.manus.im/api/llm-proxy/v1"
cd /home/ubuntu && cd /home/ubuntu/shadowlands-backend && python3.11 src/main_robust.py
export PS1="[CMD_BEGIN]\n\u@\h:\w\n[CMD_END]"; export PS2=""
export TERM=xterm-256color
export OPENAI_API_KEY="sk-hTr5CwTzq3dBc3XQS4yEJw"
export OPENAI_API_BASE="https://api.manus.im/api/llm-proxy/v1"
export OPENAI_BASE_URL="https://api.manus.im/api/llm-proxy/v1"
ps() { /bin/ps "$@" | grep -v -E '(start_server\.py|upgrade\.py|supervisor)' || true; }
pgrep() { /usr/bin/pgrep "$@" | while read pid; do [ -n "$pid" ] && cmdline=$(/bin/ps -p $pid -o command= 2>/dev/null) && ! echo "$cmdline" | grep -q -E '(start_server\.py|upgrade\.py|supervisor)' && echo "$pid"; done; }
cd /home/ubuntu/upload && cd /home/ubuntu/upload && unzip -l DarkFantasyRPGFramework\(1\).zip | head -20
cd /home/ubuntu/upload && cd /home/ubuntu/upload && ls -la *.zip
cd /home/ubuntu/upload && cd /home/ubuntu/upload && mkdir -p zip1 zip2 zip3 zip4 && unzip -q "DarkFantasyRPGFramework(1).zip" -d zip1/ && unzip -q "DarkFantasyRoleplayingGameFramework(1).zip" -d zip2/ && unzip -q "DarkFantasyRoleplayingGameFrameworkDevelopment.zip" -d zip3/ && unzip -q "CreatingaDarkFantasyRoleplayingGameFramework.zip" -d zip4/ 2>/dev/null || echo "Some extractions may have failed"
cd /home/ubuntu/upload && cd /home/ubuntu/upload && echo "=== ZIP1 Contents ===" && ls -la zip1/ && echo "=== ZIP2 Contents ===" && ls -la zip2/ && echo "=== ZIP3 Contents ===" && ls -la zip3/ && echo "=== ZIP4 Contents ===" && ls -la zip4/
cd /home/ubuntu/upload && cd /home/ubuntu/upload && find zip3/shadowlands-rpg -type f | head -20 && echo "=== Total files in shadowlands-rpg ===" && find zip3/shadowlands-rpg -type f | wc -l
cd /home/ubuntu/upload && cd /home/ubuntu/upload && find zip3/ -type d | head -10 && echo "=== Looking for React/JS files ===" && find zip3/ -name "*.jsx" -o -name "*.js" -o -name "package.json" | head -10
cd /home/ubuntu/upload && cd /home/ubuntu/upload && echo "=== ZIP2 React files ===" && find zip2/ -name "*.jsx" -o -name "*.js" | head -10 && echo "=== Quest system files comparison ===" && echo "ZIP1 quest files:" && ls -la zip1/*quest* zip1/*main* 2>/dev/null && echo "ZIP2 quest files:" && ls -la zip2/*quest* zip2/*main* 2>/dev/null && echo "ZIP3 quest files:" && ls -la zip3/*quest* zip3/*main* 2>/dev/null
cd /home/ubuntu/upload && cd /home/ubuntu/upload && echo "=== Comparing App.jsx files ===" && ls -la zip2/App.jsx zip3/App.jsx && echo "=== Looking for MobileGameInterface ===" && find zip2/ zip3/ -name "*Mobile*" -o -name "*mobile*" && echo "=== Looking for critical optimization files ===" && find zip1/ zip2/ zip3/ -name "*mobile*" -o -name "*bundle*" -o -name "*performance*" -o -name "*critical*" | head -10
cd /home/ubuntu && cd /home/ubuntu && rm -rf shadowlands-rpg shadowlands-backend 2>/dev/null && mkdir -p shadowlands-rpg/src/components/game shadowlands-backend/src/routes && echo "Created project directories"
cd /home/ubuntu && cd /home/ubuntu && cp upload/zip1/quest_engine_core.py . && cp upload/zip1/dynamic_quest_generation.py . && cp upload/zip1/quests.py shadowlands-backend/src/routes/ && cp upload/zip1/dynamic_quests.py shadowlands-backend/src/routes/ && cp upload/zip1/shared_quest_engine.py shadowlands-backend/src/ && cp upload/zip1/main_robust.py shadowlands-backend/src/main.py && echo "Copied quest system files"
cd /home/ubuntu && cd /home/ubuntu && cp upload/zip2/App.jsx shadowlands-rpg/src/ && cp upload/zip3/MobileGameInterface.jsx shadowlands-rpg/src/components/game/ && cp upload/zip2/EquipmentManager.jsx shadowlands-rpg/src/components/game/ && cp upload/zip3/CharacterEquipment.jsx shadowlands-rpg/src/components/game/ && cp upload/zip3/InventoryGrid.jsx shadowlands-rpg/src/components/game/ && echo "Copied React components"
cd /home/ubuntu && cd /home/ubuntu && cp upload/zip1/mobile_interface_fix.py . && cp upload/zip1/bundle_optimization_analyzer.py . && cp upload/zip1/performance_optimization_implementation.py . && cp upload/zip1/todo.md . && cp upload/zip1/*report*.md . 2>/dev/null && echo "Copied optimization and documentation files"
cd /home/ubuntu && cd /home/ubuntu && echo "=== Current project structure ===" && ls -la shadowlands-rpg/src/ && ls -la shadowlands-backend/src/ && echo "=== Copying test files ===" && cp upload/zip1/phase3_dynamic_quest_comprehensive_test.py . && cp upload/zip1/quest_system_comprehensive_test.py . && cp upload/zip1/*test_results*.json . 2>/dev/null && echo "Test files copied"
cd /home/ubuntu && cd /home/ubuntu && ls -la shadowlands-rpg/src/components/game/ && echo "=== Looking for config files ===" && find upload/ -name "package.json" -o -name "vite.config*" -o -name "*.config.js" | head -5 && echo "=== Checking for any missing critical files ===" && find upload/ -name "*vite*" -o -name "*package*" | head -5
cd /home/ubuntu && cd /home/ubuntu && cp upload/zip1/vite.config.simple.js shadowlands-rpg/ && echo "=== Checking for any API standardization files ===" && find upload/ -name "*api*" -name "*.py" | grep -E "(standardization|response)" | head -3 && echo "=== Current project files ===" && find . -maxdepth 1 -name "*.py" -o -name "*.md" -o -name "*.json" | wc -l
cd /home/ubuntu && cd /home/ubuntu && cp upload/zip1/api_standardization_implementation.py . && cp upload/.recovery/api_response_analysis.py . 2>/dev/null && echo "=== Final project structure ===" && echo "Backend files:" && ls -la shadowlands-backend/src/ && echo "Frontend files:" && ls -la shadowlands-rpg/src/ && echo "Root files:" && ls -la *.py | wc -l
cd /home/ubuntu && cd /home/ubuntu && echo "=== Checking quest engine location ===" && ls -la quest_engine_core.py && echo "=== Testing Python imports ===" && python3 -c "import sys; sys.path.insert(0, '.'); from quest_engine_core import QuestEngine; print('Quest engine import: SUCCESS')" 2>/dev/null && echo "SUCCESS" || echo "IMPORT FAILED"
cd /home/ubuntu && cd /home/ubuntu && echo "=== Current quest_engine_core.py size ===" && wc -l quest_engine_core.py && echo "=== Original quest_engine_core.py size ===" && wc -l upload/zip1/quest_engine_core.py && echo "=== Checking if we have the full version ===" && ls -la upload/*/quest_engine_core.py 2>/dev/null
cd /home/ubuntu && cd /home/ubuntu && echo "=== Checking for working version ===" && ls -la quest_engine_core.py.bak 2>/dev/null || echo "No backup found" && echo "=== Checking current directory for larger quest files ===" && find . -name "*quest*" -name "*.py" -exec wc -l {} \; | sort -nr | head -5
cd /home/ubuntu && cd /home/ubuntu && cp upload/.recovery/quest_engine_core.py . && echo "=== Checking new file size ===" && wc -l quest_engine_core.py && echo "=== Testing import again ===" && python3 -c "import sys; sys.path.insert(0, '.'); from quest_engine_core import QuestEngine; print('Quest engine import: SUCCESS')" 2>/dev/null && echo "SUCCESS" || echo "STILL FAILED"
cd /home/ubuntu && cd /home/ubuntu && python3 quest_system_comprehensive_test.py
cd /home/ubuntu && cd /home/ubuntu && python3 phase3_dynamic_quest_comprehensive_test.py
cd /home/ubuntu && cd /home/ubuntu && echo "=== Current React components ===" && find shadowlands-rpg/ -name "*.jsx" && echo "=== Missing components from App.jsx imports ===" && grep "import.*from" shadowlands-rpg/src/App.jsx && echo "=== Looking for missing components in uploads ===" && find upload/ -name "ResponsiveGameWrapper.jsx" -o -name "DialogueInterface.jsx" -o -name "tabs.jsx"
cd /home/ubuntu && cd /home/ubuntu && mkdir -p shadowlands-rpg/src/components/ui && cp upload/zip3/ResponsiveGameWrapper.jsx shadowlands-rpg/src/components/game/ && cp upload/zip3/DialogueInterface.jsx shadowlands-rpg/src/components/game/ && cp upload/zip3/tabs.jsx shadowlands-rpg/src/components/ui/ && echo "=== Copied missing components ===" && find shadowlands-rpg/ -name "*.jsx" | wc -l
cd /home/ubuntu && cd /home/ubuntu && echo "=== Looking for CSS files ===" && find upload/ -name "*.css" | head -5 && echo "=== Looking for package.json ===" && find upload/ -name "package.json" | head -3 && echo "=== Current React project structure ===" && tree shadowlands-rpg/ 2>/dev/null || find shadowlands-rpg/ -type f
cd /home/ubuntu && cd /home/ubuntu && cp upload/zip3/App.css shadowlands-rpg/src/ && echo "=== Creating package.json ===" && cat > shadowlands-rpg/package.json << 'EOF'
{
  "name": "shadowlands-rpg",
  "private": true,
  "version": "0.0.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview"
  },
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0"
  },
  "devDependencies": {
    "@types/react": "^18.2.15",
    "@types/react-dom": "^18.2.7",
    "@vitejs/plugin-react": "^4.0.3",
    "vite": "^4.4.5"
  }
}
EOF

echo "Package.json created"
