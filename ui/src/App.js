import React from 'react'
import Recipe from './components/RecipeDisplay'
import './App.css'
import background from './img.webp'

class App extends React.Component {
  constructor() {
    super()
    this.state = {video: null, input: '', loading: false}
  }

  stopLoading() {
    this.setState({loading: false})
  }

  search() {
    console.log('search called!')
    this.setState({loading: true})
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
              <h1>Get In My Belly</h1>
            </div>
            <div className="title-sub">
              <p>Transform any youtube video into an easy to follow recipe</p>
            </div>
          </div>
          <div className="search">
            <input placeholder={'https://www.youtube.com/watch?v=Jizr6LR83Kk'} value={this.state.input} onChange={e => this.setState({input: e.target.value})} />
            <button onClick={() => this.search()}>
              {
                this.state.loading ?
                (
                  <div class="snippet" data-title=".dot-pulse">
                    <div class="stage">
                      <div class="dot-pulse"></div>
                    </div>
                  </div>
                )
                :
                'Generate Recipe'
              }
            </button>
          </div>
        </div>
        <div className="separator"></div>
        <Recipe id={this.state.video} stopLoading={() => this.stopLoading()}/>
        <div className="background" style={{backgroundImage: `url(${background})`, backgroundSize: '100vw 100vh'}}>
        </div>
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
