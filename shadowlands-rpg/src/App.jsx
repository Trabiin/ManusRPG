import React, { useState } from 'react';
import ResponsiveGameWrapper from './components/game/ResponsiveGameWrapper';
import DialogueInterface from './components/game/DialogueInterface';
import EquipmentManager from './components/game/EquipmentManager';
import { Tabs, TabsContent, TabsList, TabsTrigger } from './components/ui/tabs';
import './App.css';

function App() {
  const [showDialogue, setShowDialogue] = useState(false);
  const [currentNPC, setCurrentNPC] = useState(null);
  const [activeTab, setActiveTab] = useState('game');

  const handleOpenDialogue = (npc) => {
    setCurrentNPC(npc);
    setShowDialogue(true);
  };

  const handleCloseDialogue = () => {
    setShowDialogue(false);
    setCurrentNPC(null);
  };

  const handleChoiceSelect = (choice) => {
    console.log('Choice selected:', choice);
    // Handle choice logic here
    setTimeout(() => {
      setShowDialogue(false);
      setCurrentNPC(null);
    }, 500);
  };

  return (
    <div className="App min-h-screen bg-gray-950">
      <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full">
        <TabsList className="grid w-full grid-cols-2 bg-gray-800 mb-4">
          <TabsTrigger value="game" className="text-white data-[state=active]:bg-gray-700">
            Game Interface
          </TabsTrigger>
          <TabsTrigger value="equipment" className="text-white data-[state=active]:bg-gray-700">
            Equipment Manager
          </TabsTrigger>
        </TabsList>

        <TabsContent value="game" className="mt-0">
          <ResponsiveGameWrapper />
        </TabsContent>

        <TabsContent value="equipment" className="mt-0 p-4">
          <EquipmentManager />
        </TabsContent>
      </Tabs>
      
      {showDialogue && currentNPC && (
        <DialogueInterface
          npc={currentNPC}
          onChoiceSelect={handleChoiceSelect}
          onClose={handleCloseDialogue}
          corruption={42} // This would come from game state
        />
      )}
      
      {/* Demo button to test dialogue - remove in production */}
      <button
        onClick={() => handleOpenDialogue({
          name: 'Mysterious Stranger',
          portrait: '/api/placeholder/120/120',
          dialogue: 'The darkness is spreading. Will you join us, or stand against the coming tide?'
        })}
        className="fixed bottom-4 right-4 bg-yellow-600 text-black px-4 py-2 rounded font-semibold z-40"
      >
        Test Dialogue
      </button>
    </div>
  );
}

export default App;

