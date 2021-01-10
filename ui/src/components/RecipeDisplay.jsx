import React from 'react'

export default class Recipe extends React.Component {
    constructor(props) {
        super(props)
        this.state = {recipe: null}
    }

    async componentDidUpdate(prevProps, prevState){
        if (prevProps.id != this.props.id && this.props.id != null) {
            let recipeId = this.props.id
            let res = await fetch(host() + 'transcribe?data=' + recipeId)
            if (!res.ok) {
                console.log('wtf why not ok')
                return
            }
            this.setState({recipe: await res.json()})
        }
    }

    render() {
        return (
            <div>
                Hello World! This is your recipe!:
                {this.state.recipe && JSON.stringify(this.state.recipe)}
            </div>
        )
    }
}

export function host() {
    let url = new URL(window.location.href)
    if (url.host.includes("localhost")) {
        return "http://localhost:5000/"
    } else {
        return "/"
    }
}