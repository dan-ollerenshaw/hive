import './App.css';
import { PlayButton, SlotMachineTable } from './components';

// TODO: finish implementing frontend
function App() {
  return (
    <div className="App">
      <header className="App-header">
        <p>
          Welcome to our online slot machine.
        </p>
        <PlayButton></PlayButton>
        <SlotMachineTable></SlotMachineTable>
        <section>
          <div>Session credit: X</div>
          <div>Account credit: Y</div>
        </section>
      </header>
    </div>
  );
}

export default App;
