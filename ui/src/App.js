import React from 'react'
import Recipe from './components/RecipeDisplay'
import './App.css'

class App extends React.Component {
  constructor() {
    super()
    this.state = {video: null, input: ''}
  }

  search() {
    console.log('search called!')
    this.setState((prevState) => {
      let v = getParam('v', prevState.input)
      if (!v) {
        console.log('what the heck')
      }
      return {video: v, input: prevState.input}
    })
  }

  render(){
    return (
      <div className="App">
        <div className="title-screen">
          <div className="title">
            <div className="title-main">
              <h1>GET IN MY BELLY</h1>
            </div>
            <div className="title-sub">
              <p>Transform any youtube video into an easy to follow recipe</p>
            </div>
          </div>
          <div className="search">
            <input placeHolder={'https://www.youtube.com/watch?v=Jizr6LR83Kk'} value={this.state.input} onChange={e => this.setState({input: e.target.value})} />
            <button onClick={() => this.search()}>Generate Recipe</button>
          </div>
        </div>
        <Recipe id={this.state.video}/>
      </div>
    )
  }
}

function getParam(name, url) {
  name = name.replace(/[\[\]]/g, '\\$&');
  var regex = new RegExp('[?&]' + name + '(=([^&#]*)|&|#|$)'),
      results = regex.exec(url);
  if (!results) return null;
  if (!results[2]) return '';
  return decodeURIComponent(results[2].replace(/\+/g, ' '));
}

export default App;
