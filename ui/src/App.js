import React from 'react'
import Recipe from './components/RecipeDisplay'

class App extends React.Component {
  constructor() {
    super()
    this.state = {video: null, input: ''}
  }

  search() {
    console.log('search called!')
    this.setState((prevState) => ({video: prevState.input, input: prevState.input}))
  }

  render(){
    return (
      <div className="App">
        <header className="App-header">
          <input value={this.state.input} onChange={e => this.setState({input: e.target.value})} />
          <button onClick={() => this.search()}>Search</button>
          <Recipe id={this.state.video}/>
        </header>
      </div>
    )
  }
}

export default App;
