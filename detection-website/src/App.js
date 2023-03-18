import './App.css';


function retrieveClasses() {
    fetch('/getClass', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({
            text: "Sending from React"
        })
    }).then(res => res.json())
    .then((data) => {
        console.log(data)
    })
}

function App() {

    retrieveClasses()

    return (
    <div className="App">
      Hello Twitter
    </div>
    );
}

export default App;
