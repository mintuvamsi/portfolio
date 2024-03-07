import './App.css';
import {Greet} from './components/Greet';
import Welcome from './components/Welcome';
import Hello from './components/Hello';


function App() {
  return (
    <div className="App">
      <Greet name='Bruce' heroName='BatMan'>
        <p>This is children props</p>
      </Greet>
      <Greet name='Clark' heroName='SuperMan'>
        <button>Action</button>
      </Greet>
      <Greet name='Diana' heroName='WonderWomen'>

      </Greet>

      <Welcome name='Bruce' heroName='BatMan'/>
      <Welcome name='Clark' heroName='Siperman'/>
      <Welcome name='Diana' heroName='WonderWomen'/>


      {/* <Welcome/> */}
      {/* <Hello/> */}
    </div>
  );
}

export default App;
